# Diff vs Flask (etapas 3 y 6): WSGI bloqueante vs ASGI concurrente
1. Flask (WSGI): cada petición ocupa un worker; `time.sleep` lo deja clavado.
2. Flask con vista `async`: gunicorn la corre en un loop nuevo por petición.
3. Ese loop por petición no comparte nada: no hay concurrencia real en I/O.
4. FastAPI (ASGI): un solo loop vivo atiende todas las peticiones.
5. `await asyncio.sleep` cede el turno: miles de /io en paralelo, 1 proceso.
6. `async + time.sleep` o CPU puro pararía ese loop único: peor que Flask.
7. Por eso /cpu va con `await asyncio.to_thread(...)`: el loop sigue libre.
8. /contador aún usa `threading.Lock`: el pool de `to_thread` mete hilos igual.
9. /validar pasa de manual a Pydantic: tipos gratis, reglas a mano.
10. Enseña: async no acelera CPU; solo deja esperar I/O sin gastar hilos.
