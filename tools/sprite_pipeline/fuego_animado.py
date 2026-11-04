#!/usr/bin/env python3
"""Reemplaza props de fuego estáticos (Sprite2D con arte IA) por fuego
animado de pixelfx (AnimatedSprite2D), apoyado donde estaba el viejo.

- La base visible del fuego nuevo (fila opaca más baja de todos sus frames)
  queda en la misma y que la base del prop viejo.
- Las luces hijas (PointLight2D) se compensan para no moverse en el mundo.
- Cada instancia arranca en un frame distinto para que no latan a la vez.

Uso:  python3 -I tools/sprite_pipeline/fuego_animado.py <escena.tscn> Nodo=efecto [Nodo=efecto ...]
      efecto = nombre en assets/sprites/props/fuego_pixelfx/ (brasero_calido, antorcha, ...)
"""
import json
import os
import re
import sys

import numpy as np
from PIL import Image

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
FX = "assets/sprites/props/fuego_pixelfx"


def base_visible(efecto):
    d = json.load(open(os.path.join(RAIZ, FX, efecto + ".json"), encoding="utf-8"))
    hoja = np.array(Image.open(os.path.join(RAIZ, FX, efecto + ".png")).getchannel("A"))
    frames = d["frames"] if isinstance(d["frames"], list) else list(d["frames"].values())
    fondo = 0
    for f in frames:
        r = f["frame"]
        a = hoja[r["y"]:r["y"] + r["h"], r["x"]:r["x"] + r["w"]] > 200
        filas = np.nonzero(a.any(1))[0]
        if len(filas):
            fondo = max(fondo, int(filas.max()) + 1)
    w, h = d["meta"]["pixelfx"]["frameSize"]
    return h, fondo, len(frames)


def main(scn, pares):
    t = open(os.path.join(RAIZ, scn), encoding="utf-8").read()
    texturas = {m.group(2): m.group(1) for m in re.finditer(r'\[ext_resource type="Texture2D"[^\]]*path="res://([^"]+)"[^\]]*id="([^"]+)"\]', t)}
    nuevos = {}
    for k, par in enumerate(pares):
        nodo, efecto = par.split("=")
        cab = re.search(r'\[node name="%s" type="Sprite2D" parent="([^"]*)"\]\n' % re.escape(nodo), t)
        if not cab:
            raise SystemExit(f"no encontré el Sprite2D {nodo}")
        fin = t.find("\n[", cab.end())
        bloque = t[cab.start():fin]
        tex = re.search(r'\ntexture = ExtResource\("([^"]+)"\)', bloque)
        pos = re.search(r'\nposition = Vector2\(([-\d.]+), ([-\d.]+)\)', bloque)
        viejo = Image.open(os.path.join(RAIZ, texturas[tex.group(1)]))
        filas = np.nonzero((np.array(viejo.getchannel("A")) > 100).any(1))[0]
        x, y = float(pos.group(1)), float(pos.group(2))
        base = round(y - viejo.height / 2 + filas.max() + 1)   # fila opaca más baja del prop viejo
        h, fondo, n = base_visible(efecto)
        off_y = int(h // 2 - fondo)
        rid = nuevos.setdefault(efecto, f"fx_{efecto}")
        nb = bloque.replace(cab.group(0), f'[node name="{nodo}" type="AnimatedSprite2D" parent="{cab.group(1)}"]\n')
        nb = nb.replace(pos.group(0), f"\nposition = Vector2({x:g}, {base:g})")
        nb = nb.replace(tex.group(0), f'\nsprite_frames = ExtResource("{rid}")\nanimation = &"default"\nautoplay = "default"\n'
                                      f'frame = {(k * 7) % n}\noffset = Vector2(0, {off_y})')
        t = t[:cab.start()] + nb + t[fin:]
        # hijos directos: compensar el corrimiento del padre
        ruta = nodo if cab.group(1) == "." else f"{cab.group(1)}/{nodo}"
        dy = base - y

        def mover(m):
            px, py = float(m.group(2)), float(m.group(3))
            return f'{m.group(1)}position = Vector2({px:g}, {py - dy:g})'
        t = re.sub(r'(\[node name="[^"]+" type="[^"]+" parent="%s"\]\n(?:[^\[\n][^\n]*\n)*?)position = Vector2\(([-\d.]+), ([-\d.]+)\)' % re.escape(ruta), mover, t)
        print(f"{nodo}: {efecto}, base y={base:g}, offset y={off_y}")
    lineas = "".join(f'[ext_resource type="SpriteFrames" path="res://{FX}/{e}_frames.tres" id="{r}"]\n' for e, r in nuevos.items())
    ultimo = list(re.finditer(r'\[ext_resource [^\n]*\]\n', t))[-1]
    t = t[:ultimo.end()] + lineas + t[ultimo.end():]
    for rid in texturas:
        if f'ExtResource("{rid}")' not in t:
            t = re.sub(r'\[ext_resource type="Texture2D"[^\n]*id="%s"\]\n' % re.escape(rid), "", t)
    open(os.path.join(RAIZ, scn), "w", encoding="utf-8").write(t)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
