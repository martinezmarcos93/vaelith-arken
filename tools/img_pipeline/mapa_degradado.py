#!/usr/bin/env python3
"""Mapa de degradado a la paleta de Vaelith Arken, conservando luces y sombras.

Por qué existe (relevamiento 2026-11-04): `recolor.py` busca el color de la
paleta más parecido a cada píxel. Con una paleta fría de 14 colores eso rompe
el orden de luminosidad: lo claro termina violeta, lo oscuro teal, y los props
se vuelven manchas ilegibles. Acá cada píxel conserva su luminosidad y se
lleva a una RAMPA de la paleta (oscuro → claro), elegida por su tono original:

  - verdes / cianes  → rampa teal
  - rojos / magentas / violetas saturados → rampa violeta
  - todo lo demás (piedra, madera, metal, hueso) → rampa índigo

Todos los colores salen de docs/guia_estilo_visual.md (núcleo + extendida).
El rojo de peligro #B41F1C no se usa: esto es arte de entorno.

Uso:  python3 -I tools/img_pipeline/mapa_degradado.py <entrada.png> <salida.png>
Solo numpy + Pillow.
"""
import colorsys
import sys

import numpy as np
from PIL import Image

RAMPAS = {
    "indigo": ["#010901", "#0C1A1C", "#11222E", "#162C3D", "#2B2E56", "#3B4272", "#3A5184", "#4947a7", "#766DBC"],
    "teal": ["#010901", "#02100E", "#041917", "#10423b", "#07424F", "#205188", "#4947a7", "#766DBC"],
    "violeta": ["#010901", "#352037", "#493165", "#4c4793", "#7a36a2", "#766DBC"],
}


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminancia(rgb):
    r, g, b = (c / 255 for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def rampa_de(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    grados = h * 360
    if s > 0.28 and v > 0.15:
        if 75 <= grados < 200:
            return "teal"
        if grados >= 280 or grados < 15:
            return "violeta"
    return "indigo"


def mapear(im):
    a = np.array(im.convert("RGBA"))
    rgb = a[..., :3].astype(float)
    lum = (0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]) / 255
    opaco = a[..., 3] > 0
    if not opaco.any():
        return im
    # estira el rango de la imagen para usar toda la rampa (el contraste interno
    # de cada prop se conserva; el tono general lo da la rampa)
    lo, hi = np.percentile(lum[opaco], 2), np.percentile(lum[opaco], 98)
    t = np.clip((lum - lo) / max(hi - lo, 1e-3), 0, 1)
    out = a.copy()
    cache = {}
    ys, xs = np.nonzero(opaco)
    for y, x in zip(ys, xs):
        clave = tuple(a[y, x, :3])
        if clave not in cache:
            cache[clave] = rampa_de(*clave)
        rampa = RAMPAS[cache[clave]]
        paso = rampa[min(len(rampa) - 1, int(round(t[y, x] * (len(rampa) - 1))))]
        out[y, x, :3] = hex_rgb(paso)
    return Image.fromarray(out, "RGBA")


if __name__ == "__main__":
    mapear(Image.open(sys.argv[1])).save(sys.argv[2])
