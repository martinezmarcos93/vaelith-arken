"""Repara "falso pixel art" (renders de IA, upscales, JPG) a pixel art real.

Envoltorio sobre pixelfixer (vendorizado en vendor/pixel-art-fixer/, de Retro
Diffusion, MIT): detecta la grilla real sobre la que se dibujo la imagen y
reconstruye cada celda como un unico pixel, a la resolucion nativa del arte.
Sin modelo de IA, solo procesamiento de imagen.

Uso:
    python tools/img_pipeline/fix_ai.py ENTRADA SALIDA [opciones]
    python tools/img_pipeline/fix_ai.py carpeta_in/ carpeta_out/ [opciones]

Opciones:
    --colors N        cuantiza a N colores como maximo (def: 0 = sin tocar color)
    --grid-from REF   detecta la grilla en REF y la reusa para toda la corrida
                      (para tiras de frames que deben compartir grilla)
    --fast            modo de latencia acotada (menos preciso)
    --json RUTA       guarda un JSON con la metadata de deteccion por archivo

Notas:
    - La deteccion tarda (segundos a decenas de segundos por imagen grande).
    - 'consensus'/'confidence' en la salida indican que tan segura fue la
      deteccion: "unanimous/high" es fiable; "arbitrated/low" conviene revisarlo.
    - Despues de fix_ai suele convenir pasar recolor.py para fijar la paleta
      canonica del juego.

Corre en Python 3.9 (pixelfixer declara requires-python >=3.9).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import List, Optional, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor", "pixel-art-fixer"))
from pixelfixer import api  # noqa: E402

IMG_EXT = (".png", ".jpg", ".jpeg", ".bmp", ".webp")


def _grid_step(ref_path: str, fast: bool) -> float:
    with open(ref_path, "rb") as fh:
        r = api.process(fh.read(), mode="fast" if fast else "full", return_png=False)
    step = 0.5 * (float(r["step_x"]) + float(r["step_y"]))
    print("Grilla de referencia ({}): step~{:.3f}  [{}/{}]".format(
        os.path.basename(ref_path), step, r["consensus"], r["confidence"]))
    return step


def fix_one(src: str, dst: str, colors: int, fast: bool,
            force_step: Optional[float]) -> dict:
    with open(src, "rb") as fh:
        data = fh.read()
    r = api.process(
        data,
        mode="fast" if fast else "full",
        k_colors=colors,
        force_step=force_step,
        return_png=True,
    )
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    with open(dst, "wb") as fh:
        fh.write(r["png"])
    print("  {} -> {}  {}x{} px  [{}/{}]  {:.1f}s".format(
        os.path.basename(src), os.path.basename(dst), r["cols"], r["rows"],
        r["consensus"], r["confidence"], r.get("detect_s", 0.0) + r.get("recon_s", 0.0)))
    meta = {k: r[k] for k in ("cols", "rows", "step_x", "step_y", "consensus", "confidence")}
    meta["src"] = os.path.basename(src)
    return meta


def iter_jobs(inp: str, outp: str) -> List[Tuple[str, str]]:
    if os.path.isdir(inp):
        jobs = []
        for name in sorted(os.listdir(inp)):
            if name.lower().endswith(IMG_EXT):
                stem = os.path.splitext(name)[0]
                jobs.append((os.path.join(inp, name), os.path.join(outp, stem + ".png")))
        return jobs
    if os.path.isdir(outp) or outp.endswith(("/", "\\")):
        stem = os.path.splitext(os.path.basename(inp))[0]
        return [(inp, os.path.join(outp, stem + ".png"))]
    return [(inp, outp)]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada")
    ap.add_argument("salida")
    ap.add_argument("--colors", type=int, default=0)
    ap.add_argument("--grid-from", default=None, metavar="REF", dest="grid_from")
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--json", default=None, metavar="RUTA", dest="json_out")
    args = ap.parse_args(argv)

    force_step = _grid_step(args.grid_from, args.fast) if args.grid_from else None

    jobs = iter_jobs(args.entrada, args.salida)
    if not jobs:
        print("Nada que procesar en {!r}".format(args.entrada), file=sys.stderr)
        return 1

    metas = []
    for src, dst in jobs:
        metas.append(fix_one(src, dst, args.colors, args.fast, force_step))

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(metas, fh, indent=2, ensure_ascii=False)
        print("Metadata -> {}".format(args.json_out))
    print("Listo: {} archivo(s).".format(len(jobs)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
