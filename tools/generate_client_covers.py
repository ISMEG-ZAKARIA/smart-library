from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "client" / "assets" / "images" / "covers"
SIZE = (900, 1200)


BOOKS = [
    ("petit-prince", "Le Petit\nPrince", "Antoine de\nSaint-Exupéry", ("#07111f", "#0f5870", "#8ed6df"), "planet"),
    ("etranger", "L'Étranger", "Albert Camus", ("#f4a332", "#f2c66d", "#14191a"), "sun"),
    ("miserables", "Les\nMisérables", "Victor Hugo", ("#171d20", "#59615a", "#d8c994"), "street"),
    ("alchemist", "L'Alchimiste", "Paulo Coelho", ("#1a2430", "#d6a438", "#e9d39a"), "desert"),
    ("nineteen-eighty-four", "1984", "George Orwell", ("#151515", "#9d1f18", "#e8e2d2"), "eye"),
    ("pride-prejudice", "Orgueil et\nPréjugés", "Jane Austen", ("#2e3b32", "#d8b56b", "#f4e8ce"), "garden"),
    ("crime-punishment", "Crime et\nChâtiment", "Fiodor Dostoïevski", ("#2a1717", "#7d1d1d", "#c7a46b"), "city"),
    ("name-rose", "Le Nom de\nla Rose", "Umberto Eco", ("#172019", "#72592b", "#d7c593"), "abbey"),
    ("kafka-shore", "Kafka sur\nle rivage", "Haruki Murakami", ("#0d1f30", "#426c84", "#f1d78f"), "shore"),
    ("dune", "Dune", "Frank Herbert", ("#6d351a", "#cc7a32", "#e7bc72"), "dunes"),
    ("sapiens", "Sapiens", "Yuval Noah Harari", ("#f7f0da", "#6f7155", "#181919"), "evolution"),
    ("atomic-habits", "Atomic\nHabits", "James Clear", ("#f5f5f2", "#d84225", "#171717"), "atoms"),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            pass
    return ImageFont.load_default()


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))


