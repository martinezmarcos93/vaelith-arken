#!/usr/bin/env python3
"""Re-extrae las poses de una lámina IA a frames de pixel art 1:1.

Por qué existe (relevamiento 2026-11-04): la extracción anterior cortaba los
cuerpos en línea recta y arrastraba restos de las poses vecinas, y los frames
se escalaban en el motor (0,5 / 1,05), así que nunca eran pixel art 1:1.

Qué hace, por cada fila de la lámina (spec JSON):
  1. Separa la fila en piezas conexas (canal alfa) y descarta las etiquetas.
  2. Ubica el centro de cada cuerpo (pico de masa opaca por columna) y le
     asigna cada pieza entera a su cuerpo más cercano: la espada que invade el
     lugar de la vecina se queda con su dueño. Si dos cuerpos se tocan, corta
     esa pieza en el valle de masa entre ambos.
  3. Ancla cada frame en el pie (fila más baja del cuerpo) y en el centro del
     cuerpo, achica UNA vez al tamaño final, endurece el alfa y reduce a una
     paleta fija común a todos los frames del personaje.

Uso:  python3 -I tools/sprite_pipeline/extraer_poses.py <spec.json>
Solo numpy + Pillow.
"""
import json
import os
import sys
from collections import deque

import numpy as np
from PIL import Image

ALFA_PIEZA = 40      # alfa mínimo para que un píxel cuente como parte de una pieza
ALFA_SOLIDO = 200    # alfa del "cuerpo" para ubicar centros y pies
ALFA_FINAL = 110     # umbral del alfa duro tras achicar


def componentes(mask):
    """Etiqueta piezas 8-conexas. Devuelve (etiquetas, cantidad)."""
    h, w = mask.shape
    lab = np.zeros((h, w), np.int32)
    n = 0
    ys, xs = np.nonzero(mask)
    for y0, x0 in zip(ys, xs):
        if lab[y0, x0]:
            continue
        n += 1
        lab[y0, x0] = n
        q = deque([(y0, x0)])
        while q:
            y, x = q.popleft()
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not lab[ny, nx]:
                        lab[ny, nx] = n
                        q.append((ny, nx))
    return lab, n


def es_etiqueta(sub, rgb):
    """Las etiquetas son banners chatos y llenos arriba de la fila (un charco
    en el piso también es chato y lleno, pero está abajo)."""
    ys, xs = np.nonzero(sub)
    h, w = ys.ptp() + 1, xs.ptp() + 1
    lleno = sub.sum() / (h * w)
    return h <= 30 and w >= 50 and lleno > 0.7 and ys.min() < 45


