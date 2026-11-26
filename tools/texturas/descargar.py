"""Descarga texturas CC0 de Poly Haven (1K: color, normal GL, ARM) a assets_fuente/texturas/<id>/.
Uso: python3 tools/texturas/descargar.py id1 id2 ...   Licencia: CC0 (https://polyhaven.com/license)."""
import json, os, sys, urllib.request

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
UA = {"User-Agent": "vaelith-texturas/1.0"}

def bajar(url, destino):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r, open(destino, "wb") as f:
        f.write(r.read())

for tid in sys.argv[1:]:
    with urllib.request.urlopen(urllib.request.Request(f"https://api.polyhaven.com/files/{tid}", headers=UA), timeout=30) as r:
        info = json.load(r)
    carpeta = os.path.join(RAIZ, "assets_fuente", "texturas", tid)
    os.makedirs(carpeta, exist_ok=True)
    for mapa, nombre in (("Diffuse", "color"), ("nor_gl", "normal"), ("arm", "arm")):
        try:
            url = info[mapa]["1k"]["jpg"]["url"]
        except KeyError:
            print(f"{tid}: sin {mapa}"); continue
        bajar(url, os.path.join(carpeta, f"{nombre}.jpg"))
    print(tid, "OK", sorted(os.listdir(carpeta)))
