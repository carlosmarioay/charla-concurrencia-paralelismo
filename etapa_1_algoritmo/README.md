# Etapa 1 — Algoritmo (sin concurrencia)
Build: `docker build -t etapa1 .`
Run: `docker run -p 5000:5000 etapa1`
Probar: `curl localhost:5000/suma/1000000` (instantáneo, antes O(n))
Probar: `curl localhost:5000/cpu` dos veces (2ª sale de caché)
Ganado: /suma pasa de O(n) a O(1) con Gauss.
Ganado: repetir /cpu o /suma con mismo valor = 0 cálculo.
Nada de hilos ni procesos: solo mejor algoritmo + caché.
Mismo Dockerfile (1 worker, 1 thread): el marco no cambió.
Moraleja: optimizar primero, escalar después.
