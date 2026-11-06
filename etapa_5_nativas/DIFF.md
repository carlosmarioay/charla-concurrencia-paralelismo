# Diff vs etapa 3/4: nativo libera el GIL, hilos bastan
1. `/cpu` antes: primos en Python puro (retiene GIL, 1 hilo a la vez) o procesos (rápido pero paga pickle + memoria).
2. `/cpu` ahora: la misma `contar_primos` compilada con numba (`nogil=True`); 8 hilos = 8 núcleos sin procesos.
3. Comparación justa: mismo N (20000) y misma respuesta (`primos`, `limite`) que e0-e4; solo cambia dónde corre.
4. `/validar` antes: ifs manuales en Python (retiene GIL); ahora pydantic v2 corre en Rust y suelta el GIL.
5. Ojo warmup: la primera llamada compila (~1 s); se precalienta en el import para no medir compilación.
