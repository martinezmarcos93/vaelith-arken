#!/usr/bin/env bash
# Convierte el audio del proyecto Godot a WAV con los nombres que usa el juego y sintetiza
# los efectos que faltan (latido, respiración, campanas, lamento). Salida: assets_fuente/audio/
set -euo pipefail
R="$(cd "$(dirname "$0")/../.." && pwd)"; G=~/src/vaelith-arken/assets/audio; O="$R/assets_fuente/audio"
mkdir -p "$O"
c() { ffmpeg -loglevel error -y -i "$G/$1" ${3:-} -ar 44100 -ac ${4:-2} "$O/$2.wav"; }
# Música (MP3 propios del proyecto original)
c music/intro.mp3 mus_intro; c music/level1.mp3 mus_catacumba; c music/level1_b.mp3 mus_bosque; c music/boss.mp3 mus_jefe
# Ambiente
c sfx/ambient/cave_loop.ogg amb_cueva; c sfx/ambient/torch_loop.ogg amb_antorcha "" 1; c sfx/ambient/water_stream_loop.ogg amb_agua "" 1
c sfx/ambient/presence_drone.wav amb_presencia
# Combate y mundo
c sfx/combat/sword_swing_01.ogg sfx_tajo "" 1; c sfx/combat/impact_flesh_01.ogg sfx_impacto_carne "" 1
c sfx/combat/impact_block_02.ogg sfx_impacto_escudo "" 1; c sfx/combat/impact_block_01.ogg sfx_bloqueo "" 1
c sfx/combat/parry_01.ogg sfx_parada "" 1; c sfx/combat/blade_clash_02.wav sfx_escudo_roto "" 1
c sfx/combat/blade_ring_01.wav sfx_desenvainar "" 1
c sfx/player/grunt_attack_01.wav sfx_esfuerzo "" 1; c sfx/player/grunt_hurt_01.wav sfx_herido "" 1
c sfx/player/footstep_stone_01.ogg sfx_paso "" 1
c sfx/world/portcullis.ogg sfx_reja "" 1; c sfx/world/gate_close.ogg sfx_cerrado "" 1; c sfx/world/gate_open.ogg sfx_cadena "" 1
c sfx/world/stone_impact_02.ogg sfx_huesos "-af asetrate=44100*1.6,aresample=44100" 1
# No-muertos: voces humanas bajadas de tono
c sfx/player/grunt_hurt_02.wav sfx_grunido "-af asetrate=44100*0.62,aresample=44100,lowpass=f=1800" 1
c sfx/player/grunt_hurt_03.wav sfx_muerte_nomuerto "-af asetrate=44100*0.55,aresample=44100,aecho=0.8:0.7:60:0.3" 1
c sfx/ambient/presence_drone.wav sfx_lamento "-t 3.5 -af asetrate=44100*1.35,aresample=44100,afade=t=in:d=0.4,afade=t=out:st=2.6:d=0.9,aecho=0.8:0.8:120:0.4" 1
# Sintetizados
s() { ffmpeg -loglevel error -y -f lavfi -i "$2" -ar 44100 -ac 1 ${3:-} "$O/$1.wav"; }
s sfx_latido "aevalsrc='0.9*sin(2*PI*48*t)*(exp(-14*t)+0.7*exp(-14*abs(t-0.28))*gte(t,0.28))+0.5*sin(2*PI*48*t)*(exp(-14*abs(t-1.1))*gte(t,1.1)+0.7*exp(-14*abs(t-1.38))*gte(t,1.38))':d=2.2"
s sfx_respiracion "anoisesrc=d=2.4:c=pink:a=0.5" "-af bandpass=f=900:w=700,volume='0.15+0.85*sin(PI*t/1.1)*lt(t,1.1)+0.6*sin(PI*(t-1.3)/1.1)*gte(t,1.3)':eval=frame,afade=t=out:st=2.1:d=0.3"
campana() { s "$1" "aevalsrc='(sin(2*PI*$2*t)+0.5*sin(2*PI*$2*2.76*t)+0.25*sin(2*PI*$2*5.4*t))*exp(-$3*t)*0.4':d=$4" "-af aecho=0.8:0.85:180|340:0.4|0.25"; }
campana sfx_manos 660 1.6 3.5
campana sfx_altar 392 0.9 5
campana sfx_liberacion 880 1.2 4.5
s sfx_recuerdo "aevalsrc='0.35*sin(2*PI*110*t+3*sin(2*PI*0.5*t))*min(t/1.5,1)*exp(-0.5*t)+0.2*sin(2*PI*164.8*t)*exp(-0.8*t)':d=6" "-af aecho=0.8:0.9:400|700:0.5|0.35"
ls "$O" | wc -l
