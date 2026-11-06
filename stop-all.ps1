# Para todo. Uso: .\stop-all.ps1
$env:Path += ";C:\Program Files\Docker\Docker\resources\bin"
docker rm -f etapa0 etapa1 etapa2 etapa3 etapa5 etapa6 etapa7 etapa8 etapa9 2>$null
docker compose -f ./etapa_4_procesos/docker-compose.yml down
docker ps
