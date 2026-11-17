"""Draw the Carapace and Abyssal diving suit art for Strata Tweaks.

Usage: python tools/strata-tweaks/art/make_art.py [--preview <dir>] [--create <Create jar>] [carapace=<a|b|c>] [abyssal=<a|b|c>]

Everything is drawn here from scratch on the vanilla armour layout (64x32, layer 1 = chestplate, layer 2 =
leggings): Create's and Deep Seas' own textures are All Rights Reserved, so nothing is derived from them.
Each tier has three looks. The picked ones (default: the ones in PICKED) are written into
tools/strata-tweaks/resources/assets/strata_tweaks/textures; --preview also writes every look and a contact
sheet (icons plus a front and back paper doll) to the given folder. Needs Pillow. Rebuild the mod afterwards.

The backtank textures (--create) are painted onto the shape of Create's backtank: the script reads where each
face of Create's models sits on the 32x32 texture and fills it with our own colours, so our models can simply
point at Create's shapes. Nothing of Create's texture is read or copied.
"""
import json
import pathlib
import sys
import zipfile

from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
TEXTURES = HERE.parent / 'resources/assets/strata_tweaks/textures'
PICKED = {'carapace': 'c', 'abyssal': 'c'}


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def ramp(*hexes):
    return [rgb(h) for h in hexes]


# zone ramps run dark -> light. P plate, P2 second plate ramp (blended in down the body), T trim, U undersuit,
# R rivets and highlights, G glow.
LOOKS = {
    'carapace': {
        'a': dict(name='Crab Shell', style='segment', lamp=False,
                  P=ramp('5a1a12', '8f2a18', 'c2441e', 'e06a2c', 'f2a35a'), T=ramp('8a6a4a', 'c9a877', 'f0dcae'),
                  U=ramp('1f1612', '33241c', '4a342a'), R=ramp('f7e3b0'), G=ramp('c9601f', 'ffb347', 'ffe0a0')),
        'b': dict(name='Bronze and Coral', style='panel', lamp=False,
                  P=ramp('2e2118', '4a3524', '6b4c30', '8c6740', 'b08a58'), T=ramp('7a1f24', 'b8323a', 'e8565a'),
                  U=ramp('17181c', '24262c', '34373f'), R=ramp('e8c66a'), G=ramp('b8323a', 'e8565a', 'ffb0a8')),
        'c': dict(name='Bone and Teal', style='segment', lamp=False,
                  P=ramp('6e6250', '9c8f76', 'c7bc9f', 'e4dcc4', 'f7f2e2'), T=ramp('8a3d14', 'c9601f', 'f08a3a'),
                  U=ramp('0f2a30', '17404a', '235a66'), R=ramp('f08a3a'), G=ramp('1f9a90', '3fd0c0', 'b8fff2')),
    },
    'abyssal': {
        'a': dict(name='Lantern', style='segment', lamp=True, seams=True,
                  P=ramp('070b16', '0e1628', '16233d', '213354', '31497a'), T=ramp('2a3d5c', '45638f', '6f93c4'),
                  U=ramp('04060b', '090d16', '101724'), R=ramp('6f93c4'), G=ramp('1fb8c9', '5ef2ff', 'd6fdff')),
        'b': dict(name='Black and Brass', style='panel', lamp=True,
                  P=ramp('121315', '1e2024', '2c2f35', '3d4149', '555b66'), T=ramp('6b4a16', 'a87b26', 'e0b64a'),
                  U=ramp('0a0a0c', '141417', '1f1f24'), R=ramp('f2d478'), G=ramp('c96a12', 'ffab2e', 'ffe29a')),
        'c': dict(name='Sea Glass', style='segment', lamp=True,
                  P=ramp('0c2f3a', '14505c', '1f7a80', '35a79c', '7fd8c0'), P2=ramp('1d1440', '35226e', '55389c', '7d5cc4', 'b59be8'),
                  T=ramp('566070', '8a98aa', 'c8d4e0'), U=ramp('0b0e24', '141a3a', '1f2855'), R=ramp('e8f4ff'),
                  G=ramp('5fd8c0', '9dfbe0', 'e6fff6')),
    },
}

