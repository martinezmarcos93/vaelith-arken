#!/usr/bin/env python3
"""Dibuja la tira de pinches góticos del Hazard (antes un ColorRect rojo).

Pixel art 1:1 en la paleta canónica (docs/guia_estilo_visual.md): hierro en
índigo con luz arriba a la izquierda y puntas en #B41F1C, que la guía
reserva justamente para "amenaza activa".

Uso:  python3 -I tools/sprite_pipeline/pinches.py <ancho> <alto> <salida.png>
"""
import sys

from PIL import Image

NEGRO, SOMBRA, MEDIO, LUZ = "#010901", "#11222E", "#2B2E56", "#3A5184"
ROJO, OXIDO = "#B41F1C", "#4d1409"


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


def dibujar(w, h):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = im.load()
    paso = 10                     # ancho de cada pinche
    base_h = 4                    # zócalo de hierro abajo
    for i, x0 in enumerate(range(0, w, paso)):
        alto = h - base_h - (2 if i % 2 else 0)   # alternan alto y bajo
        cx = x0 + paso / 2 - 0.5
        for y in range(h - base_h - alto, h - base_h):
            t = (y - (h - base_h - alto)) / alto           # 0 punta, 1 base
            media = max(0.5, t * (paso / 2 + 0.5))
            for x in range(x0, min(w, x0 + paso)):
                d = x - cx
                if abs(d) > media:
                    continue
                if t < 0.22:
                    c = ROJO if abs(d) < media - 0.3 or t < 0.1 else OXIDO
                elif abs(d) >= media - 1:
                    c = NEGRO                                 # contorno
                elif d < 0:
                    c = LUZ if t < 0.6 else MEDIO             # cara iluminada
                else:
                    c = SOMBRA
                px[x, y] = rgb(c)
    for y in range(h - base_h, h):
        for x in range(w):
            px[x, y] = rgb(NEGRO if y == h - base_h or x % 6 == 0 else (MEDIO if y == h - base_h + 1 else SOMBRA))
    return im


if __name__ == "__main__":
    dibujar(int(sys.argv[1]), int(sys.argv[2])).save(sys.argv[3])
