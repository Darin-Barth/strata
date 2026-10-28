"""Generate a unique Boss Loot Bag texture per boss (kubejs/assets/strata/...).

Every bag shares one hand-drawn 16x16 sack. Each boss gets its own colours (cloth, rope, emblem),
taken from the boss's own entity texture in its mod jar unless a palette is set by hand below, and
an emblem for its theme (flame, skull, wave, ...). Writes:
  * textures/item/boss_bag/<namespace>_<name>.png and models/item/boss_bag/<namespace>_<name>.json
  * models/item/boss_bag.json: the default bag plus one custom_model_data override per boss
  * kubejs/server_scripts/strata_boss_bag_models.js: boss ID -> custom_model_data number
    (read by strata_boss_bags.js when it makes a bag)
  * --preview <png>: a contact sheet of every bag, scaled up, for review

Run from the repo root (needs Pillow; re-run after adding a boss to #strata:boss_bags):
  python tools/build_boss_bags.py --mods <server or client mods dir> [--preview sheet.png]
"""
import argparse
import colorsys
import io
import json
import os
import zipfile

from PIL import Image, ImageDraw

ASSETS = "kubejs/assets/strata"
MODEL_SCRIPT = "kubejs/server_scripts/strata_boss_bag_models.js"

# 16x16 sack: a gathered, folded cloth top, a rope tie, a full body. O outline, D/M/L cloth
# dark/mid/light, R/r rope light/dark.
SACK = [
    "......OOOO......",
    "....OOLMMDOO....",
    "...OLLMMMMDDO...",
    "...OLMDMMDMDO...",
    "....OMMDMDMO....",
    ".....rRRRRr.....",
    "....OOrrrrOO....",
    "...OLLMMMMMDO...",
    "..OLMMMMMMMMDO..",
    ".OLMMMMMMMMMMDO.",
    ".OLMMMMMMMMMMDO.",
    ".OLMMMMMMMMMMDO.",
    ".OLMMMMMMMMMDDO.",
    "..OMMMMMMMMDDO..",
    "...ODDDDDDDDO...",
    "....OOOOOOOO....",
]
EMBLEM_AT = (5, 8)  # top-left (x, y) of the 5x5 emblem

