# Slide final: qué ganamos en cada etapa

| Etapa | Ganamos |
|---|---|
| 0 base | punto de partida: 1 worker, todo en serie |
| 1 algoritmo | O(n)→O(1): 1000x sin más hardware |
| 2 hilos I/O | /io x8 con 8 hilos; /cpu igual (GIL) |
| 3 lock | contador correcto; /contador se serializa |
| 4 procesos+Redis | /cpu xNúcleos; estado compartido real |
| 5 nativas | C/Rust libera el GIL: hilos que sí escalan |
| 6 free-threading (3.15t) | hilos Python también para CPU |
| 7 subintérpretes | aislamiento sin pagar procesos |
| 8 FastAPI async | miles de /io con 1 loop, sin hilos |
| 9 Rust | /cpu 10-50x; coste: compilar y empaquetar |

⚠️ Martillo dorado: ninguna vale para todo.
I/O → hilos/async; CPU → procesos/Rust; ¿duda? mide con `carga/`.

## Anexo medido en esta compu (4 hilos HW, 40 pet. por endpoint, conc. 8) — SIN caché en /cpu

1 petición tarda casi igual en todas (el cambio es concurrencia, no magia).
/io 1x = ~1.06s en las 10. /cpu 1x = ~0.1s Python puro, ~0.2s hash C, ~0.5s e4/e7 (crear pool por petición). /suma/1M 1x = 0.09s (e0 bucle) vs ~0.01s (Gauss).

| etapa | qué cambió | 1 pet. /io | 1 pet. /cpu | 40 pet. TOTAL | mejora vs e0 |
|---|---|---|---|---|---|
| e0 base 1x1 | todo serie | 1.05s | ~0.1s | **53.4s** (40+3.4+9.5) | 1.0x |
| e1 algoritmo | bucle→Gauss O(1); /suma con caché, /cpu sin caché | 1.05s igual | ~0.1s igual | **43.6s** (40+2.8+0.3) | 1.2x (solo suma) |
| e2 hilos 1x8 | 8 hilos, sleep libera GIL | 1.07s igual | ~0.1s igual | **11.4s** (6.5+3.5+0.3) | 4.7x (/io 40→6.5s) |
| e3 lock 1x8 | +Lock en contador | 1.10s igual | ~0.1s igual | **9.8s** (5.6+3.2+0.3) | 5.4x |
| e4 proc 2x2 | /cpu a procesos + Redis | 1.06s igual | ~0.5s crear 2 proc | **28.8s** (12.5+15.4+0.3) | 1.9x (pool por petición lastra) |
| e5 nativas 1x8 | hashlib C + pydantic | 1.05s igual | ~0.2s hash real | **8.7s** (6.1+1.7+0.3) | 6.1x (cpu 3.4→1.7s) |
| e6 1x8 | mismo que e3 + /gil | 1.05s igual | ~0.1s igual | **11.4s** (5.7+4.8+0.4) | 4.7x |
| e7 1x4+interp | /cpu a 2 intérpretes | 1.07s igual | ~0.5s crear interp | **18.8s** (10.8+6.9+0.4) | 2.8x (4 slots) |
| e8 FastAPI | 1 loop + to_thread cpu | 1.07s igual | ~0.1s igual | **9.6s** (5.5+3.1+0.4) | 5.6x sin hilos |
| e9 Rust | /cpu a Rust (aquí fallback Python) | 1.06s igual | ~0.1s igual | **8.2s** (5.6+1.8+0.3) | 6.5x |

SIN caché en /cpu: ahora /cpu mide paralelismo de verdad. Ver grafico_tiempo_total.png.
