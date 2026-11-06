# Etapa 5: código nativo que libera el GIL
1. `pip install -r requirements.txt` y `python app.py` (o `docker compose up`).
2. `/cpu` repite `hashlib.sha256` 20000 veces: corre en C, libera el GIL, los 8 hilos van en paralelo.
3. `/validar` usa pydantic v2 (Rust): valida en nativo, también escala con hilos.
4. `/suma`, `/io`, `/contador` (con Lock) y `/salud` idénticos a etapa 3.
5. Enseña: si la librería libera el GIL, hilos bastan; procesos solo para Python puro.
