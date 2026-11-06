from flask import Flask, jsonify, request
import time

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


def contar_primos(limite):
    return sum(1 for x in range(2, limite + 1) if es_primo(x))


# Cuello: bloquea 1 s el worker (simula API externa lenta).
@app.get("/io")
def io():
    time.sleep(1)
    return jsonify(ok=True, origen="io")


# Cuello: calculo puro-Python que retiene el GIL y bloquea el worker.
@app.get("/cpu")
def cpu():
    total = contar_primos(LIMITE_PRIMOS)
    return jsonify(primos=total, limite=LIMITE_PRIMOS)


# Cuello: suma O(n) con bucle ingenuo (en etapa 1 se usa Gauss).
@app.get("/suma/<int:n>")
def suma(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return jsonify(n=n, total=total)


# Cuello: validacion manual; mide coste de Python, no de E/S.
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
@app.get("/contador")
def contador():
    global visitas
    visitas += 1
    return jsonify(visitas=visitas)


# Sin cuello: healthcheck para Docker.
@app.get("/salud")
def salud():
    return jsonify(estado="ok")
