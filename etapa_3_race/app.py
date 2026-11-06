# Etapa 3 RACE: igual que etapa 3 pero SIN lock para ver visitas perdidas.
from flask import Flask, jsonify, request
import time
from functools import lru_cache

app = Flask(__name__)

visitas = 0  # contador en memoria (se pierde al reiniciar)
# SIN candado a proposito: dos hilos leen lo mismo y se pisan.

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
@app.get("/io")
def io():
    time.sleep(1)
    return jsonify(ok=True, origen="io")


@app.get("/cpu")
def cpu():
    total = contar_primos(LIMITE_PRIMOS)
    return jsonify(primos=total, limite=LIMITE_PRIMOS)


@app.get("/suma/<int:n>")
def suma(n):
    return jsonify(n=n, total=suma_gauss(n))


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


# SIN lock: dos hilos leen lo mismo y se pisan (visitas perdidas).
@app.get("/contador")
def contador():
    global visitas
    tmp = visitas + 1  # lee
    time.sleep(0.001)  # pausa: otro hilo lee lo mismo aqui
    visitas = tmp  # escribe y pisa al otro
    return jsonify(visitas=visitas)


@app.get("/salud")
def salud():
    return jsonify(estado="ok")
