#!/usr/bin/env python3
"""Separación de planos (crítica 2026-11-04, guía v2 "Capas de profundidad").

- Niebla entre capas de parallax: ParallaxLayer con un ColorRect grande en el
  color de bruma de la zona. Cada capa que queda detrás recibe una pasada más,
  así lo lejano tiene menos contraste (perspectiva atmosférica).
- Modulate por plano: fondo lejano más claro y brumoso, fondo cercano más
  oscuro, primer plano en silueta.

Idempotente: si la niebla ya existe, no la duplica.
Uso:  python3 -I tools/relevamiento/capas.py
"""
import re

NIEBLA = '''[node name="{nombre}" type="ParallaxLayer" parent="Background"]
motion_scale = Vector2({m}, {m})

[node name="Bruma" type="ColorRect" parent="Background/{nombre}"]
offset_left = -4000.0
offset_top = -1200.0
offset_right = 8000.0
offset_bottom = 1600.0
mouse_filter = 2
color = {color}

'''

ESCENAS = {
    "Intro": {
        # (después de la capa, nombre, motion, color con alfa)
        "nieblas": [("RuinsFar", "NieblaLejana", 0.2, "Color(0.086, 0.173, 0.239, 0.32)"),
                    ("RuinsNear", "NieblaCercana", 0.4, "Color(0.086, 0.173, 0.239, 0.16)")],
        "modulate": {
            ("Sprite2D", "Background/Sky"): "Color(0.3, 0.31, 0.4, 1)",
            ("Sprite2D", "Background/RuinsFar"): "Color(0.26, 0.27, 0.35, 1)",
            ("Sprite2D", "Background/RuinsNear"): "Color(0.17, 0.17, 0.24, 1)",
            ("ColB1", "ColumnsBack"): "Color(0.56, 0.55, 0.64, 1)",
            ("ColB2", "ColumnsBack"): "Color(0.52, 0.51, 0.6, 1)",
            ("ColB3", "ColumnsBack"): "Color(0.56, 0.55, 0.64, 1)",
            ("ColB4", "ColumnsBack"): "Color(0.52, 0.51, 0.6, 1)",
            ("Gargoyle1", "ColumnsBack"): "Color(0.58, 0.57, 0.66, 1)",
            ("ColFront1", "."): "Color(0.3, 0.29, 0.36, 1)",
            ("ColFront2", "."): "Color(0.3, 0.29, 0.36, 1)",
        },
    },
    "Level1": {
        "nieblas": [("Ridge", "NieblaLejana", 0.18, "Color(0.208, 0.125, 0.216, 0.3)")],
        "modulate": {},
    },
}


def bloque_de(t, nombre, padre):
    m = re.search(r'\[node name="%s" type="[^"]+" parent="%s"\]\n' % (re.escape(nombre), re.escape(padre)), t)
    if not m:
        raise SystemExit(f"no encontré {padre}/{nombre}")
    fin = t.find("\n[", m.end())
    return m.start(), fin if fin != -1 else len(t)


for escena, cfg in ESCENAS.items():
    p = f"scenes/levels/{escena}.tscn"
    t = open(p, encoding="utf-8").read()
    for (nombre, padre), color in cfg["modulate"].items():
        a, b = bloque_de(t, nombre, padre)
        bl = t[a:b]
        bl = re.sub(r"\nmodulate = [^\n]+", f"\nmodulate = {color}", bl) if "\nmodulate = " in bl \
            else bl.replace("]\n", f"]\nmodulate = {color}\n", 1)
        t = t[:a] + bl + t[b:]
    for despues, nombre, m, color in cfg["nieblas"]:
        if f'[node name="{nombre}" type="ParallaxLayer"' in t:
            continue
        # insertar después de la capa y de su sprite hijo
        a, b = bloque_de(t, "Sprite2D", f"Background/{despues}")
        t = t[:b + 1] + NIEBLA.format(nombre=nombre, m=m, color=color) + t[b + 1:].lstrip("\n")
    open(p, "w", encoding="utf-8").write(t)
    print(f"{escena}: {len(cfg['modulate'])} modulates, {len(cfg['nieblas'])} nieblas")
