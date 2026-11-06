# Etapa 7: igual que etapa 3, pero /cpu va a subintérpretes (PEP 734).
from flask import Flask, jsonify, request
import sys
import threading
import time
from functools import lru_cache

try:
    from concurrent.futures import InterpreterPoolExecutor as Pool
    TIENE_INTERPRETES = True
except ImportError:
    from concurrent.futures import ThreadPoolExecutor as Pool
    TIENE_INTERPRETES = False  # este Python no tiene PEP 734, hilos como antes

app = Flask(__name__)

visitas = 0  # contador en memoria (se pierde al reiniciar)
candado = threading.Lock()  # un hilo a la vez en /contador

# Pool global: se crea una vez en el import y se reutiliza por petición.
# Antes se creaba dentro de /cpu y cada petición pagaba arrancar 2 intérpretes.
POOL = Pool(max_workers=2)

LIMITE_PRIMOS = 20000  # N fijo para comparar entre etapas


def es_primo(x):
    if x < 2:
        return False
    for i in range(2, int(x ** 0.5) + 1):
        if x % i == 0:
            return False
    return True


# Autocontenida para intérpretes: no usa globales (cada intérprete va aislado).
# Sin lru_cache: cada intérprete tiene su caché y no se comparte nada.
def contar_primos(limite):
    def primo_local(x):
        if x < 2:
            return False
        for i in range(2, int(x ** 0.5) + 1):
            if x % i == 0:
                return False
        return True
    return sum(1 for x in range(2, limite + 1) if primo_local(x))


# Caché SÍ aplica: Gauss es puro, repetir n sale gratis.
@lru_cache(maxsize=128)
def suma_gauss(n):
    return n * (n + 1) // 2  # O(1) vs O(n) del bucle


# Cuello: bloquea 1 s el worker (simula API externa lenta).
# Caché NO aplica: simula E/S, no es cálculo repetible.
@app.get("/io")
def io():
    time.sleep(1)
    return jsonify(ok=True, origen="io")


# Cada intérprete tiene su GIL: Python puro corre en otro núcleo.
# Sin pickle entre procesos, pero sin memoria compartida (cada uno lo suyo).
# El pool ya existe (global): la petición solo encola y espera.
@app.get("/cpu")
def cpu():
    total = POOL.submit(contar_primos, LIMITE_PRIMOS).result()
    return jsonify(primos=total, limite=LIMITE_PRIMOS,
                   interpretes=TIENE_INTERPRETES)


# Optimizado: fórmula de Gauss, tiempo constante aunque n crezca.
@app.get("/suma/<int:n>")
def suma(n):
    return jsonify(n=n, total=suma_gauss(n))


# Cuello: validacion manual; mide coste de Python, no de E/S.
# Caché NO aplica: cada petición trae datos distintos.
@app.post("/validar")
def validar():
    datos = request.get_json(silent=True) or {}
    errores = []
    if not isinstance(datos.get("nombre"), str):
        errores.append("nombre debe ser texto")
    edad = datos.get("edad")
    if not isinstance(edad, int) or not 0 <= edad <= 120:
        errores.append("edad debe ser entero 0-120")
    if "@" not in str(datos.get("email", "")):
        errores.append("email debe contener @")
    if errores:
        return jsonify(ok=False, errores=errores), 400
    return jsonify(ok=True)


# Sin lock se pierden visitas: dos hilos leen lo mismo y se pisan.
# El lock deja pasar uno a la vez; el sleep muestra su costo.
@app.get("/contador")
def contador():
    global visitas
    with candado:
        tmp = visitas + 1  # lee
        time.sleep(0.001)  # pausa: sin lock otro hilo lee lo mismo
        visitas = tmp  # escribe
        return jsonify(visitas=visitas)


# Para comparar con etapa 6: en 3.15 normal siempre True; en 3.15t puede ser False.
@app.get("/gil")
def gil():
    try:
        activo = sys._is_gil_enabled()
    except AttributeError:
        activo = True  # este Python no conoce free-threading
    return jsonify(gil_activo=activo, version=sys.version)


# Sin cuello: healthcheck para Docker.
@app.get("/salud")
def salud():
    return jsonify(estado="ok")
