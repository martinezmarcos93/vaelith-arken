#!/usr/bin/env bash
# Mide rendimiento de un nivel en modo juego (no editor).
# Uso: tools/ue/medir.sh /Game/Pruebas/Lvl_Bosque_050 [/Game/...]
# Resultado: tabla por nivel (FPS medio, 1 % bajo, ms de GPU, VRAM máxima).
# Sin VSync ni límite de FPS, para ver el margen real. Resolución del monitor: 1360x768.
# Opcional: MEDIR_ARGS="-jugar -armas -ir=x,y,z,yaw" y MEDIR_ETIQUETA=loma para medir un punto del mapa.
set -uo pipefail
R="$(cd "$(dirname "$0")/../.." && pwd)"
E=~/Aplicaciones/UE_5.8/Engine/Binaries/Linux/UnrealEditor
OUT=~/Aplicaciones/UE_5.8/_logs/medicion; mkdir -p "$OUT"
pgrep -x UnrealEditor >/dev/null && { echo "cerrá el editor primero"; exit 1; }
printf "%-32s %8s %8s %8s %8s %10s\n" nivel fps_med fps_1% cpu_ms gpu_ms vram_max
for NIVEL in "$@"; do
  N=$(basename "$NIVEL")${MEDIR_ETIQUETA:+_$MEDIR_ETIQUETA}; CSVDIR=~/.config/Epic/UnrealEngine/5.8/Saved/Profiling/CSV; mkdir -p "$CSVDIR"; MARCA=$(mktemp)
  ( while true; do nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits; sleep 0.5; done ) > "$OUT/$N.vram" &
  VP=$!
  # En modo -game el log y los CSV van a ~/.config/Epic/UnrealEngine/5.8/Saved.
  # -csvExitOnCompletion no cierra el juego en Linux: se espera el CSV y se lo cierra.
  "$E" "$R/VaelithArken.uproject" "$NIVEL" -game -windowed -ResX=1360 -ResY=768 \
    -nosplash -unattended ${MEDIR_ARGS:-} -csvGpuStats -csvCaptureFrames=1500 \
    -ExecCmds="r.VSync 0,t.MaxFPS 0" -log > "$OUT/$N.log" 2>&1 &
  GP=$!
  CSV=""
  for i in $(seq 1 600); do
    CSV=$(find "$CSVDIR" -name '*.csv' -newer "$MARCA" -size +1k 2>/dev/null | head -1)
    if [ -n "$CSV" ]; then  # el CSV se escribe mientras corre: esperar a que deje de crecer
      T0=-1; until [ "$(stat -c %s "$CSV")" = "$T0" ]; do T0=$(stat -c %s "$CSV"); sleep 3; done
      break
    fi
    kill -0 $GP 2>/dev/null || break
    sleep 1
  done
  kill -TERM $GP 2>/dev/null; wait $GP 2>/dev/null
  kill $VP 2>/dev/null; rm -f "$MARCA"
  if [ -z "$CSV" ]; then printf "%-32s sin CSV (ver %s)\n" "$N" "$OUT/$N.log"; continue; fi
  cp "$CSV" "$OUT/$N.csv"
  python3 - "$OUT/$N.csv" "$OUT/$N.vram" "$N" <<'EOF'
import csv, sys, statistics as st
csv.field_size_limit(1 << 30)
filas = list(csv.reader(open(sys.argv[1], encoding="utf-8", errors="replace")))
cab = filas[0]; datos = [f for f in filas[1:] if len(f) >= len(cab)]  # las filas traen columnas de eventos extra al final
datos = datos[600:]  # descarta los primeros frames (carga y compilación de shaders)
def col(nombre):
    i = cab.index(nombre); vals = []
    for f in datos:  # al final del CSV se repite la cabecera y van los metadatos
        try: vals.append(float(f[i]))
        except ValueError: pass
    return vals
ft = col("FrameTime")
cpu = col("GameThreadTime") if "GameThreadTime" in cab else [0]
gpu = col("GPUTime") if "GPUTime" in cab else [0]
ft_ord = sorted(ft)
p99 = ft_ord[int(len(ft_ord) * 0.99) - 1]
vram = [int(x) for x in open(sys.argv[2]) if x.strip().isdigit()]
print(f"{sys.argv[3]:<32} {1000/st.mean(ft):8.1f} {1000/p99:8.1f} {st.mean(cpu):8.2f} {st.mean(gpu):8.2f} {max(vram) if vram else 0:7d} MiB")
EOF
done
