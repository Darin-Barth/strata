"""Generate Strata's quest loot bags (kubejs/...): quests give a loot bag; opening it rolls a rarity
(Common, Uncommon, Rare, Epic, Legendary), then one item from that rarity's pool.

Four bags, one per quest tier, with better rarity odds the bigger the quest. Writes:
  * kubejs/data/strata/loot_table/loot_bags/<rarity>.json: one pool per rarity (items from across
    the pack; no flight, teleport or wireless items, no gate materials)
  * kubejs/server_scripts/strata_loot_bag_odds.js: bag -> rarity weights (read by strata_loot_bags.js)
  * kubejs/assets/strata/textures/item/<bag>.png: the bag textures (same sack as the boss bags).
    Each tier looks more special: the Small bag is plain; the Loot Bag twinkles now and then; the
    Large bag twinkles more (and has the enchantment glint, set in startup_scripts/strata_loot_bags.js);
    the Grand bag has golden sparkles all around and a pulsing emblem (and the glint). Animated
    textures are vertical frame strips with a .png.mcmeta.
Check every item ID with the quest checker's registry (tools/quests/registry.json) when editing pools.

Run from the repo root (needs Pillow): python tools/build_quest_bags.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from build_boss_bags import draw_bag, hexrgb  # noqa: E402

DATA = "kubejs/data/strata/loot_table/loot_bags"
ODDS_SCRIPT = "kubejs/server_scripts/strata_loot_bag_odds.js"
TEXTURES = "kubejs/assets/strata/textures/item"
REGISTRY = "tools/quests/registry.json"

RARITIES = ["common", "uncommon", "rare", "epic", "legendary"]

# bag item -> (display name, cloth, rope, emblem colour, rarity weights in RARITIES order)
# (sparkle count, sparkle colour, emblem pulse) per bag for the animated effect; 0 sparkles = static.
BAGS = {
    "loot_bag_small": ("Small Loot Bag", "#8a5a32", "#c9a46a", "#f2efe6", [70, 22, 6, 1.8, 0.2]),
    "loot_bag": ("Loot Bag", "#2f5d9e", "#c9a46a", "#f4d35e", [50, 30, 14, 5, 1]),
    "loot_bag_large": ("Large Loot Bag", "#5b2f8a", "#d8b45a", "#f4d35e", [25, 35, 25, 12, 3]),
    "loot_bag_grand": ("Grand Loot Bag", "#c9962a", "#7a4a12", "#fff6d5", [0, 25, 40, 27, 8]),
}

# rarity -> [(item or #tag, count, weight)]; one entry is rolled per bag.
POOLS = {
    "common": [
        ("minecraft:bread", 16, 8), ("minecraft:cooked_beef", 12, 8), ("minecraft:torch", 64, 8),
        ("minecraft:iron_ingot", 12, 10), ("minecraft:copper_ingot", 24, 8), ("minecraft:coal", 32, 8),
        ("minecraft:oak_log", 32, 6), ("minecraft:experience_bottle", 6, 6), ("minecraft:arrow", 32, 5),
        ("minecraft:string", 16, 4), ("minecraft:bone_meal", 24, 5),
        ("create:andesite_alloy", 16, 8), ("create:zinc_ingot", 8, 6), ("mekanism:ingot_osmium", 12, 6),
        ("farmersdelight:hamburger", 4, 5), ("farmersdelight:beef_stew", 3, 4), ("supplementaries:rope", 32, 4),
        ("sophisticatedbackpacks:upgrade_base", 2, 4), ("ars_nouveau:source_gem", 4, 6),
        ("apotheosis:mysterious_scrap_metal", 4, 5), ("numismatics:bevel", 4, 5), ("cobblemon:poke_ball", 8, 4),
    ],
    "uncommon": [
        ("minecraft:gold_ingot", 12, 8), ("minecraft:diamond", 3, 8), ("minecraft:redstone", 48, 8),
        ("minecraft:lapis_lazuli", 32, 6), ("minecraft:emerald", 12, 6), ("minecraft:ender_pearl", 6, 5),
        ("minecraft:golden_carrot", 16, 6), ("minecraft:name_tag", 2, 4), ("minecraft:saddle", 1, 3),
        ("minecraft:quartz", 32, 5), ("apotheosis:gem_dust", 8, 5),
        ("create:brass_ingot", 8, 7), ("create:electron_tube", 4, 5), ("mekanism:basic_control_circuit", 4, 6),
        ("mekanism:alloy_infused", 4, 5), ("ae2:certus_quartz_crystal", 16, 6), ("ae2:fluix_crystal", 8, 5),
        ("ars_nouveau:magebloom_fiber", 8, 5), ("irons_spellbooks:arcane_essence", 16, 6),
        ("irons_spellbooks:common_ink", 4, 4), ("immersiveengineering:ingot_steel", 8, 6),
        ("occultism:silver_ingot", 8, 5), ("sophisticatedbackpacks:stack_upgrade_tier_1", 1, 3),
        ("apotheosis:timeworn_fabric", 4, 5), ("numismatics:cog", 2, 5), ("cobblemon:great_ball", 8, 4),
        ("#strata:pets/common", 1, 4),
    ],
    "rare": [
        ("minecraft:diamond", 8, 8), ("minecraft:emerald", 24, 6), ("minecraft:netherite_scrap", 2, 5),
        ("minecraft:golden_apple", 4, 6), ("minecraft:experience_bottle", 32, 6), ("minecraft:shulker_shell", 2, 4),
        ("minecraft:blaze_rod", 8, 5), ("apotheosis:sigil_of_socketing", 2, 5), ("apotheosis:gem_dust", 24, 4),
        ("minecraft:diamond_block", 1, 4), ("create:precision_mechanism", 4, 6),
        ("mekanism:advanced_control_circuit", 4, 6), ("mekanism:alloy_reinforced", 4, 5),
        ("ae2:engineering_processor", 4, 5), ("ae2:cell_component_16k", 1, 4),
        ("ars_nouveau:manipulation_essence", 2, 4), ("ars_nouveau:abjuration_essence", 2, 4),
        ("irons_spellbooks:rare_ink", 2, 4), ("irons_spellbooks:arcane_ingot", 2, 4),
        ("sophisticatedbackpacks:stack_upgrade_tier_2", 1, 3), ("apotheosis:luminous_crystal_shard", 3, 5),
        ("minecraft:trial_key", 2, 3), ("numismatics:crown", 1, 4), ("cobblemon:ultra_ball", 4, 4),
        ("cobblemon:rare_candy", 1, 3), ("#strata:pets/rare", 1, 3),
    ],
    "epic": [
        ("minecraft:netherite_ingot", 1, 6), ("minecraft:diamond_block", 4, 8),
        ("minecraft:enchanted_golden_apple", 1, 4), ("minecraft:totem_of_undying", 1, 4),
        ("minecraft:experience_bottle", 64, 6), ("apotheosis:sigil_of_enhancement", 1, 4),
        ("apotheosis:sigil_of_socketing", 4, 5), ("minecraft:emerald_block", 6, 5),
        ("mekanism:elite_control_circuit", 4, 5), ("ae2:cell_component_64k", 1, 4),
        ("irons_spellbooks:epic_ink", 1, 4), ("sophisticatedbackpacks:stack_upgrade_tier_3", 1, 3),
        ("apotheosis:arcane_sands", 3, 5), ("minecraft:ominous_trial_key", 1, 3), ("minecraft:breeze_rod", 6, 3),
        ("numismatics:crown", 3, 4), ("cobblemon:rare_candy", 3, 3), ("ars_nouveau:source_gem_block", 8, 4),
    ],
    "legendary": [
        ("minecraft:netherite_ingot", 2, 6), ("minecraft:enchanted_golden_apple", 2, 5),
        ("minecraft:totem_of_undying", 2, 4), ("apotheosis:sigil_of_enhancement", 3, 4),
        ("minecraft:nether_star", 1, 4), ("minecraft:heavy_core", 1, 3), ("mekanism:alloy_atomic", 8, 4),
        ("apotheosis:godforged_pearl", 1, 4), ("numismatics:sun", 1, 3),
        ("sophisticatedbackpacks:stack_upgrade_tier_4", 1, 2), ("cobblemon:master_ball", 1, 2),
        ("minecraft:sniffer_egg", 1, 2), ("minecraft:music_disc_pigstep", 1, 2),
    ],
}

EFFECTS = {
    "loot_bag_small": (0, None, False),
    "loot_bag": (2, "#ffffff", False),
    "loot_bag_large": (4, "#e6c8ff", False),
    "loot_bag_grand": (8, "#ffe27a", True),
}
FRAMES = 16
# Where sparkles can appear: transparent pixels around the sack, spread out.
SPARKLE_SPOTS = [(2, 1), (13, 2), (1, 7), (14, 8), (3, 14), (12, 14), (14, 4), (1, 11)]

QUESTION = [".EEE.", "E...E", "..EE.", ".....", "..E.."]


def entry(name, count, weight):
    if name.startswith("#"):
        return {"type": "minecraft:tag", "name": name[1:], "expand": True, "weight": weight}
    e = {"type": "minecraft:item", "name": name, "weight": weight}
    if count > 1:
        e["functions"] = [{"function": "minecraft:set_count", "count": count}]
    return e


def animated(cloth, rope, emblem, count, sparkle, pulse):
    """A vertical strip of FRAMES frames: sparkles blink in turn around the sack; with pulse, the
    emblem brightens and fades."""
    from PIL import Image
    from build_boss_bags import shade
    strip = Image.new("RGBA", (16, 16 * FRAMES), (0, 0, 0, 0))
    spots = SPARKLE_SPOTS[:count]
    for f in range(FRAMES):
        glow = 1 + 0.35 * (1 - abs(f - FRAMES / 2) / (FRAMES / 2)) if pulse else 1
        frame = draw_bag(cloth, rope, shade(emblem, glow), "question")
        px = frame.load()
        for i, (x, y) in enumerate(spots):
            # each sparkle is lit for 3 frames, spread evenly over the cycle
            age = (f - i * FRAMES // max(1, count)) % FRAMES
            if age > 2:
                continue
            if px[x, y][3] == 0:
                px[x, y] = (sparkle if age == 1 else shade(sparkle, 0.75)) + (255,)
            if age == 1:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    if 0 <= x + dx < 16 and 0 <= y + dy < 16 and px[x + dx, y + dy][3] == 0:
                        px[x + dx, y + dy] = shade(sparkle, 0.7) + (200,)
        strip.paste(frame, (0, 16 * f))
    return strip


def main():
    items = set(json.load(open(REGISTRY, encoding="utf-8"))["items"])
    bad = [n for pool in POOLS.values() for n, _, _ in pool if not n.startswith("#") and n not in items]
    if bad:
        raise SystemExit(f"unknown items: {bad}")
    os.makedirs(DATA, exist_ok=True)
    for rarity, pool in POOLS.items():
        with open(os.path.join(DATA, f"{rarity}.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump({"type": "minecraft:chest", "pools": [{"rolls": 1, "entries": [entry(*e) for e in pool]}]},
                      f, indent=2)
            f.write("\n")
    odds = {f"strata:{bag}": dict(zip(RARITIES, w)) for bag, (_, _, _, _, w) in BAGS.items()}
    with open(ODDS_SCRIPT, "w", encoding="utf-8", newline="\n") as f:
        f.write("// Generated by tools/build_quest_bags.py: quest bag -> rarity weights.\n")
        f.write("const lootBagOdds = " + json.dumps(odds, indent=2) + "\n")
    os.makedirs(TEXTURES, exist_ok=True)
    import build_boss_bags
    build_boss_bags.EMBLEMS["question"] = QUESTION
    for bag, (_, cloth, rope, emblem, _) in BAGS.items():
        count, colour, pulse = EFFECTS[bag]
        path = os.path.join(TEXTURES, f"{bag}.png")
        meta = path + ".mcmeta"
        if count == 0 and not pulse:
            draw_bag(hexrgb(cloth), hexrgb(rope), hexrgb(emblem), "question").save(path)
            if os.path.exists(meta):
                os.remove(meta)
            continue
        animated(hexrgb(cloth), hexrgb(rope), hexrgb(emblem), count, hexrgb(colour), pulse).save(path)
        with open(meta, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"animation": {"frametime": 2}}, f)
            f.write("\n")
    print(f"{len(POOLS)} rarity pools ({sum(len(p) for p in POOLS.values())} entries), {len(BAGS)} bags")


if __name__ == "__main__":
    main()
