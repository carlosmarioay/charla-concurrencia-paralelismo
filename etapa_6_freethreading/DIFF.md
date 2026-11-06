# Diff vs etapa 3: solo se suma /gil
1. Todo igual: primos puro-Python, Gauss, /io, /contador con Lock.
2. Nuevo GET /gil: dice si el GIL está activo y qué versión corre.
3. Sin GIL (3.15t) los hilos sí reparten /cpu; con GIL (3.15) no.
4. El Lock sigue necesario: sin GIL hay más paralelismo y más races.
5. Dockerfile igual (3.15); Dockerfile.t trae 3.15t vía uv (mismo CMD 1x8): compilar desde fuente tarda ~30 min, el precompilado segundos.
