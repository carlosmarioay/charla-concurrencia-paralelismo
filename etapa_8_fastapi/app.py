# Etapa 8: mismo contrato que etapa 3, pero con FastAPI async.
import asyncio
import sys
import threading
import time
from functools import lru_cache

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

visitas = 0  # contador en memoria (se pierde al reiniciar)
candado = threading.Lock()  # un hilo a la vez en /contador

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


# Un solo event loop atiende miles: sleep cede el turno sin bloquear.
# Caché NO aplica: simula E/S, no es cálculo repetible.
@app.get("/io")
async def io():
    await asyncio.sleep(1)  # NO time.sleep: eso pararía todo el loop
    return {"ok": True, "origen": "io"}


# Se delega a un pool: el cálculo pesado no bloquea el loop.
# La caché ayuda solo si se repite el mismo límite.
@app.get("/cpu")
async def cpu():
    total = await asyncio.to_thread(contar_primos, LIMITE_PRIMOS)
    return {"primos": total, "limite": LIMITE_PRIMOS}


# Optimizado: fórmula de Gauss, tiempo constante aunque n crezca.
@app.get("/suma/{n}")
def suma(n: int):
    return {"n": n, "total": suma_gauss(n)}


# Pydantic valida tipos solo; el resto se revisa a mano.
# Caché NO aplica: cada petición trae datos distintos.
class Usuario(BaseModel):
    nombre: str
    edad: int
    email: str


@app.post("/validar")
async def validar(u: Usuario):
    if not 0 <= u.edad <= 120:
        raise HTTPException(400, "edad debe ser entero 0-120")
    if "@" not in u.email:
        raise HTTPException(400, "email debe contener @")
    return {"ok": True}


# El lock sigue: /cpu va a hilos (to_thread) y hay race igual.
# Sync corre en pool de FastAPI; el sleep muestra el costo del lock.
@app.get("/contador")
def contador():
    global visitas
    with candado:
        tmp = visitas + 1  # lee
        time.sleep(0.001)  # pausa: sin lock otro hilo lee lo mismo
        visitas = tmp  # escribe
        return {"visitas": visitas}


# Sin GIL los hilos sí paralelizan CPU puro-Python: /cpu mejora con hilos.
# En 3.15 normal siempre True; en 3.15t puede ser False.
@app.get("/gil")
def gil():
    try:
        activo = sys._is_gil_enabled()
    except AttributeError:
        activo = True  # este Python no conoce free-threading
    return {"gil_activo": activo, "version": sys.version}


# Sin cuello: healthcheck para Docker.
@app.get("/salud")
def salud():
    return {"estado": "ok"}
