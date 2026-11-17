"""Small data fixes for mods whose own files don't load in 1.21.1 (found in the Nov 16 boot-log review).

Each file overrides or completes a mod's data from kubejs/data. Re-run after one of these mods updates, and drop
an entry once the mod ships the fix itself (the boot log no longer names the file):

  * The Aether's Delight 0.1.4.2: its four "wings" loot modifiers are in the pre-1.21 format ("killer", "tag"),
    so Phygs and Flying Cows never dropped wings, the only source of aethersdelight:wing.
  * My Nether's Delight 1.10.4.1: its two bastion chest modifiers use "lootTable" where Farmer's Delight reads
    "table", so the additions never appeared.
  * Croptopia 4.2.4: Oatmeal and Rhubarb Crisp ask for the tag c:oats, which nothing defines.
  * Create: Interiors 0.6.1: re-dyeing a chair asks for c:<colour>_dyes, which nothing defines (32 recipes).

Run from the repo root:  python -I tools/build_mod_fixes.py
"""
import json
import pathlib

DATA = pathlib.Path(__file__).resolve().parent.parent / "kubejs" / "data"
COLOURS = ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan", "purple",
           "blue", "brown", "green", "red", "black"]


def write(path, obj):
    path = DATA / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8", newline="\n")


def loaded(*mods):
    return [{"type": "neoforge:mod_loaded", "modid": m} for m in mods]


def wings(mob, cooked):
    return {
        "neoforge:conditions": loaded("aethersdelight", "farmersdelight", "aether"),
        "type": "farmersdelight:add_item",
        "conditions": [
            {"condition": "minecraft:entity_properties", "entity": "attacker",
             "predicate": {"equipment": {"mainhand": {"items": "#farmersdelight:tools/knives"}}}},
            {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"flags": {"is_on_fire": cooked}}},
            {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"type": f"aether:{mob}"}},
            {"condition": "minecraft:random_chance_with_enchanted_bonus", "enchantment": "minecraft:looting",
             "unenchanted_chance": 0.5, "enchanted_chance": {"type": "minecraft:linear", "base": 0.6, "per_level_above_first": 0.1}},
        ],
        "item": "aethersdelight:cooked_wing" if cooked else "aethersdelight:wing",
    }


def main():
    count = 0
    for mob in ("phyg", "flying_cow"):
        for cooked in (False, True):
            write(f"aethersdelight/loot_modifiers/scavenging_{'cooked_' if cooked else ''}wings_from_{mob}.json", wings(mob, cooked))
            count += 1
    for chest in ("bastion_treasure", "bastion_hoglin_stable"):
        write(f"mynethersdelight/loot_modifiers/add_loot_{chest}.json", {
            "neoforge:conditions": loaded("mynethersdelight", "farmersdelight"),
            "type": "farmersdelight:add_loot_table",
            "conditions": [{"condition": "neoforge:loot_table_id", "loot_table_id": f"minecraft:chests/{chest}"}],
            "table": f"mynethersdelight:chests/mnd_{chest}",
        })
        count += 1
    write("c/tags/item/oats.json", {"values": [{"id": "croptopia:oat", "required": False}]})
    count += 1
    for colour in COLOURS:
        write(f"c/tags/item/{colour}_dyes.json", {"values": [{"id": f"#c:dyes/{colour}", "required": False}]})
        count += 1
    print(f"mod fixes: {count} files")


if __name__ == "__main__":
    main()
