"""Oráculo del encargo va-01: cuadro de diálogo más bajo, marco a la mitad, texto con sombra."""
import re
import sys

t = open("scenes/ui/DialogueBox.tscn", encoding="utf-8").read()
errores = []
if "_horneado/ui/dialogue/options_frame@0.5x0.5.png" not in t:
    errores.append("el marco no apunta a la versión horneada a 0.5")
panel = t[t.index('[node name="Panel"'):t.index('[node name="Label"')]
top = float(re.search(r"offset_top = (-?[\d.]+)", panel).group(1))
bottom = float(re.search(r"offset_bottom = (-?[\d.]+)", panel).group(1))
if bottom - top > 150:
    errores.append(f"el panel mide {bottom - top:g} px de alto (máx. 150)")
if "patch_margin_left = 38" not in panel:
    errores.append("patch_margin_left no es 38")
label = t[t.index('[node name="Label"'):t.index('[node name="Hint"')]
if "font_shadow_color" not in label:
    errores.append("el texto no tiene sombra")
if "font_size = 16" not in label:
    errores.append("el texto no está a 16")
print("\n".join(errores) or "check_dialogo OK")
sys.exit(1 if errores else 0)