def centros_cuerpos(solido, n):
    """n centros de cuerpo: picos de masa opaca por columna, separados."""
    perfil = solido.sum(0).astype(float)
    k = max(3, solido.shape[1] // (n * 6))
    perfil = np.convolve(perfil, np.ones(k) / k, mode="same")
    sep = solido.shape[1] / n * 0.55
    centros = []
    for x in np.argsort(-perfil):
        if perfil[x] <= 0:
            break
        if all(abs(x - c) >= sep for c in centros):
            centros.append(int(x))
        if len(centros) == n:
            break
    if len(centros) < n:
        raise SystemExit(f"encontré {len(centros)} cuerpos y esperaba {n}")
    return sorted(centros), perfil


def extraer_fila(img, fila):
    x0, y0, x1, y1 = fila["caja"]
    n = fila["n"]
    rgba = np.array(img.crop((x0, y0, x1, y1)).convert("RGBA"))
    alfa = rgba[..., 3]
    lab, cant = componentes(alfa > ALFA_PIEZA)
    for i in range(1, cant + 1):
        sub = lab == i
        if sub.sum() < 6 or es_etiqueta(sub, rgba):
            lab[sub] = 0
    solido = (alfa > ALFA_SOLIDO) & (lab > 0)
    if "centros" in fila:  # filas con charcos o cuerpos tirados: centros a mano (x de la lámina)
        centros = [c - x0 for c in fila["centros"]]
        perfil = solido.sum(0).astype(float)
    else:
        centros, perfil = centros_cuerpos(solido, n)
    # valles entre cuerpos, por si una pieza los une
    valles = [c + int(np.argmin(perfil[c:d])) for c, d in zip(centros, centros[1:])]
    dueno = np.zeros(lab.shape, np.int32) - 1
    for i in range(1, lab.max() + 1):
        sub = lab == i
        if not sub.any():
            continue
        ys, xs = np.nonzero(sub)
        cubre = [j for j, c in enumerate(centros) if xs.min() <= c <= xs.max()]
        if len(cubre) >= 2:  # pieza que une cuerpos: se corta en los valles
            cols = np.arange(lab.shape[1])
            slot = np.searchsorted(valles, cols)
            dueno[sub] = slot[np.nonzero(sub)[1]]
        else:
            peso = alfa[sub].astype(float)
            cx = (xs * peso).sum() / peso.sum()
            dueno[sub] = int(np.argmin([abs(cx - c) for c in centros]))
    frames = []
    for j, c in enumerate(centros):
        m = dueno == j
        px = rgba.copy()
        px[~m] = 0
        sol = (px[..., 3] > ALFA_SOLIDO)
        ys = np.nonzero(sol.any(1))[0]
        pie = int(ys.max()) if len(ys) else int(np.nonzero(m.any(1))[0].max())
        frames.append((Image.fromarray(px, "RGBA"), c, pie))
    return frames


def achicar(im, ancla_x, pie, escala, lienzo, ancla_lienzo):
    """Achica una vez y pega en el lienzo final con el ancla en su lugar."""
    w, h = im.size
    nw, nh = max(1, round(w * escala)), max(1, round(h * escala))
    chico = im.resize((nw, nh), Image.LANCZOS)  # Pillow premultiplica el alfa
    ax, ay = round(ancla_x * escala), round((pie + 1) * escala)
    out = Image.new("RGBA", lienzo, (0, 0, 0, 0))
    out.paste(chico, (ancla_lienzo[0] - ax, ancla_lienzo[1] - ay), chico)
    a = np.array(out)
    a[..., 3] = np.where(a[..., 3] >= ALFA_FINAL, 255, 0)
    return Image.fromarray(a, "RGBA")


def limpiar_islas(im, minimo=3):
    a = np.array(im)
    lab, n = componentes(a[..., 3] > 0)
    for i in range(1, n + 1):
        sub = lab == i
        if sub.sum() < minimo:
            a[sub] = 0
    return Image.fromarray(a, "RGBA")


def paleta_comun(frames, colores):
    """Una paleta para todo el personaje: los frames no parpadean de color."""
    opacos = np.concatenate([np.array(f)[..., :3][np.array(f)[..., 3] > 0] for f in frames])
    muestra = Image.fromarray(opacos.reshape(-1, 1, 3), "RGB")
    return muestra.quantize(colors=colores, method=Image.MEDIANCUT, dither=Image.NONE)


def cuantizar(im, pal):
    rgb = im.convert("RGB").quantize(palette=pal, dither=Image.NONE).convert("RGB")
    out = rgb.convert("RGBA")
    out.putalpha(im.getchannel("A"))
    return out


def main(spec_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    raiz = os.path.dirname(os.path.abspath(spec_path))
    raiz = os.path.normpath(os.path.join(raiz, spec.get("raiz", ".")))
    img = Image.open(os.path.join(raiz, spec["lamina"]))
    esc, lienzo, ancla = spec["escala"], tuple(spec["lienzo"]), tuple(spec["ancla"])
    salida = os.path.join(raiz, spec["salida"])
    os.makedirs(salida, exist_ok=True)
    finales = []
    for fila in spec["filas"]:
        fr = extraer_fila(img, fila)
        for k, (im, cx, pie) in enumerate(fr):
            f = achicar(im, cx, pie, esc, lienzo, ancla)
            finales.append((fila["nombre"].format(i=k), limpiar_islas(f)))
    pal = paleta_comun([f for _, f in finales], spec.get("colores", 32))
    rep = []
    for nombre, f in finales:
        f = cuantizar(f, pal)
        f.save(os.path.join(salida, nombre + ".png"))
        a = np.array(f)[..., 3] > 0
        ys, xs = np.nonzero(a)
        if not len(xs):
            rep.append(f"{nombre:18} ¡VACÍO!")
            continue
        toca = xs.min() == 0 or xs.max() == lienzo[0] - 1 or ys.min() == 0
        rep.append(f"{nombre:18} bbox x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()}"
                   + ("  ¡TOCA EL BORDE!" if toca else ""))
    print("\n".join(rep))
    print(f"{len(finales)} frames -> {salida}")


if __name__ == "__main__":
    main(sys.argv[1])
