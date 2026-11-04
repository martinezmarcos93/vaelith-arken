#!/usr/bin/env python3
"""Hornea la escala de cada Sprite2D en su textura: 1 píxel de arte = 1 píxel
del viewport 640×360 en todo el juego.

Por qué existe (relevamiento 2026-11-04): los props estaban a escalas de 0,13
a 5,0, así que el tamaño del píxel en pantalla variaba ~38× entre objetos
vecinos. Godot no puede escalar pixel art sin romperlo; acá se re-muestrea
UNA vez, fuera del motor, y el nodo queda a escala ±1.

Cómo re-muestrea:
  - pixel art real (≤ 64 colores): achica con LANCZOS y vuelve a la paleta
    propia del original; agranda con NEAREST.
  - arte IA (muchos colores): LANCZOS y reducción a 32 colores (48 en
    fondos opacos), sin dithering.
  - alfa duro (umbral 110) salvo en fondos opacos.

Salida: assets/sprites/_horneado/<ruta original>@<sx>x<sy>.png. La escena
pasa a apuntar ahí; el original queda intacto para volver a hornear.

Uso:  python3 -I tools/sprite_pipeline/hornear_escalas.py <escena.tscn> [...]
"""
import os
import re
import sys

import numpy as np
from PIL import Image

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SALIDA = "assets/sprites/_horneado"
ALFA = 110


def colores(im):
    a = np.array(im.convert("RGBA"))
    op = a[..., 3] > 0
    return np.unique(a[..., :3][op].reshape(-1, 3), axis=0)


def hornear(src_rel, sx, sy):
    im = Image.open(os.path.join(RAIZ, src_rel)).convert("RGBA")
    w, h = im.size
    nw, nh = max(1, round(w * sx)), max(1, round(h * sy))
    pal = colores(im)
    opaco = (np.array(im)[..., 3] > 250).mean() > 0.97
    if len(pal) <= 64:
        if nw >= w and nh >= h:
            out = im.resize((nw, nh), Image.NEAREST)
        else:
            out = im.resize((nw, nh), Image.LANCZOS)
            pimg = Image.new("P", (1, 1))
            flat = list(pal.reshape(-1)) + [0] * (768 - pal.size)
            pimg.putpalette(flat[:768])
            rgb = out.convert("RGB").quantize(palette=pimg, dither=Image.NONE).convert("RGB")
            alfa = out.getchannel("A").point(lambda v: 255 if v >= ALFA else 0)
            out = rgb.convert("RGBA")
            out.putalpha(alfa)
    else:
        out = im.resize((nw, nh), Image.LANCZOS)
        n = 48 if opaco else 32
        rgb = out.convert("RGB").quantize(colors=n, method=Image.MEDIANCUT, dither=Image.NONE).convert("RGB")
        alfa = out.getchannel("A") if opaco else out.getchannel("A").point(lambda v: 255 if v >= ALFA else 0)
        out = rgb.convert("RGBA")
        out.putalpha(alfa)
    base, _ = os.path.splitext(src_rel.replace("assets/sprites/", "", 1))
    rel = f"{SALIDA}/{base}@{sx:g}x{sy:g}.png"
    os.makedirs(os.path.dirname(os.path.join(RAIZ, rel)), exist_ok=True)
    out.save(os.path.join(RAIZ, rel))
    return rel


def procesar(scn):
    t = open(scn, encoding="utf-8").read()
    ids = {m.group(2): m.group(1) for m in re.finditer(r'\[ext_resource type="Texture2D"[^\]]*path="res://([^"]+)"[^\]]*id="([^"]+)"\]', t)}
    nuevos, cambios = {}, 0
    bloques = re.split(r'\n(?=\[node )', t)
    for i, b in enumerate(bloques):
        if not b.startswith("[node") or 'type="PointLight2D"' in b:
            continue
        mt = re.search(r'\ntexture = ExtResource\("([^"]+)"\)', b)
        ms = re.search(r'\nscale = Vector2\(([-\d.e]+), ([-\d.e]+)\)', b)
        if not mt or not ms or mt.group(1) not in ids:
            continue
        sx, sy = float(ms.group(1)), float(ms.group(2))
        if abs(sx) == 1 and abs(sy) == 1:
            continue
        if any(k in b for k in ("region_enabled", "hframes", "vframes", "\noffset = ")):
            nombre = re.search(r'name="([^"]+)"', b).group(1)
            print(f"  salteo {nombre}: usa region/frames/offset")
            continue
        rel = hornear(ids[mt.group(1)], abs(sx), abs(sy))
        rid = nuevos.setdefault(rel, f"hz_{len(nuevos) + 1}")
        b = b.replace(mt.group(0), f'\ntexture = ExtResource("{rid}")')
        fx, fy = (1 if sx > 0 else -1), (1 if sy > 0 else -1)
        b = b.replace(ms.group(0), "" if (fx, fy) == (1, 1) else f"\nscale = Vector2({fx}, {fy})")
        bloques[i] = b
        cambios += 1
    if not cambios:
        return 0
    t = "\n".join(bloques)
    lineas = "".join(f'[ext_resource type="Texture2D" path="res://{rel}" id="{rid}"]\n' for rel, rid in nuevos.items())
    ultimo = list(re.finditer(r'\[ext_resource [^\n]*\]\n', t))[-1]
    t = t[:ultimo.end()] + lineas + t[ultimo.end():]
    # quitar ext_resource de texturas que ya nadie usa
    for rid, path in ids.items():
        if f'ExtResource("{rid}")' not in t:
            t = re.sub(r'\[ext_resource type="Texture2D"[^\n]*id="%s"\]\n' % re.escape(rid), "", t)
    open(scn, "w", encoding="utf-8").write(t)
    return cambios


if __name__ == "__main__":
    for scn in sys.argv[1:]:
        print(f"{scn}: {procesar(scn)} sprites horneados")
