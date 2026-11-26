#!/usr/bin/env bash
# Capturas de referencia del recorrido (menú, catacumba, cementerio, loma, cielo, pueblo, bosque oscuro, torre)
# y un mosaico. Uso: tools/ue/capturas_ref.sh <carpeta_salida> [vistas separadas por coma]
R="$(cd "$(dirname "$0")/../.." && pwd)"
D="${1:?carpeta}"; mkdir -p "$D"
declare -A V=(
  [menu]="|25"
  [catacumba]="-jugar -armas|32"
  [cementerio]="-jugar -armas -ir=6400,12000,230,90,-3|42"
  [loma]="-jugar -armas -ir=16200,47000,2420,7,-9|42"
  [cielo]="-jugar -armas -ir=16200,47000,2420,-55,28|42"
  [pueblo]="-jugar -armas -ir=37500,49800,600,7,-2|42"
  [oscuro]="-jugar -armas -ir=9500,50500,1440,157,-5|42"
  [torre]="-jugar -armas -ir=-8200,56500,30,160,-4|42"
)
ORDEN="${2:-menu,catacumba,cementerio,loma,cielo,pueblo,oscuro,torre}"
for n in ${ORDEN//,/ }; do
  IFS='|' read -r args t <<< "${V[$n]}"
  "$R/tools/ue/capturar.sh" "$args" "$t" 2>&1 | grep -E "ATENCIÓN|Fatal|Assertion" || true
  f=$(ls -t "$R"/Saved/Capturas/cap_*.png 2>/dev/null | head -1)
  [ -n "$f" ] && cp "$f" "$D/$n.png" && echo "ok $n" || echo "FALLO $n"
done
python3 - "$D" "$ORDEN" <<'PY'
import sys, os
from PIL import Image
d, orden = sys.argv[1], sys.argv[2].split(",")
ims = [Image.open(os.path.join(d, n + ".png")).convert("RGB").resize((640, 360)) for n in orden if os.path.exists(os.path.join(d, n + ".png"))]
W = Image.new("RGB", (1280, 360 * ((len(ims) + 1) // 2)))
for i, im in enumerate(ims):
    W.paste(im, ((i % 2) * 640, (i // 2) * 360))
W.save(os.path.join(d, "mosaico.png"))
PY
