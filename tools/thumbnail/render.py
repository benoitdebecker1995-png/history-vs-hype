"""Operation render templates that bake the THUMBNAIL-CRAFT-RECIPE in.

Each template enforces the Tier-1 craft by construction:
  - one hero subject, 40-60% of frame, cut out + drop-shadow separation
  - edge vignette + saturation pop (depth)
  - headline: <=3 words/line, size-FLOOR enforced (survives 160px), heavy stroke, ONE accent color
  - one accent at the focal point, in the SAME colour as the headline accent (`--accent`).
    NOT necessarily red: the own-channel data retired the "red pop = look-here signal" claim
    (CTR-THUMBNAIL-FINDINGS-2026-06: red is "neither a winner rule nor a poison rule … do not
    prescribe or penalize red from this data"). Red remains a craft option, not a channel law.
  - a 160px proof saved next to every render (judge clarity there, not at full size)

Operations:  face_compression | dossier_document | map_visual_answer | mechanism_reframe

CLI:
  python -m tools.thumbnail.render dossier  --asset coin.jpg --text "PROOF OF|A STATE" --accent yellow --out out.png
  python -m tools.thumbnail.render --demo b --project-dir "video-projects/.../58-kurdistan-statelessness-2026/thumbnails"

See: .claude/REFERENCE/THUMBNAIL-CRAFT-RECIPE.md
"""
from __future__ import annotations

import argparse
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageChops

LANCZOS = Image.Resampling.LANCZOS

W, H = 1280, 720
IMPACT = "C:/Windows/Fonts/impact.ttf"
ARIAL_BLACK = "C:/Windows/Fonts/ariblk.ttf"

# palette
WHITE = (245, 243, 238)
YELLOW = (255, 210, 63)
RED = (206, 26, 26)
CHARCOAL = (20, 22, 24)
ACCENTS = {"yellow": YELLOW, "red": RED, "white": WHITE}

# recipe constants
MIN_HEADLINE_PX = 110          # text size floor so it survives 160px (R6)
EDGE_MARGIN = 55               # keep text off edges
BADGE_ZONE = (1030, 620, W, H) # bottom-right duration badge — keep clear


# --------------------------------------------------------------------------- #
# primitives
# --------------------------------------------------------------------------- #
def _font(sz: int, path: str = IMPACT) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, sz)


def load_rgb(path: str) -> Image.Image:
    return Image.open(path).convert("RGB")


def pop(img: Image.Image, contrast=1.18, color=1.25, brightness=1.04, sharpen=True) -> Image.Image:
    """Saturation/contrast pop so the subject reads off a dark shelf (R4)."""
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Color(img).enhance(color)
    img = ImageEnhance.Brightness(img).enhance(brightness)
    if sharpen:
        img = img.filter(ImageFilter.UnsharpMask(radius=3, percent=140, threshold=2))
    return img


def square_center_crop(img: Image.Image) -> Image.Image:
    s = min(img.size)
    x = (img.width - s) // 2
    y = (img.height - s) // 2
    return img.crop((x, y, x + s, y + s))


def circular_rgba(img: Image.Image, diameter: int) -> Image.Image:
    """Cut a round subject (coin/seal) with a clean feathered edge."""
    img = square_center_crop(img).resize((diameter, diameter), LANCZOS).convert("RGBA")
    mask = Image.new("L", (diameter, diameter), 0)
    ImageDraw.Draw(mask).ellipse([4, 4, diameter - 4, diameter - 4], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(3))
    img.putalpha(mask)
    return img


def feather_left_rgba(img: Image.Image, px: int = 200) -> Image.Image:
    """Feather the left edge of a subject so it melts into the panel (faces)."""
    img = img.convert("RGBA")
    mask = Image.new("L", img.size, 255)
    d = ImageDraw.Draw(mask)
    for i in range(px):
        d.line([(i, 0), (i, img.height)], fill=int(255 * (i / px)))
    base_alpha = img.split()[3]
    img.putalpha(ImageChops.multiply(base_alpha, mask))
    return img


