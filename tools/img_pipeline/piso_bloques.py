#!/usr/bin/env python3
"""Tira de piso de 3 sillares para romper la repetición cada 64 px.

Crítica 2026-11-04: "incorporar pequeñas variaciones en las plataformas para
evitar la repetición mecánica". Toma el tile (64 px de ancho) y arma una
tira de 192 px con tres sillares de ancho distinto (48, 80 y 64 px), cada
uno con el tile desfasado (0, 21 y 43 px) y una junta oscura de 1 px en el
cuerpo (no en la superficie). Las juntas caen sin ritmo fijo y se leen como
uniones de piedra; el período pasa a 192 px.

Uso:  python3 -I tools/img_pipeline/piso_bloques.py <tile.png> <salida.png> [borde=6]
"""
import sys

import numpy as np
from PIL import Image

JUNTA = (1, 9, 1, 255)  # #010901


def tira(tile, borde=6):
    a = np.array(tile.convert("RGBA"))
    ancha = np.concatenate([a, a], axis=1)  # para recortar bloques de hasta 128 px
    bloques, x = [], 0
    for ancho, desfase in ((48, 0), (80, 21), (64, 43)):
        b = np.roll(ancha, desfase, axis=1)[:, :ancho].copy()
        b[borde:, 0] = JUNTA
        bloques.append(b)
    return Image.fromarray(np.concatenate(bloques, axis=1), "RGBA")


if __name__ == "__main__":
    borde = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    tira(Image.open(sys.argv[1]), borde).save(sys.argv[2])