def blend(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient(colors: tuple[str, str, str]) -> Image.Image:
    c1, c2, c3 = [hex_to_rgb(c) for c in colors]
    img = Image.new("RGB", SIZE)
    draw = ImageDraw.Draw(img)
    for y in range(SIZE[1]):
        t = y / (SIZE[1] - 1)
        if t < 0.56:
            c = blend(c1, c2, t / 0.56)
        else:
            c = blend(c2, c3, (t - 0.56) / 0.44)
        draw.line([(0, y), (SIZE[0], y)], fill=c)
    return img


def add_noise(img: Image.Image, amount: int = 18) -> None:
    random.seed(14)
    px = img.load()
    for _ in range(26000):
        x = random.randrange(SIZE[0])
        y = random.randrange(SIZE[1])
        value = px[x, y]
        r, g, b = value[:3]
        alpha = value[3] if len(value) == 4 else None
        delta = random.randrange(-amount, amount + 1)
        noisy = (max(0, min(255, r + delta)), max(0, min(255, g + delta)), max(0, min(255, b + delta)))
        px[x, y] = noisy + ((alpha,) if alpha is not None else ())


def glow(draw: ImageDraw.ImageDraw, xy: tuple[int, int], radius: int, color: tuple[int, int, int, int]) -> None:
    overlay = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    x, y = xy
    for step in range(9, 0, -1):
        alpha = int(color[3] * (step / 9) ** 2 * 0.22)
        r = int(radius * step / 4)
        od.ellipse((x - r, y - r, x + r, y + r), fill=color[:3] + (alpha,))
    base = draw.im
    base.paste(Image.alpha_composite(Image.new("RGBA", SIZE, (0, 0, 0, 0)), overlay).im)


def draw_theme(img: Image.Image, theme: str, colors: tuple[str, str, str]) -> None:
    draw = ImageDraw.Draw(img, "RGBA")
    w, h = SIZE

    if theme == "planet":
        for _ in range(120):
            x, y = random.randrange(w), random.randrange(60, h - 280)
            a = random.randrange(90, 220)
            draw.ellipse((x, y, x + 2, y + 2), fill=(255, 255, 230, a))
        draw.ellipse((238, 550, 675, 987), fill=(15, 83, 102, 255), outline=(111, 212, 224, 180), width=6)
        draw.arc((145, 260, 775, 650), 8, 178, fill=(245, 226, 154, 210), width=9)
        draw.ellipse((616, 285, 644, 313), fill=(255, 232, 160, 255))
        draw.line((500, 458, 500, 534), fill=(238, 175, 82, 255), width=9)
        draw.ellipse((489, 435, 514, 462), fill=(235, 176, 95, 255))
        draw.ellipse((390, 703, 426, 741), fill=(208, 45, 45, 255))
    elif theme == "sun":
        for r, alpha in [(390, 70), (290, 90), (200, 140)]:
            draw.ellipse((w // 2 - r, 120 - r, w // 2 + r, 120 + r), fill=(255, 239, 190, alpha))
        draw.ellipse((282, 188, 716, 622), fill=(255, 229, 171, 220))
        draw.ellipse((462, 256, 520, 318), fill=(18, 22, 23, 255))
        draw.rounded_rectangle((394, 312, 625, 980), radius=105, fill=(18, 22, 23, 255))
        draw.polygon([(0, 890), (285, 784), (530, 858), (900, 706), (900, 1200), (0, 1200)], fill=(25, 30, 28, 230))
    elif theme == "street":
        draw.rectangle((0, 495, w, h), fill=(27, 29, 29, 205))
        draw.polygon([(105, 500), (342, 340), (315, 970), (70, 1030)], fill=(26, 28, 29, 190))
        draw.polygon([(780, 470), (558, 350), (585, 970), (830, 1040)], fill=(26, 28, 29, 190))
        draw.polygon([(380, 402), (520, 360), (622, 390), (498, 438)], fill=(196, 28, 32, 235))
        draw.polygon([(520, 360), (612, 340), (703, 365), (622, 390)], fill=(246, 242, 232, 235))
        draw.polygon([(612, 340), (702, 315), (792, 338), (703, 365)], fill=(35, 68, 122, 235))
        for x in [185, 714]:
            draw.ellipse((x - 16, 520, x + 16, 552), fill=(240, 186, 92, 190))
            draw.rectangle((x - 5, 552, x + 5, 768), fill=(31, 25, 20, 210))
    elif theme in {"desert", "dunes"}:
        for y in range(680, h, 38):
            draw.arc((-180, y - 160, w + 180, y + 120), 185, 355, fill=(255, 226, 151, 110), width=4)
        draw.ellipse((598, 150, 690, 242), fill=(239, 202, 113, 210))
        draw.line((438, 598, 470, 760), fill=(46, 42, 38, 255), width=8)
        draw.ellipse((424, 556, 466, 600), fill=(46, 42, 38, 255))
        draw.polygon([(0, 875), (250, 760), (500, 830), (900, 700), (900, 1200), (0, 1200)], fill=(140, 79, 33, 130))
    elif theme == "eye":
        draw.rectangle((0, 0, w, h), fill=(20, 20, 20, 95))
        draw.polygon([(124, 560), (450, 350), (776, 560), (450, 765)], outline=(230, 224, 210, 230), width=8)
        draw.ellipse((318, 430, 582, 690), fill=(154, 31, 25, 210), outline=(238, 226, 204, 200), width=5)
        draw.ellipse((400, 512, 500, 612), fill=(20, 20, 20, 255))
        for y in range(0, h, 70):
            draw.line((0, y, w, y + 180), fill=(255, 255, 255, 12), width=2)
    elif theme == "garden":
        for x in range(90, 820, 90):
            draw.line((x, 400, x - 60, 950), fill=(215, 184, 111, 95), width=4)
        for _ in range(90):
            x, y = random.randrange(80, 820), random.randrange(440, 920)
            draw.ellipse((x, y, x + 16, y + 16), fill=(238, 222, 180, random.randrange(90, 170)))
        draw.arc((200, 250, 700, 900), 200, 340, fill=(242, 228, 198, 190), width=8)
    elif theme == "city":
        draw.rectangle((0, 525, w, h), fill=(34, 23, 23, 210))
        for x in range(80, 820, 120):
            draw.rectangle((x, random.randrange(400, 520), x + 80, 1060), fill=(55, 34, 32, 210))
            for y in range(560, 980, 100):
                draw.rectangle((x + 18, y, x + 40, y + 36), fill=(199, 160, 97, 95))
        draw.ellipse((585, 180, 750, 345), fill=(199, 164, 102, 115))
        draw.line((210, 650, 690, 450), fill=(125, 32, 30, 180), width=9)
    elif theme == "abbey":
        draw.rectangle((0, 515, w, h), fill=(31, 38, 31, 220))
        for x in [170, 360, 550]:
            draw.rounded_rectangle((x, 375, x + 140, 940), radius=68, outline=(213, 196, 144, 150), width=8)
        draw.polygon([(450, 190), (685, 510), (215, 510)], fill=(117, 89, 43, 170))
        draw.ellipse((410, 660, 490, 740), fill=(177, 24, 35, 200))
    elif theme == "shore":
        draw.rectangle((0, 720, w, h), fill=(10, 39, 56, 160))
        for y in range(720, 1040, 44):
            draw.arc((-160, y - 80, w + 160, y + 120), 0, 180, fill=(234, 213, 143, 115), width=3)
        draw.ellipse((620, 170, 725, 275), fill=(242, 215, 140, 200))
        draw.line((350, 510, 350, 710), fill=(20, 24, 28, 255), width=10)
        draw.ellipse((326, 456, 374, 504), fill=(20, 24, 28, 255))
    elif theme == "evolution":
        draw.rectangle((0, 0, w, h), fill=(247, 240, 218, 235))
        for i, x in enumerate(range(120, 760, 95)):
            height = 70 + i * 26
            y = 720 - i * 18
            draw.ellipse((x, y - height, x + 32, y - height + 32), fill=(50, 54, 44, 145))
            draw.line((x + 16, y - height + 32, x + 16, y), fill=(50, 54, 44, 145), width=8)
            draw.line((x + 16, y - 6, x - 10, y + 60), fill=(50, 54, 44, 130), width=7)
            draw.line((x + 16, y - 6, x + 48, y + 58), fill=(50, 54, 44, 130), width=7)
    elif theme == "atoms":
        draw.rectangle((0, 0, 140, h), fill=(19, 19, 19, 255))
        for angle in [0, 58, -58]:
            cx, cy = 505, 510
            bbox = (cx - 210, cy - 70, cx + 210, cy + 70)
            layer = Image.new("RGBA", SIZE, (0, 0, 0, 0))
            ld = ImageDraw.Draw(layer)
            ld.arc(bbox, 0, 360, fill=(216, 66, 37, 200), width=6)
            layer = layer.rotate(angle, center=(cx, cy), resample=Image.Resampling.BICUBIC)
            img.alpha_composite(layer)
        draw.ellipse((486, 492, 524, 530), fill=(216, 66, 37, 255))


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font_obj: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for raw_line in text.split("\n"):
        words = raw_line.split()
        line = ""
        for word in words:
            test = f"{line} {word}".strip()
            if draw.textbbox((0, 0), test, font=font_obj)[2] <= max_width:
                line = test
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def add_cover_text(img: Image.Image, title: str, author: str, slug: str) -> None:
    draw = ImageDraw.Draw(img, "RGBA")
    title_font = font(78 if len(title) < 14 else 62, True)
    author_font = font(32, False)
    small_font = font(19, True)
    max_width = 720
    lines = wrap_text(draw, title, title_font, max_width)
    y = 112
    draw.text((90, 62), "SMART LIBRARY", font=small_font, fill=(255, 255, 255, 185))
    for line in lines:
        draw.text((90, y), line, font=title_font, fill=(255, 255, 255, 245))
        y += title_font.size + 4
    fill = (255, 255, 255, 210) if slug not in {"sapiens", "atomic-habits"} else (24, 25, 25, 220)
    draw.text((92, 990), author, font=author_font, fill=fill)
    draw.line((90, 950, 810, 950), fill=(255, 255, 255, 90), width=2)


def make_cover(slug: str, title: str, author: str, colors: tuple[str, str, str], theme: str) -> None:
    img = gradient(colors).convert("RGBA")
    add_noise(img, 10)
    draw_theme(img, theme, colors)
    vignette = Image.new("L", SIZE, 0)
    vd = ImageDraw.Draw(vignette)
    vd.ellipse((-240, -180, SIZE[0] + 240, SIZE[1] + 170), fill=255)
    vignette = vignette.filter(ImageFilter.GaussianBlur(120))
    dark = Image.new("RGBA", SIZE, (0, 0, 0, 120))
    img = Image.composite(img, Image.alpha_composite(img, dark), vignette)
    add_cover_text(img, title, author, slug)
    img = img.convert("RGB")
    img.save(OUT / f"{slug}.png", quality=94)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for args in BOOKS:
        make_cover(*args)
    print(f"Generated {len(BOOKS)} covers in {OUT}")


if __name__ == "__main__":
    main()
