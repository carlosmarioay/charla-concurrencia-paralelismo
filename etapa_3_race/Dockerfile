FROM python:3.15-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
# 1 proceso x 8 hilos SIN lock: la race clasica de hilos se ve aqui.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--worker-class", "gthread", "--workers", "1", "--threads", "8", "app:app"]
