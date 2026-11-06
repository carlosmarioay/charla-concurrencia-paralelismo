# Carga: bench sin instalar nada (stdlib + Docker)
1. Arranca una etapa: `docker build -t etapa0 etapa_0_flask_base` + `docker run -p 5000:5000 etapa0`
2. Bench: `python carga/run_carga.py --url http://localhost:5000 --peticiones 200 --concurrencia 20 --etapa etapa_0`
3. Compara: `python carga/comparativa.py` (lee `resultados/*.csv`, escribe `comparativa.csv`)
4. Gráfico: `pip install matplotlib` + `python carga/grafico.py` → `carga/grafico.png`
5. Alternativa: `hey -n 200 -c 20 http://localhost:5000/io` (más rápido, hay que instalarlo)
6. Repite el paso 2 cambiando `--etapa` en cada etapa para comparar.
