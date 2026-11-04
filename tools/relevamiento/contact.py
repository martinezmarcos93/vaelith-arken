import sys, os
from PIL import Image, ImageDraw
out, crop, files = sys.argv[1], tuple(map(int, sys.argv[2].split(","))), sys.argv[3:]
ims = [Image.open(f).convert("RGBA").crop(crop) for f in files]
w, h = ims[0].size; k = 3
sheet = Image.new("RGBA", (w*k*len(ims), h*k+14), (40, 40, 48, 255))
d = ImageDraw.Draw(sheet)
for i, im in enumerate(ims):
    bg = Image.new("RGBA", im.size, (90, 90, 100, 255)); bg.alpha_composite(im)
    sheet.paste(bg.resize((w*k, h*k), Image.NEAREST), (i*w*k, 14))
    d.text((i*w*k+4, 1), os.path.basename(files[i]), fill="white")
    d.line([(i*w*k, 14+(214-crop[1])*k), ((i+1)*w*k, 14+(214-crop[1])*k)], fill=(255,0,0,255))
sheet.save(out)
