# Bench con stdlib: mide rps, p50 y p95 por endpoint.
# Uso desde la raíz: python carga/run_carga.py --etapa etapa_0
import argparse, csv, json, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

# Una petición: devuelve (latencia_ms, texto_respuesta).
# El texto se conserva para /contador (visitas) y se ignora en el resto.
def pedir(url, metodo, cuerpo):
    req = urllib.request.Request(url, data=cuerpo, method=metodo)
    if cuerpo:  # POST JSON de /validar
        req.add_header("Content-Type", "application/json")
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=60) as r:
        texto = r.read().decode()
    return (time.perf_counter() - t0) * 1000, texto

# Lanza n peticiones con c hilos; devuelve rps, p50, p95, total_s y cuerpos.
def medir(url, metodo, cuerpo, n, c):
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=c) as ex:
        resultados = list(ex.map(lambda _: pedir(url, metodo, cuerpo), range(n)))
    total = time.perf_counter() - t0  # tiempo pared total, lo mas entendible
    lats = sorted(lat for lat, _ in resultados)
    cuerpos = [texto for _, texto in resultados]
    p50 = lats[int(len(lats) * 0.50)]  # mediana aproximada
    p95 = lats[min(len(lats) - 1, int(len(lats) * 0.95))]  # cola del 95%
    return round(n / total, 1), round(p50, 1), round(p95, 1), round(total, 1), cuerpos

# Lee /contador y devuelve visitas (o None si falla).
def leer_visitas(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return json.loads(r.read()).get("visitas")
    except Exception:
        return None

# Recorre los 5 endpoints y guarda un CSV por etapa.
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://localhost:5000")
    ap.add_argument("--peticiones", type=int, default=200)
    ap.add_argument("--concurrencia", type=int, default=20)
    ap.add_argument("--etapa", default="etapa_0")  # nombre del CSV salida
    a = ap.parse_args()
    cuerpo = json.dumps({"nombre": "Ana", "edad": 30, "email": "a@b.es"}).encode()
    objetivos = [("/io", "GET", None), ("/cpu", "GET", None),  # E/S vs CPU
                 ("/suma/1000000", "GET", None), ("/validar", "POST", cuerpo),
                 ("/contador", "GET", None)]
    filas = []  # (endpoint, rps, p50, p95, total_s)
    visitas_detalle = []  # valores de /contador para ver la race
    for ruta, metodo, dato in objetivos:
        if ruta == "/contador":
            antes = leer_visitas(a.url + ruta)  # valor previo
        rps, p50, p95, total, cuerpos = medir(a.url + ruta, metodo, dato, a.peticiones, a.concurrencia)
        extra = ""
        if ruta == "/contador":
            despues = leer_visitas(a.url + ruta)  # valor posterior
            for t in cuerpos:  # conserva cada visitas devuelto
                try:
                    visitas_detalle.append(json.loads(t).get("visitas"))
                except Exception:
                    pass
            unicos = len(set(visitas_detalle))  # con race hay menos unicos
            esperado = a.peticiones + 1  # +1 por el GET final
            incremento = (despues - antes) if antes is not None and despues is not None else None
            estado = "OK" if incremento == esperado and unicos == a.peticiones else f"RACE? (esperado +{esperado})"
            extra = f" visitas antes={antes} despues={despues} incremento=+{incremento} unicos={unicos}/{a.peticiones} {estado}"
        print(f"{ruta}: total={total}s {rps} rps p50={p50}ms p95={p95}ms{extra}")
        filas.append((ruta, rps, p50, p95, total))
    with open(f"carga/resultados/{a.etapa}.csv", "w", newline="") as f:
        w = csv.writer(f)  # columnas pedidas en la charla
        w.writerow(["endpoint", "rps", "p50_ms", "p95_ms", "total_s"])
        w.writerows(filas)
    with open(f"carga/resultados/{a.etapa}_contador.csv", "w", newline="") as f:
        w = csv.writer(f)  # detalle para comparar e0 vs e3
        w.writerow(["visitas"])
        w.writerows([[v] for v in visitas_detalle])

if __name__ == "__main__":
    # Uso (desde la raiz del proyecto):
    #   1) Arranca la etapa 0: docker build -t etapa0 etapa_0_flask_base
    #                          docker run -p 5000:5000 etapa0
    #   2) Prueba rapida (40 peticiones, 8 en paralelo):
    #      python carga/run_carga.py --etapa etapa_0 --url http://localhost:5000 --peticiones 40 --concurrencia 8
    #   3) Serie pura (1 cliente, sin cola):
    #      python carga/run_carga.py --etapa etapa_0_c1 --url http://localhost:5000 --peticiones 40 --concurrencia 1
    #   4) Salida: carga/resultados/<etapa>.csv con rps, p50_ms, p95_ms y total_s.
    #   5) /contador: guarda carga/resultados/<etapa>_contador.csv con cada visitas
    #      e imprime antes/despues/incremento para ver la race (e0 vs e3).
    main()
