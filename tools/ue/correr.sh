#!/usr/bin/env bash
# Abre el editor con el proyecto, ejecuta un script de Python y lo cierra.
# El script debe terminar llamando a unreal.SystemLibrary.quit_editor() (ver _cerrar.py).
# Uso: tools/ue/correr.sh tools/ue/<script>.py     Log: ~/Aplicaciones/UE_5.8/_logs/<script>.log
set -euo pipefail
R="$(cd "$(dirname "$0")/../.." && pwd)"
S="$(realpath "$1")"; N="$(basename "$S" .py)"
pgrep -x UnrealEditor >/dev/null && { echo "cerrá el editor primero"; exit 1; }
LOG=~/Aplicaciones/UE_5.8/_logs/$N.log
TMP="$(mktemp --suffix=.py)"; trap 'rm -f "$TMP"' EXIT
{ echo "__file__ = '$S'"; cat "$S"; echo; cat "$R/tools/ue/_cerrar.py"; } > "$TMP"
timeout ${CORRER_TIMEOUT:-900} ~/Aplicaciones/UE_5.8/Engine/Binaries/Linux/UnrealEditor "$R/VaelithArken.uproject" \
  -ExecutePythonScript="$TMP" -unattended -nosplash -log > "$LOG" 2>&1 || true
grep -E '\[vaelith\]|LogPython: Error' "$LOG" | sed 's/^\[[^]]*\]\[[^]]*\]//' | head -40
grep -q 'LogPython: Error' "$LOG" && exit 1 || exit 0
