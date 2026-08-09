"""Generate richer scene background images for Summon Rhythm Box."""
from PIL import Image, ImageDraw, ImageFilter
import argparse
import math
import os
import random

os.makedirs("images", exist_ok=True)
W, H = 1200, 900


def vertical_gradient(top, bottom):
    img = Image.new("RGB", (W, H), top)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        color = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        draw.line([(0, y), (W, y)], fill=color)
    return img


def add_glow(base, center, radius, color, alpha):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    x, y = center
    for step in range(7, 0, -1):
        r = radius * step / 7
        a = int(alpha * (step / 7) ** 2)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(*color, a))
    return Image.alpha_composite(base.convert("RGBA"), overlay)


def add_film_grain(img, rng, amount=10):
    px = img.load()
    for y in range(H):
        for x in range(W):
            n = rng.randint(-amount, amount)
            r, g, b = px[x, y]
            px[x, y] = tuple(max(0, min(255, c + n)) for c in (r, g, b))
    return img


def make_space():
    img = vertical_gradient((8, 8, 27), (22, 21, 69)).convert("RGBA")
    rng = random.Random(42)

    for center, radius, color, alpha in [
        ((260, 250), 320, (120, 85, 255), 62),
        ((1250, 210), 280, (255, 90, 166), 58),
        ((820, 860), 360, (27, 168, 255), 44),
    ]:
        img = add_glow(img, center, radius, color, alpha)

    draw = ImageDraw.Draw(img)
    # Distant ribbon nebulae give the world a clear depth direction.
    for offset, color in [(0, (122, 98, 255, 72)), (88, (76, 193, 255, 48)), (184, (255, 114, 184, 40))]:
        points = []
        for x in range(-80, W + 100, 40):
            y = 710 + offset + math.sin(x * 0.006 + offset) * 70
            points.append((x, y))
        draw.line(points, fill=color, width=34)
    for _ in range(900):
        x, y = rng.randint(0, W - 1), rng.randint(0, H - 1)
        r = rng.choice([1, 1, 1, 2, 2, 3])
        c = rng.choice([(255, 255, 255), (194, 220, 255), (255, 224, 190), (255, 182, 224)])
        draw.ellipse([x - r, y - r, x + r, y + r], fill=c + (255,))
        if r >= 2:
            draw.line([(x - r * 2, y), (x + r * 2, y)], fill=c + (150,), width=1)
            draw.line([(x, y - r * 2), (x, y + r * 2)], fill=c + (150,), width=1)

    # Ringed planet and a small moon form a recognisable landmark.
    draw.ellipse([1060, 130, 1280, 350], fill=(42, 65, 146, 255))
    draw.ellipse([1088, 158, 1252, 322], fill=(114, 152, 255, 255))
    draw.ellipse([1120, 175, 1195, 250], fill=(144, 176, 255, 100))
    draw.arc([1000, 170, 1340, 380], 20, 330, fill=(255, 211, 136, 220), width=8)
    draw.ellipse([280, 760, 354, 834], fill=(230, 191, 141, 255))
    draw.ellipse([301, 775, 327, 801], fill=(176, 139, 104, 255))
    for x in range(70, W, 180):
        y = 105 + int(math.sin(x * .013) * 24)
        draw.line([(x, y), (x + 70, y + 22)], fill=(222, 244, 255, 160), width=2)
        draw.line([(x + 40, y - 10), (x + 110, y + 12)], fill=(222, 244, 255, 55), width=1)

    img = img.convert("RGB")
    img.save("images/bg-space-v2.png", quality=92)
    print("Created images/bg-space-v2.png")


