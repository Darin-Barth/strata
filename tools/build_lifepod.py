"""Textures for the Abyssal Plain's Lifepod (docs/abyssal-plain-design.md): white and orange hull
panels, the hatch, portholes, deck grating, skids, lamps and the Return to Surface console.
Blocks: kubejs/startup_scripts/pokeworld_portal.js; the pod itself: kubejs/server_scripts/abyssal_rules.js.

Usage: python tools/build_lifepod.py     (from the repo root; needs Pillow, so not -I)
"""
import math
import os
import random

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "kubejs", "assets", "strata", "textures", "block")

WHITE = (226, 228, 230)
ORANGE = (226, 104, 34)
SEAM = (150, 154, 160)
DARK = (54, 58, 64)


def shade(c, d):
    return tuple(max(0, min(255, v + d)) for v in c) + (255,)


def panel(base, seed, stripe=None):
    """A hull panel: base colour with a little grain, seams on two edges (they tile into a grid),
    a bevel highlight, two rivets and an optional horizontal stripe."""
    rnd = random.Random(seed)
    img = Image.new("RGBA", (16, 16))
    px = img.load()
    for y in range(16):
        for x in range(16):
            c = base
            if stripe and stripe[0] <= y <= stripe[1]:
                c = stripe[2]
            px[x, y] = shade(c, rnd.randint(-5, 3))
    for i in range(16):
        px[i, 15] = shade(SEAM, -10)
        px[15, i] = shade(SEAM, -10)
        px[i, 0] = shade(px[i, 0][:3], 14)
        px[0, i] = shade(px[0, i][:3], 14)
    for (x, y) in ((2, 2), (13, 13)):
        px[x, y] = shade(SEAM, -30)
        px[x + 1, y] = shade(SEAM, 10)
    return img


def hatch(wheel):
    """The round end hatch: orange plate with a bolt ring; the centre block carries the handle."""
    img = panel(ORANGE, 41)
    px = img.load()
    for a in range(0, 360, 45):
        x = int(round(7.5 + 5.5 * math.cos(math.radians(a))))
        y = int(round(7.5 + 5.5 * math.sin(math.radians(a))))
        px[x, y] = shade(DARK, 20)
    if wheel:
        for y in range(16):
            for x in range(16):
                d = math.hypot(x - 7.5, y - 7.5)
                if 3.2 <= d <= 4.4:
                    px[x, y] = shade((190, 192, 196), 0 if y < 8 else -30)
        for i in range(3, 13):
            px[i, 7] = px[i, 8] = shade((190, 192, 196), -10)
        for (x, y) in ((7, 7), (8, 7), (7, 8), (8, 8)):
            px[x, y] = shade(DARK, 0)
    return img


def porthole():
    """A round window: white rim, bolt ring, dark blue glass with a highlight; corners see-through."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for y in range(16):
        for x in range(16):
            d = math.hypot(x - 7.5, y - 7.5)
            if d <= 5.2:
                g = 120 if (x - y) in (-3, -2) and x < 8 else 70
                px[x, y] = (30, 70 + g // 3, 110 + g // 2, 120)
            elif d <= 7.6:
                px[x, y] = shade(WHITE, -8 if y > 8 else 4)
            else:
                px[x, y] = shade(WHITE, -2)
    for a in range(0, 360, 60):
        x = int(round(7.5 + 6.4 * math.cos(math.radians(a))))
        y = int(round(7.5 + 6.4 * math.sin(math.radians(a))))
        px[x, y] = shade(SEAM, -40)
    return img


def deck():
    """Floor grating: dark steel slats over a darker gap."""
    img = Image.new("RGBA", (16, 16))
    px = img.load()
    for y in range(16):
        for x in range(16):
            slat = (y % 4) != 3
            px[x, y] = shade((108, 112, 118) if slat else (36, 38, 42), -6 if y % 4 == 2 else 0)
    for y in range(16):
        px[0, y] = px[15, y] = shade((80, 84, 90), 0)
    return img


def frame():
    """The skids: dark gunmetal with a yellow-black hazard edge."""
    img = panel(DARK, 77)
    px = img.load()
    for x in range(16):
        for y in (13, 14):
            px[x, y] = (230, 190, 40, 255) if ((x + y) // 2) % 2 == 0 else (30, 30, 30, 255)
    return img


def lamp(colour, seed):
    """A recessed light: metal rim around a bright lens."""
    img = panel((176, 180, 186), seed)
    px = img.load()
    for y in range(3, 13):
        for x in range(3, 13):
            t = 1 - max(abs(x - 7.5), abs(y - 7.5)) / 5
            px[x, y] = tuple(min(255, int(c + 60 * t)) for c in colour) + (255,)
    return img


def console_screen():
    """The Return to Surface screen: dark glass, a bright up arrow over a wave line."""
    img = panel((84, 88, 96), 90)
    px = img.load()
    for y in range(2, 14):
        for x in range(2, 14):
            px[x, y] = (12, 34, 44, 255)
    cyan = (90, 230, 230, 255)
    for i in range(4):  # arrow head
        for x in range(7 - i, 9 + i):
            px[x, 3 + i] = cyan
    for y in range(7, 10):  # arrow shaft
        px[7, y] = px[8, y] = cyan
    for x in range(3, 13):  # waves
        px[x, 11 + (1 if (x // 2) % 2 else 0)] = (60, 150, 220, 255)
    return img


def console_side():
    img = panel((84, 88, 96), 91)
    px = img.load()
    for (x, y, c) in ((4, 5, (220, 60, 50)), (7, 5, (240, 200, 60)), (10, 5, (70, 200, 90))):
        px[x, y] = px[x + 1, y] = (*c, 255)
    for x in range(3, 13):
        px[x, 9] = shade(DARK, -10)
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    out = {
        "lifepod_hull": panel(WHITE, 1),
        "lifepod_hull_stripe": panel(WHITE, 2, stripe=(9, 12, ORANGE)),
        "lifepod_hull_orange": panel(ORANGE, 3),
        "lifepod_hatch": hatch(False),
        "lifepod_hatch_wheel": hatch(True),
        "lifepod_window": porthole(),
        "lifepod_deck": deck(),
        "lifepod_frame": frame(),
        "lifepod_lamp": lamp((200, 210, 215), 5),
        "lifepod_beacon": lamp((220, 110, 30), 6),
        "lifepod_console": console_side(),
        "lifepod_console_screen": console_screen(),
    }
    for name, img in out.items():
        img.save(os.path.join(OUT, name + ".png"))
    print(f"wrote {len(out)} textures to {OUT}")


if __name__ == "__main__":
    main()
