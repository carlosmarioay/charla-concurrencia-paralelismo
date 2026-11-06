# Etapa 7: subintérpretes (/cpu con InterpreterPoolExecutor)
1. Requiere Python >= 3.14: `docker build -t etapa7 .` (usa python:3.15-slim).
2. Local: `python app.py` o `flask run`; `curl localhost:5000/cpu` dice `interpretes: true/false`.
3. Si tu Python es < 3.14, /cpu cae a hilos (igual que etapa 3) sin romper nada.
4. Compara tiempos de `/cpu` contra etapa 3 (hilos, 1 GIL), etapa 4 (procesos) y etapa 6 (3.15t).
5. Compara `/gil` con etapa 6: aquí el GIL sigue activo, cada intérprete tiene el suyo.
6. Enseña: paralelismo CPU sin procesos (sin pickle costoso) y sin quitar el GIL global.
