# Python 3.15 free-threaded precompilado (uv) + FastAPI + numba.
# Loop para /io, nativo nogil para /cpu, hilos que sí paralelizan.
FROM debian:trixie-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl \
 && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
ENV UV_PYTHON_INSTALL_DIR=/opt/uv-python \
    VIRTUAL_ENV=/app/.venv \
    PATH=/app/.venv/bin:$PATH
# 3.15t = CPython 3.15 con --disable-gil.
RUN uv python install 3.15t \
 && uv venv --python 3.15t /app/.venv
WORKDIR /app
COPY requirements.txt .
RUN uv pip install --python /app/.venv/bin/python --no-cache -r requirements.txt
COPY app.py .
EXPOSE 5000
# 1 worker ASGI: el loop reparte /io; /cpu va a hilos que ya no pelean GIL.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "1"]
