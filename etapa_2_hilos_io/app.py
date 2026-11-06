# Etapa 2: mismo código, cambia el servidor (hilos).
from flask import Flask, jsonify, request
import time
from functools import lru_cache

app = Flask(__name__)

visitas = 0  # contador en memoria (se pierde al reiniciar)

LIMITE_PRIMOS = 20000  # N fijo para comparar entre etapas


def es_primo(x):
    if x < 2:
        return False
    for i in range(2, int(x ** 0.5) + 1):
        if x % i == 0:
            return False
    return True


# SIN caché a propósito: si se cachea, la carga repite el mismo límite
# y ya no mide paralelismo (39/40 hits). La caché vive solo en /suma.
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


# Cuello: calculo puro-Python que retiene el GIL y bloquea el worker.
# La caché ayuda solo si se repite el mismo límite.
@app.get("/cpu")
def cpu():
    total = contar_primos(LIMITE_PRIMOS)
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


# Cuello: memoria local, no se comparte entre workers ni replicas.
# Caché NO aplica: el estado cambia en cada llamada.
@app.get("/contador")
def contador():
    global visitas
    visitas += 1
    return jsonify(visitas=visitas)


# Sin cuello: healthcheck para Docker.
@app.get("/salud")
def salud():
    return jsonify(estado="ok")
