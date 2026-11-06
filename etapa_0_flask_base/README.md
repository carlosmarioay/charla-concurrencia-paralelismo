# Etapa 0 — Flask base
Build: `docker build -t etapa0 .`
Run: `docker run -p 5000:5000 etapa0`
Probar: `curl localhost:5000/salud` · `curl localhost:5000/io`
Probar: `curl localhost:5000/cpu` · `curl localhost:5000/suma/100`
Probar: `curl localhost:5000/contador`
Probar: `curl -X POST localhost:5000/validar -H "Content-Type: application/json" -d "{\"nombre\":\"Ana\",\"edad\":30,\"email\":\"a@x.com\"}"`
Cuellos: io bloquea 1s · cpu retiene el GIL · suma es O(n) con bucle.
Cuellos: validar es manual con `if` · contador es memoria local.
