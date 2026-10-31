"""Generate the End portal eye rework (docs/end-eyes.md): every eye has one fixed, guaranteed source.

  * bosses: the Wither, the Elder Guardian, Ignis, the Netherite Monstrosity and the Harbinger always drop
    their eye (boss loot bags roll the boss's table for every player in the fight)
  * places: one treasure chest type per eye, always holding it (Lootr gives every player their own copy)
  * crafting: the Rogue Eye (Create sequenced assembly, comes off red-hot, then quenched in a water fan) and the Magical Eye
    (Ars Nouveau Enchanting Apparatus, then awakened in an Imbuement Chamber)
  * spares: Undead, Witch and Exotic Eyes keep End Remastered's own recipes; the portal takes any 12
    different eyes, so they stand in for an eye someone can't or won't get. The Cryptic Eye (enchanting
    luck) and the Evil Eye's Cleric trade are off in config/EndRemastered-NeoForge/endrem.json.

Writes into kubejs/data (and kubejs/assets for textures and lore):
  * endrem/loot_table/minecraft/...: End Remastered's own injected tables, emptied (no eyes in random chests
    or from Evokers) or set to 100% (Wither, Elder Guardian)
  * strata/loot_table/end_eyes/<eye>.json + strata/loot_modifiers/end_eyes/...: add_table modifiers
  * strata/recipe/end_eyes/*.json: the Rogue and Magical Eye recipes
  * strata/tags/worldgen/structure/seeker/<key>.json: what each Seeker's Compass finds
    (server_scripts/strata_end_eyes.js makes the compasses and points them)
  * assets/strata/textures/item/{incomplete_rogue_eye,red_hot_rogue_eye,dormant_magical_eye}.png
  * assets/endrem/textures/{item,block/eyes}/rogue_eye.png: the Rogue Eye redrawn as a machine (brass gear housing,
    green lens), in the hand and in the portal frame
  * assets/endrem/lang/en_us.json: the eyes' lore lines, rewritten to name where each eye rests

Run from the repo root (needs Pillow; re-run after an End Remastered, Create, Ars Nouveau or structure-mod
update, and check the IDs below still exist):
  python tools/build_end_eyes.py --mods <server or client mods dir>
"""
import argparse
import io
import json
import os
import zipfile

from PIL import Image, ImageEnhance

NS = "strata"

# eye -> loot tables that always give it (chest tables: one chest type per eye; entity tables: bosses)
SOURCES = {
    "old_eye": ["betterdeserttemples:chests/tomb_pharaoh"],
    "evil_eye": ["betterjungletemples:chests/treasure"],
    "lost_eye": ["dungeons_arise:chests/foundry/foundry_treasure"],
    "black_eye": ["dungeons_arise_seven_seas:chests/corsair_corvette/corsair_corvette_treasure",
                  "dungeons_arise_seven_seas:chests/pirate_junk/pirate_junk_treasure",
                  "dungeons_arise:chests/undead_pirate_ship/undead_pirate_ship_treasure"],
    "cold_eye": ["minecraft:chests/igloo_chest"],  # igloo basements and the Frostbitten Temple
    "cursed_eye": ["cataclysm:entities/ignis"],
    "nether_eye": ["cataclysm:entities/netherite_monstrosity"],
    "corrupted_eye": ["cataclysm:entities/the_harbinger"],
}
# End Remastered's own tables (injected by the mod): chests and Evokers give nothing, these two always drop
ENDREM_EMPTY = ["chests/" + t for t in (
    "abandoned_mineshaft", "bastion_treasure", "buried_treasure", "desert_pyramid", "igloo_chest",
    "jungle_temple", "nether_bridge", "pillager_outpost", "shipwreck_treasure", "simple_dungeon",
    "woodland_mansion")] + ["entities/evoker"]
ENDREM_ALWAYS = {"entities/wither": "wither_eye", "entities/elder_guardian": "guardian_eye"}

# Seeker's Compass key -> structures it points to (missing mods are skipped: required false). YUNG's temples and
# monuments replace the vanilla ones in this pack, so the vanilla IDs would only add empty search spots.
SEEKERS = {
    "old": ["betterdeserttemples:desert_temple"],
    "evil": ["betterjungletemples:jungle_temple"],
    "lost": ["dungeons_arise:foundry"],
    "black": ["dungeons_arise_seven_seas:corsair_corvette", "dungeons_arise_seven_seas:pirate_junk",
              "dungeons_arise:undead_pirate_ship"],
    "cold": ["legendary_monsters:frostbitten_temple"],
    "guardian": ["betteroceanmonuments:ocean_monument"],
}


def item(i, count=1):
    return {"count": count, "id": i}


