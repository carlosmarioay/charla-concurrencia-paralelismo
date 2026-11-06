# Para free-threading usa python:3.15t-slim o compila con --disable-gil.
FROM python:3.15-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
# 8 hilos: /io libera el GIL en sleep y corre en paralelo.
# /cpu no mejora: Python puro retiene el GIL, un hilo a la vez.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--worker-class", "gthread", "--workers", "1", "--threads", "8", "app:app"]