# ---- the armour layout (x, y, w, h) ----
BODY = dict(front=(20, 20, 8, 12), back=(32, 20, 8, 12), right=(16, 20, 4, 12), left=(28, 20, 4, 12), top=(20, 16, 8, 4))
ARM = dict(outer=(40, 20, 4, 12), front=(44, 20, 4, 12), inner=(48, 20, 4, 12), back=(52, 20, 4, 12), top=(44, 16, 4, 4))
LEG = dict(outer=(0, 20, 4, 12), front=(4, 20, 4, 12), inner=(8, 20, 4, 12), back=(12, 20, 4, 12), top=(4, 16, 4, 4), bottom=(8, 16, 4, 4))
HEAD = dict(right=(0, 8, 8, 8), front=(8, 8, 8, 8), left=(16, 8, 8, 8), back=(24, 8, 8, 8), top=(8, 0, 8, 8))


def colour(look, zone, shade, t=0.0):
    r = look[zone]
    shade = max(0, min(len(r) - 1, shade))
    c = r[shade]
    if zone == 'P' and 'P2' in look:
        c2 = look['P2'][shade]
        c = tuple(round(a + (b - a) * t) for a, b in zip(c, c2))
    return c + (255,)


# light falls from the upper left: per-column shade offsets for plates on 8- and 4-wide faces
LIGHT = {8: (0, 1, 0, 0, 0, 0, -1, -1), 4: (1, 0, 0, -1)}


def paint(img, look, rect, fn, t0=0.0, t1=1.0, dim=0):
    x, y, w, h = rect
    for r in range(h):
        for c in range(w):
            cell = fn(c, r, w, h)
            if cell is None:
                continue
            zone, shade = cell
            if zone == 'P':
                shade += LIGHT[w][c] - dim if shade > 0 else 0
                shade = max(0, shade)
            img.putpixel((x + c, y + r), colour(look, zone, shade, t0 + (t1 - t0) * r / max(1, h - 1)))


def breastplate(look, c, r, w):
    """Rows 1-6 of a body face. Segments: two overlapping shells that droop towards the sides. Panels: one riveted plate."""
    if look['style'] == 'segment':
        k = r - 1 + (0 if 2 <= c <= w - 3 else 1)
        if k > 5:
            return ('U', 1)
        i = k % 3
        if i == 2:
            return ('G', 0) if look.get('seams') and 0 < c < w - 1 else ('P', 0)
        return ('P', 4 if i == 0 else 3)
    if r == 1:
        return ('P', 4)
    if r == 6:
        return ('P', 0)
    if c in (1, w - 2) and r in (2, 5):
        return ('R', 0)
    return ('P', 3 if r < 4 else 2)


