# Construye las 10 imágenes (una por etapa). Uso: .\build-all.ps1
$ErrorActionPreference = "Stop"
$env:Path += ";C:\Program Files\Docker\Docker\resources\bin"

# 0-3,5,7: Flask base (mismo patrón)
docker build -t charla/etapa0:1 ./etapa_0_flask_base
docker build -t charla/etapa1:1 ./etapa_1_algoritmo
docker build -t charla/etapa2:1 ./etapa_2_hilos_io
docker build -t charla/etapa3:1 ./etapa_3_lock
docker build -t charla/etapa5:1 ./etapa_5_nativas
docker build -t charla/etapa7:1 ./etapa_7_interpretes

# 4: compose (app + redis), imagen se crea con compose build
docker compose -f ./etapa_4_procesos/docker-compose.yml build

# 6: normal (3.15). La variante .t solo si existe la imagen base.
docker build -t charla/etapa6:1 ./etapa_6_freethreading
# docker build -t charla/etapa6t:1 -f ./etapa_6_freethreading/Dockerfile.t ./etapa_6_freethreading

# 8-9: FastAPI (uvicorn)
docker build -t charla/etapa8:1 ./etapa_8_fastapi
docker build -t charla/etapa9:1 ./etapa_9_rust

docker images --filter "reference=charla/etapa*"
