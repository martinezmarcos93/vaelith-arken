#!/usr/bin/env python3
"""Ajuste de iluminación por fuente (crítica 2026-11-04, Fase 2).

- Halos escalonados: el degradado de las PointLight2D pasa a 4 bandas con
  interpolación constante (halo de pixel art) en vez de un degradado liso.
- Fuego: radio y energía suficientes para iluminar columnas y suelo vecinos.
- Violeta: menos saturado e intenso en el centro, más ancho, para que se
  proyecte sobre estructuras y piso en vez de quemar el punto.

Uso:  python3 -I tools/relevamiento/luces.py   (edita las 3 escenas en el lugar)
"""
import re

BANDAS = ('[sub_resource type="Gradient" id="Gradient_glow"]\n'
          'interpolation_mode = 1\n'
          'offsets = PackedFloat32Array(0, 0.3, 0.55, 0.8)\n'
          'colors = PackedColorArray(1, 1, 1, 1, 1, 1, 1, 0.62, 1, 1, 1, 0.32, 1, 1, 1, 0)\n')

# nombre de luz -> (color o None, energía, escala de textura)
AJUSTES = {
    "Intro": {
        "Brazier1Light": (None, 1.3, 2.2), "Brazier2Light": (None, 1.3, 2.2),
        "Torch1Light": (None, 1.15, 1.8), "Torch2Light": (None, 1.15, 1.8),
        "CryptDoorLight": ("Color(0.6, 0.44, 0.92, 1)", 1.1, 2.6),
        "BrazierVioletLight": ("Color(0.6, 0.44, 0.92, 1)", 0.9, 1.8),
    },
    "Level1": {
        "BonfireLight": (None, 1.4, 2.6),
        "EyeLight": ("Color(0.6, 0.44, 0.92, 1)", 1.0, 2.2),
    },
    "TorreSector": {
        "BrazierWarmLight": (None, 1.5, 2.4), "WallTorchBackLight": (None, 1.15, 1.8),
        "CandelabrumLight": (None, 1.6, 2.6),
        "BrazierVioletLight": ("Color(0.6, 0.44, 0.92, 1)", 1.0, 2.4),
        "ThresholdLight": ("Color(0.58, 0.42, 0.92, 1)", 1.4, 4.2),
    },
}


def cambiar(bloque, campo, valor):
    if re.search(r"\n%s = " % campo, bloque):
        return re.sub(r"\n%s = [^\n]+" % campo, f"\n{campo} = {valor}", bloque)
    return bloque.rstrip("\n") + f"\n{campo} = {valor}\n"


for escena, luces in AJUSTES.items():
    p = f"scenes/levels/{escena}.tscn"
    t = open(p, encoding="utf-8").read()
    t = re.sub(r'\[sub_resource type="Gradient" id="Gradient_glow"\]\n(?:[^\[\n][^\n]*\n)*', BANDAS, t, count=1)
    bloques = re.split(r"\n(?=\[node )", t)
    hechos = set()
    for i, b in enumerate(bloques):
        m = re.match(r'\[node name="([^"]+)" type="PointLight2D"', b)
        if not m or m.group(1) not in luces:
            continue
        color, energia, escala = luces[m.group(1)]
        if color:
            b = cambiar(b, "color", color)
        b = cambiar(b, "energy", energia)
        b = cambiar(b, "texture_scale", escala)
        bloques[i] = b
        hechos.add(m.group(1))
    faltan = set(luces) - hechos
    assert not faltan, f"{escena}: no encontré {faltan}"
    open(p, "w", encoding="utf-8").write("\n".join(bloques))
    print(f"{escena}: {len(hechos)} luces ajustadas")
