#!/usr/bin/env bash
# Capturas de referencia de las tres escenas jugables en <carpeta> + mosaicos.
# Uso: tools/relevamiento/recorrer_todo.sh <carpeta>
set -e
G=${GODOT:-$HOME/Aplicaciones/godot/Godot_v4.7.2-stable_linux.x86_64}
OUT=$1; mkdir -p "$OUT"
cd "$(dirname "$0")/../.."
timeout 120 "$G" --path . -s tools/relevamiento/recorrido.gd -- res://scenes/levels/Intro.tscn "$OUT" 150,500,900,1300 >/dev/null 2>&1 || true
timeout 120 "$G" --path . -s tools/relevamiento/recorrido.gd -- res://scenes/levels/Level1.tscn "$OUT" 200,900,1700,2500,3150,3500 >/dev/null 2>&1 || true
timeout 120 "$G" --path . -s tools/relevamiento/recorrido.gd -- res://scenes/levels/TorreSector.tscn "$OUT" 120,400,700 >/dev/null 2>&1 || true
python3 -I - "$OUT" <<'PY'
import sys, glob, os
from PIL import Image
out = sys.argv[1]
fs = sorted(glob.glob(os.path.join(out, "*_x*.png")))
cols = 3
filas = (len(fs) + cols - 1) // cols
c = Image.new("RGB", (640 * cols, 360 * filas))
for i, f in enumerate(fs):
    c.paste(Image.open(f).convert("RGB"), ((i % cols) * 640, (i // cols) * 360))
c.save(os.path.join(out, "mosaico.png"))
print(len(fs), "capturas")
PY