def drop_shadow(base: Image.Image, subject_rgba: Image.Image, xy, blur=26, offset=(14, 20), opacity=150):
    """Paste a blurred shadow under the subject = depth/separation (R4)."""
    sx, sy = xy
    alpha = subject_rgba.split()[3]
    shadow = Image.new("L", base.size, 0)
    shadow.paste(alpha, (sx + offset[0], sy + offset[1]))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    shadow = shadow.point(lambda v: int(v * opacity / 255))
    black = Image.new("RGB", base.size, (0, 0, 0))
    base.paste(black, (0, 0), shadow)
    return base


def vignette(img: Image.Image, strength=0.5) -> Image.Image:
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).ellipse(
        [-img.width * 0.22, -img.height * 0.22, img.width * 1.22, img.height * 1.22], fill=255
    )
    mask = mask.filter(ImageFilter.GaussianBlur(170))
    dark = Image.new("RGB", img.size, (0, 0, 0))
    return Image.composite(img, Image.blend(img, dark, strength), mask)


def radial_glow(base: Image.Image, box, color) -> Image.Image:
    glow = Image.new("RGB", base.size, (0, 0, 0))
    ImageDraw.Draw(glow).ellipse(box, fill=color)
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    return ImageChops.screen(base, glow)


def gradient_panel(c_left, c_right) -> Image.Image:
    base = Image.new("RGB", (W, H))
    px = base.load()
    for x in range(W):
        t = x / W
        col = tuple(int(c_left[i] + t * (c_right[i] - c_left[i])) for i in range(3))
        for y in range(H):
            px[x, y] = col
    return base


