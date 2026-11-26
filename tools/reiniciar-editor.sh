#!/usr/bin/env bash
# Cierra el editor (si está) y lo abre con el proyecto. Log en ~/Aplicaciones/UE_5.8/_logs/editor.log
E=~/Aplicaciones/UE_5.8/Engine/Binaries/Linux/UnrealEditor
for p in $(pgrep -x UnrealEditor); do kill -TERM "$p"; done
for i in $(seq 1 30); do pgrep -x UnrealEditor >/dev/null || break; sleep 1; done
pgrep -x UnrealEditor >/dev/null && { echo "el editor no cerró"; exit 1; }
rm -f "${XDG_RUNTIME_DIR:-/tmp}/ue-mcp-session"
cd ~/Aplicaciones/UE_5.8 && setsid nohup "$E" "$HOME/src/vaelith-arken-unreal/VaelithArken.uproject" -log > _logs/editor.log 2>&1 < /dev/null &
echo "editor lanzado"
