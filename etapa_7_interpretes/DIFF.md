# Diff vs etapa 3: /cpu a intérpretes, se suma /gil
1. Ganancia: 2 intérpretes = 2 GIL = Python puro en 2 núcleos a la vez.
2. Vs procesos (etapa 4): sin pickle costoso ni copiar memoria por proceso; arranque más barato.
3. Vs free-threading (etapa 6): no quita el GIL global, cada intérprete trae el suyo.
4. Límite: sin memoria compartida; solo entran y salen datos simples (un número).
5. Contador igual: `visitas` y Lock viven en el proceso principal; /cpu no los toca.
6. /gil copiado de etapa 6 para comparar: aquí sigue activo (True) en 3.15 normal.
7. Truco: `contar_primos` autocontenida (sin globales) porque el intérprete no ve `es_primo` de fuera.
8. Refactor: pool global reutilizado (antes se creaba por petición y cada una pagaba arrancar 2 intérpretes).
