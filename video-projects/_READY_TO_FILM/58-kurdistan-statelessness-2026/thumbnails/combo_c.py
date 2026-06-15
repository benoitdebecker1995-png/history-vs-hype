"""Combo C — fractured map. Duotone the CIA 1992 PD map to charcoal->yellow,
keep the real national borders slicing the Kurdish region, add country labels
+ '30 MILLION'. Real PD source, no AI gen."""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageChops
import os

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")
W, H = 1280, 720
IMPACT = "C:/Windows/Fonts/impact.ttf"
YELLOW = (255, 210, 63)
WHITE = (245, 243, 238)
RED = (227, 18, 24)


def font(sz):
    return ImageFont.truetype(IMPACT, sz)


# duotone LUT: charcoal -> amber -> yellow
def duotone_luts():
    stops = [(0, (18, 20, 22)), (110, (120, 72, 26)), (190, (200, 140, 45)), (255, (255, 214, 70))]
    r, g, b = [], [], []
    for i in range(256):
        for k in range(len(stops) - 1):
            x0, c0 = stops[k]
            x1, c1 = stops[k + 1]
            if x0 <= i <= x1:
                t = (i - x0) / (x1 - x0)
                r.append(int(c0[0] + t * (c1[0] - c0[0])))
                g.append(int(c0[1] + t * (c1[1] - c0[1])))
                b.append(int(c0[2] + t * (c1[2] - c0[2])))
                break
    return r + g + b


src = Image.open(os.path.join(A, "kurd_map_cia.jpg")).convert("RGB")
# crop to the Kurdish region + 4 countries, drop seas at edges
crop = src.crop((40, 110, 790, 660))            # 750 x 550
gray = crop.convert("L")
gray = ImageEnhance.Contrast(gray).enhance(1.3)
duo = Image.merge("RGB", [gray, gray, gray]).point(duotone_luts() * 1)
# scale to fill width, center-crop to 720 tall
scale = W / duo.width
duo = duo.resize((W, int(duo.height * scale)), Image.LANCZOS)
top = (duo.height - H) // 2
duo = duo.crop((0, top, W, top + H))

# vignette
mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(mask).ellipse([-W*0.2, -H*0.2, W*1.2, H*1.2], fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(160))
duo = Image.composite(duo, Image.blend(duo, Image.new("RGB", (W, H)), 0.55), mask)

duo.save(os.path.join(HERE, "comboC_base.png"))
print("comboC base saved", duo.size)
