"""Texturas de la fase D, generadas (sin descargas): agua y hierro oxidado. Todas tileables.
  T_Agua_N.png        normal de ondas suaves (lineal; el material lo desempaqueta)
  T_Oxido_C.png       color del hierro oxidado (sRGB)
  T_Oxido_ARM.png     AO, rugosidad, metal (lineal)
  T_Oxido_N.png       normal del óxido (lineal)
Uso: python3 tools/texturas_d.py   Salida: assets_fuente/texturas/
"""
import os

import numpy as np
from PIL import Image

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SALIDA = os.path.join(RAIZ, "assets_fuente", "texturas")
rng = np.random.default_rng(11)


def ruido_tileable(n, frecuencias):
    """Suma de ondas con frecuencias enteras: tilea perfecto."""
    y, x = np.mgrid[0:n, 0:n].astype(np.float32) / n * 2 * np.pi
    h = np.zeros((n, n), np.float32)
    for f, a in frecuencias:
        for _ in range(9):
            fx, fy = rng.integers(-f, f + 1, 2)
            if fx == 0 and fy == 0:
                continue
            h += a * np.sin(fx * x + fy * y + rng.uniform(0, 2 * np.pi))
    h -= h.min()
    return h / max(1e-6, h.max())


def normal_de_altura(h, fuerza):
    dx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * fuerza
    dy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) * fuerza
    n = np.dstack([-dx, -dy, np.ones_like(h)])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    return ((n * 0.5 + 0.5) * 255).astype(np.uint8)


def guardar(arr, nombre):
    Image.fromarray(arr).save(os.path.join(SALIDA, nombre))


def agua():
    h = ruido_tileable(512, [(2, 1.0), (4, 0.6), (7, 0.35), (11, 0.2)])
    guardar(normal_de_altura(h, 6.0), "T_Agua_N.png")


def oxido():
    n = 512
    base = ruido_tileable(n, [(3, 1.0), (8, 0.5), (19, 0.3), (41, 0.15)])
    manchas = ruido_tileable(n, [(2, 1.0), (5, 0.7), (13, 0.3)])
    oxido = np.clip((manchas - 0.35) * 2.2, 0, 1) ** 1.3          # dónde ganó el óxido
    grano = rng.random((n, n)).astype(np.float32) * 0.12
    hierro = np.array([0.16, 0.16, 0.17])
    rojo = np.array([0.36, 0.16, 0.07])
    naranja = np.array([0.55, 0.28, 0.10])
    col = hierro[None, None] * (0.7 + 0.5 * base[..., None])
    rust = rojo[None, None] * (1 - base[..., None]) + naranja[None, None] * base[..., None]
    col = col * (1 - oxido[..., None]) + rust * oxido[..., None]
    col = np.clip(col + grano[..., None] * 0.3 - 0.03, 0, 1) ** (1 / 2.2)
    guardar((col * 255).astype(np.uint8), "T_Oxido_C.png")
    ao = 0.75 + 0.25 * base
    rug = np.clip(0.45 + 0.5 * oxido + grano, 0, 1)
    met = np.clip(0.85 - 0.8 * oxido, 0, 1)
    guardar((np.dstack([ao, rug, met]) * 255).astype(np.uint8), "T_Oxido_ARM.png")
    guardar(normal_de_altura(base * 0.5 + oxido * 0.5 + grano, 3.0), "T_Oxido_N.png")


if __name__ == "__main__":
    os.makedirs(SALIDA, exist_ok=True)
    agua()
    oxido()
    print("OK", SALIDA)