def chest_layer(look):
    img = Image.new('RGBA', (64, 32), (0, 0, 0, 0))

    def front(c, r, w, h):
        if r == 0:
            return ('T', 2 if 2 <= c <= 5 else 1)
        if r <= 6:
            if c in (3, 4) and r in (2, 3):
                if look['lamp']:
                    return ('G', 2 if (c, r) == (3, 2) else 1)
                return ('T', 2 if r == 2 else 1)
            if look['lamp'] and (c in (2, 5) and r in (2, 3) or c in (3, 4) and r in (1, 4)):
                return ('T', 1 if r < 3 else 0)
            return breastplate(look, c, r, w)
        if r <= 9:
            if 2 <= c <= 5 and r <= 8:
                return ('P', 3 if r == 7 else 1)
            return ('U', 0 if r == 7 else 1)
        if r == 10:
            return ('R', 0) if c in (3, 4) else ('T', 2 if c not in (0, 7) else 1)
        return ('P', 2) if 1 <= c <= 6 else ('U', 1)

    def back(c, r, w, h):
        if c in (2, 5) and r <= 8:
            return ('T', 2 if r < 4 else 1)
        if r == 0:
            return ('T', 1)
        if r <= 6:
            if c in (3, 4):
                if (c, r) in ((3, 2), (4, 5)):
                    return ('R', 0)
                return ('U', 2 if 2 <= r <= 5 else 1)
            return breastplate(look, c, r, w)
        if r <= 9:
            return ('U', 0 if r == 7 else 1)
        if r == 10:
            return ('T', 2 if c not in (0, 7) else 1)
        return ('P', 2) if 1 <= c <= 6 else ('U', 1)

    def side(c, r, w, h):
        if r == 0:
            return ('P', 2)
        if r <= 5:
            return ('P', 3 if r % 3 else 0) if c in (1, 2) else ('U', 1)
        if r <= 9:
            return ('U', 0 if r == 6 else 1)
        return ('T', 1) if r == 10 else ('P', 1)

    def top(c, r, w, h):
        return ('T', 1) if 2 <= c <= 5 and 1 <= r <= 2 else ('P', 3)

    def arm(face):
        plated = face in ('outer', 'front')

        def fn(c, r, w, h):
            if r <= 3:
                if face == 'outer' and r == 1 and c in (1, 2):
                    return ('R', 0)
                if r == 3:
                    return ('G', 0) if look.get('seams') and face != 'inner' else ('P', 0)
                return ('P', (4, 3, 2)[r])
            if r <= 5:
                return ('U', 0 if r == 4 else 1)
            if r <= 7:
                return ('P', 3 if r == 6 else 0) if plated else ('U', 1)
            if r <= 9:
                return ('P', 3 if r == 8 else 2) if face != 'inner' else ('U', 1)
            if r == 10:
                return ('T', 2 if plated else 1)
            return None
        return fn

    paint(img, look, BODY['front'], front, 0.0, 0.5)
    paint(img, look, BODY['back'], back, 0.0, 0.5, dim=1)
    paint(img, look, BODY['right'], side, 0.0, 0.5)
    paint(img, look, BODY['left'], side, 0.0, 0.5, dim=1)
    paint(img, look, BODY['top'], top)
    for face in ('outer', 'front', 'inner', 'back'):
        paint(img, look, ARM[face], arm(face), 0.0, 0.5, dim=1 if face in ('inner', 'back') else 0)
    paint(img, look, ARM['top'], lambda c, r, w, h: ('R', 0) if (c, r) in ((1, 1), (2, 2)) else ('P', 4 if r < 2 else 3))

    # --- helmet: a dome with a round window, small side ports and a valve on top ---
    def dome(r):
        return 4 if r <= 1 else 3 if r <= 4 else 2

    def helm_front(c, r, w, h):
        if r == 7:
            return ('T', 0)
        if 2 <= c <= 5 and 2 <= r <= 5:
            return ('G', 2 if (c, r) in ((2, 2), (3, 2), (2, 3)) else 0 if (c, r) in ((5, 5), (4, 5), (5, 4)) else 1)
        if 1 <= c <= 6 and 1 <= r <= 6:
            return ('T', 2 if r == 1 or c == 1 else 1)
        return ('P', dome(r))

    def helm_side(c, r, w, h):
        if r == 7:
            return ('T', 0)
        if c in (3, 4) and r in (3, 4):
            return ('G', 2 if (c, r) == (3, 3) else 1)
        if 2 <= c <= 5 and 2 <= r <= 5 and (c in (3, 4) or r in (3, 4)):
            return ('T', 1)
        return ('P', dome(r))

    def helm_back(c, r, w, h):
        if r == 7:
            return ('T', 0)
        if c in (3, 4) and 1 <= r <= 5:
            return ('R', 0) if (c, r) == (3, 2) else ('T', 2 if c == 3 else 1)
        return ('P', dome(r))

    def helm_top(c, r, w, h):
        if c in (3, 4) and r in (3, 4):
            return ('R', 0) if (c, r) == (3, 3) else ('T', 1)
        return ('P', 4 if 1 <= c <= 6 and 1 <= r <= 6 else 3)

    paint(img, look, HEAD['front'], helm_front, 0.0, 0.0)
    paint(img, look, HEAD['right'], helm_side, 0.0, 0.0)
    paint(img, look, HEAD['left'], helm_side, 0.0, 0.0, dim=1)
    paint(img, look, HEAD['back'], helm_back, 0.0, 0.0, dim=1)
    paint(img, look, HEAD['top'], helm_top, 0.0, 0.0)

    # --- boots: a cuff, a plated shoe and a dark weighted sole ---
    def boot(face):
        def fn(c, r, w, h):
            if r < 8:
                return None
            if r == 8:
                return ('T', 2 if face in ('front', 'outer') else 1)
            if r == 11:
                return ('U', 0)
            if face == 'front' and r == 10 and c in (1, 2):
                return ('R', 0)
            return ('P', 4 if r == 9 else 2)
        return fn

    for face in ('outer', 'front', 'inner', 'back'):
        paint(img, look, LEG[face], boot(face), 1.0, 1.0, dim=1 if face in ('inner', 'back') else 0)
    paint(img, look, LEG['bottom'], lambda c, r, w, h: ('U', 0))
    return img


