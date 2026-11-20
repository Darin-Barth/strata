"""Draw the Omnistrata's item icon: a brushed-steel tool case with a handle, a copper band and two gold latches
(Darin's pick, Nov 20, from a dozen tries: design "M").

Usage: python tools/strata-tweaks/art/make_omnistrata.py     (needs Pillow; writes into ../resources)
Drawn from scratch, pixel by pixel, in the vanilla item style (light from the top left, a ramp of shades per
material, the outline in the material's darkest shade); not derived from any mod's texture.
"""
import pathlib

from PIL import Image

OUT = pathlib.Path(__file__).resolve().parent.parent / 'resources/assets/strata_tweaks/textures/item/omnistrata.png'


def rgb(s):
    return tuple(int(s[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


P = {
    '.': (0, 0, 0, 0),
    'x': rgb('#2f343c'),  # steel, outline
    'j': rgb('#6b727c'),  # steel, shade
    'i': rgb('#9aa2ac'),  # steel
    'I': rgb('#d8dde2'),  # steel, light
    'W': rgb('#ffffff'),  # glint
    'r': rgb('#b5633c'),  # copper, shade
    'R': rgb('#e8905c'),  # copper
    'y': rgb('#c8922e'),  # gold, shade
    'Y': rgb('#f6d86a'),  # gold
}

ROWS = [
    '................',
    '................',
    '.....xxxxxx.....',
    '....xIx..xjx....',
    '....xix..xjx....',
    '.xxxxxxxxxxxxxx.',
    'xIWIIIIIIiiiijjx',
    'xIIIIIIiiiiijjjx',
    'xrRRRRRRRRrrrrrx',
    'xxxxyYxxxxyYxxxx',
    'xiiiyyiiiiyyjjjx',
    'xiiiiiiiijjjjjjx',
    'xiiiiiijjjjjjjjx',
    'xjjjjjjjjjjjjjjx',
    '.xxxxxxxxxxxxxx.',
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


# The 8x8 mark drawn in the corner of a tool that is out of the Omnistrata (client/OmnistrataClient).
MARK_OUT = OUT.parent.parent / 'gui/omnistrata_mark.png'
MARK = [
    '........',
    '..xxxx..',
    '..x..x..',
    'xxxxxxxx',
    'xIIiijjx',
    'xRRRrrrx',
    'xiYiiYjx',
    'xxxxxxxx',
]


def mark():
    img = Image.new('RGBA', (8, 8))
    for y, row in enumerate(MARK):
        assert len(row) == 8, (y, row)
        for x, ch in enumerate(row):
            img.putpixel((x, y), P[ch])
    MARK_OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(MARK_OUT)
    print('wrote', MARK_OUT)


mark() if __name__ == '__main__' else None
