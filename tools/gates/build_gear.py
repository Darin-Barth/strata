"""Gear gates G1-G6 of docs/gate-map.md , as datapack overrides.

Reads each original file from the mod jar, applies the change, and writes it back at the same
path under kubejs/data, so the mod's own recipe or advancement is replaced. Re-run after a mod
update.

Usage:
  python -I tools/gates/build_gear.py --mods <mods dir> --out kubejs/data

  G1  apotheosis:progression/summit (world tier): also have owned a Hollow Ember
  G2  apotheosis:progression/pinnacle (world tier): also have owned an Abyssal Pearl
  G3  apotheosis:augmenting_table: + Hollow Ember (top slot pair)
  G4  apotheosis:gem_cutting/flawless: + Abyssal Pearl; apothic_enchanting heart and crystal
      seashelves: + Abyssal Pearl
  G5  oritech:augment/flight: + one Ice and Fire dragon heart in its research cost
  G6  panascraftrpgmod:ultimate_lord_ingot_recipe: nether star -> cursium ingot (Maledictus),
      two amethyst corners -> void gems
"""
import argparse
import glob
import json
import os
import zipfile

EMBER = "strata:hollow_ember"
PEARL = "strata:abyssal_pearl"
DRAGON_HEARTS = ["iceandfire:fire_dragon_heart", "iceandfire:ice_dragon_heart", "iceandfire:lightning_dragon_heart"]


def jar(mods, prefix):
    hits = sorted(glob.glob(os.path.join(mods, prefix + "*.jar")))
    if not hits:
        raise SystemExit(f"no jar matching {prefix}* in {mods}")
    return hits[0]


def read(jar_path, path):
    with zipfile.ZipFile(jar_path) as z:
        return json.loads(z.read(path))


def write(out, path, data):
    dest = os.path.join(out, path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    print("wrote", path)


def own_item(adv, key, item):
    adv["criteria"][key] = {"trigger": "minecraft:inventory_changed",
                            "conditions": {"items": [{"items": item}]}}
    adv["requirements"].append([key])
    return adv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mods", required=True)
    ap.add_argument("--out", default="kubejs/data")
    a = ap.parse_args()
    apoth = jar(a.mods, "Apotheosis-")
    ench = jar(a.mods, "ApothicEnchanting-")
    ori = jar(a.mods, "oritech-")
    panas = jar(a.mods, "panascraftrpgmod-")

    # G1, G2: world tiers
    for name, key, item in (("summit", "strata_hollow_ember", EMBER), ("pinnacle", "strata_abyssal_pearl", PEARL)):
        p = f"apotheosis/advancement/progression/{name}.json"
        write(a.out, p, own_item(read(apoth, "data/" + p), key, item))

    # G3: augmenting table (pattern " N " / "GEG" / "PPP"): Hollow Embers beside the nether star
    p = "apotheosis/recipe/augmenting_table.json"
    r = read(apoth, "data/" + p)
    assert r["pattern"][0] == " N ", r["pattern"]
    r["pattern"][0] = "HNH"
    r["key"]["H"] = {"item": EMBER}
    write(a.out, p, r)

    # G4: flawless gem cutting and the two best seashelves
    p = "apotheosis/recipe/gem_cutting/flawless.json"
    r = read(apoth, "data/" + p)
    r["right"].append({"count": 1, "item": PEARL})
    write(a.out, p, r)
    for name, row, before, after in (("crystal_seashelf", 2, "P P", "PAP"), ("heart_seashelf", 0, " H ", "AHA")):
        p = f"apothic_enchanting/recipe/{name}.json"
        r = read(ench, "data/" + p)
        assert r["pattern"][row] == before, (name, r["pattern"])
        r["pattern"][row] = after
        r["key"]["A"] = {"item": PEARL}
        write(a.out, p, r)

    # G5: Oritech flight augment research needs a dragon heart (any of the three)
    p = "oritech/recipe/augment/flight.json"
    r = read(ori, "data/" + p)
    r["researchCost"].append({"count": 1, "ingredient": [{"item": h} for h in DRAGON_HEARTS]})
    write(a.out, p, r)

    # G6: Apocalyptic Bosses' ultimate ingot (pattern "aba" / "bcb" / "aba", c = nether star)
    p = "panascraftrpgmod/recipe/ultimate_lord_ingot_recipe.json"
    r = read(panas, "data/" + p)
    assert r["pattern"] == ["aba", "bcb", "aba"], r["pattern"]
    r["pattern"][0] = "vbv"
    r["key"]["c"] = {"item": "cataclysm:cursium_ingot"}
    r["key"]["v"] = {"item": "panascraftrpgmod:void_gem"}
    write(a.out, p, r)


if __name__ == "__main__":
    main()