def ing(i):
    return {"tag": i[1:]} if i.startswith("#") else {"item": i}


INC = f"{NS}:incomplete_rogue_eye"
RECIPES = {
    # Rogue Eye, step 1: a Create production line. Two loops of: deploy a brass sheet (the housing), deploy a
    # precision mechanism, deploy an electron tube, pour in lava (it heats the metal), press. It comes off red-hot.
    "rogue_eye_assembly": {
        "type": "create:sequenced_assembly", "ingredient": ing("minecraft:ender_eye"), "loops": 2,
        "results": [{"id": f"{NS}:red_hot_rogue_eye"}], "transitional_item": {"id": INC},
        "sequence": [
            {"type": "create:deploying", "ingredients": [ing(INC), ing("create:brass_sheet")],
             "results": [{"id": INC}]},
            {"type": "create:deploying", "ingredients": [ing(INC), ing("create:precision_mechanism")],
             "results": [{"id": INC}]},
            {"type": "create:deploying", "ingredients": [ing(INC), ing("create:electron_tube")],
             "results": [{"id": INC}]},
            {"type": "create:filling", "ingredients": [ing(INC), {"type": "neoforge:single", "amount": 250,
                                                                   "fluid": "minecraft:lava"}],
             "results": [{"id": INC}]},
            {"type": "create:pressing", "ingredients": [ing(INC)], "results": [{"id": INC}]},
        ]},
    # Rogue Eye, step 2: hardened by quenching: an Encased Fan blowing through water ("splashing", Create's Bulk
    # Washing). No other block does this.
    "rogue_eye_quenching": {"type": "create:splashing", "ingredients": [ing(f"{NS}:red_hot_rogue_eye")],
                            "results": [{"id": "endrem:rogue_eye"}]},
    # Magical Eye, step 1: bound on the Enchanting Apparatus with every essence.
    "magical_eye_binding": {
        "type": "ars_nouveau:enchanting_apparatus", "keepNbtOfReagent": False,
        "reagent": ing("minecraft:ender_eye"), "result": item(f"{NS}:dormant_magical_eye"), "sourceCost": 5000,
        "pedestalItems": [ing("ars_nouveau:" + e + "_essence") for e in (
            "fire", "water", "earth", "air", "abjuration", "conjuration", "manipulation")]
        + [ing("ars_nouveau:source_gem_block")]},
    # Magical Eye, step 2: awakened in an Imbuement Chamber (slowly drinks source from nearby jars).
    "magical_eye_awakening": {
        "type": "ars_nouveau:imbuement", "input": ing(f"{NS}:dormant_magical_eye"),
        "output": item("endrem:magical_eye"), "source": 5000,
        "pedestalItems": [ing("minecraft:amethyst_cluster"), ing("minecraft:ghast_tear"),
                          ing("ars_nouveau:source_gem_block")]},
}

S7 = "§7§o"
LORE = {  # item.endrem.<eye>.description: the old legend, plus where the eye rests now
    "old_eye": "Buried with the Pharaoh, who swore to watch over the desert until the end of days",
    "evil_eye": "A holy talisman against bad luck, hidden behind a hundred traps in the jungle temples",
    "lost_eye": "Forged by the first blacksmiths in the fires of the Foundry, and lost among its furnaces",
    "black_eye": "It gave sight to the legendary Black Pearl. Pirate captains still fight over it",
    "cold_eye": "The Iceologers sealed it in ice before they vanished: in the Frostbitten Temple and some "
                "igloo cellars",
    "wither_eye": "Has witnessed destruction. Maybe it also witnessed your stuff disappear",
    "guardian_eye": "It has seen many warriors drown. The Elder Guardian keeps it in the ocean monument",
    "cursed_eye": "Ignis swore to guard it in the Burning Arena, and the oath burned itself into him",
    "nether_eye": "Lost by a demon in the war between the Aether and the Nether, now locked in the "
                  "Netherite Monstrosity's forge-heart",
    "corrupted_eye": "The eye of a greedy king, wired into the Harbinger by those who wanted his fortune",
    "rogue_eye": "The machine eye that taught our ancestors Redstone. Only a working factory can forge another",
    "magical_eye": "Without this eye the Evoker has no power. Bound by an enchanter, woken with source",
    "undead_eye": "Remembrance of the past lives of those who live in death. A spare eye",
    "witch_eye": "It saw the ancient brewing recipes lost in time. A spare eye",
    "exotic_eye": "Those who followed it found Atlantis and were never seen again. A spare eye",
    "cryptic_eye": "The sixteenth eye. No one has ever found it",
}


