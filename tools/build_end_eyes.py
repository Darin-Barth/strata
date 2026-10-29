"""Generate the End portal eye rework (docs/end-eyes.md): every eye has one fixed, guaranteed source.

  * bosses: the Wither, the Elder Guardian, Ignis, the Netherite Monstrosity and the Harbinger always drop
    their eye (boss loot bags roll the boss's table for every player in the fight)
  * places: one treasure chest type per eye, always holding it (Lootr gives every player their own copy)
  * crafting: the Rogue Eye (Create sequenced assembly, then cured in a soul-fire fan) and the Magical Eye
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
  * assets/strata/textures/item/{incomplete_rogue_eye,uncured_rogue_eye,dormant_magical_eye}.png
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
    # Rogue Eye, step 1: a Create production line. Two loops of: deploy a precision mechanism, deploy an
    # electron tube, pour in lava, press.
    "rogue_eye_assembly": {
        "type": "create:sequenced_assembly", "ingredient": ing("minecraft:ender_eye"), "loops": 2,
        "results": [{"id": f"{NS}:uncured_rogue_eye"}], "transitional_item": {"id": INC},
        "sequence": [
            {"type": "create:deploying", "ingredients": [ing(INC), ing("create:precision_mechanism")],
             "results": [{"id": INC}]},
            {"type": "create:deploying", "ingredients": [ing(INC), ing("create:electron_tube")],
             "results": [{"id": INC}]},
            {"type": "create:filling", "ingredients": [ing(INC), {"type": "neoforge:single", "amount": 250,
                                                                   "fluid": "minecraft:lava"}],
             "results": [{"id": INC}]},
            {"type": "create:pressing", "ingredients": [ing(INC)], "results": [{"id": INC}]},
        ]},
    # Rogue Eye, step 2: cured in an Encased Fan's soul-fire stream ("haunting"). No other block does this.
    "rogue_eye_curing": {"type": "create:haunting", "ingredients": [ing(f"{NS}:uncured_rogue_eye")],
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
    "rogue_eye": "It taught our ancestors Redstone. Only a working machine can build it again",
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


def textures(mods, out):
    jar = next(os.path.join(mods, f) for f in os.listdir(mods) if f.startswith("endrem"))
    z = zipfile.ZipFile(jar)

    def tex(name):  # first 16x16 frame (some eyes are animated strips)
        im = Image.open(io.BytesIO(z.read(f"assets/endrem/textures/item/{name}.png"))).convert("RGBA")
        return im.crop((0, 0, im.width, im.width))

    def tint(im, rgb, amount):
        over = Image.new("RGBA", im.size, rgb + (255,))
        mixed = Image.blend(im, over, amount)
        mixed.putalpha(im.getchannel("A"))
        return mixed

    rogue = tex("rogue_eye")
    incomplete = ImageEnhance.Brightness(ImageEnhance.Color(rogue).enhance(0.15)).enhance(0.75)
    uncured = tint(ImageEnhance.Color(rogue).enhance(0.4), (214, 140, 40), 0.45)
    dormant = ImageEnhance.Brightness(ImageEnhance.Color(tex("magical_eye")).enhance(0.1)).enhance(0.6)
    d = os.path.join(out, "assets", NS, "textures", "item")
    os.makedirs(d, exist_ok=True)
    for name, im in (("incomplete_rogue_eye", incomplete), ("uncured_rogue_eye", uncured),
                     ("dormant_magical_eye", dormant)):
        im.save(os.path.join(d, name + ".png"))


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
