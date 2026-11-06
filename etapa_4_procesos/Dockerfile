FROM python:3.15-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
# 2 procesos x 8 hilos: comparable a 1x8 en /io (16 slots, sin cola con 8 clientes).
# /cpu usa procesos (sin GIL), /io usa hilos (sleep libera GIL).
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--worker-class", "gthread", "--workers", "2", "--threads", "8", "app:app"]
