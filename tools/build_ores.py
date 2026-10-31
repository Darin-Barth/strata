"""Generate Strata's ore map (docs/ore-map.md): which ores spawn where.

Writes:
  * config/Mekanism/world.toml: thin osmium and fluorite at home; Mekanism's lead and uranium off
    (Immersive Engineering's are the Almost Unified targets). Built from Mekanism's own default file.
  * kubejs/data overrides (each mod's own file, same path, so a mod update can't silently undo it):
      - duplicate and moved ores off (biome modifier -> neoforge:none): Occultism, Ice and Fire and
        Werewolves silver; Oritech nickel, uranium patch and Overworld platinum; Extreme Reactors
        yellorite; Draconic Evolution's Overworld draconium
      - thinner at home (placed feature counts): Create Propulsion platinum, Iron's Spells mithril
      - #mekanism:spawn_ores limited to the real Overworld (it also reached a mining dimension through
        #c:is_overworld)
  * new Strata ores (configured + placed feature + biome modifier, namespace strata):
      - abyssal_osmium: rich deepslate osmium across the Abyssal Plain
      - abyssal_fluorite: rich deepslate fluorite in the Hydrothermal Field
      - hollow_mithril: rich mithril in the Hollow's grimstone
    Abyssal Plain features use count + height range (never a heightmap: the rock ceiling breaks them).

Run from the repo root (re-run after updating any mod named above):
  python -I tools/build_ores.py --mods <server mods dir> --mekanism-default <a server's config/Mekanism/world.toml>
"""
import argparse
import copy
import glob
import json
import os
import re
import zipfile

OUT = "kubejs/data"
MEK_CONFIG = "config/Mekanism/world.toml"

JARS = {
    "occultism": "occultism-*.jar", "iceandfire": "iceandfire-*.jar", "werewolves": "werewolves-*.jar",
    "oritech": "oritech-*.jar", "bigreactors": "ExtremeReactors*.jar", "draconicevolution": "Draconic-Evolution*.jar",
    "createpropulsion": "createpropulsion-*.jar", "irons_spellbooks": "irons_spellbooks-*.jar",
}

OFF = {  # namespace -> biome modifier files to turn off
    "occultism": ["add_ore_silver", "add_ore_silver_deepslate"],
    "iceandfire": ["silver_ore"],
    "werewolves": ["gen/silver_ore"],
    "oritech": ["ore_nickel", "uranium_patch", "ore_platinum"],
    "bigreactors": ["yellorite", "yellorite_deepslate"],
    "draconicevolution": ["overworld_draconium_ore"],
}

# placed feature -> new count (or rarity chance for rarity_filter features); "thin at home"
THIN = {
    ("createpropulsion", "ore_platinum"): ("count", 3),          # was 7
    ("createpropulsion", "ore_platinum_buried"): ("count", 2),   # was 4
    ("createpropulsion", "ore_platinum_large"): ("chance", 18),  # was 1 in 9
    ("createpropulsion", "ore_platinum_medium"): ("count", 1),   # was 2
    ("irons_spellbooks", "ore_mithril_placement"): ("count", 2), # was 7
}

# Mekanism world.toml: (section path, key) -> value
MEK = {
    ("osmium.upper", "perChunk"): 13,   # was 65
    ("osmium.middle", "perChunk"): 1,   # was 6
    ("osmium.small", "perChunk"): 2,    # was 8
    ("fluorite.normal", "perChunk"): 2, # was 5
    ("fluorite.buried", "perChunk"): 1, # was 3
    ("fluorite.buried", "maxVeinSize"): 6, # was 13
    ("uranium", "shouldGenerate"): "false",
    ("lead", "shouldGenerate"): "false",
}

