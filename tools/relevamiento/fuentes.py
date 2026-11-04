#!/usr/bin/env python3
"""Tipografía nítida: Gothic Pixels solo en múltiplos de su tamaño nativo (16).

Medido el 2026-11-04 (PIL, sin antialias): a 16 y 32 px la fuente cae en la
grilla (0 % de píxeles grises); en cualquier otro tamaño se deforma. Mapeo:
<=20 -> 16, 21-39 -> 32, >=40 -> 48. También deja el import sin antialias,
sin hinting y sin posicionamiento subpíxel.
Uso:  python3 -I tools/relevamiento/fuentes.py
"""
import glob
import re


def nativo(n):
    return 16 if n <= 20 else 32 if n < 40 else 48


cambios = 0
for p in glob.glob("scenes/**/*.tscn", recursive=True):
    t = open(p, encoding="utf-8").read()
    t2 = re.sub(r"(font_sizes/font_size = )(\d+)", lambda m: m.group(1) + str(nativo(int(m.group(2)))), t)
    if t2 != t:
        cambios += sum(1 for a, b in zip(re.findall(r"font_size = (\d+)", t), re.findall(r"font_size = (\d+)", t2)) if a != b)
        open(p, "w", encoding="utf-8").write(t2)
imp = "assets/fonts/Gothic Pixels.ttf.import"
t = open(imp, encoding="utf-8").read()
t = re.sub(r"\nantialiasing=\d", "\nantialiasing=0", t)
t = re.sub(r"\nhinting=\d", "\nhinting=0", t)
t = re.sub(r"\nsubpixel_positioning=\d", "\nsubpixel_positioning=0", t)
open(imp, "w", encoding="utf-8").write(t)
print(f"{cambios} tamaños ajustados; import sin antialias/hinting/subpíxel")