def write(root, rel, data):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def one_item_table(kind, iid):
    return {"type": f"minecraft:{kind}", "pools": [{"rolls": 1, "entries": [
        {"type": "minecraft:item", "name": iid}]}]}



# The Rogue Eye as a machine: a gear-toothed brass housing, a steel inner ring with rivets, a glowing lens.
# "incomplete" is the bare steel frame on the assembly line, "hot" is fresh off the press, "done" is quenched.
MACHINE = {  # light, mid, dark per part; outline
    "done": {"housing": ("f2c25a", "c58a2e", "8a5a1e"), "ring": ("6b7480", "4f5760", "343a42"),
             "lens": ("8dffb0", "13bf4a", "0b7a30"), "pupil": "06331a", "glint": "e6fff0", "rivet": "fff0b0",
             "outline": "2a1a0a"},
    "hot": {"housing": ("ffc46a", "f07a22", "b23e10"), "ring": ("e0662a", "b8461a", "7a2a10"),
            "lens": ("fff0a0", "ffb030", "e06a10"), "pupil": "7a1e06", "glint": "fffbe0", "rivet": "fff2c0",
            "outline": "3a0c04"},
    "incomplete": {"housing": ("d9b25e", "a8803a", "735420"), "ring": ("5c646d", "444b53", "2e3339"),
                   "lens": ("23272c", "1b1e22", "141619"), "pupil": "0e1012", "glint": None, "rivet": "e8d8a8",
                   "outline": "2a1a0a"},
}