NEW = {  # name: (biomes, ore block, target rule, size, count, min y, max y)
    "abyssal_osmium": ("#strata:abyssal_plain_biomes", "mekanism:deepslate_osmium_ore",
                       {"predicate_type": "minecraft:tag_match", "tag": "minecraft:deepslate_ore_replaceables"},
                       10, 10, -40, 330),
    "abyssal_fluorite": ("strata:hydrothermal_field", "mekanism:deepslate_fluorite_ore",
                         {"predicate_type": "minecraft:tag_match", "tag": "minecraft:deepslate_ore_replaceables"},
                         12, 24, 150, 330),
    "hollow_mithril": ("#strata:hollow_biomes", "irons_spellbooks:mithril_ore",
                       {"predicate_type": "minecraft:block_match", "block": "grim_and_bleak:grimstone"},
                       4, 6, -60, 40),
}


def write(rel, data):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def read_jar(mods, ns, path):
    jars = sorted(glob.glob(os.path.join(mods, JARS[ns])))
    if not jars:
        raise SystemExit(f"no jar for {ns} ({JARS[ns]}) in {mods}")
    with zipfile.ZipFile(jars[0]) as z:
        return json.loads(z.read(f"data/{ns}/{path}"))


def mekanism(default_path):
    lines = open(default_path, encoding="utf-8").read().split("\n")
    section, done = None, set()
    for i, line in enumerate(lines):
        m = re.match(r"\s*\[([a-z_.]+)\]\s*$", line)
        if m:
            section = m.group(1)
            continue
        m = re.match(r"(\s*)([A-Za-z]+)\s*=", line)
        if m and (section, m.group(2)) in MEK:
            lines[i] = f"{m.group(1)}{m.group(2)} = {MEK[(section, m.group(2))]}"
            done.add((section, m.group(2)))
    missing = set(MEK) - done
    if missing:
        raise SystemExit(f"Mekanism world.toml keys not found: {sorted(missing)}")
    os.makedirs(os.path.dirname(MEK_CONFIG), exist_ok=True)
    with open(MEK_CONFIG, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mods", required=True)
    ap.add_argument("--mekanism-default", required=True)
    a = ap.parse_args()

    mekanism(a.mekanism_default)
    n = 0
    for ns, files in OFF.items():
        for f in files:
            read_jar(a.mods, ns, f"neoforge/biome_modifier/{f}.json")  # fails loudly if the mod renamed it
            write(f"{ns}/neoforge/biome_modifier/{f}.json", {"type": "neoforge:none"})
            n += 1
    for (ns, f), (kind, value) in THIN.items():
        pf = copy.deepcopy(read_jar(a.mods, ns, f"worldgen/placed_feature/{f}.json"))
        hit = False
        for p in pf["placement"]:
            if kind == "count" and p["type"] in ("minecraft:count", "count"):
                p["count"], hit = value, True
            if kind == "chance" and p["type"] in ("minecraft:rarity_filter", "rarity_filter"):
                p["chance"], hit = value, True
        if not hit:
            raise SystemExit(f"{ns}:{f}: no {kind} placement to change")
        write(f"{ns}/worldgen/placed_feature/{f}.json", pf)
        n += 1
    write("mekanism/tags/worldgen/biome/spawn_ores.json", {"replace": True, "values": ["#minecraft:is_overworld"]})
    for name, (biomes, block, target, size, count, lo, hi) in NEW.items():
        write(f"strata/worldgen/configured_feature/{name}.json", {"type": "minecraft:ore", "config": {
            "size": size, "discard_chance_on_air_exposure": 0.0,
            "targets": [{"target": target, "state": {"Name": block}}]}})
        write(f"strata/worldgen/placed_feature/{name}.json", {"feature": f"strata:{name}", "placement": [
            {"type": "minecraft:count", "count": count}, {"type": "minecraft:in_square"},
            {"type": "minecraft:height_range", "height": {"type": "minecraft:uniform",
             "min_inclusive": {"absolute": lo}, "max_inclusive": {"absolute": hi}}},
            {"type": "minecraft:biome"}]})
        write(f"strata/neoforge/biome_modifier/{name}.json", {"type": "neoforge:add_features", "biomes": biomes,
              "features": f"strata:{name}", "step": "underground_ores"})
        n += 1
    print(f"ore map: {MEK_CONFIG} + {n} data files ({len(NEW)} new Strata ores)")


if __name__ == "__main__":
    main()
