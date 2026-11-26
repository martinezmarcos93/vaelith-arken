"""Arte de interfaz propio (reemplaza los PNG del proyecto Godot). Todo generado: se puede reajustar.

Estilo: marco gótico dorado, hueso, violeta de Pharasma, piedra oscura. Supermuestreo x4 para bordes limpios.
Salida (assets_fuente/ui_unreal/):
  T_UI_Titulo, T_UI_Subtitulo, T_UI_Boton, T_UI_Boton_Sobre, T_UI_Placa (9-slice), T_UI_Barra_Marco,
  T_UI_Barra_Pista, T_UI_Espiral, T_UI_Rombo, T_UI_Mapa_Marco, T_UI_Flecha, T_UI_Pergamino,
  T_Mapa_Exterior (mapa del mundo en tinta sobre pergamino, desde tools/terreno.py), T_Mapa_Catacumba (desde el plano).
Uso: python3 tools/ui_generar.py
"""
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SALIDA = os.path.join(RAIZ, "assets_fuente", "ui_unreal")
FUENTES = os.path.join(RAIZ, "assets_fuente", "fuentes")
sys.path.insert(0, os.path.join(RAIZ, "tools"))
import terreno as TER  # noqa: E402

SS = 4
ORO = (214, 178, 102)
ORO_CLARO = (246, 222, 160)
ORO_OSCURO = (122, 88, 38)
HUESO = (226, 218, 198)
VIOLETA = (150, 96, 230)
PIEDRA = (20, 18, 24)
TINTA = (52, 38, 26)


def fuente(nombre, tam):
    return ImageFont.truetype(os.path.join(FUENTES, nombre), tam)


def lienzo(w, h):
    return Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))


def bajar(im, w, h):
    return im.resize((w, h), Image.LANCZOS)


def guardar(im, nombre):
    im.save(os.path.join(SALIDA, nombre + ".png"))


def gradiente_oro(w, h):
    """Relleno dorado con brillo arriba y sombra abajo (metal grabado)."""
    y = np.linspace(0, 1, h)[:, None]
    t = 0.5 + 0.5 * np.cos((y - 0.28) * math.pi * 1.6)
    base = np.array(ORO_OSCURO)[None, None] * (1 - t[..., None]) + np.array(ORO_CLARO)[None, None] * t[..., None]
    base = np.repeat(base, w, axis=1)
    return Image.fromarray(base.clip(0, 255).astype(np.uint8), "RGB")


def texto_grabado(texto, f, w, h, sombra=True, brillo_violeta=False):
    """Texto dorado con relleno de metal, contorno oscuro y halo opcional violeta."""
    im = lienzo(w, h)
    d = ImageDraw.Draw(im)
    caja = d.textbbox((0, 0), texto, font=f)
    x = (w * SS - (caja[2] - caja[0])) // 2 - caja[0]
    y = (h * SS - (caja[3] - caja[1])) // 2 - caja[1]
    mascara = Image.new("L", im.size, 0)
    ImageDraw.Draw(mascara).text((x, y), texto, font=f, fill=255)
    if brillo_violeta:
        halo = Image.new("RGBA", im.size, VIOLETA + (0,))
        halo.putalpha(mascara.filter(ImageFilter.GaussianBlur(14 * SS)).point(lambda v: int(v * 0.55)))
        im = Image.alpha_composite(im, halo)
    if sombra:
        borde = mascara.filter(ImageFilter.MaxFilter(2 * SS + 1))
        capa = Image.new("RGBA", im.size, (12, 8, 6, 0))
        capa.putalpha(borde)
        im = Image.alpha_composite(im, capa)
    oro = gradiente_oro(im.size[0], im.size[1]).convert("RGBA")
    oro.putalpha(mascara)
    return Image.alpha_composite(im, oro)


def espiral(d, cx, cy, r, ancho, color, vueltas=2.4):
    pts = []
    for k in range(240):
        t = k / 239
        a = t * vueltas * 2 * math.pi
        rr = r * (0.08 + 0.92 * t)
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d.line(pts, fill=color, width=max(1, int(ancho)), joint="curve")


