# Puertos por etapa (host -> 5000 en contenedor)

| Etapa | Carpeta | Puerto host | Imagen | Servidor |
|---|---|---|---|---|
| 0 | etapa_0_flask_base | 5000 | charla/etapa0:1 | gunicorn 1x1 |
| 1 | etapa_1_algoritmo | 5001 | charla/etapa1:1 | gunicorn 1x1 |
| 2 | etapa_2_hilos_io | 5002 | charla/etapa2:1 | gunicorn gthread 1x8 |
| 3 | etapa_3_lock | 5003 | charla/etapa3:1 | gunicorn gthread 1x8 |
| 4 | etapa_4_procesos | 5004 | compose (app+redis) | gunicorn gthread 2x2 |
| 5 | etapa_5_nativas | 5005 | charla/etapa5:1 | gunicorn gthread 1x8 |
| 6 | etapa_6_freethreading | 5006 | charla/etapa6:1 | gunicorn gthread 1x8 (3.15) |
| 6t | etapa_6_freethreading (Dockerfile.t) | 5016 | charla/etapa6t:1 | idem pero 3.15t si existe imagen |
| 7 | etapa_7_interpretes | 5007 | charla/etapa7:1 | gunicorn gthread 1x4 + intérpretes |
| 8 | etapa_8_fastapi | 5008 | charla/etapa8:1 | uvicorn 1 worker |
| 9 | etapa_9_rust | 5009 | charla/etapa9:1 | uvicorn 1 worker (fallback Python sin .so) |

Probar: `curl localhost:PUERTO/salud`
