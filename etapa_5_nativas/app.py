# Etapa 5: igual que etapa 3, pero /cpu y /validar usan código nativo.
from flask import Flask, jsonify, request
import numba
import threading
import time
from functools import lru_cache
from pydantic import BaseModel, Field, ValidationError

app = Flask(__name__)

visitas = 0  # contador en memoria (se pierde al reiniciar)
candado = threading.Lock()  # un hilo a la vez en /contador

LIMITE_PRIMOS = 20000  # mismo N que e0-e4: comparacion directa y justa


# Rust libera el GIL: validar corre en nativo, los hilos sí paralelizan.
# EmailStr NO: pide email-validator; str simple basta para el slide.
class Usuario(BaseModel):
    nombre: str
    edad: int = Field(ge=0, le=120)
    email: str


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


# Misma funcion que e0-e4 pero compilada: numba la lleva a nativo.
# nogil=True suelta el GIL: 8 hilos = CPU en paralelo sin procesos.
@numba.njit(nogil=True)
def es_primo_nb(x):
    if x < 2:
        return False
    i = 2
    while i * i <= x:  # sin ** ni sqrt: njit prefiere enteros
        if x % i == 0:
            return False
        i += 1
    return True


@numba.njit(nogil=True)
def contar_primos_nb(limite):
    total = 0
    for x in range(2, limite + 1):
        if es_primo_nb(x):
            total += 1
    return total


contar_primos_nb(100)  # calienta: compila una vez aqui, no en la primera peticion


# Mismo trabajo y misma respuesta que e0-e4: solo cambia donde corre.
@app.get("/cpu")
def cpu():
    total = contar_primos_nb(LIMITE_PRIMOS)
    return jsonify(primos=int(total), limite=LIMITE_PRIMOS)


# Optimizado: fórmula de Gauss, tiempo constante aunque n crezca.
@app.get("/suma/<int:n>")
def suma(n):
    return jsonify(n=n, total=suma_gauss(n))


# Nativo (Rust) en vez de ifs manuales; mide coste de validar, no de E/S.
# Caché NO aplica: cada petición trae datos distintos.
@app.post("/validar")
def validar():
    try:
        Usuario(**(request.get_json(silent=True) or {}))
    except ValidationError as e:
        return jsonify(ok=False, errores=[x["msg"] for x in e.errors()]), 400
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


# Sin cuello: healthcheck para Docker.
@app.get("/salud")
def salud():
    return jsonify(estado="ok")
