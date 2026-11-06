# Rust se compila aquí: rustup mínimo + maturin build --release.
# El .whl se instala con pip; `import rust_cpu` ya no hace fallback.
FROM python:3.15-slim
RUN apt-get update && apt-get install -y --no-install-recommends curl build-essential \
 && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal \
 && rm -rf /var/lib/apt/lists/*
ENV PATH="/root/.cargo/bin:${PATH}"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY rust_cpu ./rust_cpu
# PyO3 0.22 solo conoce hasta 3.13: se compila contra el ABI estable.
ENV PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1
RUN cd rust_cpu && maturin build --release && pip install target/wheels/*.whl
COPY app.py .
EXPOSE 5000
# 1 worker ASGI: /cpu en Rust no necesita GIL; fallback Python va a pool.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "1"]
