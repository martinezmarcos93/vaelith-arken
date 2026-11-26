#!/usr/bin/env bash
# Abre el juego y graba la pantalla con el sonido hasta que el juego se cierra.
# Graba con ffmpeg desde X11, sin tocar la ventana del juego (los grabadores que
# toman la ventana le pueden mandar un cierre). Codifica en la GPU (NVENC) para no robarle CPU al juego.
# Uso: tools/grabar_partida.sh [args extra del juego]   Salida: ~/Vídeos/vaelith-AAAA-MM-DD-HHMM.mp4
R="$(cd "$(dirname "$0")/.." && pwd)"
pgrep -x UnrealEditor >/dev/null && { echo "el juego o el editor ya están abiertos: cerralos primero"; exit 1; }
DIR="$HOME/Vídeos"; mkdir -p "$DIR"
OUT="$DIR/vaelith-$(date +%Y-%m-%d-%H%M).mp4"
TAM=$(xdpyinfo 2>/dev/null | awk '/dimensions:/{print $2}'); TAM=${TAM:-1360x768}

~/Aplicaciones/UE_5.8/Engine/Binaries/Linux/UnrealEditor "$R/VaelithArken.uproject" -game -windowed -ResX=1280 -ResY=720 \
  "$@" > /tmp/vaelith-grabacion-juego.log 2>&1 &
G=$!
sleep 3
ffmpeg -hide_banner -loglevel error -y \
  -f x11grab -framerate 30 -video_size "$TAM" -i "${DISPLAY:-:1}" \
  -f pulse -i @DEFAULT_MONITOR@ \
  -c:v h264_nvenc -preset p5 -cq 21 -pix_fmt yuv420p -c:a aac -b:a 160k "$OUT" < /dev/null &
F=$!
echo "grabando en $OUT (se detiene sola al cerrar el juego)"
wait $G
kill -INT $F 2>/dev/null; wait $F 2>/dev/null
ls -la "$OUT"
