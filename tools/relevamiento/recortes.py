# Por cada SpriteFrames: frames con el cuerpo cortado en línea recta (columna/fila del borde del bbox
# muy poblada) y frames con restos sueltos (más de una isla grande de píxeles).
import re, sys, os, glob
from PIL import Image
root = sys.argv[1]
def islas(a):
    W, H = a.size; px = a.load(); seen = set(); sizes = []
    for y in range(H):
        for x in range(W):
            if px[x, y] > 20 and (x, y) not in seen:
                st = [(x, y)]; seen.add((x, y)); n = 0
                while st:
                    cx, cy = st.pop(); n += 1
                    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                        nx, ny = cx+dx, cy+dy
                        if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in seen and px[nx, ny] > 20:
                            seen.add((nx, ny)); st.append((nx, ny))
                sizes.append(n)
    return sorted(sizes, reverse=True)
for tres in sorted(glob.glob(os.path.join(root, "assets/**/_frames.tres"), recursive=True)):
    txt = open(tres, encoding="utf-8").read()
    paths = re.findall(r'path="res://([^"]+\.png)"', txt)
    malos = []
    for p in paths:
        im = Image.open(os.path.join(root, p)).convert("RGBA"); a = im.getchannel("A")
        bb = a.point(lambda v: 255 if v > 20 else 0).getbbox()
        if not bb: malos.append((os.path.basename(p), "vacío")); continue
        x0, y0, x1, y1 = bb; h = y1 - y0; w = x1 - x0
        corte = []
        for name, col in (("izq", x0), ("der", x1 - 1)):
            n = sum(1 for y in range(y0, y1) if a.getpixel((col, y)) > 20)
            if n > 0.35 * h: corte.append(f"corte {name} {n}px")
        isl = islas(a)
        restos = [s for s in isl[1:] if s > 30]
        if restos: corte.append(f"{len(restos)} restos sueltos (mayor {restos[0]}px)")
        if corte: malos.append((os.path.basename(p), ", ".join(corte)))
    rel = os.path.relpath(os.path.dirname(tres), root)
    print(f"\n{rel}: {len(malos)}/{len(paths)} frames con problemas")
    for m in malos[:40]: print("   ", m[0], "->", m[1])
