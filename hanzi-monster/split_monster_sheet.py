from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
SHEET = ROOT / "images" / "hanzi-monster" / "_sheet.png"
OUT_DIR = ROOT / "images" / "hanzi-monster" / "classic"

NAMES = [
    "momo", "doudou", "tuantuan", "yaya", "huohuo", "nuannuan",
    "qiqiu", "mifen", "keke", "lulu", "tangtang", "xingxing",
    "shanbao", "shuizai", "fengfeng", "yunbao", "huahua", "guoguo",
]

COLS = 6
ROWS = 3
TARGET = 256


def avg_rgb(points: Iterable[tuple[int, int, int]]) -> tuple[int, int, int]:
    items = list(points)
    n = max(1, len(items))
    return (
        round(sum(v[0] for v in items) / n),
        round(sum(v[1] for v in items) / n),
        round(sum(v[2] for v in items) / n),
    )


def sample_bg(img: Image.Image) -> tuple[int, int, int]:
    w, h = img.size
    pts = [
        img.getpixel((5, 5))[:3],
        img.getpixel((w - 6, 5))[:3],
        img.getpixel((5, h - 6))[:3],
        img.getpixel((w - 6, h - 6))[:3],
    ]
    return avg_rgb(pts)


def diff(px: tuple[int, int, int], bg: tuple[int, int, int]) -> int:
    return abs(px[0] - bg[0]) + abs(px[1] - bg[1]) + abs(px[2] - bg[2])


def bbox_for_cell(cell: Image.Image, bg: tuple[int, int, int]) -> tuple[int, int, int, int]:
    w, h = cell.size
    minx, miny, maxx, maxy = w, h, -1, -1
    for y in range(h):
      for x in range(w):
        if diff(cell.getpixel((x, y))[:3], bg) > 60:
            if x < minx:
                minx = x
            if y < miny:
                miny = y
            if x > maxx:
                maxx = x
            if y > maxy:
                maxy = y
    if maxx < minx or maxy < miny:
        return (0, 0, w, h)
    return (max(minx - 6, 0), max(miny - 6, 0), min(maxx + 7, w), min(maxy + 7, h))


def remove_bg(img: Image.Image, bg: tuple[int, int, int]) -> Image.Image:
    out = img.convert("RGBA")
    pixels = out.load()
    w, h = out.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            d = diff((r, g, b), bg)
            if d < 35:
                pixels[x, y] = (r, g, b, 0)
            elif d < 80:
                alpha = round((d - 35) / 45 * 255)
                pixels[x, y] = (r, g, b, alpha)
            else:
                pixels[x, y] = (r, g, b, a)
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img = Image.open(SHEET).convert("RGBA")
    bg = sample_bg(img)
    w, h = img.size
    cell_w = w / COLS
    cell_h = h / ROWS

    for idx, name in enumerate(NAMES):
        col = idx % COLS
        row = idx // COLS
        x0 = round(col * cell_w)
        y0 = round(row * cell_h)
        x1 = round((col + 1) * cell_w)
        y1 = round((row + 1) * cell_h)
        cell = img.crop((x0, y0, x1, y1))
        box = bbox_for_cell(cell, bg)
        crop = cell.crop(box)
        scale = min(TARGET / max(1, crop.width), TARGET / max(1, crop.height))
        new_size = (max(1, round(crop.width * scale)), max(1, round(crop.height * scale)))
        resized = crop.resize(new_size, Image.LANCZOS)
        canvas = Image.new("RGBA", (TARGET, TARGET), (0, 0, 0, 0))
        paste_xy = ((TARGET - new_size[0]) // 2, (TARGET - new_size[1]) // 2)
        canvas.paste(remove_bg(resized, bg), paste_xy, remove_bg(resized, bg))
        canvas.save(OUT_DIR / f"{name}.png")


if __name__ == "__main__":
    main()
