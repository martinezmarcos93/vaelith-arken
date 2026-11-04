"""Oráculo del encargo va-02: calavera a 24 px y corrupción en el violeta canónico."""
import sys

t = open("scenes/ui/HUD.tscn", encoding="utf-8").read()
errores = []
if "skull_icon@0.75x0.75.png" not in t:
    errores.append("la calavera no usa la versión a 0.75")
cor = t[t.index('[node name="CorruptionLabel"'):t.index('[node name="BossBar"')]
if "Color(0.463, 0.427, 0.737, 1)" not in cor:
    errores.append("Corrupción no usa #766DBC")
if "font_size = 14" not in cor:
    errores.append("Corrupción no está a 14")
icono = t[t.index('[node name="SkullIcon"'):t.index('[node name="SkullCount"')]
if "offset_right = 28.0" not in icono:
    errores.append("SkullIcon no mide 24 px")
print("\n".join(errores) or "check_hud OK")
sys.exit(1 if errores else 0)