def filigrana(d, x0, y0, x1, y1, color, grosor):
    """Marco con esquinas de arco apuntado (gótico) y una espiral en el centro de los lados largos."""
    g = grosor
    d.rectangle([x0, y0, x1, y1], outline=color, width=g)
    d.rectangle([x0 + 3 * g, y0 + 3 * g, x1 - 3 * g, y1 - 3 * g], outline=ORO_OSCURO, width=max(1, g // 2))
    r = 7 * g
    for cx, cy, a0 in ((x0, y0, 0), (x1, y0, 90), (x1, y1, 180), (x0, y1, 270)):
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 90, fill=color, width=g)
        d.ellipse([cx - 1.6 * g, cy - 1.6 * g, cx + 1.6 * g, cy + 1.6 * g], fill=ORO_CLARO)


def piedra(w, h, alfa=235, semilla=1):
    rng = np.random.default_rng(semilla)
    n = rng.random((h // 8 + 1, w // 8 + 1)).astype(np.float32)
    n = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
    base = np.array(PIEDRA, np.float32)[None, None] * (0.75 + 0.5 * n[..., None])
    im = Image.fromarray(base.clip(0, 255).astype(np.uint8), "RGB").convert("RGBA")
    im.putalpha(alfa)
    return im


# ---------------------------------------------------------------- piezas

def titulo():
    w, h = 1800, 560
    f = fuente("Cinzel.ttf", 250 * SS)
    im = texto_grabado("VAELITH", f, w, 380, brillo_violeta=True)
    total = lienzo(w, h)
    total.alpha_composite(im, (0, 0))
    f2 = fuente("Cinzel.ttf", 82 * SS)
    arken = texto_grabado("A R K E N", f2, w, 150)
    total.alpha_composite(arken, (0, 380 * SS))
    d = ImageDraw.Draw(total)
    y = 395 * SS
    for lado in (-1, 1):
        x0 = w * SS // 2 + lado * 330 * SS
        x1 = w * SS // 2 + lado * 820 * SS
        d.line([(x0, y + 60 * SS), (x1, y + 60 * SS)], fill=ORO + (255,), width=4 * SS)
        d.polygon([(x1, y + 48 * SS), (x1 + lado * 26 * SS, y + 60 * SS), (x1, y + 72 * SS)], fill=ORO + (255,))
    espiral(d, w * SS // 2, 12 * SS + 18 * SS, 16 * SS, 3 * SS, VIOLETA + (255,))
    guardar(bajar(total, w, h), "T_UI_Titulo")


def subtitulo():
    w, h = 1300, 200
    im = lienzo(w, h)
    d = ImageDraw.Draw(im)
    banda = piedra(w * SS, 110 * SS, 210, 3)
    im.alpha_composite(banda, (0, 45 * SS))
    d.line([(60 * SS, 45 * SS), (w * SS - 60 * SS, 45 * SS)], fill=ORO + (255,), width=3 * SS)
    d.line([(60 * SS, 155 * SS), (w * SS - 60 * SS, 155 * SS)], fill=ORO + (255,), width=3 * SS)
    for cx in (110 * SS, w * SS - 110 * SS):
        espiral(d, cx, 100 * SS, 34 * SS, 4 * SS, VIOLETA + (255,))
    txt = texto_grabado("La espada de Pharasma", fuente("Cinzel.ttf", 70 * SS), w, h, sombra=True)
    im.alpha_composite(txt)
    guardar(bajar(im, w, h), "T_UI_Subtitulo")


def boton(sobre):
    w, h = 640, 140
    im = lienzo(w, h)
    m = 10 * SS
    cuerpo = piedra(w * SS - 2 * m, h * SS - 2 * m, 240 if not sobre else 250, 5)
    im.alpha_composite(cuerpo, (m, m))
    d = ImageDraw.Draw(im)
    color = (ORO_CLARO if sobre else ORO) + (255,)
    filigrana(d, m, m, w * SS - m, h * SS - m, color, 3 * SS)
    for cx in (52 * SS, w * SS - 52 * SS):
        espiral(d, cx, h * SS // 2, 20 * SS, 3 * SS, (VIOLETA if sobre else ORO_OSCURO) + (255,))
    if sobre:
        brillo = Image.new("RGBA", im.size, VIOLETA + (0,))
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).rectangle([m, m, w * SS - m, h * SS - m], fill=60)
        brillo.putalpha(mask.filter(ImageFilter.GaussianBlur(20 * SS)))
        im = Image.alpha_composite(im, brillo)
    guardar(bajar(im, w, h), "T_UI_Boton_Sobre" if sobre else "T_UI_Boton")


def placa():
    """Panel 9-slice de 256: márgenes de 48 px quedan fijos al estirar."""
    n = 256
    im = lienzo(n, n)
    im.alpha_composite(piedra(n * SS - 16 * SS, n * SS - 16 * SS, 225, 8), (8 * SS, 8 * SS))
    d = ImageDraw.Draw(im)
    filigrana(d, 8 * SS, 8 * SS, n * SS - 8 * SS, n * SS - 8 * SS, ORO + (255,), 3 * SS)
    guardar(bajar(im, n, n), "T_UI_Placa")


def barras():
    w, h = 420, 44
    im = lienzo(w, h)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([2 * SS, 6 * SS, w * SS - 2 * SS, h * SS - 6 * SS], 6 * SS, outline=ORO + (255,), width=3 * SS)
    d.rounded_rectangle([7 * SS, 11 * SS, w * SS - 7 * SS, h * SS - 11 * SS], 4 * SS, outline=ORO_OSCURO + (255,), width=1 * SS)
    for cx in (2 * SS, w * SS - 2 * SS):
        d.polygon([(cx, h * SS // 2 - 12 * SS), (cx + (9 if cx < 50 else -9) * SS, h * SS // 2), (cx, h * SS // 2 + 12 * SS)], fill=ORO_CLARO + (255,))
    guardar(bajar(im, w, h), "T_UI_Barra_Marco")
    pista = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(pista).rounded_rectangle([8, 12, w - 8, h - 12], 4, fill=(10, 8, 12, 210))
    guardar(pista, "T_UI_Barra_Pista")


def iconos():
    n = 128
    im = lienzo(n, n)
    d = ImageDraw.Draw(im)
    espiral(d, n * SS // 2, n * SS // 2, 54 * SS, 9 * SS, (255, 255, 255, 255), 2.2)
    guardar(bajar(im, n, n), "T_UI_Espiral")
    im = lienzo(64, 64)
    d = ImageDraw.Draw(im)
    c = 32 * SS
    d.polygon([(c, 4 * SS), (60 * SS, c), (c, 60 * SS), (4 * SS, c)], fill=(255, 255, 255, 255))
    d.polygon([(c, 14 * SS), (50 * SS, c), (c, 50 * SS), (14 * SS, c)], fill=(200, 200, 200, 255))
    guardar(bajar(im, 64, 64), "T_UI_Rombo")
    im = lienzo(64, 64)
    d = ImageDraw.Draw(im)
    d.polygon([(32 * SS, 4 * SS), (54 * SS, 58 * SS), (32 * SS, 44 * SS), (10 * SS, 58 * SS)], fill=HUESO + (255,), outline=(20, 14, 10, 255))
    guardar(bajar(im, 64, 64), "T_UI_Flecha")


def marco_mapa():
    n = 512
    im = lienzo(n, n)
    d = ImageDraw.Draw(im)
    c, r = n * SS // 2, n * SS // 2 - 10 * SS
    d.ellipse([c - r, c - r, c + r, c + r], outline=ORO + (255,), width=12 * SS)
    d.ellipse([c - r + 22 * SS, c - r + 22 * SS, c + r - 22 * SS, c + r - 22 * SS], outline=ORO_OSCURO + (255,), width=4 * SS)
    for k in range(12):  # muescas como en un reloj (el tiempo es de Pharasma)
        a = k * math.pi / 6
        x0, y0 = c + math.cos(a) * (r - 6 * SS), c + math.sin(a) * (r - 6 * SS)
        x1, y1 = c + math.cos(a) * (r - 30 * SS), c + math.sin(a) * (r - 30 * SS)
        d.line([(x0, y0), (x1, y1)], fill=ORO_CLARO + (255,), width=5 * SS)
    espiral(d, c, 26 * SS, 18 * SS, 4 * SS, VIOLETA + (255,))
    guardar(bajar(im, n, n), "T_UI_Mapa_Marco")


def pergamino(n=512, semilla=4):
    rng = np.random.default_rng(semilla)
    base = rng.random((n // 16 + 1, n // 16 + 1)).astype(np.float32)
    base = np.asarray(Image.fromarray((base * 255).astype(np.uint8)).resize((n, n), Image.BICUBIC), np.float32) / 255
    grano = rng.random((n, n)).astype(np.float32)
    claro = np.array([66, 54, 40], np.float32)
    oscuro = np.array([30, 24, 18], np.float32)
    t = (0.55 * base + 0.15 * grano)[..., None]
    col = oscuro * (1 - t) + claro * t
    return Image.fromarray(col.clip(0, 255).astype(np.uint8), "RGB")


def mapa_exterior():
    """El mundo en tinta sobre pergamino oscuro: curvas de nivel, bosque punteado, arroyo, sendero e hitos."""
    n = 1024
    x0, x1, y0, y1 = TER.X0, TER.X1, TER.Y0, TER.Y1
    esc = n / max(x1 - x0, y1 - y0)
    im = pergamino(n, 9).convert("RGBA")
    d = ImageDraw.Draw(im)
    # curvas de nivel cada 300 cm
    alt = np.zeros((n, n), np.float32)
    for j in range(0, n, 4):
        for i in range(0, n, 4):
            alt[j:j + 4, i:i + 4] = TER.altura(x0 + i / esc, y0 + j / esc)
    nivel = np.floor(alt / 300.0)
    borde = (nivel != np.roll(nivel, 1, 0)) | (nivel != np.roll(nivel, 1, 1))
    tinta = np.zeros((n, n, 4), np.uint8)
    tinta[borde] = (150, 120, 80, 90)
    im = Image.alpha_composite(im, Image.fromarray(tinta, "RGBA"))
    d = ImageDraw.Draw(im)

    def p(x, y):
        return ((x - x0) * esc, (y - y0) * esc)
    rnd = random.Random(3)
    # bosques: puntitos (más densos en el bosque oscuro)
    for _ in range(9000):
        x, y = rnd.uniform(x0, x1), rnd.uniform(21000, y1)
        oscuro = x < 3000 and y > 43000
        if math.hypot(x - TER.PUEBLO[0], y - TER.PUEBLO[1]) < TER.RADIO_PUEBLO + 1500 or math.hypot(x - TER.LOMA[0], y - TER.LOMA[1]) < 4500:
            continue
        if not oscuro and rnd.random() < 0.55:
            continue
        cx, cy = p(x, y)
        r = 1.6 if oscuro else 1.2
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(110, 140, 90, 150) if not oscuro else (70, 90, 70, 190))
    # arroyo
    d.line([p(x0, TER.ARROYO_Y), p(x1, TER.ARROYO_Y)], fill=(90, 120, 150, 200), width=5)
    # cementerio: cruces
    for _ in range(60):
        cx, cy = p(rnd.uniform(1600, 11200), rnd.uniform(8000, 19500))
        d.line([(cx - 3, cy), (cx + 3, cy)], fill=(170, 150, 120, 200), width=1)
        d.line([(cx, cy - 4), (cx, cy + 3)], fill=(170, 150, 120, 200), width=1)
    # sendero (punteado)
    camino = [(6400, 6400), (6400, 21400), (7000, 26000), (8200, 30500), (8200, 35500), (10500, 39000), (14000, 44500)]
    for (ax, ay), (bx, by) in zip(camino, camino[1:]):
        pa, pb = p(ax, ay), p(bx, by)
        pasos = int(math.dist(pa, pb) // 9)
        for k in range(pasos):
            if k % 2 == 0:
                t0, t1 = k / pasos, (k + 1) / pasos
                d.line([(pa[0] + (pb[0] - pa[0]) * t0, pa[1] + (pb[1] - pa[1]) * t0), (pa[0] + (pb[0] - pa[0]) * t1, pa[1] + (pb[1] - pa[1]) * t1)],
                       fill=(200, 175, 130, 220), width=2)
    # hitos: pueblo (casitas), torre, loma, arco
    px, py = p(*TER.PUEBLO)
    for k in range(9):
        a = k * 2 * math.pi / 9
        hx, hy = px + math.cos(a) * 16, py + math.sin(a) * 12
        d.rectangle([hx - 4, hy - 3, hx + 4, hy + 4], outline=(220, 190, 130, 230), width=1)
        d.polygon([(hx - 5, hy - 3), (hx, hy - 8), (hx + 5, hy - 3)], outline=(220, 190, 130, 230))
    tx, ty = p(*TER.TORRE)
    d.ellipse([tx - 9, ty - 9, tx + 9, ty + 9], outline=(160, 110, 230, 255), width=3)
    d.line([(tx, ty - 16), (tx, ty + 16)], fill=(160, 110, 230, 255), width=2)
    lx, ly = p(*TER.LOMA)
    d.polygon([(lx - 10, ly + 6), (lx, ly - 8), (lx + 10, ly + 6)], outline=(200, 175, 130, 230), width=2)
    ax, ay = p(*TER.ARCO)
    d.arc([ax - 8, ay - 8, ax + 8, ay + 8], 180, 360, fill=(200, 175, 130, 230), width=3)
    # rótulos
    f = fuente("Cinzel.ttf", 22)
    for txt, (x, y) in (("Camposanto de Varo", (6400, 13500)), ("Varo", (TER.PUEBLO[0], TER.PUEBLO[1] - 7500)),
                        ("Torre", (TER.TORRE[0], TER.TORRE[1] - 3500)), ("Bosque de los Centinelas", (9000, 27500))):
        cx, cy = p(x, y)
        caja = d.textbbox((0, 0), txt, font=f)
        d.text((cx - (caja[2] - caja[0]) / 2, cy), txt, font=f, fill=(225, 200, 150, 235))
    im.save(os.path.join(SALIDA, "T_Mapa_Exterior.png"))
    return (x0, y0, n / esc)


def mapa_catacumba():
    """El plano ASCII de la catacumba en tinta: celdas de 4 m."""
    sys.path.insert(0, os.path.join(RAIZ, "tools", "ue"))
    texto = open(os.path.join(RAIZ, "tools", "ue", "construir_nivel.py"), encoding="utf-8").read()
    ini = texto.index("PLANO = [")
    fin = texto.index("]", ini)
    plano = [l.strip().strip('",') for l in texto[ini + 9:fin].splitlines() if l.strip().startswith('"')]
    filas, cols = len(plano), len(plano[0])
    c = 32
    n = 1024
    im = pergamino(n, 12).convert("RGBA")
    d = ImageDraw.Draw(im)
    ox, oy = (n - cols * c) // 2, (n - filas * c) // 2
    for f, fila in enumerate(plano):
        for k, ch in enumerate(fila):
            if ch == "#":
                continue
            x, y = ox + k * c, oy + f * c
            d.rectangle([x, y, x + c, y + c], fill=(78, 64, 48, 255))
            for df, dk, lado in ((-1, 0, "n"), (1, 0, "s"), (0, -1, "o"), (0, 1, "e")):
                ff, kk = f + df, k + dk
                if not (0 <= ff < filas and 0 <= kk < cols) or plano[ff][kk] == "#":
                    seg = {"n": [(x, y), (x + c, y)], "s": [(x, y + c), (x + c, y + c)], "o": [(x, y), (x, y + c)], "e": [(x + c, y), (x + c, y + c)]}[lado]
                    d.line(seg, fill=(200, 175, 130, 255), width=3)
            if ch in "PT":
                d.line([(x + 4, y + c // 2), (x + c - 4, y + c // 2)], fill=(150, 110, 230, 255), width=4)
            elif ch == "A":
                d.ellipse([x + 8, y + 8, x + c - 8, y + c - 8], outline=(230, 190, 110, 255), width=3)
            elif ch == "X":
                d.polygon([(x + c // 2, y + 6), (x + c - 6, y + c - 6), (x + 6, y + c - 6)], outline=(230, 190, 110, 255), width=2)
    im.save(os.path.join(SALIDA, "T_Mapa_Catacumba.png"))
    return (ox, oy, c, filas, cols)


if __name__ == "__main__":
    os.makedirs(SALIDA, exist_ok=True)
    titulo()
    subtitulo()
    boton(False)
    boton(True)
    placa()
    barras()
    iconos()
    marco_mapa()
    pergamino().save(os.path.join(SALIDA, "T_UI_Pergamino.png"))
    ext = mapa_exterior()
    cat = mapa_catacumba()
    print("OK", SALIDA, "exterior", ext, "catacumba", cat)