# 5x5 emblems. E emblem colour, e emblem shade, . cloth.
EMBLEMS = {
    "flame": ["..E..", ".EE..", ".EEE.", "EEeEE", ".EEE."],
    "skull": [".EEE.", "EEEEE", "EeEeE", ".EEE.", ".E.E."],
    "drop": ["..E..", ".EeE.", "EEeEE", "EeeeE", ".EEE."],
    "eye": [".....", ".EEE.", "EEeEE", ".EEE.", "....."],
    "snow": ["E.E.E", ".EEE.", "EEeEE", ".EEE.", "E.E.E"],
    "sun": ["E.E.E", ".EEE.", "EEeEE", ".EEE.", "E.E.E"],
    "crown": ["E.E.E", "EEEEE", "EeEeE", "EEEEE", "....."],
    "leaf": ["...EE", "..EEE", ".EeE.", "EEE..", "E...."],
    "gear": [".E.E.", "EEEEE", ".EeE.", "EEEEE", ".E.E."],
    "bolt": ["..EE.", ".EE..", "EEEE.", "..EE.", ".EE.."],
    "horns": ["E...E", "E...E", ".EEE.", ".EeE.", "..E.."],
    "pyramid": ["..E..", ".EEE.", ".EeE.", "EEEEE", "EeEeE"],
    "spiral": ["EEEE.", "E..E.", "E.EE.", "E....", "EEEEE"],
    "pincer": ["EE.EE", "E...E", "EE.EE", ".EEE.", "..E.."],
    "star": ["..E..", ".EEE.", "EEeEE", ".EEE.", "..E.."],
    "cloud": [".....", ".EE..", "EEEEE", "EeeeE", "....."],
    "cube": ["EEEEE", "EeeeE", "EeEeE", "EeeeE", "EEEEE"],
    "feather": ["...EE", "..EeE", ".EeE.", "EeE..", "E...."],
    "fang": ["E...E", "EE.EE", ".E.E.", ".E.E.", "....."],
    "lure": ["EEE..", "..E..", "..E..", ".EEE.", ".EeE."],
    "fist": ["E.E.E", "EEEEE", "EEEEE", "EEEEe", ".EEE."],
    "moon": [".EEE.", "EE...", "E....", "EE...", ".EEE."],
    "obelisk": ["..E..", ".EEE.", ".EeE.", ".EeE.", ".EEE."],
    "bloom": ["E...E", ".EEE.", ".EeE.", ".EEE.", "E...E"],
    "golem": ["EEEEE", "EeEeE", "EEEEE", "E.E.E", "EEEEE"],
    "ghost": [".EEE.", "EeEeE", "EEEEE", "EEEEE", "E.E.E"],
    "trident": ["E.E.E", "E.E.E", "EEEEE", "..E..", "..E.."],
    "tentacle": [".EE..", "E..E.", "...E.", "..E.E", ".E..."],
    "comet": ["...EE", "..EEE", ".EEE.", "EeE..", "EE..."],
    "sword": ["....E", "...E.", "E.E..", ".E...", "E.E.."],
    "rift": ["E...E", ".E.E.", "..E..", ".E.E.", "E...E"],
    "axe": [".EEE.", "EEeE.", ".EE..", "..E..", "..E.."],
    "pillar": ["EEEEE", ".EeE.", ".EeE.", ".EeE.", "EEEEE"],
    "mask": ["EEEEE", "E.E.E", "EEEEE", ".EEE.", "..E.."],
    "snake": [".EEE.", "E....", ".EEE.", "....E", "EEE.."],
    "mushroom": [".EEE.", "EEeEE", "EEEEE", "..E..", ".EEE."],
    "hydra": ["E...E", ".E.E.", "E.E.E", ".EEE.", "..E.."],
    "shield": ["EEEEE", "EeEeE", "EEEEE", ".EEE.", "..E.."],
    "tears": ["EEEEE", "E.E.E", "EEEEE", "E.E.E", "E.E.E"],
    "paw": [".E.E.", "E...E", ".EEE.", "EEEEE", ".EEE."],
    "icicle": ["EEEEE", ".EEE.", ".EEE.", "..E..", "..E.."],
    "wing": ["E....", "EE...", "EEE.E", "EEEEE", ".EEE."],
    "maw": [".EEE.", "E.E.E", "EE.EE", "E.E.E", ".EEE."],
    "helm": [".EEE.", "EEEEE", "EeeeE", "EEEEE", ".E.E."],
    "portal": ["EEEEE", "E...E", "E.e.E", "E...E", "EEEEE"],
    "cross": ["..E..", "EEEEE", "..E..", "..E..", "..E.."],
    "keep": ["E.E.E", "EEEEE", "E.e.E", "EEEEE", "EEEEE"],
    "hourglass": ["EEEEE", ".EeE.", "..E..", ".EeE.", "EEEEE"],
}

