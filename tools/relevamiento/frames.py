import re, sys, os
from PIL import Image
root, tres = sys.argv[1], sys.argv[2]
txt = open(os.path.join(root, tres), encoding="utf-8").read()
ids = dict((m.group(2), m.group(1)) for m in re.finditer(r'path="res://([^"]+)" id="([^"]+)"', txt))
for block in re.finditer(r'\{\s*"frames": \[(.*?)\],\s*"loop": (\w+),\s*"name": &"(\w+)",\s*"speed": ([\d.]+)', txt, re.S):
    frames = re.findall(r'ExtResource\("([^"]+)"\)', block.group(1))
    durs = re.findall(r'"duration": ([\d.]+)', block.group(1))
    print(f"\n[{block.group(3)}] {len(frames)} frames @ {block.group(4)} fps loop={block.group(2)}")
    for fid, d in zip(frames, durs):
        p = ids[fid]; im = Image.open(os.path.join(root, p)).convert("RGBA")
        a = im.getchannel("A"); bb = a.point(lambda v: 255 if v > 20 else 0).getbbox()
        cols = len(set(im.getdata())) 
        W, H = im.size
        print(f"  {os.path.basename(p):18} {W}x{H} bbox={bb} pie_y={bb[3] if bb else None} centro_x={(bb[0]+bb[2])//2 if bb else None} alto={bb[3]-bb[1] if bb else 0} colores={cols} dur={d}")
