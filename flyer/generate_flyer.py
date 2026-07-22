#!/usr/bin/env python3
"""Generate a print-ready A4 flyer for Edda – Doula."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
OUT_PNG = ROOT / "flyer-a4.png"
OUT_PREVIEW = ROOT / "flyer-preview.png"
OUT_PDF = ROOT / "flyer.pdf"
ARTIFACT = Path("/opt/cursor/artifacts/screenshots/edda-doula-flyer-a4.png")

# A4 at 300 DPI
DPI = 300
W = int(210 / 25.4 * DPI)  # 2480
H = int(297 / 25.4 * DPI)  # 3508

# Brand colors
BG = (251, 246, 240)
BG_WARM = (245, 232, 222)
PRIMARY = (196, 108, 74)
PRIMARY_DARK = (143, 69, 41)
SAGE = (124, 146, 113)
SAGE_DARK = (67, 89, 60)
TEXT = (53, 41, 31)
MUTED = (111, 97, 87)
BORDER = (232, 220, 205)
WHITE = (255, 255, 255)

FONTS = ROOT / "fonts"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / name), size)


def mm(value: float) -> int:
    return int(value / 25.4 * DPI)


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
) -> tuple[int, int]:
    draw.text(xy, text, font=fnt, fill=fill)
    box = draw.textbbox(xy, text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def wrap_text(
    text: str,
    fnt: ImageFont.FreeTypeFont,
    max_width: int,
    draw: ImageDraw.ImageDraw,
) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def rounded_mask(size: tuple[int, int], radii: tuple[int, int, int, int]) -> Image.Image:
    """radii = (tl, tr, br, bl)"""
    w, h = size
    tl, tr, br, bl = radii
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    d.rectangle([tl, 0, w - tr, h], fill=255)
    d.rectangle([0, tl, w, h - bl], fill=255)
    d.rectangle([bl, 0, w - br, h], fill=255)
    d.pieslice([0, 0, 2 * tl, 2 * tl], 180, 270, fill=255)
    d.pieslice([w - 2 * tr, 0, w, 2 * tr], 270, 360, fill=255)
    d.pieslice([w - 2 * br, h - 2 * br, w, h], 0, 90, fill=255)
    d.pieslice([0, h - 2 * bl, 2 * bl, h], 90, 180, fill=255)
    return mask


def paste_rounded(
    base: Image.Image,
    img: Image.Image,
    box: tuple[int, int, int, int],
    radii: tuple[int, int, int, int],
) -> None:
    x0, y0, x1, y1 = box
    target = img.resize((x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
    mask = rounded_mask(target.size, radii)
    base.paste(target, (x0, y0), mask)


def draw_logo(base: Image.Image, x: int, y: int, size: int) -> None:
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # Terracotta circle + cream offset circle (logo mark from website)
    margin = size * 0.06
    d.ellipse([margin, margin, size - margin * 0.2, size - margin * 0.2], fill=PRIMARY + (255,))
    ox = size * 0.22
    d.ellipse(
        [margin + ox, margin * 0.7, size - margin * 0.05 + ox * 0.2, size - margin * 0.4],
        fill=BG + (255,),
    )
    base.paste(layer, (x, y), layer)


def vertical_gradient(size: tuple[int, int], top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    w, h = size
    img = Image.new("RGB", size, top)
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        # Ease
        t = t * t * (3 - 2 * t)
        color = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        for x in range(w):
            px[x, y] = color
    return img


def soft_radial(base: Image.Image, center: tuple[int, int], radius: int, color: tuple[int, int, int], alpha: int) -> None:
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    cx, cy = center
    for i in range(12, 0, -1):
        r = int(radius * i / 12)
        a = int(alpha * (1 - i / 12) ** 1.4)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (a,))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=mm(8)))
    base.alpha_composite(overlay)


def make_flyer() -> Image.Image:
    base = vertical_gradient((W, H), BG, (243, 230, 218)).convert("RGBA")
    soft_radial(base, (W, 0), mm(120), PRIMARY, 55)
    soft_radial(base, (0, H), mm(110), SAGE, 60)

    draw = ImageDraw.Draw(base)

    # Top accent bar
    for x in range(W):
        t = x / (W - 1)
        if t < 0.55:
            local = t / 0.55
            color = tuple(int(PRIMARY_DARK[i] + (PRIMARY[i] - PRIMARY_DARK[i]) * local) for i in range(3))
        else:
            local = (t - 0.55) / 0.45
            color = tuple(int(PRIMARY[i] + (SAGE[i] - PRIMARY[i]) * local) for i in range(3))
        draw.line([(x, 0), (x, mm(6.5))], fill=color + (255,))

    # Margins
    left = mm(14)
    right = W - mm(14)
    content_w = right - left

    # Brand
    y = mm(16)
    logo_size = mm(12)
    draw_logo(base, left, y, logo_size)

    brand_font = font("lora-700.ttf", mm(9.5))
    brand_x = left + logo_size + mm(3.2)
    brand_y = y + mm(0.5)
    draw.text((brand_x, brand_y), "Edda", font=brand_font, fill=TEXT)
    edda_w = draw.textlength("Edda", font=brand_font)
    dot_font = font("lora-400.ttf", mm(9.5))
    draw.text((brand_x + edda_w + mm(1.2), brand_y), "·", font=dot_font, fill=PRIMARY)
    dot_w = draw.textlength("·", font=dot_font)
    draw.text((brand_x + edda_w + mm(1.2) + dot_w + mm(1.2), brand_y), "Doula", font=brand_font, fill=TEXT)

    sub_font = font("inter-500.ttf", mm(3.1))
    draw.text(
        (brand_x, brand_y + mm(10.5)),
        "GEBURTSBEGLEITUNG IN ERKELENZ & KREIS HEINSBERG",
        font=sub_font,
        fill=SAGE_DARK,
    )

    # Hero
    y = mm(36)
    portrait_path = REPO / "assets/img/edda-portrait-1200.jpg"
    portrait = Image.open(portrait_path).convert("RGB")

    photo_w = mm(78)
    photo_h = mm(98)
    photo_x1 = right
    photo_x0 = photo_x1 - photo_w
    photo_y0 = y
    photo_y1 = y + photo_h

    # Soft shadow under portrait
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle(
        [photo_x0 + mm(2), photo_y0 + mm(3), photo_x1 + mm(2), photo_y1 + mm(3)],
        radius=mm(4),
        fill=(53, 41, 31, 45),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(mm(4)))
    base.alpha_composite(shadow)

    paste_rounded(
        base,
        portrait,
        (photo_x0, photo_y0, photo_x1, photo_y1),
        (mm(2), mm(16), mm(2), mm(16)),
    )

    # Headline + lead beside photo
    copy_w = photo_x0 - left - mm(8)
    h1_font = font("lora-600.ttf", mm(9.2))
    h1 = "Einfühlsame Begleitung für deine Geburt"
    h1_lines = wrap_text(h1, h1_font, copy_w, draw)
    ty = y + mm(6)
    line_gap = mm(11)
    for line in h1_lines:
        draw.text((left, ty), line, font=h1_font, fill=TEXT)
        ty += line_gap

    lead_font = font("inter-400.ttf", mm(3.7))
    lead = (
        "Als deine Doula begleite ich dich vor, während und nach der Geburt – "
        "liebevoll, zuverlässig und ganz an deiner Seite."
    )
    ty += mm(3)
    for line in wrap_text(lead, lead_font, copy_w, draw):
        draw.text((left, ty), line, font=lead_font, fill=MUTED)
        ty += mm(5.2)

    # Divider
    div_y = max(photo_y1, ty) + mm(8)
    draw.line([(left, div_y), (right, div_y)], fill=BORDER + (255,), width=max(2, mm(0.35)))

    # Two columns: offerings + area
    col_gap = mm(8)
    col1_w = int(content_w * 0.58)
    col2_x = left + col1_w + col_gap
    col2_w = right - col2_x

    y = div_y + mm(7)
    label_font = font("inter-600.ttf", mm(2.8))
    h2_font = font("lora-600.ttf", mm(5.0))
    body_font = font("inter-400.ttf", mm(3.4))
    num_font = font("lora-700.ttf", mm(3.6))
    strong_font = font("inter-500.ttf", mm(3.4))

    draw.text((left, y), "SO BEGLEITE ICH DICH", font=label_font, fill=PRIMARY)
    draw.text((col2_x, y), "EINSATZGEBIET", font=label_font, fill=PRIMARY)
    y += mm(5)

    draw.text((left, y), "Von der Schwangerschaft bis danach", font=h2_font, fill=TEXT)
    draw.text((col2_x, y), "Zuhause im Kreis Heinsberg", font=h2_font, fill=TEXT)
    y += mm(8)

    offerings = [
        ("01", "Mindestens drei Vorbereitungstreffen in der Schwangerschaft"),
        ("02", "Rufbereitschaft rund um den Geburtstermin (Tag und Nacht)"),
        ("03", "Begleitung während der gesamten Geburt – Klinik, Geburtshaus oder zu Hause"),
        ("04", "Nachgespräch, um das Erlebte in Ruhe zu besprechen"),
    ]

    oy = y
    for num, text in offerings:
        draw.text((left, oy), num, font=num_font, fill=SAGE)
        tx = left + mm(8)
        lines = wrap_text(text, body_font, col1_w - mm(8), draw)
        for i, line in enumerate(lines):
            draw.text((tx, oy + (mm(0.2) if i == 0 else 0) + i * mm(4.6)), line, font=body_font, fill=TEXT)
        oy += max(mm(11), len(lines) * mm(4.6) + mm(4))

    area_intro = "Ich begleite Familien in Erkelenz und der gesamten Region:"
    ay = y
    for line in wrap_text(area_intro, body_font, col2_w, draw):
        draw.text((col2_x, ay), line, font=body_font, fill=MUTED)
        ay += mm(4.8)

    ay += mm(2)
    places = (
        "Erkelenz · Heinsberg · Wegberg · Wassenberg · Hückelhoven · "
        "Geilenkirchen · Übach-Palenberg · Gangelt · Selfkant · Waldfeucht"
    )
    for line in wrap_text(places, strong_font, col2_w, draw):
        draw.text((col2_x, ay), line, font=strong_font, fill=TEXT)
        ay += mm(4.8)

    ay += mm(3)
    note = "Auch etwas außerhalb: gerne persönlich melden."
    for line in wrap_text(note, body_font, col2_w, draw):
        draw.text((col2_x, ay), line, font=body_font, fill=MUTED)
        ay += mm(4.6)

    # Footer band
    footer_top = max(oy, ay) + mm(10)
    draw.line([(left, footer_top), (right, footer_top)], fill=BORDER + (255,), width=max(2, mm(0.35)))

    fy = footer_top + mm(7)
    contact_h2 = font("lora-600.ttf", mm(4.6))
    draw.text((left, fy), "Lass uns sprechen", font=contact_h2, fill=TEXT)

    # QR on the right
    qr = Image.open(ROOT / "qr-code.png").convert("RGB")
    qr_size = mm(34)
    qr_x0 = right - qr_size
    qr_y0 = fy
    # QR frame
    pad = mm(2)
    draw.rounded_rectangle(
        [qr_x0 - pad, qr_y0 - pad, right + pad * 0.2, qr_y0 + qr_size + pad],
        radius=mm(2),
        outline=BORDER + (255,),
        width=max(2, mm(0.45)),
        fill=BG + (255,),
    )
    base.paste(qr.resize((qr_size, qr_size), Image.Resampling.LANCZOS), (qr_x0, qr_y0))

    qr_caption = font("inter-400.ttf", mm(2.6))
    qr_url = font("inter-600.ttf", mm(2.6))
    cap = "Mehr erfahren"
    url = "www.edda-die-doula.de"
    cap_w = draw.textlength(cap, font=qr_caption)
    url_w = draw.textlength(url, font=qr_url)
    cy = qr_y0 + qr_size + mm(3)
    draw.text((qr_x0 + (qr_size - cap_w) / 2, cy), cap, font=qr_caption, fill=MUTED)
    draw.text((qr_x0 + (qr_size - url_w) / 2, cy + mm(3.5)), url, font=qr_url, fill=PRIMARY_DARK)

    # Contact rows
    label_f = font("inter-600.ttf", mm(2.7))
    value_f = font("inter-500.ttf", mm(3.5))
    rows = [
        ("TELEFON", "0157 5835 7374"),
        ("WHATSAPP", "0157 5835 7374"),
        ("E-MAIL", "kontakt@edda-die-doula.de"),
    ]
    ry = fy + mm(8)
    for label, value in rows:
        draw.text((left, ry + mm(0.6)), label, font=label_f, fill=MUTED)
        draw.text((left + mm(24), ry), value, font=value_f, fill=TEXT)
        ry += mm(6.2)

    price_font = font("inter-400.ttf", mm(3.2))
    price_strong = font("inter-600.ttf", mm(3.2))
    ry += mm(2)
    prefix = "Geburtsbegleitung: "
    draw.text((left, ry), prefix, font=price_font, fill=SAGE_DARK)
    pw = draw.textlength(prefix, font=price_font)
    draw.text((left + pw, ry), "1.000 € VB", font=price_strong, fill=TEXT)

    cred_font = font("inter-400.ttf", mm(2.8))
    ry += mm(7)
    draw.line([(left, ry), (left + mm(70), ry)], fill=BORDER + (255,), width=max(1, mm(0.3)))
    ry += mm(3.5)
    draw.text(
        (left, ry),
        "Edda Möller · Ausgebildete Doula (GfG Berlin, 2022)",
        font=cred_font,
        fill=MUTED,
    )

    return base.convert("RGB")


def save_pdf_from_png(png_path: Path, pdf_path: Path) -> None:
    """Embed the 300 dpi PNG on an exact A4 page."""
    import fitz

    doc = fitz.open()
    rect = fitz.Rect(0, 0, 595.2756, 841.8898)
    page = doc.new_page(width=rect.width, height=rect.height)
    page.insert_image(rect, filename=str(png_path))
    doc.save(str(pdf_path), deflate=True, garbage=4)
    doc.close()


def main() -> None:
    flyer = make_flyer()
    flyer.save(OUT_PNG, "PNG", dpi=(DPI, DPI), optimize=True)
    save_pdf_from_png(OUT_PNG, OUT_PDF)

    # Screen preview ~150 DPI
    preview = flyer.resize((W // 2, H // 2), Image.Resampling.LANCZOS)
    preview.save(OUT_PREVIEW, "PNG", optimize=True)

    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    preview.save(ARTIFACT, "PNG", optimize=True)

    print(f"A4 PNG: {OUT_PNG} ({OUT_PNG.stat().st_size} bytes) {flyer.size}")
    print(f"PDF:    {OUT_PDF} ({OUT_PDF.stat().st_size} bytes)")
    print(f"Preview:{OUT_PREVIEW} {preview.size}")
    print(f"Artifact:{ARTIFACT}")


if __name__ == "__main__":
    main()