# boss: (emblem, texture path inside its jar or None, optional hand-picked (cloth, rope, emblem))
BOSSES = {
    "minecraft:wither": ("skull", None, ("#2b2b30", "#5b5b63", "#d9d9e0")),
    "minecraft:warden": ("spiral", None, ("#0e2a33", "#123d47", "#2ad1d1")),
    "aether:slider": ("cube", "assets/aether/textures/entity/mobs/slider/slider_awake.png", None),
    "aether:valkyrie_queen": ("feather", "assets/aether/textures/entity/mobs/valkyrie/valkyrie.png", ("#e8e4d8", "#c9a43a", "#f4d35e")),
    "aether:sun_spirit": ("sun", "assets/aether/textures/entity/mobs/sun_spirit/sun_spirit.png", ("#d9541e", "#f2a33a", "#fff2a8")),
    "deep_aether:eots_controller": ("bolt", "assets/deep_aether/textures/entity/eots/eots_controller.png", None),
    "alexscaves:luxtructosaurus": ("fang", "assets/alexscaves/textures/entity/luxtructosaurus.png", ("#3a2a22", "#8a4a20", "#ffb000")),
    "alexscaves:hullbreaker": ("lure", "assets/alexscaves/textures/entity/hullbreaker.png", None),
    "ars_nouveau:wilden_boss": ("horns", "assets/ars_nouveau/textures/entity/wilden_chimera.png", None),
    "bosses_of_mass_destruction:gauntlet": ("fist", "assets/bosses_of_mass_destruction/textures/entity/gauntlet.png", None),
    "bosses_of_mass_destruction:lich": ("moon", "assets/bosses_of_mass_destruction/textures/entity/lich.png", ("#2a3550", "#6a8ab0", "#9fe8ff")),
    "bosses_of_mass_destruction:obsidilith": ("obelisk", "assets/bosses_of_mass_destruction/textures/entity/obsidilith.png", None),
    "bosses_of_mass_destruction:void_blossom": ("bloom", "assets/bosses_of_mass_destruction/textures/entity/void_blossom.png", None),
    "cataclysm:ancient_remnant": ("pyramid", "assets/cataclysm/textures/entity/ancient_remnant/ancient_remnant.png", None),
    "cataclysm:ender_guardian": ("eye", "assets/cataclysm/textures/entity/ender_guardian/new_ender_guardian.png", None),
    "cataclysm:ender_golem": ("star", "assets/cataclysm/textures/entity/ender_golem.png", None),
    "cataclysm:ignis": ("flame", "assets/cataclysm/textures/entity/ignis/ignis_idle_0.png", None),
    "cataclysm:maledictus": ("ghost", "assets/cataclysm/textures/entity/maledictus/maledictus_armor.png", ("#2c3440", "#5f7d94", "#8fe3ff")),
    "cataclysm:netherite_monstrosity": ("golem", "assets/cataclysm/textures/entity/monstrosity/netherite_monstrosity.png", ("#3b3536", "#6b2d1a", "#ff7a1a")),
    "cataclysm:scylla": ("trident", "assets/cataclysm/textures/entity/scylla/scylla.png", None),
    "cataclysm:the_harbinger": ("gear", None, ("#3a3a40", "#8a1c1c", "#ff3b3b")),
    "cataclysm:the_leviathan": ("tentacle", None, ("#1b1f3a", "#3a2f6b", "#9b6bff")),
    "cataclysm:the_baby_leviathan": ("drop", "assets/cataclysm/textures/entity/leviathan/the_baby_leviathan.png", None),
    "irons_spellbooks:dead_king": ("crown", "assets/irons_spellbooks/textures/entity/dead_king/dead_king.png", None),
    "irons_spellbooks:fire_boss": ("comet", None, ("#4a1f14", "#c2401a", "#ffb347")),
    "legendary_monsters:cloud_golem": ("cloud", "assets/legendary_monsters/textures/entity/cloud_golem/cloud_golem.png", None),
    "legendary_monsters:posessed_paladin": ("sword", None, ("#5a5f6b", "#b08d3a", "#e04545")),
    "legendary_monsters:the_obliterator": ("rift", None, ("#2a1840", "#6b2a8a", "#e05cff")),
    "mowziesmobs:ferrous_wroughtnaut": ("axe", None, ("#5b5e63", "#8a6b45", "#c9cdd2")),
    "mowziesmobs:frostmaw": ("snow", "assets/mowziesmobs/textures/entity/frostmaw.png", None),
    "mowziesmobs:sculptor": ("pillar", "assets/mowziesmobs/textures/entity/sculptor.png", None),
    "mowziesmobs:umvuthi": ("mask", "assets/mowziesmobs/textures/entity/umvuthi.png", None),
    "twilightforest:naga": ("snake", "assets/twilightforest/textures/entity/nagahead.png", None),
    "twilightforest:lich": ("cross", "assets/twilightforest/textures/entity/twilightlich64.png", None),
    "twilightforest:minoshroom": ("mushroom", "assets/twilightforest/textures/entity/minoshroomtaur.png", None),
    "twilightforest:hydra": ("hydra", "assets/twilightforest/textures/entity/hydra4.png", ("#2b2d2a", "#5a3a1f", "#ff6a2a")),
    "twilightforest:knight_phantom": ("shield", "assets/twilightforest/textures/entity/knightphantom.png", ("#2f3a36", "#6b7f72", "#b7f0c8")),
    "twilightforest:ur_ghast": ("tears", None, ("#d8d0c8", "#7a1f1f", "#ff5a3a")),
    "twilightforest:alpha_yeti": ("paw", "assets/twilightforest/textures/entity/yetialpha.png", ("#e6e6e6", "#9aa3ad", "#5fb4e8")),
    "twilightforest:snow_queen": ("icicle", "assets/twilightforest/textures/entity/snowqueen.png", ("#cfe6f2", "#7fb1d9", "#3f86d6")),
    "twilightforest:plateau_boss": ("keep", None, ("#4d4a3f", "#8c7d55", "#e8d48a")),
    "block_factorys_bosses:infernal_dragon": ("wing", None, ("#3b1010", "#9e2a14", "#ff8a2a")),
    "block_factorys_bosses:yeti": ("paw", "assets/block_factorys_bosses/textures/entity/yeti_boss.png", None),
    "block_factorys_bosses:sandworm": ("maw", "assets/block_factorys_bosses/textures/entity/sandworm.png", None),
    "block_factorys_bosses:underworld_knight": ("helm", None, ("#2a2a2e", "#7a2a14", "#ff7a2a")),
    "block_factorys_bosses:kraken": ("tentacle", "assets/block_factorys_bosses/textures/entity/kraken.png", ("#1f3a4a", "#3d6b6b", "#7fe0c8")),
    "alexsmobs:void_worm": ("portal", "assets/alexsmobs/textures/entity/void_worm/void_worm_body.png", None),
    "hybrid_aquatic:karkinos": ("pincer", "assets/hybrid_aquatic/textures/entity/miniboss/karkinos/karkinos.png", ("#a8342a", "#e0a060", "#ffd0a0")),
    "graveyard:lich": ("hourglass", "assets/graveyard/textures/entity/lich_texture.png", None),
}


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def shade(rgb, f):
    """f < 1 darkens, f > 1 lightens (towards white)."""
    if f <= 1:
        return tuple(max(0, int(c * f)) for c in rgb)
    return tuple(min(255, int(c + (255 - c) * (f - 1))) for c in rgb)


