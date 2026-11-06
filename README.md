# Python 3.15: concurrencia y paralelismo (charla con 10 etapas)

Cada etapa es una app Flask/FastAPI en `http://localhost:5000` con `/io /cpu /suma /validar /contador`.

| Etapa | Carpeta | Qué enseña |
|---|---|---|
| 0 | etapa_0_flask_base | base Flask 1 worker: todo bloquea |
| 1 | etapa_1_algoritmo | Gauss O(1): el mejor speedup es algoritmo |
| 2 | etapa_2_hilos_io | hilos: /io en paralelo, /cpu no (GIL) |
| 3 | etapa_3_lock | Lock: contador correcto pero serializa |
| 4 | etapa_4_procesos | procesos + Redis: /cpu paralelo, estado común |
| 5 | etapa_5_nativas | C/Rust (hashlib, pydantic): hilos sin GIL |
| 6 | etapa_6_freethreading | Python 3.15t sin GIL: hilos también para CPU |
| 7 | etapa_7_interpretes | subintérpretes: un GIL por intérprete |
| 8 | etapa_8_fastapi | AsyncIO: miles de /io sin hilos |
| 9 | etapa_9_rust | Rust+maturin: /cpu 10-50x |

## Correr una etapa con Docker
```powershell
docker build -t etapa0 etapa_0_flask_base
docker run --rm -p 5000:5000 etapa0
```
Etapa 6 usa `python:3.15t-slim` (free-threading); resto `python:3.15-slim`.
Etapa 4 lleva Redis: `docker compose -f etapa_4_procesos/docker-compose.yml up --build`.
Etapa 8/9 usan uvicorn (ASGI); etapa 9 exige el `.so` compilado (ver su README).

## Medir (carga)
```powershell
python carga/run_carga.py --etapa etapa_0
python carga/comparativa.py
```
Gráfico: `pip install matplotlib; python carga/grafico.py` → `carga/grafico.png`.

## Requisitos
Docker Desktop; Python 3.15 (`python --version`); Rust + maturin solo etapa 9.
Detalle de bench y `hey` alternativo: ver `carga/README.md`.
