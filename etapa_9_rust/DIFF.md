# DIFF etapa 8 → etapa 9: Rust acelera /cpu

## Qué cambia

- Nuevo `rust_cpu/`: crate PyO3 con `contar_primos(limite)` en Rust.
- `/cpu` intenta `from rust_cpu import contar_primos as contar_rust`:
  si hay `.so`, responde `"motor": "rust"`; si no, `"motor": "python"`.
- `/gil` suma el campo `usa_rust` para mostrar el motor en slides.
- Resto de rutas (`/io`, `/suma`, `/validar`, `/contador`, `/salud`) igual.

## allow_threads vs detach

- 0.22 (este repo): `py.allow_threads(|| cálculo)` — suelta el GIL.
- >= 0.26: `py.detach(|| cálculo)` — mismo, nombre nuevo.
- El `lib.rs` usa `allow_threads` coherente con `Cargo.toml` 0.22.

## Por qué Rust no tiene races

- Ownership + borrow checker: un `&mut` excluye cualquier otro acceso.
- `Send`: el valor puede viajar a otro hilo. `Sync`: se puede compartir.
- Sin `Send/Sync` el `to_thread` ni compilaría; en Python el error
  aparece corriendo (contador perdido), en Rust no compila y punto.