def palette_from_texture(img):
    """(cloth, rope, emblem) from an entity texture: cloth = most common solid colour band,
    rope = the most common colour clearly different from it, emblem = the brightest saturated one."""
    img = img.convert("RGBA")
    counts = {}
    for r, g, b, a in img.get_flattened_data():
        if a < 200:
            continue
        key = (r // 24 * 24 + 12, g // 24 * 24 + 12, b // 24 * 24 + 12)
        counts[key] = counts.get(key, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: -kv[1])
    if not ranked:
        return None

    def dist(a, b):
        return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5

    def hsv(c):
        return colorsys.rgb_to_hsv(*(x / 255 for x in c))

    # cloth: most common colour that isn't nearly black or white
    cloth = next((c for c, _ in ranked if 0.12 < hsv(c)[2] < 0.92), ranked[0][0])
    rope = next((c for c, _ in ranked if dist(c, cloth) > 70 and hsv(c)[2] > 0.12), shade(cloth, 0.6))
    top = [c for c, n in ranked[:40] if n >= 3]
    emblem = max(top, key=lambda c: hsv(c)[1] * 0.6 + hsv(c)[2] * 0.4 + (0.3 if dist(c, cloth) > 90 else 0))
    if dist(emblem, cloth) < 70:
        emblem = shade(cloth, 1.7)
    return cloth, rope, emblem


def find_texture(mods, path):
    for f in sorted(os.listdir(mods)):
        if not f.endswith(".jar"):
            continue
        try:
            with zipfile.ZipFile(os.path.join(mods, f)) as z:
                if path in z.namelist():
                    return Image.open(io.BytesIO(z.read(path)))
        except zipfile.BadZipFile:
            continue
    return None


def draw_bag(cloth, rope, emblem, emblem_name):
    cols = {
        "O": shade(cloth, 0.35), "D": shade(cloth, 0.72), "M": cloth, "L": shade(cloth, 1.35),
        "R": rope, "r": shade(rope, 0.65),
    }
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(SACK):
        for x, ch in enumerate(row):
            if ch in cols:
                px[x, y] = cols[ch] + (255,)
    ex, ey = EMBLEM_AT
    for dy, row in enumerate(EMBLEMS[emblem_name]):
        for dx, ch in enumerate(row):
            if ch == "E":
                px[ex + dx, ey + dy] = emblem + (255,)
            elif ch == "e":
                px[ex + dx, ey + dy] = shade(emblem, 0.6) + (255,)
    return img


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mods", required=True)
    ap.add_argument("--preview")
    a = ap.parse_args()

    tex_dir = os.path.join(ASSETS, "textures/item/boss_bag")
    os.makedirs(tex_dir, exist_ok=True)
    overrides, numbers, sheet = [], {}, []
    for n, (boss, (emblem, tex, manual)) in enumerate(sorted(BOSSES.items()), start=1):
        if manual:
            cloth, rope, em = (hexrgb(c) for c in manual)
        else:
            img = find_texture(a.mods, tex) if tex else None
            pal = palette_from_texture(img) if img else None
            if not pal:
                raise SystemExit(f"{boss}: texture {tex} not found; give it a hand-picked palette")
            cloth, rope, em = pal
        name = boss.replace(":", "_")
        bag = draw_bag(cloth, rope, em, emblem)
        bag.save(os.path.join(tex_dir, f"{name}.png"))
        write_json(os.path.join(ASSETS, f"models/item/boss_bag/{name}.json"),
                   {"parent": "minecraft:item/generated", "textures": {"layer0": f"strata:item/boss_bag/{name}"}})
        overrides.append({"predicate": {"custom_model_data": n}, "model": f"strata:item/boss_bag/{name}"})
        numbers[boss] = n
        sheet.append((boss, bag))

    # default bag (no boss): the Ignis-free neutral one, a plain leather sack with a star
    plain = draw_bag(hexrgb("#7a5230"), hexrgb("#c9a46a"), hexrgb("#f4d35e"), "star")
    plain.save(os.path.join(tex_dir, "default.png"))
    write_json(os.path.join(ASSETS, "models/item/boss_bag.json"),
               {"parent": "minecraft:item/generated", "textures": {"layer0": "strata:item/boss_bag/default"},
                "overrides": overrides})
    with open(MODEL_SCRIPT, "w", encoding="utf-8", newline="\n") as f:
        f.write("// Generated by tools/build_boss_bags.py: boss ID -> custom_model_data of its bag texture.\n")
        f.write("const bossBagModels = " + json.dumps(numbers, indent=2) + "\n")

    if a.preview:
        scale, cols = 6, 10
        cell = 16 * scale + 8
        rows = (len(sheet) + cols) // cols
        out = Image.new("RGBA", (cols * cell, rows * (cell + 14)), (40, 40, 44, 255))
        d = ImageDraw.Draw(out)
        for i, (boss, bag) in enumerate(sheet + [("default", plain)]):
            x, y = (i % cols) * cell, (i // cols) * (cell + 14)
            out.paste(bag.resize((16 * scale, 16 * scale), Image.NEAREST), (x + 4, y + 4), bag.resize((16 * scale, 16 * scale), Image.NEAREST))
            d.text((x + 4, y + cell - 2), boss.split(":")[-1][:16], fill=(220, 220, 220, 255))
        out.save(a.preview)
    print(f"{len(sheet)} boss bags written")


if __name__ == "__main__":
    main()
