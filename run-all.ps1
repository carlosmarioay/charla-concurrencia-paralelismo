# Levanta una etapa por puerto. Uso: .\run-all.ps1
# Para una sola: docker run --rm -p 5000:5000 charla/etapa0:1
$ErrorActionPreference = "Stop"
$env:Path += ";C:\Program Files\Docker\Docker\resources\bin"

# Limpia restos anteriores (no borra imágenes)
docker rm -f etapa0 etapa1 etapa2 etapa3 etapa5 etapa6 etapa7 etapa8 etapa9 2>$null

docker run -d --name etapa0 -p 5000:5000 charla/etapa0:1
docker run -d --name etapa1 -p 5001:5000 charla/etapa1:1
docker run -d --name etapa2 -p 5002:5000 charla/etapa2:1
docker run -d --name etapa3 -p 5003:5000 charla/etapa3:1
docker run -d --name etapa5 -p 5005:5000 charla/etapa5:1
docker run -d --name etapa6 -p 5006:5000 charla/etapa6:1
docker run -d --name etapa7 -p 5007:5000 charla/etapa7:1
docker run -d --name etapa8 -p 5008:5000 charla/etapa8:1
docker run -d --name etapa9 -p 5009:5000 charla/etapa9:1

# Etapa 4 va con compose (app 5004 + redis)
docker compose -f ./etapa_4_procesos/docker-compose.yml up -d

docker ps --format "table {{.Names}}\t{{.Ports}}\t{{.Status}}"