def _fit_size(draw, text, font_path, max_w, start=190, floor=MIN_HEADLINE_PX):
    """Largest font that fits max_w (stroke included), never below the legibility floor."""
    sz = start
    while sz > floor:
        f = _font(sz, font_path)
        sw = max(7, sz // 16)
        bbox = draw.textbbox((0, 0), text, font=f, stroke_width=sw)
        if (bbox[2] - bbox[0]) <= max_w:
            return f, sz, True
        sz -= 4
    return _font(floor, font_path), floor, False  # below floor => caller should cut words


def headline(img: Image.Image, lines, anchor_xy, max_w=None, font_path=IMPACT):
    """Draw stacked lines, each (text, color). Enforces the size floor; warns if a line
    is too long to fit at the floor (=> overlay has too many words, R1/R6)."""
    d = ImageDraw.Draw(img)
    max_w = max_w or int(W * 0.56)
    x, y = anchor_xy
    warnings = []
    longest = max(lines, key=lambda L: len(L[0]))[0]
    f, sz, ok = _fit_size(d, longest, font_path, max_w)
    if not ok:
        warnings.append(f"headline '{longest}' can't fit at the {MIN_HEADLINE_PX}px floor — use fewer words")
    stroke = max(7, sz // 16)
    line_h = int(sz * 1.02)
    for text, color in lines:
        d.text((x, y), text, font=f, fill=color, stroke_width=stroke,
               stroke_fill=(8, 8, 8), anchor="la")
        y += line_h
    bbox = (x, anchor_xy[1], x + max_w, y)
    return warnings, bbox


def _darken(color, factor=0.55):
    return tuple(max(0, int(c * factor)) for c in color)


def accent_bar(img: Image.Image, xy, w, h=14, color=RED):
    ImageDraw.Draw(img).rectangle([xy[0], xy[1], xy[0] + w, xy[1] + h], fill=color)


def accent_seal(img: Image.Image, center, r=46, color=RED):
    """Small distressed wax-seal dot = the focal accent without an amateur box."""
    seal = Image.new("RGBA", (r * 2, r * 2), (0, 0, 0, 0))
    sd = ImageDraw.Draw(seal)
    sd.ellipse([2, 2, r * 2 - 2, r * 2 - 2], fill=tuple(color) + (235,))
    sd.ellipse([int(r * 0.5), int(r * 0.5), int(r * 1.5), int(r * 1.5)],
               outline=_darken(color) + (255,), width=4)
    img.paste(seal, (center[0] - r, center[1] - r), seal)


def proof_160(img: Image.Image, out_path: str):
    """Save the 160px proof — clarity is judged HERE (R3)."""
    p160 = img.resize((160, 90), LANCZOS)
    proof = out_path.replace(".png", "_160.png").replace(".jpg", "_160.png")
    p160.save(proof)
    return proof


def save(img: Image.Image, out_path: str):
    img.convert("RGB").save(out_path, quality=92)
    proof_160(img, out_path)
    return out_path


# --------------------------------------------------------------------------- #
# operation templates
# --------------------------------------------------------------------------- #
def face_compression(asset, lines, out, crop=None, accent_box=(720, 40, 1180, 540),
                     glow=(150, 92, 38), ground=(CHARCOAL, (74, 54, 40))):
    """Ideological / recognizable-subject: subject right, headline in left negative space."""
    src = load_rgb(asset)
    if crop:
        src = src.crop(crop)
    src = pop(src, contrast=1.16, color=1.26, brightness=1.06, sharpen=False)
    scale = (H + 80) / src.height
    src = src.resize((int(src.width * scale), int(src.height * scale)), LANCZOS)
    subj = feather_left_rgba(src, px=220)

    base = gradient_panel(*ground)
    base = radial_glow(base, list(accent_box), glow)
    fx, fy = W - subj.width + 40, H - subj.height + 40
    base.paste(subj, (fx, fy), subj)
    base = vignette(base, 0.5)
    warns, _ = headline(base, lines, (EDGE_MARGIN, 300))
    return save(base, out), warns


def dossier_document(asset, lines, out, accent="yellow", seal=True):
    """Treaty/legal/evidence: a sharp, cut-out evidence object on a dark ground,
    drop-shadow separation, headline in the left negative space, ONE accent colour.

    `accent` was accepted and then ignored until 2026-08-04: the bar and seal were hard-coded red
    while the CLI coloured the headline yellow, so a default render shipped TWO accents — against
    this module's own Tier-1 rule. Pass `accent="red"` for the pre-fix look.
    """
    coin = pop(load_rgb(asset), contrast=1.35, color=1.05, brightness=1.12)
    D = 560
    subj = circular_rgba(coin, D)

    base = Image.new("RGB", (W, H), CHARCOAL)
    base = radial_glow(base, [710, 110, 1180, 600], (46, 52, 58))  # cool lift, no brown halo
    cx, cy = 715, 80
    base = drop_shadow(base, subj, (cx, cy))
    base.paste(subj, (cx, cy), subj)
    base = vignette(base, 0.42)

    warns, bbox = headline(base, lines, (EDGE_MARGIN, 250))
    color = ACCENTS[accent] if accent in ACCENTS else accent
    accent_bar(base, (EDGE_MARGIN, bbox[3] + 14), w=int(W * 0.30), color=color)
    if seal:
        accent_seal(base, (cx + D - 70, cy + 70), color=color)
    return save(base, out), warns


def map_visual_answer(asset, lines, out, contested=None):
    """Territorial: a SIMPLE map + one red contested area + <=3 words.
    `contested` = optional path to a red-zone overlay PNG (transparent) to composite."""
    m = pop(load_rgb(asset).resize((W, H), LANCZOS), contrast=1.1, color=1.15, brightness=1.02)
    base = m
    if contested:
        zone = Image.open(contested).convert("RGBA").resize((W, H), LANCZOS)
        base = Image.alpha_composite(base.convert("RGBA"), zone).convert("RGB")
    base = vignette(base, 0.35)
    # headline top-left, kept short
    warns, _ = headline(base, lines, (EDGE_MARGIN, 40), max_w=int(W * 0.5))
    return save(base, out), warns


def mechanism_reframe(asset, lines, out, accent="yellow"):
    """HOW/mechanism: same craft as dossier but the overlay names the THESIS, not the topic."""
    return dossier_document(asset, lines, out, accent=accent, seal=False)


# --------------------------------------------------------------------------- #
# variants + demos
# --------------------------------------------------------------------------- #
def _report(out, warns):
    flag = "  ! " + "; ".join(warns) if warns else "  ok"
    print(f"saved {os.path.basename(out)} (+_160){flag}")


def demo_b(project_dir):
    """Rebuild Kurdistan Combo B as a dossier coin — 3 non-duplicating overlay variants.
    Title B already says 'coins', so NO overlay may say 'coin' (curiosity-gap, R2)."""
    asset = os.path.join(project_dir, "assets", "coin.jpg")
    variants = [
        ("comboB_v2_proof", [("PROOF OF", WHITE), ("A STATE", YELLOW)]),
        ("comboB_v2_kings", [("A KING'S", WHITE), ("RIGHT", YELLOW)]),
        ("comboB_v2_ruled", [("THEY", WHITE), ("RULED", YELLOW)]),
    ]
    for name, lines in variants:
        out, warns = dossier_document(asset, lines, os.path.join(project_dir, name + ".png"))
        _report(out, warns)


def demo_a(project_dir):
    """Re-render Combo A via the module (parity check — A is the known-good face_compression)."""
    asset = os.path.join(project_dir, "assets", "saladin.jpg")
    out, warns = face_compression(
        asset, [("HE WAS", WHITE), ("KURDISH", YELLOW)],
        os.path.join(project_dir, "comboA_v2.png"), crop=(560, 300, 2140, 2520))
    _report(out, warns)


def demo_c(project_dir):
    """Rebuild Combo C as a SIMPLE map + short overlay (no scale-stat). Honest note:
    a clean fractured-border map ideally comes from MapChart; this uses the region asset."""
    asset = os.path.join(project_dir, "assets", "kurd_map_cia.jpg")
    out, warns = map_visual_answer(
        asset, [("CARVED", WHITE), ("BY FOUR", WHITE), ("STATES", YELLOW)],
        os.path.join(project_dir, "comboC_v2.png"))
    _report(out, warns)


def main():
    p = argparse.ArgumentParser(description="Thumbnail operation render templates")
    p.add_argument("operation", nargs="?", choices=["face", "dossier", "map", "mechanism"])
    p.add_argument("--asset")
    p.add_argument("--text", help="overlay, lines split by | (e.g. 'PROOF OF|A STATE')")
    p.add_argument("--accent", default="yellow", choices=list(ACCENTS))
    p.add_argument("--out")
    p.add_argument("--demo", choices=["a", "b", "c"])
    p.add_argument("--project-dir", default=os.getcwd())
    args = p.parse_args()

    if args.demo:
        {"a": demo_a, "b": demo_b, "c": demo_c}[args.demo](args.project_dir)
        return

    if not (args.operation and args.asset and args.text and args.out):
        p.error("need operation + --asset + --text + --out (or --demo)")
    acc = ACCENTS[args.accent]
    parts = args.text.split("|")
    lines = [(t, WHITE) for t in parts[:-1]] + [(parts[-1], acc)]
    fn = {"face": face_compression, "dossier": dossier_document,
          "map": map_visual_answer, "mechanism": mechanism_reframe}[args.operation]
    # Templates that take an accent get the chosen one — `--accent` used to be a no-op for them.
    kwargs = {"accent": args.accent} if args.operation in {"dossier", "mechanism"} else {}
    out, warns = fn(args.asset, lines, args.out, **kwargs)
    _report(out, warns)


if __name__ == "__main__":
    main()