def legs_layer(look):
    img = Image.new('RGBA', (64, 32), (0, 0, 0, 0))

    def waist(c, r, w, h):
        if r < 7:
            return None
        if r == 7:
            return ('T', 2)
        if r == 8:
            return ('R', 0) if w == 8 and c in (3, 4) else ('T', 0)
        return ('P', 3 if r == 9 else 2 if r == 10 else 1)

    def leg(face):
        def fn(c, r, w, h):
            if r <= 3:
                if face == 'inner':
                    return ('U', 1)
                if r == 3:
                    return ('G', 0) if look.get('seams') else ('P', 0)
                return ('P', (3, 3, 2)[r])
            if r == 4 and face != 'front':
                return ('U', 0)
            if r <= 6:
                if face == 'front':
                    if r == 5 and c in (1, 2):
                        return ('G', 1) if look['lamp'] else ('R', 0)
                    return ('P', (4, 3, 0)[r - 4])
                return ('U', 1)
            if r <= 8:
                return ('P', 3 if r == 7 else 2) if face in ('front', 'outer') else ('U', 1)
            return None
        return fn

    for face in ('front', 'back', 'right', 'left'):
        paint(img, look, BODY[face], waist, 0.5, 0.6)
    for face in ('outer', 'front', 'inner', 'back'):
        paint(img, look, LEG[face], leg(face), 0.55, 1.0, dim=1 if face in ('inner', 'back') else 0)
    paint(img, look, LEG['top'], lambda c, r, w, h: ('P', 2))
    return img


# ---- item icons (our own 16x16 drawings; '.' is empty) ----
ICON_CHEST = """
................
..PP........PP..
.PPPP.TTTT.PPPP.
.PPPPPTUUTPPPPP.
.PPPPPPPPPPPPPP.
.PPUPPPPPPPPUPP.
.PP.PPPGGPPP.PP.
.TT.PPPGGPPP.TT.
....PPPPPPPP....
....PRPPPPRP....
....UUUUUUUU....
....UUUUUUUU....
....TTTRRTTT....
....PPPPPPPP....
................
................
"""
ICON_LEGS = """
................
................
...TTTTTTTTTT...
...TTTTRRTTTT...
...PPPPPPPPPP...
...PPPPPPPPPP...
...PPPP..PPPP...
...UUUU..UUUU...
...PPPP..PPPP...
...PGGP..PGGP...
...PPPP..PPPP...
...UUUU..UUUU...
...PPPP..PPPP...
...PPPP..PPPP...
................
................
"""
ICON_HELMET = """
................
....PPPPPPPP....
...PPPPPPPPPP...
..PPPTTTTTTPPP..
..PPTWWWWWWTPP..
..PPTWWWWWWTPP..
..PPTWWWWWWTPP..
..PPTWWWWWWTPP..
..PPPTTTTTTPPP..
..PRPPPPPPPPRP..
...PPPPPPPPPP...
...TTTTTTTTTT...
..TTTTTTTTTTTT..
................
................
................
"""
ICON_BOOTS = """
................
................
................
....TTTT..TTTT..
....PPPP..PPPP..
....PPPP..PPPP..
....PPPP..PPPP..
....PPPP..PPPP..
...PPPPP.PPPPP..
..PPPPPP.PPPPPP.
..PRPPPP.PRPPPP.
..UUUUUU.UUUUUU.
..UUUUUU.UUUUUU.
................
................
................
"""
# the metal of the Create backtank underneath: its cogs, shaft and bands keep that colour
METALS = {'copper': ramp('7a4630', 'a8623f', 'd08a5a'), 'netherite': ramp('2a2528', '443c40', '6b5f63')}
ICON_PLATING = """
................
................
.....PPPPPPPP...
....PPPPPPPPPP..
...PRPPPPPPPPRP.
...PPPPPPPPPPPP.
...TTTTTTTTTTTT.
..PPPPPPPPPPPP..
.PPPPPPPPPPPPP..
.PRPPPPPPPPPRP..
.PPPPPPPPPPPPP..
.PPPPPPPPPPPPP..
.TTTTTTTTTTTTT..
................
................
................
"""


