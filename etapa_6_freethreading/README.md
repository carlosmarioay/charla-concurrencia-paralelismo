# Etapa 6: free-threading (/gil)
1. Normal (3.15 con GIL): `docker build -t etapa6 .` y corre 1x8 como etapa 3.
2. Sin GIL (3.15t): `docker build -f Dockerfile.t -t etapa6t .` y compara `/cpu`. Ojo: no hay imagen `3.15t` en Hub; Dockerfile.t trae el binario free-threaded con uv en segundos.
3. Local: `python check_gil.py` y `curl localhost:5000/gil` en cada versión.
4. Verás: en 3.15 `/cpu` no escala con hilos; en 3.15t sí baja el tiempo.
5. Ojo: en 3.15t numpy y otras nativas aún pueden fallar o ir más lento.
6. Enseña: sin GIL el mismo código con hilos ya paraleliza CPU puro-Python.
