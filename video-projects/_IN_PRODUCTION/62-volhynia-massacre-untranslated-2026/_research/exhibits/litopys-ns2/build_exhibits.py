from pathlib import Path
from PIL import Image, ImageDraw

SRC = Path(r"C:\Users\benoi\AppData\Local\Temp\litopys_ns2_finalrenders")
OUT = Path(r"G:\History vs Hype\video-projects\_IN_PRODUCTION\62-volhynia-massacre-untranslated-2026\_research\exhibits\litopys-ns2\resolve-assets")
OUT.mkdir(parents=True, exist_ok=True)


def save_copy(source, name):
    Image.open(SRC / source).save(OUT / name)


def crop(source, box, name):
    Image.open(SRC / source).crop(box).save(OUT / name)


def highlighted(source, box, rectangles, name):
    image = Image.open(SRC / source).crop(box).convert("RGBA")
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for rectangle in rectangles:
        draw.rounded_rectangle(rectangle, radius=8, fill=(232, 178, 45, 58), outline=(190, 125, 0, 215), width=5)
    Image.alpha_composite(image, overlay).convert("RGB").save(OUT / name)


# Document 100: printed pp. 173-175; PDF pages 233-235.
save_copy("huta-234.png", "huta-doc100-full-page.png")
crop("huta-234.png", (55, 0, 1065, 1510), "huta-doc100-detail.png")
highlighted(
    "huta-234.png",
    (55, 0, 1065, 1510),
    [(80, 425, 950, 825)],
    "huta-doc100-highlight.png",
)
save_copy("huta-233.png", "huta-doc100-support-01.png")
save_copy("huta-235.png", "huta-doc100-support-02.png")

# Document 149-A/B: both sentences are on printed p. 310; PDF page 370.
save_copy("doc149-370.png", "doc149-full-page.png")
crop("doc149-370.png", (55, 650, 1065, 1260), "doc149-destroying-poles-detail.png")
highlighted(
    "doc149-370.png",
    (55, 650, 1065, 1260),
    [(65, 180, 950, 225)],
    "doc149-destroying-poles-highlight.png",
)
crop("doc149-370.png", (55, 790, 1065, 1280), "doc149-active-polish-element-detail.png")
highlighted(
    "doc149-370.png",
    (55, 790, 1065, 1280),
    [(65, 65, 950, 190)],
    "doc149-active-polish-element-highlight.png",
)

# Document 149-C: narrow control observation on printed p. 305; continuation p. 306.
save_copy("doc149-365.png", "doc149-control-full-page.png")
save_copy("doc149-366.png", "doc149-control-support-full-page.png")
crop("doc149-365.png", (55, 900, 1070, 1550), "doc149-control-detail.png")
highlighted(
    "doc149-365.png",
    (55, 900, 1070, 1550),
    [(55, 155, 960, 265), (55, 350, 960, 570)],
    "doc149-control-highlight.png",
)

# Provenance/signature page, printed p. 313; PDF page 373.
save_copy("doc149-373.png", "doc149-provenance-full-page.png")
