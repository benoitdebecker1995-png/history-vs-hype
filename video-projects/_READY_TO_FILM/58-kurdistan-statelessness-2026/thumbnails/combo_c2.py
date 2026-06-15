"""Combo C v2 — Cambridge-sourced Kurdish region as a solid yellow shape on
charcoal, country labels on the lobes, '30 MILLION'. Mask upscaled + flat-filled
so it stays crisp. Real CC-BY-SA source (Cambridge History of the Kurds map)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import os

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")
W, H = 1280, 720
IMPACT = "C:/Windows/Fonts/impact.ttf"
YELLOW = (255, 210, 63)
YELLOW_D = (210, 150, 30)
WHITE = (245, 243, 238)
CHARCOAL = (26, 30, 33)


def font(sz):
    return ImageFont.truetype(IMPACT, sz)


def label(d, xy, text, sz, fill=WHITE, anchor="mm", stroke=6):
    d.text(xy, text, font=font(sz), fill=fill, anchor=anchor,
           stroke_width=stroke, stroke_fill=(8, 8, 8))


# --- extract green region mask ---
im = Image.open(os.path.join(A, "kurd_areas.png")).convert("RGBA")
a = np.array(im)
r, g, b = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
green = (g > 85) & (g > r + 18) & (g > b + 18)
mask = Image.fromarray((green * 255).astype("uint8"), "L").crop((520, 588, 815, 738))
# upscale mask big, smooth, re-threshold -> crisp solid shape
us = 5
mask = mask.resize((mask.width * us, mask.height * us), Image.LANCZOS)
mask = mask.filter(ImageFilter.GaussianBlur(3)).point(lambda v: 255 if v > 110 else 0)
# scale to ~1000 wide on canvas
target_w = 1020
sc = target_w / mask.width
region = mask.resize((target_w, int(mask.height * sc)), Image.LANCZOS)
region = region.filter(ImageFilter.GaussianBlur(1.2))

# --- canvas ---
base = Image.new("RGB", (W, H), CHARCOAL)
# warm under-glow
from PIL import ImageChops
glow = Image.new("RGB", (W, H), (0, 0, 0))
gx0 = (W - region.width) // 2
gy0 = (H - region.height) // 2
# neutral cool lift (no brown — pushes the thumbnail away from the terrain-map pack)
ImageDraw.Draw(glow).ellipse([gx0 - 40, gy0 - 40, gx0 + region.width + 40,
                              gy0 + region.height + 40], fill=(40, 47, 54))
glow = glow.filter(ImageFilter.GaussianBlur(90))
base = ImageChops.screen(Image.new("RGB", (W, H), (20, 23, 26)), glow)

# region position
rx = (W - region.width) // 2 + 30
ry = (H - region.height) // 2 - 10
# dark stroke (offset shadow) for pop
shadow = region.filter(ImageFilter.MaxFilter(9))
base.paste(Image.new("RGB", region.size, (8, 9, 10)), (rx, ry), shadow)
base.paste(Image.new("RGB", region.size, YELLOW), (rx, ry), region)

d = ImageDraw.Draw(base)
# country labels on lobes (compass-correct: TR north, SY west, IRAQ south, IRAN east)
label(d, (rx + int(region.width*0.36), ry + int(region.height*0.16)), "TURKEY", 60)
label(d, (rx + int(region.width*0.12), ry + int(region.height*0.44)), "SYRIA", 50)
label(d, (rx + int(region.width*0.42), ry + int(region.height*0.78)), "IRAQ", 55)
label(d, (rx + int(region.width*0.88), ry + int(region.height*0.40)), "IRAN", 55)

# overlay headline
label(d, (40, 60), "30 MILLION", 110, fill=YELLOW, anchor="lm", stroke=9)
label(d, (44, 150), "NO COUNTRY", 70, fill=WHITE, anchor="lm", stroke=7)

base.save(os.path.join(HERE, "comboC_map_v1.png"))
print("comboC v1 saved")
