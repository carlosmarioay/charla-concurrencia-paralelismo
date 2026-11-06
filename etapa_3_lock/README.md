# Etapa 3: race + Lock
1. Corre: `python repro_race.py` (sin Flask, solo hilos).
2. Sin lock verás menos de 1000: dos hilos leen igual y se pisan.
3. Con lock verás 1000: un hilo a la vez, correcto pero más lento.
4. Enseña: compartir estado entre hilos sin Lock pierde datos.
5. Enseña: el Lock ordena, no acelera; el sleep(0.001) lo hace visible.
