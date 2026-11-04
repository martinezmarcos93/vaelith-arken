#!/usr/bin/env python3
"""Piso legible: superficie clara arriba, cuerpo oscuro y de bajo contraste.

Crítica 2026-11-04: el patrón del suelo era "demasiado repetitivo y
contrastado" y no se distinguía qué es transitable. Se re-mapea el tile con
mapa_degradado en dos tramos de la rampa: las primeras `borde` filas (la
superficie que se pisa) en un tramo medio-claro, y el resto en un tramo
oscuro y angosto, así el patrón de la roca queda como textura de fondo.

Uso:  python3 -I tools/img_pipeline/piso_legible.py <entrada.png> <salida.png> [borde=6]
"""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mapa_degradado import mapear  # noqa: E402

SUPERFICIE = (0.55, 0.95)
CUERPO = (0.25, 0.55)


def piso(im, borde=6):
    im = im.convert("RGBA")
    # en gris: así mapa_degradado usa siempre la rampa índigo (piedra) y no
    # la teal/violeta según el tinte que traía el pack
    gris = im.convert("L").convert("RGBA")
    gris.putalpha(im.getchannel("A"))
    im = gris
    w, h = im.size
    arriba = mapear(im.crop((0, 0, w, borde)), *SUPERFICIE)
    abajo = mapear(im.crop((0, borde, w, h)), *CUERPO)
    out = Image.new("RGBA", (w, h))
    out.paste(arriba, (0, 0))
    out.paste(abajo, (0, borde))
    return out


if __name__ == "__main__":
    borde = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    piso(Image.open(sys.argv[1]), borde).save(sys.argv[2])
