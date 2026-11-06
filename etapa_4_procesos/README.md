# Etapa 4: procesos + Redis
1. `docker compose up`: app (2 procesos x 8 hilos).
2. `/cpu` va a ProcessPoolExecutor: más rápido, pero paga arranque + pickle + memoria.
3. `/contador` miente con 2 workers: cada proceso tiene su copia, vuelve a 1 y 1.
4. En prod el contador vive en Redis (INCR atómico), no en `visitas`.
5. Enseña: procesos dan CPU real; el estado compartido exige servicio externo.
