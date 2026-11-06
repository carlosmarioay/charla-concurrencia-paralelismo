# Revisa si este Python corre con GIL o sin GIL.
import sys
print(sys.version)
gil = getattr(sys, "_is_gil_enabled", None)
if gil is None:
    print("gil_activo: True (este Python no conoce _is_gil_enabled)")
else:
    print("gil_activo:", gil())
# True = 3.15 normal; False = 3.15t sin GIL.
# Corre: python check_gil.py
