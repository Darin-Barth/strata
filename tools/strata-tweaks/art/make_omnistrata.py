"""Draw the Omnistrata's item icon (a rolled leather tool roll with a brass buckle and three tool handles).

Usage: python tools/strata-tweaks/art/make_omnistrata.py     (needs Pillow; writes into ../resources)
Drawn from scratch, pixel by pixel; not derived from any mod's texture.
"""
import pathlib

from PIL import Image

OUT = pathlib.Path(__file__).resolve().parent.parent / 'resources/assets/strata_tweaks/textures/item/omnistrata.png'

P = {
    '.': (0, 0, 0, 0),
    'o': (43, 26, 16, 255),     # outline
    'd': (92, 56, 32, 255),     # leather, dark
    'l': (133, 84, 48, 255),    # leather
    'h': (171, 115, 68, 255),   # leather, light
    's': (58, 40, 30, 255),     # strap
    'b': (226, 180, 76, 255),   # brass
    'B': (255, 226, 138, 255),  # brass highlight
    'w': (120, 86, 52, 255),    # wooden handle
    'W': (160, 120, 76, 255),   # wooden handle, light
    'i': (198, 204, 210, 255),  # iron
    'I': (236, 240, 244, 255),  # iron highlight
    'c': (86, 196, 190, 255),   # diamond
}

ROWS = [
    '................',
    '....iI...c...ii.',
    '...iIi..cc..iIi.',
    '....W...W....W..',
    '....w...w....w..',
    '..ooooooooooooo.',
    '.ohhhhhsshhhhhho',
    '.ohlllhsslllllho',
    '.olllllsslllllo.',
    '.ollllbBbbllllo.',
    '.ollllbssbllllo.',
    '.olllldssdllllo.',
    '.odllldssdlllddo',
    '.odddddssddddddo',
    '..ooooooooooooo.',
    '................',
]


def main():
    img = Image.new('RGBA', (16, 16))
    for y, row in enumerate(ROWS):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            img.putpixel((x, y), P[ch])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT)
    print('wrote', OUT)


if __name__ == '__main__':
    main()
