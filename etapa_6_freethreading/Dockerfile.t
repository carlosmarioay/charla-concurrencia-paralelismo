# Python 3.15 free-threaded precompilado (uv) + misma app 1x8.
# No hay imagen 3.15t en Hub y compilar desde fuente tarda ~30 min: uv trae el binario en segundos.
FROM debian:trixie-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl \
 && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
ENV UV_PYTHON_INSTALL_DIR=/opt/uv-python \
    VIRTUAL_ENV=/app/.venv \
    PATH=/app/.venv/bin:$PATH
# 3.15t = CPython 3.15 con --disable-gil (uv elige el build x86_64+freethreaded).
RUN uv python install 3.15t \
 && uv venv --python 3.15t /app/.venv
WORKDIR /app
COPY requirements.txt .
RUN uv pip install --python /app/.venv/bin/python --no-cache -r requirements.txt
COPY app.py .
EXPOSE 5000
# Mismo 1x8 que etapa 6: la unica diferencia es el interprete sin GIL.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--worker-class", "gthread", "--workers", "1", "--threads", "8", "app:app"]
