FROM python:3.15-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
# 8 hilos: numba (nativo, nogil) y pydantic (Rust) liberan el GIL y corren en paralelo.
# Sin procesos: lo nativo ya usa todos los núcleos desde hilos.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--worker-class", "gthread", "--workers", "1", "--threads", "8", "app:app"]
