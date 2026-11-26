#!/usr/bin/env bash
# Reconstruye Lvl_Vaelith desde construir_nivel.py (el mapa es 100 % generado por script).
# Respalda el mapa anterior en Saved/respaldo_mapa/ antes de borrarlo.
# Uso: tools/ue/regenerar_nivel.sh
set -euo pipefail
R="$(cd "$(dirname "$0")/../.." && pwd)"
M="$R/Content/Vaelith/Mapas/Lvl_Vaelith.umap"
if [ -f "$M" ]; then
  mkdir -p "$R/Saved/respaldo_mapa"
  cp "$M" "$R/Saved/respaldo_mapa/Lvl_Vaelith-$(date +%Y%m%d-%H%M%S).umap"
  rm "$M"
fi
CORRER_TIMEOUT=3000 "$R/tools/ue/correr.sh" "$R/tools/ue/construir_nivel.py" 2>&1 | grep -v "Violación de segmento"
test -f "$M" || { echo "ERROR: el mapa no se generó"; exit 1; }