def icon(look, art):
    rows = [line for line in art.strip('\n').split('\n')]
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))

    def at(c, r):
        return rows[r][c] if 0 <= r < 16 and 0 <= c < 16 else '.'

    for r in range(16):
        for c in range(16):
            z = at(c, r)
            if z == '.':
                continue
            edge = '.' in (at(c - 1, r), at(c + 1, r), at(c, r - 1), at(c, r + 1))
            lit = at(c, r - 1) == '.' or at(c - 1, r) == '.'
            if z == 'P':
                shade = 3
                if look['style'] == 'segment' and r % 3 == 2:
                    shade = 1
                elif r + c > 16:
                    shade = 2
                if edge:
                    shade = 4 if lit and at(c, r + 1) != '.' and at(c + 1, r) != '.' else 0
            elif z == 'W':
                z, shade = 'G', (2 if lit else 0 if edge or at(c + 1, r) != 'W' or at(c, r + 1) != 'W' else 1)
            elif z == 'G':
                if not look['lamp'] and art is not ICON_PLATING:
                    z, shade = 'T', 2
                else:
                    shade = 2 if at(c - 1, r) != 'G' and at(c, r - 1) != 'G' else 1
            elif z == 'R':
                shade = 0
            else:
                shade = (1 if edge and not lit else 2) if z == 'T' else (0 if edge else 1 + r % 2)
            img.putpixel((c, r), colour(look, z, shade, r / 15))
    return img


# ---- preview: paper doll ----
SKIN = (176, 176, 180, 255)
SKIN_DARK = (150, 150, 156, 255)


