# Diff vs etapa 3: /cpu a procesos, /contador se rompe
1. Ganancia: 2 procesos = 2 GIL = Python puro en 2 núcleos a la vez.
2. Costo arranque: crear procesos por petición frena; el pool global gasta memoria siempre.
3. Costo pickle: args y retorno viajan serializados; vale para números, no para locks ni conexiones.
4. Contador roto: `visitas` vive en cada worker; con 2 procesos verás 1,1,2,2 en vez de 1,2,3,4.
5. Lock no cruza procesos: ordena hilos dentro de uno; entre procesos solo Redis (INCR) ordena.
