# make develop compila Rust; make run levanta la API.
develop:
	cd rust_cpu && maturin develop --release

run:
	uvicorn app:app --port 5000
