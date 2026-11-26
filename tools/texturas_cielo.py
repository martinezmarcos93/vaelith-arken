"""Texturas del cielo nocturno, generadas (sin descargas ni licencias):
  T_Estrellas.png  equirectangular 4096x2048: estrellas con color y brillo variados + una banda
                   tenue de vía láctea. u = acimut, v = 0 en el cenit, 1 en el nadir.
  T_Luna.png       512x512: disco con mares, cráteres y oscurecimiento del borde; halo en el alfa.
Uso: python3 tools/texturas_cielo.py   Salida: assets_fuente/texturas/
"""
import math
import os

import numpy as np
from PIL import Image, ImageFilter

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SALIDA = os.path.join(RAIZ, "assets_fuente", "texturas")
rng = np.random.default_rng(7)


def ruido_suave(w, h, escalas):
    """Ruido de valor sumado en varias escalas (0..1)."""
    total = np.zeros((h, w), np.float32)
    peso = 0.0
    for esc, a in escalas:
        g = rng.random((max(2, h // esc), max(2, w // esc))).astype(np.float32)
        im = Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        total += a * np.asarray(im, np.float32) / 255.0
        peso += a
    return total / peso


def estrellas():
    W, H = 4096, 2048
    img = np.zeros((H, W, 3), np.float32)
    # Vía láctea: banda inclinada sobre la esfera (gran círculo), con nubes de ruido
    v, u = np.mgrid[0:H, 0:W].astype(np.float32)
    tita = v / H * math.pi                      # 0 cenit .. pi nadir
    fi = u / W * 2 * math.pi
    d = np.stack([np.sin(tita) * np.cos(fi), np.sin(tita) * np.sin(fi), np.cos(tita)], -1)
    eje = np.array([0.35, -0.55, 0.76]); eje /= np.linalg.norm(eje)
    banda = np.exp(-(d @ eje) ** 2 / 0.035)
    nubes = ruido_suave(W, H, [(256, 1.0), (64, 0.6), (16, 0.35)])
    via = banda * (0.35 + 0.65 * nubes) ** 2
    img += via[..., None] * np.array([0.07, 0.07, 0.10], np.float32)
    # Estrellas: más densas en la banda. Brillo con ley de potencia (pocas brillantes)
    n = 26000
    sin_t = rng.uniform(-1, 1, n)               # uniformes sobre la esfera
    tt = np.arccos(sin_t)
    ff = rng.uniform(0, 2 * math.pi, n)
    dd = np.stack([np.sin(tt) * np.cos(ff), np.sin(tt) * np.sin(ff), np.cos(tt)], -1)
    en_banda = np.exp(-(dd @ eje) ** 2 / 0.035)
    quedan = rng.random(n) < (0.45 + 0.55 * en_banda)
    tt, ff = tt[quedan], ff[quedan]
    brillo = rng.pareto(2.2, len(tt)) * 0.35 + 0.08
    tintes = np.array([[0.75, 0.85, 1.0], [1.0, 1.0, 1.0], [1.0, 0.92, 0.78], [1.0, 0.8, 0.65]], np.float32)
    tinte = tintes[rng.choice(4, len(tt), p=[0.3, 0.4, 0.2, 0.1])]
    ys = np.clip((tt / math.pi * H).astype(int), 0, H - 1)
    xs = (ff / (2 * math.pi) * W).astype(int) % W
    for y, x, b, c in zip(ys, xs, brillo, tinte):
        # cerca de los polos el píxel equirect se estira: ensanchar en x
        ancho = int(min(6, 1 / max(0.15, math.sin(y / H * math.pi))))
        for dx in range(-ancho // 2, ancho // 2 + 1):
            img[y, (x + dx) % W] += c * min(b, 4.0)
        if b > 1.2:  # las brillantes tienen un pequeño halo en cruz
            for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                img[min(H - 1, max(0, y + dy)), (x + dx) % W] += c * b * 0.25
    img = np.clip(img / 2.0, 0, 1) ** (1 / 2.2)  # textura sRGB; el material reescala el brillo
    Image.fromarray((img * 255).astype(np.uint8)).save(os.path.join(SALIDA, "T_Estrellas.png"))


def luna():
    N = 512
    y, x = np.mgrid[0:N, 0:N].astype(np.float32)
    px, py = (x - N / 2) / (N * 0.30), (y - N / 2) / (N * 0.30)   # disco de radio 1 = 30 % del lado
    r2 = px * px + py * py
    disco = r2 <= 1.0
    nz = np.sqrt(np.clip(1 - r2, 0, 1))
    luz = 0.35 + 0.65 * nz ** 0.6                                    # oscurecimiento del borde
    mares = ruido_suave(N, N, [(160, 1.0), (64, 0.6), (12, 0.25)])
    base = 0.86 - 0.42 * np.clip((mares - 0.42) * 2.6, 0, 1) + 0.05 * (ruido_suave(N, N, [(4, 1.0)]) - 0.5)
    for _ in range(40):                                              # cráteres
        cx, cy = rng.uniform(-0.9, 0.9, 2)
        rr = rng.pareto(3.0) * 0.025 + 0.012
        dist = np.sqrt((px - cx) ** 2 + (py - cy) ** 2) / rr
        base -= 0.05 * np.exp(-(dist / 0.7) ** 2)
        base += 0.03 * np.exp(-((dist - 1.0) / 0.2) ** 2)
    lum = np.clip(base * luz, 0, 1) * disco
    rgb = np.stack([lum * 0.93, lum * 0.96, lum * 1.0], -1)
    # Halo: el alfa marca el disco (1) y un resplandor suave alrededor (lo usa el material)
    rr = np.sqrt(r2)
    halo = np.clip(np.exp(-(rr - 1.0) * 2.2) * 0.35, 0, 0.35) * (rr > 1.0)
    alfa = np.where(disco, 1.0, halo)
    im = Image.fromarray((np.dstack([rgb, alfa]) * 255).astype(np.uint8), "RGBA")
    im = im.filter(ImageFilter.GaussianBlur(0.6))
    im.save(os.path.join(SALIDA, "T_Luna.png"))


if __name__ == "__main__":
    os.makedirs(SALIDA, exist_ok=True)
    estrellas()
    luna()
    print("OK", SALIDA)
