"""One-off script to crop and optimize the source photos for the new website.
Not part of the deployed site; kept here for reproducibility.
"""
from PIL import Image, ImageOps
import os

SRC = os.path.join(os.path.dirname(__file__), "originals")
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
os.makedirs(OUT, exist_ok=True)


def save(im, name, widths, quality=82, webp_quality=78):
    im = ImageOps.exif_transpose(im)
    for w in widths:
        ratio = w / im.width
        h = round(im.height * ratio)
        resized = im.resize((w, h), Image.LANCZOS)
        jpg_path = os.path.join(OUT, f"{name}-{w}.jpg")
        webp_path = os.path.join(OUT, f"{name}-{w}.webp")
        resized.convert("RGB").save(jpg_path, "JPEG", quality=quality, optimize=True, progressive=True)
        resized.convert("RGB").save(webp_path, "WEBP", quality=webp_quality)
        print("wrote", jpg_path, resized.size, os.path.getsize(jpg_path))
        print("wrote", webp_path, resized.size, os.path.getsize(webp_path))


# 1) Hero / about portrait (outdoors, scarf) -> keep close to native portrait ratio
portrait = Image.open(os.path.join(SRC, "portrait-edda-raw.jpg"))
# Slight crop to tighten composition (remove a little empty space at the very top)
w, h = portrait.size
portrait_cropped = portrait.crop((0, int(h * 0.02), w, h))
save(portrait_cropped, "edda-portrait", widths=[640, 900, 1200, 1600])

# 2) Edda holding newborn in green sweater -> use the full original photo,
#    uncropped, so it keeps its true (portrait, ~9:16) aspect ratio. Displayed
#    fairly small on the page (max ~300px wide), so only two source sizes
#    are needed.
baby2 = Image.open(os.path.join(SRC, "edda-baby-2-raw.jpg"))
save(baby2, "edda-baby-newborn", widths=[480, 800])

# 3) Small accent photo (striped shirt, sleeping baby) -> already small, just re-encode
baby1 = Image.open(os.path.join(SRC, "edda-baby-1-raw.jpg"))
save(baby1, "edda-baby-sleeping", widths=[360, 480])

print("done")
