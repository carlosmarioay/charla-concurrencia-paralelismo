# DIFF etapa 0 → 1 (conceptual)
1. `/suma`: bucle O(n) → Gauss `n*(n+1)//2` O(1). Por qué: n grande ya no cuesta.
2. `+ suma_gauss(n)` con `@lru_cache`: repetir n sale gratis.
3. `contar_primos` SIN caché a propósito: con caché la carga (mismo límite)
   daría 39/40 hits y taparía el paralelismo que miden las etapas 2-9.
4. Caché NO en /io, /cpu, /validar, /contador: E/S, cálculo a medir, datos únicos o estado mutable.
5. Sin hilos/procesos: misma latencia en 1ª llamada a /cpu e /io.
6. Lección: el algoritmo rinde antes que la concurrencia.
