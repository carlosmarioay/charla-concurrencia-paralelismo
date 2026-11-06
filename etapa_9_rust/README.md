# Etapa 9: Rust + Python (PyO3)

Mismo contrato que etapa 8, pero `/cpu` usa Rust si está compilado.

## Compilar la extensión

```bash
cd rust_cpu
maturin develop --release   # compila e instala el .so en el venv actual
```

Otros comandos útiles:

```bash
maturin new rust_cpu              # crear un crate nuevo (ya hecho aquí)
maturin build --release           # genera el .whl en target/wheels
pip install target/wheels/*.whl   # instala el .whl a mano
```

## Probar

```bash
make develop   # = maturin develop --release dentro de rust_cpu/
make run       # = uvicorn app:app --port 5000
```

Sin compilar también funciona: `app.py` hace fallback a Python puro
y `/cpu` responde con `"motor": "python"` en vez de `"motor": "rust"`.

## allow_threads vs detach

- PyO3 0.22 (este repo): `py.allow_threads(|| ...)` suelta el GIL.
- PyO3 >= 0.26: se renombró a `py.detach(|| ...)` (mismo efecto).
- Se fija `0.22` por estable/documentado; si subes a `>=0.26`,
  cambia `allow_threads` por `detach`.

## Por qué Rust no tiene data races

- Ownership: cada valor tiene un único dueño; el préstamo (`&`/`&mut`)
  lo revisa el compilador, no hay dos escritores a la vez.
- Send/Sync: solo los tipos marcados `Send` cruzan hilos y solo los
  `Sync` se comparten por referencia. Lo demás no compila.
- Resultado: si el crate compila, la race se rechazó en compilación,
  no con un lock en ejecución como en Python.
