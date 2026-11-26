"""Une capturas en una hoja 2xN (mitad de tamaño) con el nombre de cada una. Uso: hoja.py salida.png a.png b.png ..."""
import sys
from PIL import Image, ImageDraw
salida, archivos = sys.argv[1], sys.argv[2:]
ims = [Image.open(a).convert("RGB") for a in archivos]
w, h = ims[0].width // 2, ims[0].height // 2
cols = 2; filas = (len(ims) + 1) // 2
hoja = Image.new("RGB", (w * cols, h * filas))
for i, (im, nombre) in enumerate(zip(ims, archivos)):
    im = im.resize((w, h))
    ImageDraw.Draw(im).text((8, 8), nombre.split("/")[-1], fill=(255, 255, 0))
    hoja.paste(im, ((i % cols) * w, (i // cols) * h))
hoja.save(salida)
