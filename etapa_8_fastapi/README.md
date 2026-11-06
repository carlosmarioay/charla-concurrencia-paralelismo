# Etapa 8: FastAPI async (mismo contrato que etapa 3)
1. Instala: `pip install -r requirements.txt`.
2. Corre: `uvicorn app:app --port 5000 --workers 1` (un solo loop).
3. Prueba: `curl localhost:5000/io` no bloquea a otros en paralelo.
4. Prueba: `curl localhost:5000/cpu` delega a pool con `to_thread`.
5. Prueba: `curl localhost:5000/suma/100` usa Gauss + caché.
6. Prueba: `curl -X POST localhost:5000/validar -d '{"nombre":"Ana","edad":30,"email":"a@x.es"}'`.
7. Prueba: `curl localhost:5000/contador` y `curl localhost:5000/salud`.
8. Verás: /io escala sin hilos; /cpu necesita pool o procesos.
9. Ojo: `async def` + `time.sleep` bloquea el loop; usa `await asyncio.sleep`.
10. Enseña: ASGI = un loop concurrente; WSGI = un worker ocupado por petición.
