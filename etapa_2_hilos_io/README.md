# Etapa 2 — Hilos para E/S (gthread: 1 proceso, 8 hilos)
Build: `docker build -t etapa2 .`
Run: `docker run -p 5000:5000 etapa2`
Probar: 8x `curl localhost:5000/io` en paralelo (~1 s total).
Probar: 2x `curl localhost:5000/cpu` en paralelo (no mejora).
GIL: se libera en `sleep` y E/S, los hilos sí avanzan.
GIL: NO se libera en Python puro, /cpu va un hilo a la vez.
Ganado: /io escala x8 sin tocar ni una línea Python.
Comparar: etapa 1 (1 hilo) tardaba ~8 s en 8x /io.
Moraleja: hilos para esperar, no para calcular.
