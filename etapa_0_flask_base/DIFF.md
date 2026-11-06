# DIFF — etapa 0 (linea base, sin cambios)
Base sincrona: 1 worker, 1 hilo.
`/io` mide espera bloqueante (1s); `/cpu` mide GIL (primos hasta 20000).
`/suma` mide O(n); `/validar` mide validacion manual; `/contador` mide estado local.
Las etapas 1-10 comparan contra estos tiempos.
