#!/usr/bin/env bash
# Lanza el juego, saca capturas en los segundos indicados y lo cierra.
# Uso: tools/ue/capturar.sh "<args extra, ej: -jugar -ir=x,y,z>" t1,t2,...   Salida: lista de PNG
# La ventana tiene que entrar en pantalla (si el escritorio la achica, el motor aborta al capturar): CAPTURA_X/CAPTURA_Y.
R="$(cd "$(dirname "$0")/../.." && pwd)"; S="$R/Saved/Capturas"; rm -f "$S"/cap_*.png; mkdir -p "$S"
pgrep -x UnrealEditor >/dev/null && { echo "cerrá el editor primero"; exit 1; }
M=$(mktemp); ULT=$(echo "$2" | tr ',' '\n' | sort -n | tail -1)
~/Aplicaciones/UE_5.8/Engine/Binaries/Linux/UnrealEditor "$R/VaelithArken.uproject" -game -windowed -ResX=${CAPTURA_X:-1280} -ResY=${CAPTURA_Y:-720} \
  -nosplash -unattended $1 -capturas="$2" -log > ~/Aplicaciones/UE_5.8/_logs/captura.log 2>&1 &
G=$!
LIM=$(python3 -c "print(int($ULT)+90)")
for i in $(seq 1 $LIM); do
  N=$(find "$S" -name '*.png' -newer "$M" | wc -l)
  [ "$N" -ge "$(echo "$2" | tr ',' '\n' | wc -l)" ] && { sleep 2; break; }
  kill -0 $G 2>/dev/null || break; sleep 1
done
kill -TERM $G 2>/dev/null; wait $G 2>/dev/null
find "$S" -name '*.png' -newer "$M" | sort; rm -f "$M"
grep -E '\[vaelith\]|Fatal|Assertion|Caught signal' "$R/Saved/Logs/VaelithArken.log" 2>/dev/null | sed 's/^\[[^]]*\]\[[^]]*\]//' | head -10
F=$(grep -c "Failed to compile Material" "$R/Saved/Logs/VaelithArken.log" 2>/dev/null); [ "${F:-0}" -gt 0 ] && echo "ATENCIÓN: $F material(es) no compilan en el juego (grep \"Failed to compile\" Saved/Logs/VaelithArken.log)"; true
