"""Generate a cohesive sprite set for Summon Rhythm Box."""
from PIL import Image, ImageDraw, ImageFilter
import os

os.makedirs("images", exist_ok=True)
SIZE = 192

CHARS = [
    {"id": "raddy", "aliases": ["raddy"], "body": (228, 64, 78), "dark": (140, 18, 42), "accent": (255, 214, 96), "type": "horns"},
    {"id": "garnold", "aliases": ["garnold"], "body": (255, 183, 53), "dark": (180, 122, 14), "accent": (0, 210, 230), "type": "visor"},
    {"id": "black", "aliases": ["black"], "body": (44, 45, 58), "dark": (8, 8, 14), "accent": (255, 255, 255), "type": "hat"},
    {"id": "gray", "aliases": ["gray"], "body": (172, 177, 191), "dark": (98, 104, 122), "accent": (245, 246, 250), "type": "cat"},
    {"id": "funbot", "aliases": ["funbot", "fun-bot"], "body": (176, 191, 202), "dark": (104, 123, 139), "accent": (255, 213, 88), "type": "robot"},
    {"id": "sky", "aliases": ["sky"], "body": (113, 213, 255), "dark": (35, 124, 196), "accent": (235, 244, 255), "type": "bear"},
    {"id": "oren", "aliases": ["oren"], "body": (255, 163, 55), "dark": (196, 84, 18), "accent": (255, 242, 192), "type": "antenna"},
    {"id": "mrsun", "aliases": ["mrsun", "mr-sun"], "body": (255, 209, 64), "dark": (216, 136, 18), "accent": (255, 244, 187), "type": "sun"},
    {"id": "mrtree", "aliases": ["mrtree", "mr-tree"], "body": (126, 94, 72), "dark": (74, 50, 36), "accent": (103, 198, 105), "type": "tree"},
    {"id": "jevin", "aliases": ["jevin"], "body": (48, 88, 182), "dark": (14, 28, 78), "accent": (193, 215, 255), "type": "hood"},
    {"id": "pinki", "aliases": ["pinki"], "body": (247, 148, 188), "dark": (192, 44, 111), "accent": (255, 233, 244), "type": "bunny"},
]


def rounded_box(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def add_glow(canvas, center, radius, color, alpha=70):
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    x, y = center
    for step in range(6, 0, -1):
        r = radius * step / 6
        a = int(alpha * (step / 6) ** 2)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(*color, a))
    return Image.alpha_composite(canvas, overlay)


def draw_body(draw, char):
    cx, cy = SIZE // 2, SIZE // 2 + 10
    w, h = 92, 112
    rounded_box(draw, [cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2], 34, char["body"], char["dark"], 5)
    rounded_box(draw, [cx - 28, cy + 16, cx + 28, cy + 44], 18, tuple(min(255, c + 18) for c in char["body"]))
    for side in (-1, 1):
        ax = cx + side * 56
        draw.ellipse([ax - 18, cy - 22, ax + 18, cy + 10], fill=char["body"], outline=char["dark"], width=4)
    return cx, cy


def draw_face(draw, cx, cy, char):
    eye_y = cy - 18
    for side in (-1, 1):
        ex = cx + side * 18
        draw.ellipse([ex - 12, eye_y - 12, ex + 12, eye_y + 12], fill=(255, 255, 255), outline=char["dark"], width=2)
        draw.ellipse([ex - 5, eye_y - 4, ex + 5, eye_y + 8], fill=char["dark"])
    draw.arc([cx - 18, cy + 6, cx + 18, cy + 28], 15, 165, fill=char["dark"], width=4)
    draw.ellipse([cx - 32, cy - 40, cx + 32, cy - 10], fill=(255, 255, 255, 55))


