# DIFF etapa 1 → 2 (conceptual)
1. Python: 0 líneas cambiadas, solo comentario de etapa.
2. Servidor: 1 worker/1 hilo → 1 proceso/8 hilos (gthread).
3. /io escala: `sleep` libera el GIL, 8 peticiones ~1 s.
4. /cpu igual: puro-Python retiene el GIL, sin paralelismo.
5. Lección: hilos sirven para E/S, no para CPU.
