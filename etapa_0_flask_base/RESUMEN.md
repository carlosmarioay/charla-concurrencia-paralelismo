# Etapa 0 — tabla resumen (1 worker sync, 4 hilos HW, solo usa 1)

| Endpoint | 1x serie | 4x concurrente | Carga 40/8 | Cuello |
|---|---|---|---|---|
| /salud | 0.08s ok | — | — | ninguno, healthcheck |
| /io | 1.01s | 4.03s total (1.01/2.01/3.02/4.02s) | 1.0 rps, p50 8.0s | sleep bloquea worker, cola serie |
| /cpu (primos 20k) | 0.05s, 2262 | 0.39s total (0.08/0.15/0.25/0.38s) | 9.5 rps, p50 0.72s | Python puro + GIL, cola serie |
| /suma/100 | 0.01s, 5050 | — | — | bucle O(n) ingenuo |
| /suma/1M | 0.14s | — | 2.9 rps, p50 2.5s | O(n): servicio 0.14s + cola |
| /validar | 0.016s ok, 0.007s 400 | — | 184 rps | if manual, sin librería |
| /contador | 0.01s (52,53,54) | — | 163 rps | global en memoria, se pierde |

Lectura: con 1 worker todo es serie. 4x /io debería ser ~1s en paralelo, tarda 4s.
El p50 alto en carga es espera en cola, no servicio.
