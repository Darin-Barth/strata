"""Generate Strata's Inventory Pets loot (kubejs/data/...): pets are found, not crafted.

Design: pets should be fun finds in loot, not crafted (their recipes are removed in
kubejs/server_scripts/strata_pets.js), and the strong ones stay but are weaker (config and
upkeep food in config/inventorypets-common.toml). This writes:
  * three item tags, strata:pets/common, strata:pets/rare and strata:pets/legendary
  * one loot table per tier that gives one random pet from its tag
  * NeoForge add_table loot modifiers that add that table to structure chests with a chance:
    common pets in early structures, rare ones in strongholds, mansions, fortresses and the
    like, legendary ones only in end-game chests (End cities, ancient cities, bastion treasure)
Lootr makes those chests per player, so every player gets their own roll.

Left out: the House and End Portal pets (disabled in the config, teleports), the holiday and
April Fools pets, and the Meta pets (they only turn pets into other pets).

Run from the repo root (re-run after an Inventory Pets update adds pets):
  python -I tools/build_pet_loot.py --out kubejs/data
"""
import argparse
import json
import os

NS = "strata"

TIERS = {
    # cute, cozy and handy pets
    "common": ["chicken", "cow", "mooshroom", "ocelot", "pig", "sheep", "squid", "wolf", "siamese",
               "torch", "banana", "apple", "cheetah", "heart", "shield", "dubstep", "moon", "lead",
               "quiver", "sponge", "spider", "snow_golem", "creeper", "magma_cube", "blaze", "ghast",
               "bed", "brewing_stand", "chest", "crafting_table", "double_chest", "enchanting_table",
               "ender_chest", "jukebox", "saddle", "cobblestone", "dirt"],
    # pets that stand in for a machine, a mining trip or a lot of armor
    "rare": ["anvil", "furnace", "iron_golem", "enderman", "nether_portal", "flying_saddle", "biome",
             "dingot", "pingot", "loot", "pixie", "purplicious_cow", "qcm", "mickerson", "juggernaut",
             "illuminati", "pacman", "silverfish"],
    # the mod's own legendary pets
    "legendary": ["black_hole", "slime", "wither", "sun", "cloud", "pufferfish"],
}

# chest loot table -> chance that one pet of that tier is added
CHESTS = {
    "common": 0.08,
    "rare": 0.08,
    "legendary": 0.05,
}
TABLES = {
    "common": [
        "minecraft:chests/simple_dungeon", "minecraft:chests/abandoned_mineshaft",
        "minecraft:chests/desert_pyramid", "minecraft:chests/jungle_temple",
        "minecraft:chests/shipwreck_treasure", "minecraft:chests/buried_treasure",
        "minecraft:chests/igloo_chest", "minecraft:chests/pillager_outpost",
        "minecraft:chests/ruined_portal",
        "betterdungeons:small_dungeon/chests/loot_piles", "betterdungeons:skeleton_dungeon/chests/common",
        "betterdungeons:zombie_dungeon/chests/common", "betterdungeons:spider_dungeon/chests/egg_room",
        "betterdeserttemples:chests/storage", "betterjungletemples:chests/campsite",
        "betterwitchhuts:chests/hut_0",
    ],
    "rare": [
        "minecraft:chests/stronghold_library", "minecraft:chests/stronghold_corridor",
        "minecraft:chests/woodland_mansion", "minecraft:chests/nether_bridge",
        "minecraft:chests/bastion_other", "minecraft:chests/trial_chambers/reward",
        "betterdungeons:skeleton_dungeon/chests/middle", "betterdungeons:zombie_dungeon/chests/tombstone",
        "betterdeserttemples:chests/tomb", "betterjungletemples:chests/treasure",
        "betterfortresses:chests/keep", "betterfortresses:chests/hall",
        "betteroceanmonuments:chests/upper_side_chamber",
        "integrated_stronghold:chests/grand_library", "integrated_stronghold:chests/treasure",
        "integrated_stronghold:chests/armory",
    ],
    "legendary": [
        "minecraft:chests/end_city_treasure", "minecraft:chests/ancient_city",
        "minecraft:chests/bastion_treasure", "minecraft:chests/trial_chambers/reward_ominous",
        "betterdeserttemples:chests/tomb_pharaoh", "integrated_stronghold:chests/sanctorum",
    ],
}


def write(out, rel, data):
    path = os.path.join(out, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="kubejs/data")
    out = ap.parse_args().out
    entries = []
    for tier, pets in TIERS.items():
        write(out, f"{NS}/tags/item/pets/{tier}.json", {"values": [f"inventorypets:pet_{p}" for p in pets]})
        write(out, f"{NS}/loot_table/inject/pets_{tier}.json", {"type": "minecraft:chest", "pools": [{
            "rolls": 1, "entries": [{"type": "minecraft:tag", "name": f"{NS}:pets/{tier}", "expand": True}]}]})
        for table in TABLES[tier]:
            ns, path = table.split(":")
            name = f"pets/{tier}/{ns}/{path.replace('chests/', '')}"
            write(out, f"{NS}/loot_modifiers/{name}.json", {"type": "neoforge:add_table", "conditions": [
                {"condition": "neoforge:loot_table_id", "loot_table_id": table},
                {"condition": "minecraft:random_chance", "chance": CHESTS[tier]}],
                "table": f"{NS}:inject/pets_{tier}"})
            entries.append(f"{NS}:{name}")
    glm_path = os.path.join(out, "neoforge/loot_modifiers/global_loot_modifiers.json")
    with open(glm_path, encoding="utf-8") as f:
        glm = json.load(f)
    glm["entries"] = [e for e in glm["entries"] if not e.startswith(f"{NS}:pets/")] + entries
    write(out, "neoforge/loot_modifiers/global_loot_modifiers.json", glm)
    print(f"Pet loot: {sum(len(p) for p in TIERS.values())} pets in {len(TIERS)} tiers, "
          f"{len(entries)} chest loot tables, written to {out}")


if __name__ == "__main__":
    main()
