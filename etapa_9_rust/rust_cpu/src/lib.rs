// Etapa 9: primos en Rust, sin GIL ni data races.
use pyo3::prelude::*;

// División por prueba: simple, ideal para slides.
fn es_primo(x: u32) -> bool {
    if x < 2 {
        return false;
    }
    let tope = (x as f64).sqrt() as u32;
    (2..=tope).all(|i| x % i != 0)
}

// allow_threads suelta el GIL durante el cálculo.
// En PyO3 >=0.26 se renombró a detach (mismo efecto).
#[pyfunction]
fn contar_primos(py: Python<'_>, limite: u32) -> u32 {
    py.allow_threads(|| (2..=limite).filter(|&x| es_primo(x)).count() as u32)
}

// El .so final se importa como `import rust_cpu`.
#[pymodule]
fn rust_cpu(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(contar_primos, m)?)?;
    Ok(())
}
