FROM python:3.15-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
# 4 hilos: /io libera el GIL en sleep y corre en paralelo.
# /cpu no usa hilos: va a 2 intérpretes, cada uno con su GIL.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--worker-class", "gthread", "--workers", "1", "--threads", "4", "app:app"]
