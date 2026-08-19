"""Extrae una paleta dominante de la imagen de referencia estetica.
Uso: python _extract_palette.py <ruta_imagen> <n_colores>
"""
import sys
from PIL import Image

def extract(path, n=12):
    img = Image.open(path).convert("RGB")
    img = img.resize((160, 160))
    quant = img.quantize(colors=n, method=Image.MEDIANCUT)
    palette = quant.getpalette()[: n * 3]
    counts = sorted(quant.getcolors(), reverse=True)
    result = []
    for count, idx in counts:
        r, g, b = palette[idx * 3 : idx * 3 + 3]
        result.append((count, f"#{r:02X}{g:02X}{b:02X}"))
    return result

if __name__ == "__main__":
    path = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    for count, hexcode in extract(path, n):
        print(f"{hexcode}  (peso={count})")
