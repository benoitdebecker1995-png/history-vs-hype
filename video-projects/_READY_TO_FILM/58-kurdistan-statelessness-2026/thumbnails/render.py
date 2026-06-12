"""Render draft v1 thumbnails for #58 Kurdistan — real PD assets, SERP-grounded.
Combo A (Saladin face) + Combo B (coin). Combo C (fractured map) = MapChart manual.
No AI gen — PIL compositing of real Wikimedia/LACMA images only.
"""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageChops
import os

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")
W, H = 1280, 720
IMPACT = "C:/Windows/Fonts/impact.ttf"

YELLOW = (255, 210, 63)
WHITE = (245, 243, 238)
RED = (227, 18, 24)
CHARCOAL = (28, 32, 34)


def font(sz):
    return ImageFont.truetype(IMPACT, sz)


def draw_text(d, xy, text, fnt, fill, anchor="la", stroke=8, stroke_fill=(8, 8, 8)):
    d.text(xy, text, font=fnt, fill=fill, anchor=anchor,
           stroke_width=stroke, stroke_fill=stroke_fill)


def vignette(img, strength=0.55):
    mask = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([-img.width*0.25, -img.height*0.25,
                img.width*1.25, img.height*1.25], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(180))
    dark = Image.new("RGB", img.size, (0, 0, 0))
    return Image.composite(img, Image.blend(img, dark, strength), mask)


# ---------- COMBO A — SALADIN ----------
def combo_a():
    src = Image.open(os.path.join(A, "saladin.jpg")).convert("RGB")
    # crop out the wooden frame -> painting interior (orig 2346x2934, frame ~4x preview)
    sal = src.crop((560, 300, 2140, 2520))  # turban-top through chest, no frame
    # warm grade: boost warmth + contrast + saturation
    sal = ImageEnhance.Contrast(sal).enhance(1.18)
    sal = ImageEnhance.Color(sal).enhance(1.28)
    sal = ImageEnhance.Brightness(sal).enhance(1.06)
    # amber warm overlay (screen-ish warmth via blend)
    warm = Image.new("RGB", sal.size, (150, 86, 30))
    sal = ImageChops.screen(sal, Image.eval(warm, lambda v: int(v*0.30)))
    # scale to fill height with bleed
    scale = (H + 80) / sal.height
    sal = sal.resize((int(sal.width*scale), int(sal.height*scale)), Image.LANCZOS)

    # base canvas: warm-dark horizontal gradient (charcoal left -> warm right)
    base = Image.new("RGB", (W, H))
    for x in range(W):
        t = x / W
        r = int(28 + t*46)
        g = int(32 + t*22)
        b = int(34 + t*6)
        for_col = (r, g, b)
        ImageDraw.Draw(base).line([(x, 0), (x, H)], fill=for_col)

    # warm radial glow where the head will sit (right side)
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([720, 40, 1180, 540], fill=(150, 92, 38))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    base = ImageChops.screen(base, glow)

    # paste Saladin on the right, feather the left edge into the panel
    fx = W - sal.width + 40   # nudge so head sits right-of-center
    fy = H - sal.height + 40
    edge = Image.new("L", sal.size, 255)
    ed = ImageDraw.Draw(edge)
    for i in range(220):  # feather left edge
        ed.line([(i, 0), (i, sal.height)], fill=int(255 * (i/220)))
    base.paste(sal, (fx, fy), edge)

    base = vignette(base, 0.50)
    d = ImageDraw.Draw(base)
    # text left/lower
    draw_text(d, (60, 300), "HE WAS", font(150), WHITE, stroke=10)
    draw_text(d, (60, 450), "KURDISH", font(168), YELLOW, stroke=11)
    base.save(os.path.join(HERE, "comboA_saladin_v1.png"))
    print("comboA saved")


# ---------- COMBO B — COIN ----------
def combo_b():
    src = Image.open(os.path.join(A, "coin.jpg")).convert("RGB")
    # coin is ~centered, gray bg. crop tight to coin then circular-mask onto charcoal.
    coin = src.crop((25, 30, 535, 540))
    coin = ImageEnhance.Contrast(coin).enhance(1.35)
    coin = ImageEnhance.Brightness(coin).enhance(1.12)
    coin = coin.filter(ImageFilter.UnsharpMask(radius=3, percent=160, threshold=2))
    # warm the silver slightly
    coin = ImageChops.screen(coin, Image.new("RGB", coin.size, (40, 24, 6)))
    D = 600
    coin = coin.resize((D, D), Image.LANCZOS)
    cmask = Image.new("L", (D, D), 0)
    ImageDraw.Draw(cmask).ellipse([6, 6, D-6, D-6], fill=255)
    cmask = cmask.filter(ImageFilter.GaussianBlur(4))

    base = Image.new("RGB", (W, H), CHARCOAL)
    # subtle radial charcoal vignette + warm under-glow behind coin
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    ImageDraw.Draw(glow).ellipse([640, 70, 1240, 670], fill=(70, 44, 14))
    glow = glow.filter(ImageFilter.GaussianBlur(110))
    base = ImageChops.screen(base, glow)
    cx, cy = 700, 60  # coin center-right
    base.paste(coin, (cx, cy), cmask)
    # warm rim ring
    rd = ImageDraw.Draw(base)
    rd.ellipse([cx+4, cy+4, cx+D-4, cy+D-4], outline=(150, 96, 40), width=5)

    base = vignette(base, 0.42)
    d = ImageDraw.Draw(base)
    # "THEIR COINS" red rubber-stamp, angled
    stamp = Image.new("RGBA", (760, 300), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.text((20, 20), "THEIR", font=font(140), fill=RED + (255,), stroke_width=3,
            stroke_fill=(120, 8, 10, 255))
    sd.text((20, 150), "COINS", font=font(140), fill=RED + (255,), stroke_width=3,
            stroke_fill=(120, 8, 10, 255))
    sd.rectangle([6, 6, 470, 290], outline=RED + (255,), width=8)
    stamp = stamp.rotate(13, expand=True, resample=Image.BICUBIC)
    base.paste(stamp, (40, 200), stamp)
    base.save(os.path.join(HERE, "comboB_coin_v1.png"))
    print("comboB saved")


combo_a()
combo_b()
print("done")
