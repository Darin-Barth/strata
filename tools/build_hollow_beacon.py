"""Textures for the Hollow's progression items (docs/hollow-progression.md): the Pale Beacon (lit and
dormant block) and the six Pale Survey log pages. Blocks and items: kubejs/startup_scripts/hollow_beacon.js.

Usage: python tools/build_hollow_beacon.py     (from the repo root; needs Pillow, so not -I)
"""
import os
import random

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "kubejs", "assets", "strata", "textures")


def beacon(lit):
    rnd = random.Random(17)
    img = Image.new("RGBA", (16, 16))
    px = img.load()
    for y in range(16):
        for x in range(16):
            # weathered pale stone: resin-tinted grey with speckles
            v = 150 + rnd.randint(-14, 10)
            px[x, y] = (v, v + 2, v + 8, 255)
    # dark frame
    for i in range(16):
        for (x, y) in ((i, 0), (i, 15), (0, i), (15, i)):
            px[x, y] = (62, 64, 72, 255)
    for i in range(1, 15):
        for (x, y) in ((i, 1), (i, 14), (1, i), (14, i)):
            px[x, y] = (96, 98, 108, 255)
    # core: a soft diamond of light (or ash when dormant)
    cx, cy = 7.5, 7.5
    for y in range(3, 13):
        for x in range(3, 13):
            d = abs(x - cx) + abs(y - cy)
            if d > 5.2:
                continue
            t = 1 - d / 5.2
            if lit:
                px[x, y] = (int(180 + 75 * t), int(200 + 55 * t), int(215 + 40 * t), 255)
            else:
                g = int(70 + 40 * t)
                px[x, y] = (g, g, g + 6, 255)
    # four rivets
    for (x, y) in ((3, 3), (12, 3), (3, 12), (12, 12)):
        px[x, y] = (40, 42, 50, 255)
    return img


def page(n):
    rnd = random.Random(100 + n)
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    # a torn, yellowed sheet
    for y in range(1, 15):
        for x in range(3, 13):
            if (x in (3, 12) and rnd.random() < 0.3) or (y in (1, 14) and rnd.random() < 0.35):
                continue
            v = rnd.randint(-10, 8)
            px[x, y] = (214 + v, 204 + v, 172 + v, 255)
    # handwriting lines
    for y in range(3, 12, 2):
        for x in range(5, 11 if y < 11 else 8):
            if rnd.random() < 0.8:
                px[x, y] = (70, 64, 80, 255)
    # a stain, and the page number as tick marks along the bottom
    sx, sy = rnd.randint(5, 9), rnd.randint(4, 9)
    px[sx, sy] = (150, 120, 96, 255)
    for i in range(n):
        px[4 + i, 13] = (120, 40, 40, 255)
    return img


def main():
    os.makedirs(os.path.join(ASSETS, "block"), exist_ok=True)
    os.makedirs(os.path.join(ASSETS, "item"), exist_ok=True)
    beacon(True).save(os.path.join(ASSETS, "block", "pale_beacon.png"))
    beacon(False).save(os.path.join(ASSETS, "block", "pale_beacon_dormant.png"))
    for n in range(1, 7):
        page(n).save(os.path.join(ASSETS, "item", f"pale_survey_page_{n}.png"))
    print("Pale Beacon (2) and Pale Survey pages (6) written to kubejs/assets/strata/textures")


if __name__ == "__main__":
    main()
