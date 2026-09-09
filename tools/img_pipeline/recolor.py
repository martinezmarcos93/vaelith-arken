"""Recolorea una imagen a la paleta canonica de Vaelith Arken.

Envoltorio sobre pyxelate: cuantiza (y opcionalmente aplica dithering) forzando
la paleta fija de docs/guia_estilo_visual.md, en vez de dejar que pyxelate
busque un palette propio. Pensado para bajar packs de terceros y referencias a
la identidad cromatica del proyecto sin recolorear a mano.

Uso:
    python tools/img_pipeline/recolor.py ENTRADA SALIDA [opciones]
    python tools/img_pipeline/recolor.py carpeta_in/ carpeta_out/ [opciones]

Opciones:
    --dither {none,naive,bayer,floyd,atkinson}  algoritmo de tramado (def: none)
    --extended            suma palette_extended.hex al nucleo
    --palette RUTA        archivo .hex extra (se puede repetir)
    --factor N            downscaling entero antes de cuantizar (def: sin bajar)
    --upscale N           re-escala el resultado por N con nearest (def: 1)
    --alpha-threshold T   corte 0-255 para binarizar el canal alpha (def: 128;
                          usar 0 para conservar el alpha original tal cual)
    --check               verifica que la salida use SOLO colores de la paleta

Requiere el venv de tools/img_pipeline/requirements.txt y corre en Python 3.9
gracias a _compat.py (importado antes que pyxelate).
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from typing import List, Tuple

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _compat  # noqa: F401,E402  (shim skimage; debe ir antes de pyxelate)
from pyxelate import Pal, Pyx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
IMG_EXT = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp")


def load_palette(paths: List[str]) -> List[str]:
    """Lee archivos .hex (un #RRGGBB por linea, # = comentario) y devuelve la lista."""
    colors: List[str] = []
    for path in paths:
        with open(path, "r", encoding="utf-8") as fh:
            for lineno, raw in enumerate(fh, 1):
                line = raw.strip()
                if not line or line.startswith("#") and not HEX_RE.match(line):
                    continue
                if not HEX_RE.match(line):
                    raise ValueError("{}:{}: no es un hex valido: {!r}".format(path, lineno, line))
                up = line.upper()
                if up not in colors:
                    colors.append(up)
    if len(colors) < 2:
        raise ValueError("La paleta necesita al menos 2 colores (tiene {}).".format(len(colors)))
    return colors


def _hex_to_rgb(h: str) -> Tuple[int, int, int]:
    return int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)


def recolor_one(src: str, dst: str, palette: List[str], dither: str,
                factor: int, upscale: int, alpha_threshold: int, check: bool) -> None:
    img = Image.open(src).convert("RGBA")
    arr = np.array(img)
    rgb, alpha = arr[:, :, :3], arr[:, :, 3]

    pyx = Pyx(
        factor=factor if factor and factor > 1 else None,
        upscale=upscale,
        palette=Pal.from_hex(palette),
        dither=dither,
    )
    pyx.fit(rgb)
    out_rgb = np.asarray(pyx.transform(rgb))[:, :, :3].astype(np.uint8)

    h2, w2 = out_rgb.shape[:2]
    a2 = np.array(Image.fromarray(alpha).resize((w2, h2), Image.NEAREST))
    if alpha_threshold > 0:
        a2 = np.where(a2 >= alpha_threshold, 255, 0).astype(np.uint8)

    out = np.dstack([out_rgb, a2]).astype(np.uint8)
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    Image.fromarray(out).save(dst)

    msg = "  {} -> {}  ({}x{}, dither={})".format(
        os.path.basename(src), os.path.basename(dst), w2, h2, dither)
    if check:
        pal_set = {_hex_to_rgb(c) for c in palette}
        visible = out_rgb[a2 > 0] if (a2 > 0).any() else out_rgb.reshape(-1, 3)
        seen = {tuple(int(v) for v in px) for px in np.unique(visible.reshape(-1, 3), axis=0)}
        stray = sorted(seen - pal_set)
        if stray:
            msg += "\n  [CHECK] {} color(es) fuera de la paleta: {}".format(
                len(stray), ["#%02X%02X%02X" % c for c in stray[:8]])
        else:
            msg += "\n  [CHECK] OK - solo colores de la paleta ({} usados)".format(len(seen))
    print(msg)


def iter_jobs(inp: str, outp: str):
    if os.path.isdir(inp):
        for name in sorted(os.listdir(inp)):
            if name.lower().endswith(IMG_EXT):
                stem = os.path.splitext(name)[0]
                yield os.path.join(inp, name), os.path.join(outp, stem + ".png")
    else:
        if os.path.isdir(outp) or outp.endswith(("/", "\\")):
            stem = os.path.splitext(os.path.basename(inp))[0]
            yield inp, os.path.join(outp, stem + ".png")
        else:
            yield inp, outp


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada", help="imagen o carpeta de entrada")
    ap.add_argument("salida", help="imagen o carpeta de salida")
    ap.add_argument("--dither", default="none", choices=["none", "naive", "bayer", "floyd", "atkinson"])
    ap.add_argument("--extended", action="store_true", help="suma palette_extended.hex")
    ap.add_argument("--palette", action="append", default=[], metavar="RUTA",
                    help="archivo .hex extra (repetible)")
    ap.add_argument("--factor", type=int, default=1)
    ap.add_argument("--upscale", type=int, default=1)
    ap.add_argument("--alpha-threshold", type=int, default=128, dest="alpha_threshold")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)

    pal_files = [os.path.join(HERE, "palette_canon.hex")]
    if args.extended:
        pal_files.append(os.path.join(HERE, "palette_extended.hex"))
    pal_files.extend(args.palette)
    palette = load_palette(pal_files)
    print("Paleta: {} colores ({})".format(len(palette), ", ".join(os.path.basename(p) for p in pal_files)))

    jobs = list(iter_jobs(args.entrada, args.salida))
    if not jobs:
        print("Nada que procesar en {!r}".format(args.entrada), file=sys.stderr)
        return 1
    for src, dst in jobs:
        recolor_one(src, dst, palette, args.dither, args.factor, args.upscale,
                    args.alpha_threshold, args.check)
    print("Listo: {} archivo(s).".format(len(jobs)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
