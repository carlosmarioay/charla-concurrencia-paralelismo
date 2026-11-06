# Diff vs etapa 2: solo /contador cambia
1. Race: leer-modificar-escribir no es atómico; con hilos se intercalan.
2. Sin lock: dos hilos leen `visitas=5`, ambos escriben `6`: se pierde una.
3. Pasa con hilos porque comparten memoria en un mismo proceso.
4. Lock: solo un hilo entra al `with`; el resto espera su turno.
5. Costo: el `sleep(0.001)` dentro del lock frena a todos: orden sí, gratis no.