def make_ocean():
    img = vertical_gradient((8, 25, 52), (3, 85, 108)).convert("RGBA")
    rng = random.Random(99)

    for center, radius, color, alpha in [
        ((280, -60), 460, (119, 238, 255), 70),
        ((1200, 90), 340, (94, 182, 255), 48),
        ((1360, 700), 380, (28, 126, 164), 42),
    ]:
        img = add_glow(img, center, radius, color, alpha)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for x in [150, 420, 680, 970, 1250]:
        od.polygon([(x - 140, 0), (x - 35, 0), (x + 160, H), (x - 40, H)], fill=(155, 230, 255, 24))
    img = Image.alpha_composite(img, overlay.filter(ImageFilter.GaussianBlur(14)))

    draw = ImageDraw.Draw(img)
    floor_y = H - 165
    for y in range(floor_y, H):
        t = (y - floor_y) / (H - floor_y)
        draw.line([(0, y), (W, y)], fill=(12, int(88 + 30 * t), int(74 + 20 * t), 255))

    for i in range(18):
        base_x = 50 + i * 92 + rng.randint(-15, 15)
        height = rng.randint(180, 360)
        width = rng.randint(16, 28)
        points = []
        for step in range(8):
            t = step / 7
            sway = math.sin(t * math.pi * 1.4 + i) * 30
            points.append((base_x + sway, floor_y - height * t))
        draw.line(points, fill=(34, 132, 112, 220), width=width)
        draw.line(points, fill=(83, 214, 162, 70), width=max(1, width // 4))

    for _ in range(14):
        fx = rng.randint(80, W - 120)
        fy = rng.randint(240, floor_y - 120)
        size = rng.randint(34, 78)
        body = rng.choice([(255, 170, 92), (115, 195, 255), (255, 214, 103), (255, 118, 146)])
        draw.ellipse([fx - size, fy - size * 0.48, fx + size, fy + size * 0.48], fill=body + (220,))
        tail = [(fx + size * 0.55, fy), (fx + size * 1.15, fy - size * 0.45), (fx + size * 1.05, fy + size * 0.45)]
        draw.polygon(tail, fill=body + (220,))
        draw.ellipse([fx - size * 0.55, fy - size * 0.12, fx - size * 0.4, fy + size * 0.03], fill=(255, 255, 255, 240))

    for _ in range(95):
        x, y = rng.randint(0, W), rng.randint(100, floor_y)
        r = rng.randint(5, 16)
        draw.ellipse([x - r, y - r, x + r, y + r], outline=(198, 241, 255, 160), width=2)
        draw.ellipse([x - r * 0.35, y - r * 0.5, x, y - r * 0.1], fill=(245, 255, 255, 180))

    img = img.convert("RGB")
    img.save("images/bg-ocean.png", quality=95)
    print("Created images/bg-ocean.png")


def make_forest():
    img = vertical_gradient((13, 39, 34), (55, 105, 54)).convert("RGBA")
    rng = random.Random(77)
    draw = ImageDraw.Draw(img)

    for _ in range(40):
        x = rng.randint(0, W)
        y = rng.randint(H - 240, H)
        r = rng.randint(80, 190)
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.ellipse([x - r, y - r * 0.48, x + r, y + r * 0.48], fill=(215, 231, 188, 11))
        img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)
    # A far tree line starts the parallax-like depth stack.
    for x in range(-40, W + 80, 70):
        h = rng.randint(180, 320)
        draw.rectangle([x + 25, H - h, x + 43, H], fill=(30, 69, 44, 230))
        draw.polygon([(x - 15, H - h + 60), (x + 34, H - h - 80), (x + 86, H - h + 60)], fill=(37, 91, 51, 230))
    for _ in range(16):
        tx = rng.randint(70, W - 70)
        th = 410 + rng.randint(0, 260)
        tw = 34 + rng.randint(0, 42)
        draw.rounded_rectangle([tx - tw // 2, H - th, tx + tw // 2, H], radius=10, fill=(66, 44, 24, 255))
        draw.line([(tx, H - th + 80), (tx - tw * 3, H - th + 20)], fill=(66, 44, 24, 255), width=10)
        draw.line([(tx, H - th + 125), (tx + tw * 3, H - th + 60)], fill=(66, 44, 24, 255), width=9)
        for layer in range(3):
            fr = tw * 3 + rng.randint(28, 80) - layer * 14
            fy = H - th + 45 + layer * 62
            draw.ellipse([tx - fr, fy - fr * 0.62, tx + fr, fy + fr * 0.62], fill=(45 + layer * 12, 102 + layer * 23, 55, 255))

    for _ in range(115):
        x, y = rng.randint(0, W), rng.randint(70, H - 100)
        r = rng.randint(2, 5)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 229, 116, 220))
    for _ in range(55):
        x, y = rng.randint(0, W), rng.randint(H - 260, H - 45)
        draw.line([(x, y), (x + rng.randint(-10, 10), y - rng.randint(12, 34))], fill=(129, 191, 92, 170), width=2)
        draw.ellipse([x - 4, y - 30, x + 4, y - 22], fill=rng.choice([(255, 173, 198, 220), (167, 214, 255, 220), (255, 230, 130, 220)]))
    mist = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    md = ImageDraw.Draw(mist)
    for _ in range(14):
        x, y = rng.randint(-100, W), rng.randint(H - 230, H - 40)
        md.ellipse([x - 180, y - 36, x + 180, y + 36], fill=(191, 238, 198, 22))
    img = Image.alpha_composite(img, mist.filter(ImageFilter.GaussianBlur(18)))

    img = img.convert("RGB")
    img.save("images/bg-forest-v2.png", quality=92)
    print("Created images/bg-forest-v2.png")


def make_cyber():
    img = vertical_gradient((10, 11, 28), (23, 17, 56)).convert("RGBA")
    rng = random.Random(33)

    for center, radius, color, alpha in [
        ((240, 240), 300, (0, 208, 255), 58),
        ((1120, 280), 300, (177, 85, 255), 64),
        ((1330, 760), 260, (255, 88, 160), 44),
    ]:
        img = add_glow(img, center, radius, color, alpha)

    draw = ImageDraw.Draw(img)
    horizon = H - 300
    for x in range(-80, W + 80, 40):
        sx = W / 2 + (x - W / 2) * 0.18
        draw.line([(sx, horizon), (x, H)], fill=(0, 229, 255, 70), width=2)
    for i in range(13):
        y = horizon + i * 26
        draw.line([(0, y), (W, y)], fill=(0, 229, 255, max(18, 90 - i * 6)), width=2)

    for _ in range(8):
        cx, cy = rng.randint(120, W - 120), rng.randint(120, horizon - 40)
        w = rng.randint(80, 180)
        h = rng.randint(140, 320)
        body = rng.choice([(20, 184, 255), (255, 95, 164), (170, 88, 255)])
        draw.rounded_rectangle([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2], radius=16, outline=body + (200,), width=4)
        draw.line([(cx - w // 2, cy), (cx + w // 2, cy)], fill=body + (90,), width=2)
        draw.line([(cx, cy - h // 2), (cx, cy + h // 2)], fill=body + (90,), width=2)

    for _ in range(180):
        x = rng.randint(0, W - 20)
        y = rng.randint(0, H - 1)
        length = rng.randint(14, 60)
        color = rng.choice([(0, 229, 255, 70), (154, 98, 255, 55), (255, 88, 160, 45)])
        draw.line([(x, y), (x + length, y)], fill=color, width=1)

    img = img.filter(ImageFilter.GaussianBlur(0.35)).convert("RGB")
    img.save("images/bg-cyber.png", quality=95)
    print("Created images/bg-cyber.png")


def make_candy():
    img = vertical_gradient((65, 28, 76), (136, 74, 128)).convert("RGBA")
    rng = random.Random(55)

    for center, radius, color, alpha in [
        ((240, 180), 320, (255, 178, 215), 66),
        ((1180, 240), 280, (146, 208, 255), 50),
        ((910, 840), 320, (255, 211, 124), 44),
    ]:
        img = add_glow(img, center, radius, color, alpha)

    draw = ImageDraw.Draw(img)
    stripe_colors = [(255, 173, 206, 42), (255, 217, 142, 36), (169, 228, 255, 34), (222, 179, 255, 34)]
    for i in range(9):
        y0 = i * H // 9
        y1 = (i + 1) * H // 9
        draw.rectangle([0, y0, W, y1], fill=stripe_colors[i % len(stripe_colors)])

    for _ in range(12):
        lx = rng.randint(90, W - 90)
        ly = rng.randint(180, H - 220)
        r = rng.randint(48, 92)
        stick_h = rng.randint(120, 220)
        base = rng.choice([(255, 126, 180), (255, 208, 112), (121, 218, 255), (193, 132, 255)])
        draw.rounded_rectangle([lx - 7, ly + r * 0.75, lx + 7, ly + r * 0.75 + stick_h], radius=7, fill=(237, 237, 245, 220))
        draw.ellipse([lx - r, ly - r, lx + r, ly + r], fill=base + (235,))
        draw.ellipse([lx - r + 10, ly - r + 10, lx + r - 10, ly + r - 10], outline=(255, 255, 255, 185), width=6)
        for angle in range(0, 360, 25):
            rad = math.radians(angle)
            x1 = lx + math.cos(rad) * r * 0.18
            y1 = ly + math.sin(rad) * r * 0.18
            x2 = lx + math.cos(rad + 0.75) * r * 0.78
            y2 = ly + math.sin(rad + 0.75) * r * 0.78
            draw.line([(x1, y1), (x2, y2)], fill=(255, 255, 255, 145), width=4)

    for _ in range(260):
        x, y = rng.randint(0, W), rng.randint(0, H)
        r = rng.choice([1, 1, 2, 2, 3])
        c = rng.choice([(255, 255, 255), (255, 228, 130), (255, 180, 221), (173, 228, 255)])
        draw.ellipse([x - r, y - r, x + r, y + r], fill=c + (255,))

    img = img.convert("RGB")
    img.save("images/bg-candy.png", quality=95)
    print("Created images/bg-candy.png")


SCENE_GENERATORS = {
    "space": make_space,
    "ocean": make_ocean,
    "forest": make_forest,
    "cyber": make_cyber,
    "candy": make_candy,
}


def main():
    parser = argparse.ArgumentParser(description="Generate one or all game backgrounds.")
    parser.add_argument(
        "scene",
        nargs="?",
        choices=[*SCENE_GENERATORS, "all"],
        default="all",
        help="Scene to generate. Defaults to all.",
    )
    args = parser.parse_args()
    selected = SCENE_GENERATORS.items() if args.scene == "all" else [(args.scene, SCENE_GENERATORS[args.scene])]
    for name, generator in selected:
        print(f"Generating {name} background...")
        generator()
    print("Done.")


if __name__ == "__main__":
    main()
