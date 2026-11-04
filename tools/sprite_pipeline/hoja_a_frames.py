#!/usr/bin/env python3
"""Convierte una hoja de sprites de pixelfx (PNG + JSON estilo Aseprite) en
un SpriteFrames de Godot (.tres) con una animación "default" en loop.

Imprime el `offset` que hay que darle al AnimatedSprite2D para que la
posición del nodo sea el pivote del efecto (meta.pixelfx.pivot: la base del
brasero, el pie de la hoguera, el soporte de la antorcha).

Uso:  python3 -I tools/sprite_pipeline/hoja_a_frames.py assets/sprites/props/fuego_pixelfx/brasero_calido.json
"""
import json
import os
import sys

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def main(json_rel):
    d = json.load(open(os.path.join(RAIZ, json_rel), encoding="utf-8"))
    meta = d["meta"]["pixelfx"]
    frames = d["frames"] if isinstance(d["frames"], list) else list(d["frames"].values())
    png_rel = json_rel[:-5] + ".png"
    w, h = meta["frameSize"]
    px, py = meta["pivot"]
    sub = []
    for i, f in enumerate(frames):
        r = f["frame"]
        sub.append(f'[sub_resource type="AtlasTexture" id="f{i}"]\natlas = ExtResource("1_hoja")\n'
                   f'region = Rect2({r["x"]}, {r["y"]}, {r["w"]}, {r["h"]})\n')
    lista = ", ".join('{\n"duration": 1.0,\n"texture": SubResource("f%d")\n}' % i for i in range(len(frames)))
    out = [f'[gd_resource type="SpriteFrames" load_steps={len(frames) + 2} format=3]\n',
           f'[ext_resource type="Texture2D" path="res://{png_rel}" id="1_hoja"]\n']
    out += sub
    out += ["[resource]",
            'animations = [{\n"frames": [%s],\n"loop": %s,\n"name": &"default",\n"speed": %.1f\n}]\n'
            % (lista, "true" if meta["loop"] else "false", meta["fps"])]
    tres = json_rel[:-5] + "_frames.tres"
    open(os.path.join(RAIZ, tres), "w", encoding="utf-8").write("\n".join(out))
    off = (w // 2 - px, h // 2 - py)
    print(f"{tres}: {len(frames)} frames @ {meta['fps']} fps, offset = Vector2({off[0]}, {off[1]})")


if __name__ == "__main__":
    for a in sys.argv[1:]:
        main(a)
