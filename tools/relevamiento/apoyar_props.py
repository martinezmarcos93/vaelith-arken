#!/usr/bin/env python3
"""Apoya en el piso los props que reporta props_flotantes.gd.

Lee su salida (líneas "PROP <nombre> ... gap=<px>") y mueve en la escena la
`position.y` de cada uno para que su fila opaca más baja quede 1 px dentro
del piso.

Uso:  godot ... -s tools/relevamiento/props_flotantes.gd -- res://<escena> \
        | python3 -I tools/relevamiento/apoyar_props.py <escena.tscn>
"""
import re
import sys

scn = sys.argv[1]
t = open(scn, encoding="utf-8").read()
movidos = 0
for linea in sys.stdin:
    m = re.match(r"PROP (\S+) .*gap=(-?[\d.]+)", linea)
    if not m:
        continue
    nombre, gap = m.group(1), float(m.group(2))
    delta = round(gap) + 1
    patron = re.compile(r'(\[node name="%s"[^\n]*\]\nposition = Vector2\()([-\d.]+), ([-\d.]+)(\))' % re.escape(nombre))
    mm = patron.search(t)
    if not mm:
        print(f"no encontré {nombre}")
        continue
    y = float(mm.group(3)) + delta
    t = t[:mm.start()] + f"{mm.group(1)}{mm.group(2)}, {y:g}{mm.group(4)}" + t[mm.end():]
    movidos += 1
    print(f"{nombre}: y {mm.group(3)} -> {y:g}")
open(scn, "w", encoding="utf-8").write(t)
print(f"{movidos} props apoyados")