def hexc(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def machine_eye(variant, pal=None):
    import math
    pal = pal or MACHINE[variant]
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    missing = {1, 4, 6} if variant == "incomplete" else set()  # teeth not fitted yet
    for y in range(16):
        for x in range(16):
            dx, dy = x - 7.5, y - 7.5
            r = math.hypot(dx, dy)
            light = -(dx + dy) / (r * 1.414) if r else 0
            shade = 0 if light > 0.45 else (2 if light < -0.35 else 1)
            ang = math.degrees(math.atan2(dy, dx)) % 360
            tooth = round(ang / 45) % 8
            on_tooth = abs(ang - round(ang / 45) * 45) <= 12 and tooth not in missing
            if r <= 1.6:
                c = pal["pupil"]
            elif r <= 4.0:
                c = pal["lens"][shade]
            elif r <= 5.0:
                c = pal["ring"][shade]
            elif r <= 6.4:
                c = pal["housing"][shade]
                if abs(r - 5.6) < 0.6 and abs((ang - 45) % 90 - 45) > 38:
                    c = pal["rivet"]
            elif r <= 7.7 and on_tooth:
                c = pal["housing"][shade]
            else:
                continue
            im.putpixel((x, y), hexc(c))
    if pal["glint"]:
        im.putpixel((6, 6), hexc(pal["glint"]))
    out = im.copy()
    for y in range(16):
        for x in range(16):
            if im.getpixel((x, y))[3]:
                continue
            if any(0 <= x + a < 16 and 0 <= y + b < 16 and im.getpixel((x + a, y + b))[3]
                   for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out.putpixel((x, y), hexc(pal["outline"]))
    return out


# The Red-Hot Rogue Eye pulses: frames blend the hot colours toward white-hot and back (an animated strip).
WHITE_HOT = {"housing": ("fff4c8", "ffd27a", "ff8a2a"), "ring": ("ffb060", "f0802a", "c0501a"),
             "lens": ("fffff0", "ffe8a0", "ffb040"), "pupil": "c04010", "glint": "ffffff", "rivet": "fffbe8",
             "outline": "5a1806"}
HOT_PULSE = (0.0, 0.2, 0.45, 0.65, 0.45, 0.2)


def mix(a, b, t):
    ca, cb = hexc(a), hexc(b)
    return "".join(f"{round(ca[i] + (cb[i] - ca[i]) * t):02x}" for i in range(3))


def hot_eye():
    frames = []
    for t in HOT_PULSE:
        pal = {}
        for k, v in MACHINE["hot"].items():
            w = WHITE_HOT[k]
            pal[k] = tuple(mix(a, b, t) for a, b in zip(v, w)) if isinstance(v, tuple) else mix(v, w, t)
        frames.append(machine_eye("hot", pal))
    strip = Image.new("RGBA", (16, 16 * len(frames)), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        strip.alpha_composite(f, (0, 16 * i))
    return strip


FRAME_TOP = ["rbbbbbbr",  # the Rogue Eye seated in a portal frame, seen from above (8x8, used twice)
             "bsssssst",
             "bsLGGgst",
             "bsGPPgst",
             "bsGPPgst",
             "bsgggSst",
             "bstttttt",
             "rtttttTr"]
FRAME_KEY = {"r": "fff0b0", "b": "c58a2e", "t": "8a5a1e", "T": "5c3a12", "s": "4f5760", "S": "343a42",
             "L": "8dffb0", "G": "13bf4a", "g": "0b7a30", "P": "06331a"}


def frame_eye():
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    for ox in (8, 16):
        for y, row in enumerate(FRAME_TOP):
            for x, ch in enumerate(row):
                im.putpixel((ox + x, y), hexc(FRAME_KEY[ch]))
    for x in range(32):  # the sides: brass with a riveted band
        im.putpixel((x, 8), hexc("f2c25a"))
        im.putpixel((x, 9), hexc("fff0b0" if x % 8 in (2, 5) else "c58a2e"))
        im.putpixel((x, 10), hexc("8a5a1e"))
    return im


def textures(mods, out):
    jar = next(os.path.join(mods, f) for f in os.listdir(mods) if f.startswith("endrem"))
    z = zipfile.ZipFile(jar)

    def tex(name):  # first 16x16 frame (some eyes are animated strips)
        im = Image.open(io.BytesIO(z.read(f"assets/endrem/textures/item/{name}.png"))).convert("RGBA")
        return im.crop((0, 0, im.width, im.width))

    dormant = ImageEnhance.Brightness(ImageEnhance.Color(tex("magical_eye")).enhance(0.1)).enhance(0.6)
    d = os.path.join(out, "assets", NS, "textures", "item")
    os.makedirs(d, exist_ok=True)
    for name, im in (("incomplete_rogue_eye", machine_eye("incomplete")), ("red_hot_rogue_eye", hot_eye()),
                     ("dormant_magical_eye", dormant)):
        im.save(os.path.join(d, name + ".png"))
    with open(os.path.join(d, "red_hot_rogue_eye.png.mcmeta"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"animation": {"frametime": 4, "interpolate": True}}, f)
        f.write("\n")
    e = os.path.join(out, "assets", "endrem", "textures")
    os.makedirs(os.path.join(e, "item"), exist_ok=True)
    os.makedirs(os.path.join(e, "block", "eyes"), exist_ok=True)
    machine_eye("done").save(os.path.join(e, "item", "rogue_eye.png"))
    frame_eye().save(os.path.join(e, "block", "eyes", "rogue_eye.png"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mods", required=True)
    ap.add_argument("--kubejs", default="kubejs")
    a = ap.parse_args()
    data = os.path.join(a.kubejs, "data")
    entries = []
    for t in ENDREM_EMPTY:
        write(data, f"endrem/loot_table/minecraft/{t}.json",
              {"type": "minecraft:chest" if t.startswith("chests") else "minecraft:entity", "pools": []})
    for t, eye in ENDREM_ALWAYS.items():
        write(data, f"endrem/loot_table/minecraft/{t}.json", one_item_table("entity", "endrem:" + eye))
    for eye, tables in SOURCES.items():
        kind = "entity" if "entities/" in tables[0] else "chest"
        write(data, f"{NS}/loot_table/end_eyes/{eye}.json", one_item_table(kind, "endrem:" + eye))
        for table in tables:
            ns, path = table.split(":")
            name = f"end_eyes/{ns}/{path.split('/')[-1]}"
            write(data, f"{NS}/loot_modifiers/{name}.json", {"type": "neoforge:add_table", "conditions": [
                {"condition": "neoforge:loot_table_id", "loot_table_id": table}],
                "table": f"{NS}:end_eyes/{eye}"})
            entries.append(f"{NS}:{name}")
    glm_path = os.path.join(data, "neoforge/loot_modifiers/global_loot_modifiers.json")
    with open(glm_path, encoding="utf-8") as f:
        glm = json.load(f)
    glm["entries"] = [e for e in glm["entries"] if not e.startswith(f"{NS}:end_eyes/")] + entries
    write(data, "neoforge/loot_modifiers/global_loot_modifiers.json", glm)
    for name, r in RECIPES.items():
        write(data, f"{NS}/recipe/end_eyes/{name}.json", r)
    for key, structures in SEEKERS.items():
        write(data, f"{NS}/tags/worldgen/structure/seeker/{key}.json",
              {"values": [{"id": s, "required": False} for s in structures]})
    write(os.path.join(a.kubejs, "assets"), "endrem/lang/en_us.json",
          {f"item.endrem.{e}.description": S7 + text for e, text in LORE.items()})
    textures(a.mods, a.kubejs)
    print(f"End eyes: {len(entries)} loot modifiers, {len(RECIPES)} recipes, {len(SEEKERS)} compasses")


if __name__ == "__main__":
    main()
