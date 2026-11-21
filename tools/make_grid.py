"""Build images/photo_grid.jpg from the hand photos (justified rows, equal width)."""
import sys
from pathlib import Path
from PIL import Image, ImageOps

SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "Downloads"
OUT = Path(__file__).resolve().parent.parent / "images" / "photo_grid.jpg"
ROWS = [
    ["PXL_20260122_111415105~2.jpg", "PXL_20260120_175004121~2.jpg", "PXL_20260201_032522987.jpg"],
    ["PXL_20260201_031905454.jpg", "PXL_20260201_042711444.jpg"],
]
W, GAP, BG = 2400, 12, (255, 255, 255)

rows = []
for names in ROWS:
    ims = [ImageOps.exif_transpose(Image.open(SRC / n)).convert("RGB") for n in names]
    aspect = sum(im.width / im.height for im in ims)
    h = round((W - GAP * (len(ims) - 1)) / aspect)
    rows.append([im.resize((round(h * im.width / im.height), h), Image.LANCZOS) for im in ims])

H = sum(r[0].height for r in rows) + GAP * (len(rows) - 1)
canvas = Image.new("RGB", (W, H), BG)
y = 0
for r in rows:
    x = 0
    for i, im in enumerate(r):
        if i == len(r) - 1:  # absorb rounding in the last tile
            im = im.resize((W - x, im.height), Image.LANCZOS)
        canvas.paste(im, (x, y))
        x += im.width + GAP
    y += r[0].height + GAP
canvas.save(OUT, quality=88, optimize=True)
print(OUT, canvas.size)
