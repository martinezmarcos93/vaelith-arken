#!/usr/bin/env python3
"""Escribe el SpriteFrames (.tres) de un personaje a partir de su spec.

La sección "animaciones" del spec dice, por animación: prefijo de archivo
(o lista de archivos), fps y si hace loop. Los frames se toman de la carpeta
"salida" en orden numérico.

Uso:  python3 -I tools/sprite_pipeline/armar_frames.py <spec.json>
"""
import glob
import json
import os
import re
import sys


def main(spec_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    raiz = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(spec_path)), spec.get("raiz", ".")))
    carpeta = spec["salida"]
    num = lambda f: int(re.search(r"_(\d+)\.png$", f).group(1))
    recursos, anims = [], []
    for nombre, a in spec["animaciones"].items():
        if "archivos" in a:
            archivos = a["archivos"]
        else:
            archivos = sorted((os.path.basename(f) for f in glob.glob(os.path.join(raiz, carpeta, a["prefijo"] + "_*.png"))), key=num)
        if not archivos:
            raise SystemExit(f"{nombre}: no hay frames")
        ids = []
        for f in archivos:
            if not os.path.exists(os.path.join(raiz, carpeta, f)):
                raise SystemExit(f"{nombre}: falta {f}")
            rid = f"{len(recursos) + 1}_{f[:-4]}"
            if f not in [r[0] for r in recursos]:
                recursos.append((f, rid))
            ids.append(dict(recursos)[f])
        frames = ",\n".join('{\n"duration": 1.0,\n"texture": ExtResource("%s")\n}' % i for i in ids)
        anims.append('{\n"frames": [%s],\n"loop": %s,\n"name": &"%s",\n"speed": %.1f\n}'
                     % (frames, "true" if a["loop"] else "false", nombre, a["fps"]))
        print(f"{nombre:12} {len(ids)} frames @ {a['fps']} fps ({len(ids) / a['fps']:.2f} s)")
    out = [f"[gd_resource type=\"SpriteFrames\" load_steps={len(recursos) + 1} format=3]\n"]
    out += [f'[ext_resource type="Texture2D" path="res://{carpeta}/{f}" id="{rid}"]' for f, rid in recursos]
    out += ["", "[resource]", "animations = [" + ", ".join(anims) + "]", ""]
    open(os.path.join(raiz, carpeta, "_frames.tres"), "w", encoding="utf-8").write("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1])