def doll(chest, legs, back=False):
    """Front (or back) view, 18x32: a mannequin in a plain copper helmet and boots (standing in for the Create
    ones, which stay as they are) with the two layers on top."""
    img = Image.new('RGBA', (18, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    copper = [rgb(h) + (255,) for h in ('7a4630', 'a8623f', 'c98458', 'e0a878')]
    d.rectangle((5, 0, 12, 7), fill=copper[1])
    d.rectangle((5, 0, 12, 0), fill=copper[3])
    d.rectangle((5, 7, 12, 7), fill=copper[0])
    d.rectangle((5, 1, 5, 6), fill=copper[2])
    if not back:
        d.rectangle((7, 2, 10, 5), fill=copper[0])
        d.rectangle((8, 3, 9, 4), fill=(96, 168, 176, 255))
        d.point((8, 3), fill=(190, 236, 240, 255))
    d.rectangle((5, 8, 12, 19), fill=SKIN_DARK)
    d.rectangle((0, 8, 3, 19), fill=SKIN)
    d.rectangle((14, 8, 17, 19), fill=SKIN)
    d.rectangle((5, 20, 8, 31), fill=SKIN)
    d.rectangle((9, 20, 12, 31), fill=SKIN_DARK)
    d.rectangle((5, 29, 12, 31), fill=copper[1])
    d.rectangle((5, 29, 12, 29), fill=copper[2])
    d.line((9, 29, 9, 31), fill=copper[0])
    face = 'back' if back else 'front'

    def crop(layer, rect, flip=False):
        x, y, w, h = rect
        part = layer.crop((x, y, x + w, y + h))
        return part.transpose(Image.FLIP_LEFT_RIGHT) if flip else part

    img.alpha_composite(crop(chest, HEAD[face]), (5, 0))
    boots = crop(chest, LEG[face])
    img.alpha_composite(crop(legs, BODY[face]), (5, 8))
    img.alpha_composite(crop(chest, BODY[face]), (5, 8))
    img.alpha_composite(crop(chest, ARM[face], back), (0, 8))
    img.alpha_composite(crop(chest, ARM[face], not back), (14, 8))
    img.alpha_composite(crop(legs, LEG[face], back), (5, 20))
    img.alpha_composite(crop(legs, LEG[face], not back), (9, 20))
    img.alpha_composite(crop(chest, LEG[face], back), (5, 20))
    img.alpha_composite(crop(chest, LEG[face], not back), (9, 20))
    return img


def big(img, scale):
    return img.resize((img.width * scale, img.height * scale), Image.NEAREST)


def sheet(out):
    from PIL import ImageFont
    try:
        font = ImageFont.truetype('arial.ttf', 22)
        small = ImageFont.truetype('arial.ttf', 16)
    except OSError:
        font = small = ImageFont.load_default()
    cell_w, cell_h = 520, 430
    canvas = Image.new('RGBA', (cell_w * 3, cell_h * 2 + 20), (58, 74, 92, 255))
    d = ImageDraw.Draw(canvas)
    for row, tier in enumerate(('carapace', 'abyssal')):
        for col, key in enumerate('abc'):
            look = LOOKS[tier][key]
            chest, legs = chest_layer(look), legs_layer(look)
            x0, y0 = col * cell_w + 16, row * cell_h + 14
            d.text((x0, y0), f"{tier.capitalize()} {key.upper()}: {look['name']}", fill=(255, 255, 255, 255), font=font)
            canvas.alpha_composite(big(doll(chest, legs), 10), (x0, y0 + 40))
            canvas.alpha_composite(big(doll(chest, legs, True), 10), (x0 + 196, y0 + 40))
            d.text((x0 + 68, y0 + 366), 'front', fill=(210, 220, 230, 255), font=small)
            d.text((x0 + 266, y0 + 366), 'back', fill=(210, 220, 230, 255), font=small)
            for i, art in enumerate((ICON_HELMET, ICON_CHEST, ICON_LEGS, ICON_BOOTS, ICON_PLATING)):
                tile = Image.new('RGBA', (72, 72), (139, 139, 139, 255))
                tile = Image.new('RGBA', (52, 52), (139, 139, 139, 255))
                tile.alpha_composite(big(icon(look, art), 3), (2, 2))
                canvas.alpha_composite(tile, (x0 + 392 + (i % 2) * 56, y0 + 44 + (i // 2) * 56))
    canvas.save(out / 'suit_choices.png')


# ---- backtank textures, painted onto the shape of Create's backtank ----
BODY_PARTS = {  # Create's five body boxes (from, to) -> what we paint them as
    ((5, 0, 5), (11, 4, 11)): 'base', ((5, 10, 5), (11, 12, 11)): 'cap', ((4, 4, 4), (12, 10, 12)): 'body',
    ((4, 4, 9), (12, 10, 11)): 'gauge', ((5, 2, 3), (11, 11, 5)): 'harness'}


def tank_texture(look, metal, create_jar):
    look = dict(look, M=METALS[metal])
    faces = []
    with zipfile.ZipFile(create_jar) as z:
        for model in ('block', 'item', 'block_cogs', 'block_shaft_input'):
            data = json.loads(z.read(f'assets/create/models/block/{metal}_backtank/{model}.json'))
            for element in data['elements']:
                part = BODY_PARTS.get((tuple(element['from']), tuple(element['to'])), 'metal')
                for side, face in element['faces'].items():
                    u1, v1, u2, v2 = (round(v * 2) for v in face['uv'])
                    x1, x2, y1, y2 = min(u1, u2), max(u1, u2), min(v1, v2), max(v1, v2)
                    if x2 > x1 and y2 > y1:
                        faces.append((x1, y1, x2, y2, part, side))
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    # big faces first, so the small ones that share a corner of the texture keep their own colours
    for x1, y1, x2, y2, part, side in sorted(faces, key=lambda f: -(f[2] - f[0]) * (f[3] - f[1])):
        w, h = x2 - x1, y2 - y1
        for y in range(y1, min(y2, 32)):
            for x in range(x1, min(x2, 32)):
                c, r = x - x1, y - y1
                lift = (1 if side == 'up' else -1 if side == 'down' else 0)
                if h >= 3:
                    lift += 1 if r == 0 else -1 if r == h - 1 else 0
                if w >= 4 and c == w - 1:
                    lift -= 1
                if part == 'body':
                    zone, shade = ('T', 1) if side not in ('up', 'down') and r == h // 2 else ('P', 3 + lift)
                elif part == 'base':
                    zone, shade = 'P', 2 + lift
                elif part == 'cap':
                    zone, shade = 'T', 1 + lift
                elif part == 'gauge':
                    zone, shade = 'G', 1
                elif part == 'harness':
                    zone, shade = ('T', 1) if w >= 4 and c in (0, w - 1) else ('U', 1 + lift)
                else:
                    zone, shade = 'M', 1 + lift
                # the second plate colour (Sea Glass) comes in down the tank
                t = {'cap': 0.0, 'base': 1.0}.get(part, r / max(1, h - 1) if side not in ('up', 'down') else 0.15)
                img.putpixel((x, y), colour(look, zone, shade, t))
    return img


def write_tanks(folder, tier, key, create_jar):
    (folder / 'block').mkdir(parents=True, exist_ok=True)
    for metal in METALS:
        tank_texture(LOOKS[tier][key], metal, create_jar).save(folder / f'block/{tier}_{metal}_backtank.png')


def write(folder, tier, key):
    look = LOOKS[tier][key]
    (folder / 'models/armor').mkdir(parents=True, exist_ok=True)
    (folder / 'item').mkdir(parents=True, exist_ok=True)
    chest_layer(look).save(folder / f'models/armor/{tier}_diving_layer_1.png')
    legs_layer(look).save(folder / f'models/armor/{tier}_diving_layer_2.png')
    icon(look, ICON_CHEST).save(folder / f'item/{tier}_diving_chestplate.png')
    icon(look, ICON_LEGS).save(folder / f'item/{tier}_diving_leggings.png')
    icon(look, ICON_PLATING).save(folder / f'item/{tier}_plating.png')
    icon(look, ICON_HELMET).save(folder / f'item/{tier}_diving_helmet.png')
    icon(look, ICON_BOOTS).save(folder / f'item/{tier}_diving_boots.png')



def main():
    picked, preview, create_jar = dict(PICKED), None, None
    args = sys.argv[1:]
    while args:
        a = args.pop(0)
        if a == '--preview':
            preview = pathlib.Path(args.pop(0))
        elif a == '--create':
            create_jar = pathlib.Path(args.pop(0))
        elif '=' in a and a.split('=')[0] in LOOKS and a.split('=')[1] in 'abc':
            picked[a.split('=')[0]] = a.split('=')[1]
        else:
            sys.exit(__doc__)
    for tier, key in picked.items():
        write(TEXTURES, tier, key)
        if create_jar:
            write_tanks(TEXTURES, tier, key, create_jar)
        print(f'{tier}: look {key} ({LOOKS[tier][key]["name"]}) -> resources')
    if preview:
        preview.mkdir(parents=True, exist_ok=True)
        for tier in LOOKS:
            for key in LOOKS[tier]:
                write(preview / f'{tier}_{key}', tier, key)
        sheet(preview)
        print('preview sheet:', preview / 'suit_choices.png')


if __name__ == '__main__':
    main()
