#!/usr/bin/env python3
"""Hornea la escala de un AnimatedSprite2D en sus frames (como hornear_escalas.py
para Sprite2D): genera cada frame re-muestreado en assets/sprites/_horneado/ y un
SpriteFrames nuevo "<original>@<escala>.tres" que apunta a ellos.

Uso:  python3 -I tools/sprite_pipeline/hornear_frames.py <frames.tres> <escala>
Imprime la ruta res:// del SpriteFrames nuevo.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hornear_escalas import RAIZ, hornear  # noqa: E402

tres, esc = sys.argv[1], float(sys.argv[2])
t = open(os.path.join(RAIZ, tres), encoding="utf-8").read()


def cambiar(m):
    return f'path="res://{hornear(m.group(1), esc, esc)}"'


t = re.sub(r'path="res://([^"]+\.png)"', cambiar, t)
base, _ = os.path.splitext(tres.replace("assets/sprites/", "", 1))
salida = f"assets/sprites/_horneado/{base}@{esc:g}.tres"
os.makedirs(os.path.dirname(os.path.join(RAIZ, salida)), exist_ok=True)
open(os.path.join(RAIZ, salida), "w", encoding="utf-8").write(t)
print(f"res://{salida}")
