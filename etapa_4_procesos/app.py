# Etapa 4: igual que etapa 3, pero /cpu va a procesos.
from flask import Flask, jsonify, request
import threading
import time
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache

app = Flask(__name__)

visitas = 0  # contador en memoria (se pierde al reiniciar)
candado = threading.Lock()  # vale dentro del proceso, no entre procesos

LIMITE_PRIMOS = 20000  # N fijo para comparar entre etapas


def es_primo(x):
    if x < 2:
        return False
    for i in range(2, int(x ** 0.5) + 1):
        if x % i == 0:
            return False
    return True


# Pura y top-level para pickle: solo entra limite, solo sale un número.
# Sin lru_cache: el wrapper complica pickle y cada proceso tendría su caché.
def contar_primos(limite):
    return sum(1 for x in range(2, limite + 1) if es_primo(x))


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


# Procesos sí liberan el GIL: Python puro corre en otro núcleo.
# Costos: arrancar procesos, pickle de args/retorno, más memoria (cada uno copia lo suyo).
@app.get("/cpu")
def cpu():
    with ProcessPoolExecutor(max_workers=2) as pool:
        total = pool.submit(contar_primos, LIMITE_PRIMOS).result()
    return jsonify(primos=total, limite=LIMITE_PRIMOS)


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


# El lock ordena hilos dentro de un proceso, pero no entre procesos.
@app.get("/contador")
def contador():
    global visitas
    with candado:
        tmp = visitas + 1  # lee
        time.sleep(0.001)  # pausa: sin lock otro hilo lee lo mismo
        visitas = tmp  # escribe
        # ROTO entre procesos: cada worker tiene su copia
        return jsonify(visitas=visitas, nota="local al worker, usa Redis en prod")


# Sin cuello: healthcheck para Docker.
@app.get("/salud")
def salud():
    return jsonify(estado="ok")
