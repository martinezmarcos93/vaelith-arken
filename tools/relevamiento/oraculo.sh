#!/usr/bin/env bash
# Oráculo visual/técnico de Vaelith Arken. Sale con código != 0 si algo falla.
#   1. El proyecto importa sin errores.
#   2. Las escenas de scenes/ cargan sin errores (se ignora el ruido de cierre).
#   3. Ningún Sprite2D / TextureRect / TextureProgressBar tiene escala distinta de ±1
#      (pixel 1:1). Quedan afuera las PointLight2D, las texturas procedurales
#      (SubResource: sombras de degradado) y Zombi/BringerOfDeath, que no se usan
#      en ningún nivel.
#   4. Ningún prop flota sobre el piso en Intro, Level1 y TorreSector
#      (salvo SpectralGate, que flota a propósito).
# Uso:  bash tools/relevamiento/oraculo.sh        (desde la raíz del repo)
set -u
G=${GODOT:-$HOME/Aplicaciones/godot/Godot_v4.7.2-stable_linux.x86_64}
cd "$(dirname "$0")/../.."
TMP=$(mktemp -d)
falla=0
ruido='resources still in use|RID allocations|leaked at exit|ObjectDB instances|~CompressedTexture2D|RenderingServer::get_singleton|~Utilities|Texture with GL ID'

# dos pasadas: en la primera, un PNG nuevo puede dar "Failed loading resource"
# pasajero (la escena se escanea antes de importar la imagen); vale la segunda.
timeout 900 "$G" --headless --path . --import > /dev/null 2>&1
timeout 900 "$G" --headless --path . --import > "$TMP/import.log" 2>&1
if grep -E "ERROR" "$TMP/import.log" | grep -vqE "$ruido"; then
  echo "FALLA import:"; grep -E "ERROR" -A2 "$TMP/import.log" | grep -vE "$ruido" | head -10; falla=1
fi

for s in $(find scenes -name '*.tscn' | sort); do
  timeout 60 "$G" --headless --path . --quit-after 120 "res://$s" > "$TMP/l.log" 2>&1
  if grep -E "SCRIPT ERROR|ERROR" "$TMP/l.log" | grep -vqE "$ruido"; then
    echo "FALLA escena $s:"; grep -E "ERROR" -A3 "$TMP/l.log" | grep -vE "$ruido" | head -8; falla=1
  fi
done

python3 -I - <<'PY' || falla=1
import re, glob, sys
malos = []
for scn in sorted(glob.glob("scenes/**/*.tscn", recursive=True)):
    if scn.endswith(("Zombi.tscn", "BringerOfDeath.tscn")):
        continue
    t = open(scn, encoding="utf-8").read()
    for b in re.split(r'\n(?=\[node )', t):
        ty = re.search(r'type="([^"]+)"', b.split("\n")[0])
        if not ty or ty.group(1) not in ("Sprite2D", "TextureRect", "TextureProgressBar", "AnimatedSprite2D"):
            continue
        if "texture = SubResource(" in b:
            continue
        m = re.search(r'\nscale = Vector2\(([-\d.e]+), ([-\d.e]+)\)', b)
        if m and (abs(float(m.group(1))) != 1 or abs(float(m.group(2))) != 1):
            malos.append(f"{scn}: {re.search(r'name=\"([^\"]+)\"', b).group(1)} scale {m.group(1)},{m.group(2)}")
if malos:
    print("FALLA escala no 1:1:"); print("\n".join(malos[:20])); sys.exit(1)
PY

for par in "Intro:" "Level1:" "TorreSector:MG,FG,Threshold"; do
  esc=${par%%:*}; padres=${par#*:}
  timeout 120 "$G" --headless --path . -s tools/relevamiento/props_flotantes.gd -- "res://scenes/levels/$esc.tscn" $padres 2>/dev/null \
    | grep "^PROP" | grep -v "SpectralGate" | awk '{split($NF,a,"="); if (a[2]+0 > 0.5) print}' > "$TMP/flota.txt"
  if [ -s "$TMP/flota.txt" ]; then echo "FALLA props flotando en $esc:"; cat "$TMP/flota.txt"; falla=1; fi
done

rm -rf "$TMP"
if [ $falla -eq 0 ]; then echo "ORACULO OK"; fi
exit $falla