def draw_type_details(draw, cx, cy, char):
    t = char["type"]
    accent = char["accent"]
    dark = char["dark"]
    if t == "horns":
        for dx in (-26, -10, 10, 26):
            draw.polygon([(cx + dx - 6, cy - 55), (cx + dx + 6, cy - 55), (cx + dx, cy - 82)], fill=accent, outline=dark)
    elif t == "visor":
        rounded_box(draw, [cx - 34, cy - 28, cx + 34, cy - 2], 12, (26, 34, 52), accent, 4)
    elif t == "hat":
        rounded_box(draw, [cx - 28, cy - 74, cx + 28, cy - 32], 8, dark)
        draw.rectangle([cx - 44, cy - 38, cx + 44, cy - 30], fill=dark)
        draw.polygon([(cx - 8, cy + 10), (cx + 8, cy + 10), (cx, cy + 42)], fill=accent)
    elif t == "cat":
        draw.polygon([(cx - 42, cy - 36), (cx - 18, cy - 78), (cx - 8, cy - 28)], fill=char["body"], outline=dark)
        draw.polygon([(cx + 42, cy - 36), (cx + 18, cy - 78), (cx + 8, cy - 28)], fill=char["body"], outline=dark)
    elif t == "robot":
        rounded_box(draw, [cx - 30, cy - 40, cx + 30, cy + 2], 14, (86, 98, 112), accent, 4)
        for side in (-1, 1):
            draw.line([(cx + side * 16, cy - 58), (cx + side * 20, cy - 42)], fill=dark, width=4)
            draw.ellipse([cx + side * 16 - 5, cy - 66, cx + side * 16 + 5, cy - 56], fill=accent)
    elif t == "bear":
        for side in (-1, 1):
            draw.ellipse([cx + side * 22 - 14, cy - 72, cx + side * 22 + 14, cy - 42], fill=char["body"], outline=dark, width=4)
            draw.ellipse([cx + side * 22 - 7, cy - 65, cx + side * 22 + 7, cy - 49], fill=accent)
    elif t == "antenna":
        for side in (-1, 1):
            draw.line([(cx + side * 12, cy - 58), (cx + side * 18, cy - 82)], fill=dark, width=4)
            draw.ellipse([cx + side * 18 - 6, cy - 88, cx + side * 18 + 6, cy - 76], fill=accent)
        rounded_box(draw, [cx - 36, cy - 6, cx + 36, cy + 14], 10, (38, 48, 64), accent, 4)
    elif t == "sun":
        for angle in range(0, 360, 30):
            import math
            rad = math.radians(angle)
            x1 = cx + math.cos(rad) * 44
            y1 = cy - 18 + math.sin(rad) * 44
            x2 = cx + math.cos(rad) * 66
            y2 = cy - 18 + math.sin(rad) * 66
            draw.line([(x1, y1), (x2, y2)], fill=accent, width=5)
    elif t == "tree":
        draw.ellipse([cx - 52, cy - 80, cx + 52, cy - 2], fill=accent, outline=(52, 120, 56), width=4)
        draw.rectangle([cx - 10, cy - 18, cx + 10, cy + 42], fill=(106, 75, 51))
    elif t == "hood":
        draw.pieslice([cx - 54, cy - 58, cx + 54, cy + 42], 180, 360, fill=dark)
        draw.rectangle([cx - 38, cy - 12, cx + 38, cy + 50], fill=dark)
    elif t == "bunny":
        for side in (-1, 1):
            draw.rounded_rectangle([cx + side * 16 - 10, cy - 96, cx + side * 16 + 10, cy - 36], radius=10, fill=accent, outline=dark, width=4)


def draw_sprite(char):
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    img = add_glow(img, (SIZE // 2, SIZE // 2 + 8), 76, char["accent"], 52)
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([38, 142, 154, 172], fill=(0, 0, 0, 70))
    img = Image.alpha_composite(img, shadow.filter(ImageFilter.GaussianBlur(6)))

    draw = ImageDraw.Draw(img)
    cx, cy = draw_body(draw, char)
    draw_type_details(draw, cx, cy, char)
    draw_face(draw, cx, cy, char)
    draw.ellipse([cx - 20, cy + 54, cx - 4, cy + 78], fill=char["dark"])
    draw.ellipse([cx + 4, cy + 54, cx + 20, cy + 78], fill=char["dark"])
    draw.rounded_rectangle([cx - 12, cy - 6, cx + 12, cy + 16], radius=8, fill=(255, 255, 255, 34))
    return img


def draw_doghead():
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    img = add_glow(img, (SIZE // 2, SIZE // 2 + 12), 70, (255, 196, 116), 42)
    draw = ImageDraw.Draw(img)
    draw.ellipse([42, 48, 150, 144], fill=(150, 102, 60), outline=(96, 61, 32), width=5)
    draw.ellipse([42, 38, 80, 94], fill=(150, 102, 60), outline=(96, 61, 32), width=4)
    draw.ellipse([112, 38, 150, 94], fill=(150, 102, 60), outline=(96, 61, 32), width=4)
    for side in (-1, 1):
        ex = SIZE // 2 + side * 24
        draw.ellipse([ex - 9, 84, ex + 9, 102], fill=(35, 24, 18))
        draw.ellipse([ex - 3, 87, ex + 1, 94], fill=(255, 255, 255))
    draw.ellipse([84, 102, 108, 122], fill=(56, 34, 25))
    draw.arc([72, 110, 96, 134], 180, 360, fill=(56, 34, 25), width=3)
    draw.arc([96, 110, 120, 134], 180, 360, fill=(56, 34, 25), width=3)
    for x in (56, 74, 92, 110, 128):
        draw.line([(x, 34), (x, 144)], fill=(112, 112, 122, 210), width=4)
    return img


for char in CHARS:
    sprite = draw_sprite(char)
    for alias in char["aliases"]:
        sprite.save(f"images/{alias}.png")
        print(f"Created images/{alias}.png")

dog = draw_doghead()
dog.save("images/doghead.png")
print("Created images/doghead.png")
print("Done.")
