import re, sys, os, glob
from PIL import Image
root = sys.argv[1]
rows = {}
for scn in sorted(glob.glob(os.path.join(root, "scenes/**/*.tscn"), recursive=True)):
    txt = open(scn, encoding="utf-8").read()
    ids = dict((m.group(2), m.group(1)) for m in re.finditer(r'path="res://([^"]+\.(?:png|jpg|webp))" id="([^"]+)"', txt))
    for node in re.split(r'\n(?=\[node )', txt):
        m = re.search(r'texture = ExtResource\("([^"]+)"\)', node)
        if not m or m.group(1) not in ids: continue
        sc = re.search(r'\nscale = Vector2\(([-\d.]+), ([-\d.]+)\)', node)
        s = abs(float(sc.group(1))) if sc else 1.0
        name = re.search(r'name="([^"]+)"', node).group(1)
        rows.setdefault(ids[m.group(1)], []).append((os.path.basename(scn), name, s))
tf = os.path.join(root, ".godot"); 
print(f"{'textura':70} {'tamaño':>10} {'colores':>7} {'escalas':>18} usos")
for p, uses in sorted(rows.items()):
    try: im = Image.open(os.path.join(root, p)).convert("RGBA")
    except Exception as e: print(p, "ERR", e); continue
    cols = len(set(c for c in im.getdata() if c[3] > 0))
    scs = sorted(set(round(u[2], 3) for u in uses))
    print(f"{p[-70:]:70} {im.size[0]:>4}x{im.size[1]:<5} {cols:>7} {str(scs):>18} {len(uses)}")
