# Prueba rápida de cada etapa (salud + suma + contador). Uso: .\probar.ps1
$puertos = @(5000,5001,5002,5003,5004,5005,5006,5007,5008,5009)
foreach ($p in $puertos) {
  Write-Output "=== puerto $p ==="
  try { Invoke-RestMethod -Uri "http://localhost:$p/salud" -TimeoutSec 5 | ConvertTo-Json -Compress } catch { "FALLO /salud: $_" }
  try { Invoke-RestMethod -Uri "http://localhost:$p/suma/100" -TimeoutSec 5 | ConvertTo-Json -Compress } catch { "FALLO /suma: $_" }
  try { Invoke-RestMethod -Uri "http://localhost:$p/contador" -TimeoutSec 5 | ConvertTo-Json -Compress } catch { "FALLO /contador: $_" }
}
