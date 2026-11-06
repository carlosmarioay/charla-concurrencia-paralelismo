# Race: 50 hilos x 20 = 1000 esperado. Sin lock se pierden.
import threading
import time
from concurrent.futures import ThreadPoolExecutor

total = 0
candado = threading.Lock()

def sin_lock():
    global total
    tmp = total + 1  # lee
    time.sleep(0.001)  # otro hilo lee lo mismo aqui
    total = tmp  # escribe y pisa al otro

def con_lock():
    global total
    with candado:  # uno a la vez
        tmp = total + 1
        time.sleep(0.001)
        total = tmp

def corre(fn):
    global total
    total = 0
    with ThreadPoolExecutor(max_workers=50) as p:
        for _ in range(1000):
            p.submit(fn)
    return total  # esperado: 1000
print("sin lock:", corre(sin_lock))  # < 1000: visitas perdidas
print("con lock:", corre(con_lock))  # 1000: correcto, mas lento
