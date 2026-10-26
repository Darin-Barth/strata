"""Generate the tech gates T1-T10 (docs/gate-map.md section 2) as datapack recipe overrides.

Each gated recipe is read from its mod jar, changed by adding (or, where the 3x3 grid is full,
swapping in) a gate ingredient, and written at the SAME path under kubejs/data/<ns>/recipe/, so it
replaces the mod's own file. Recipe type, keys, conditions and output are kept as they are.

Gate materials: strata:hollow_ember (E), strata:abyssal_pearl (P) and boss drops.

Every change names the slot it touches and the key it expects there; if a mod update moves its
recipe around, the script stops with an error instead of writing a wrong override. Re-run after
updating any of these mods:
  Mekanism, Mekanism Generators, Create: New Age, Extreme Reactors, AE2, AppliedFlux, Ad Astra,
  Draconic Evolution, Extended Crafting.

Run from the repo root:
  python -I tools/gates/build_tech.py --mods <mods dir> --out kubejs/data
"""
import argparse
import json
import os
import zipfile

EMBER = "strata:hollow_ember"
PEARL = "strata:abyssal_pearl"
IGNITIUM = "cataclysm:ignitium_ingot"
LAVA_CELL = "cataclysm:lava_power_cell"
WITHERITE = "cataclysm:witherite_ingot"
VOID_CORE = "cataclysm:void_core"
FIERY_BLOOD = "twilightforest:fiery_blood"
STORM = "cataclysm:essence_of_the_storm"
ABYSSAL_EGG = "cataclysm:abyssal_egg"

# Jar file name prefixes (lower case).
MEK = "mekanism-1.21.1"
MEKGEN = "mekanismgenerators-"
NEWAGE = "create-new-age-"
ER = "extremereactors2-"
AE2 = "appliedenergistics2-"
FLUX = "appliedflux-"
ADASTRA = "adastra-"
DE = "draconic-evolution-"
EC = "extendedcrafting-"

# Ops for shaped recipes (minecraft:crafting_shaped and mekanism:mek_data):
#   ("add", item, [(row, col), ...])            put item into empty slots (rows past the end of a
#                                               short pattern are added)
#   ("swap", item, old_key, [(row, col), ...])  replace that key at those slots
# Ops for list recipes (draconicevolution:fusion_crafting):
#   ("append", item, count)
#   ("replace", item, old_ingredient, count)    swap the first `count` entries matching old_ingredient
FACTORIES = ["combining", "compressing", "crushing", "enriching", "infusing", "injecting",
             "purifying", "sawing", "smelting"]
MEKASUIT = ["mekasuit_helmet", "mekasuit_bodyarmor", "mekasuit_pants", "mekasuit_boots"]

GATES = [
    # T1 nuclear: 1 ignitium ingot
    ("T1", MEKGEN, "mekanismgenerators", "fission_reactor/port", "mekanismgenerators:fission_reactor_port",
     [("add", IGNITIUM, [(0, 0)])]),
    ("T1", NEWAGE, "create_new_age", "shaped/reactor_fuel_acceptor", "create_new_age:reactor_fuel_acceptor",
     [("add", IGNITIUM, [(2, 1)])]),
    ("T1", ER, "bigreactors", "reactor/reinforced/controller_ingots_uranium", "bigreactors:reinforced_reactorcontroller",
     [("swap", IGNITIUM, "R", [(2, 1)])]),
    ("T1", ER, "bigreactors", "reactor/reinforced/controller_ingots_yellorium", "bigreactors:reinforced_reactorcontroller",
     [("swap", IGNITIUM, "R", [(2, 1)])]),
    ("T1", ER, "bigreactors", "turbine/reinforced/controller", "bigreactors:reinforced_turbinecontroller",
     [("swap", IGNITIUM, "R", [(2, 1)])]),
    # T2 Mekanism ultimate tier: 1 lava power cell (every grid is full, so a cheap slot is swapped)
    ("T2", MEK, "mekanism", "bin/ultimate", "mekanism:ultimate_bin",
     [("swap", LAVA_CELL, "_", [(2, 1)])]),
    ("T2", MEK, "mekanism", "chemical_tank/ultimate", "mekanism:ultimate_chemical_tank",
     [("swap", LAVA_CELL, "O", [(0, 1)])]),
    ("T2", MEK, "mekanism", "energy_cube/ultimate", "mekanism:ultimate_energy_cube",
     [("swap", LAVA_CELL, "I", [(1, 0)])]),
    *[("T2", MEK, "mekanism", f"factory/ultimate/{f}", f"mekanism:ultimate_{f}_factory",
       [("swap", LAVA_CELL, "I", [(1, 0)])]) for f in FACTORIES],
    ("T2", MEK, "mekanism", "fluid_tank/ultimate", "mekanism:ultimate_fluid_tank",
     [("swap", LAVA_CELL, "I", [(0, 1)])]),
    ("T2", MEK, "mekanism", "induction/cell/ultimate", "mekanism:ultimate_induction_cell",
     [("swap", LAVA_CELL, "E", [(0, 0)])]),
    ("T2", MEK, "mekanism", "induction/provider/ultimate", "mekanism:ultimate_induction_provider",
     [("swap", LAVA_CELL, "C", [(0, 0)])]),
    ("T2", MEK, "mekanism", "tier_installer/ultimate", "mekanism:ultimate_tier_installer",
     [("swap", LAVA_CELL, "P", [(1, 1)])]),
    # Ultimate transmitters (cables, pipes, tubes) are left ungated: they're crafted in bulk, so a
    # cell per 8 would pile up on any real network; the tier is gated through the items above.
    # T3 fusion reactor controller: 1 witherite ingot + 4 E (grid full)
    ("T3", MEKGEN, "mekanismgenerators", "reactor/controller", "mekanismgenerators:fusion_reactor_controller",
     [("swap", WITHERITE, "G", [(0, 1)]),
      ("swap", EMBER, "T", [(1, 1)]),
      ("swap", EMBER, "F", [(2, 0), (2, 1), (2, 2)])]),
    # T4 MekaSuit and Meka-Tool: 2 E each (grids full; two HDPE sheets swapped)
    *[("T4", MEK, "mekanism", p, f"mekanism:{p}", [("swap", EMBER, "P", [(1, 0), (1, 2)])]) for p in MEKASUIT],
    ("T4", MEK, "mekanism", "meka_tool", "mekanism:meka_tool",
     [("swap", EMBER, "P", [(1, 0), (1, 2)])]),
    # T5 SPS: 2 P each
    ("T5", MEK, "mekanism", "supercharged_coil", "mekanism:supercharged_coil",
     [("swap", PEARL, "c", [(0, 0), (0, 2)])]),
    ("T5", MEK, "mekanism", "sps_port", "mekanism:sps_port",
     [("add", PEARL, [(0, 0), (0, 2)])]),
    ("T5", MEK, "mekanism", "antiprotonic_nucleosynthesizer", "mekanism:antiprotonic_nucleosynthesizer",
     [("swap", PEARL, "#", [(0, 0), (0, 2)])]),
    # T6 top storage: 1 void core (grids full; cheapest ingredient swapped)
    ("T6", AE2, "ae2", "network/cells/item_storage_components_cell_256k_part", "ae2:cell_component_256k",
     [("swap", VOID_CORE, "a", [(0, 0)])]),
    ("T6", FLUX, "appflux", "256m_core", "appflux:core_256m",
     [("swap", VOID_CORE, "D", [(0, 0)])]),
    ("T6", MEK, "mekanism", "qio_drive_supermassive", "mekanism:qio_drive_supermassive",
     [("swap", VOID_CORE, "I", [(0, 0)])]),
    # T7 desh engine: 1 fiery blood
    ("T7", ADASTRA, "ad_astra", "desh_engine", "ad_astra:desh_engine",
     [("add", FIERY_BLOOD, [(2, 0)])]),
    # T8 calorite engine: 2 essence of the storm (the jet suit chestplate consumes this engine)
    ("T8", ADASTRA, "ad_astra", "calorite_engine", "ad_astra:calorite_engine",
     [("add", STORM, [(2, 0), (2, 2)])]),
    # T9 Draconic awakened core: 2 E replace 2 of its 4 awakened draconium ingots, so the craft
    # still uses 8 fusion injectors (the dragon heart behind awakened draconium stays required)
    ("T9", DE, "draconicevolution", "components/awakened_core", "draconicevolution:awakened_core",
     [("replace", EMBER, {"tag": "c:ingots/draconium_awakened"}, 2)]),
    # T10 Extended Crafting ultimate table: abyssal egg + 4 P. The table's grid is full, so the egg
    # replaces the emerald block and the 4 pearls go into the ultimate catalyst's empty corners
    # (the catalyst's only use is this table).
    ("T10", EC, "extendedcrafting", "ultimate_table", "extendedcrafting:ultimate_table",
     [("swap", ABYSSAL_EGG, "I", [(1, 1)])]),
    ("T10", EC, "extendedcrafting", "ultimate_catalyst", "extendedcrafting:ultimate_catalyst",
     [("add", PEARL, [(0, 0), (0, 2), (2, 0), (2, 2)])]),
]

SHAPED = {"minecraft:crafting_shaped", "mekanism:mek_data"}
LIST_TYPES = {"draconicevolution:fusion_crafting": "ingredients"}
FREE_KEYS = "XYZWQVUJKMNOLHGBDRSTFEPAIC0123456789"


def find_jar(mods, prefix):
    hits = [f for f in os.listdir(mods) if f.lower().startswith(prefix) and f.endswith(".jar")]
    if len(hits) != 1:
        raise SystemExit(f"expected one jar starting with {prefix!r}, found {hits}")
    return os.path.join(mods, hits[0])


def key_for(recipe, item):
    keys = recipe["key"]
    for k, v in keys.items():
        if v == {"item": item}:
            return k
    for k in FREE_KEYS:
        if k not in keys:
            keys[k] = {"item": item}
            return k
    raise SystemExit("no free key letter")


def set_slot(pattern, row, col, ch, expect):
    width = max(3, max(len(r) for r in pattern))
    while len(pattern) <= row:
        pattern.append(" " * width)
    line = pattern[row].ljust(col + 1)
    if line[col] != expect:
        raise SystemExit(f"slot {row},{col} holds {line[col]!r}, expected {expect!r} in {pattern}")
    pattern[row] = line[:col] + ch + line[col + 1:]


def apply_shaped(recipe, ops):
    pattern = list(recipe["pattern"])
    for op in ops:
        if op[0] == "add":
            _, item, slots = op
            k = key_for(recipe, item)
            for r, c in slots:
                set_slot(pattern, r, c, k, " ")
        elif op[0] == "swap":
            _, item, old, slots = op
            k = key_for(recipe, item)
            for r, c in slots:
                set_slot(pattern, r, c, k, old)
        else:
            raise SystemExit(f"op {op[0]} not valid for a shaped recipe")
    width = max(len(r) for r in pattern)
    if len(pattern) > 3 or width > 3:
        raise SystemExit(f"pattern grew past 3x3: {pattern}")
    pattern = [r.ljust(width) for r in pattern]
    used = set("".join(pattern)) - {" "}
    for k in list(recipe["key"]):
        if k not in used:          # a fully swapped-out key must go, or the recipe fails to load
            del recipe["key"][k]
    recipe["pattern"] = pattern


def apply_list(recipe, field, ops):
    items = recipe[field]
    sample = items[0]
    for op in ops:
        if op[0] == "replace":
            _, item, old, count = op
            hits = [i for i, e in enumerate(items) if (e.get("ingredient") if isinstance(e, dict) and "ingredient" in e else e) == old]
            if len(hits) < count:
                raise SystemExit(f"only {len(hits)} of {old} in {recipe}")
            for i in hits[:count]:
                if "ingredient" in items[i]:
                    items[i] = {**items[i], "ingredient": {"item": item}}
                else:
                    items[i] = {"item": item}
            continue
        if op[0] != "append":
            raise SystemExit(f"op {op[0]} not valid for a list recipe")
        _, item, count = op
        for _ in range(count):
            if isinstance(sample, dict) and "ingredient" in sample:     # fusion crafting
                items.append({"consume": True, "ingredient": {"item": item}})
            else:
                items.append({"item": item})


def build(mods, out):
    jars = {}
    written = []
    for tier, prefix, ns, path, result, ops in GATES:
        jar = jars.get(prefix) or jars.setdefault(prefix, zipfile.ZipFile(find_jar(mods, prefix)))
        src = f"data/{ns}/recipe/{path}.json"
        try:
            recipe = json.loads(jar.read(src))
        except KeyError:
            raise SystemExit(f"{tier}: {src} not in {jar.filename}")
        if recipe.get("result", {}).get("id") != result:
            raise SystemExit(f"{tier}: {src} makes {recipe.get('result')}, expected {result}")
        rtype = recipe["type"]
        if rtype in SHAPED:
            apply_shaped(recipe, ops)
        elif rtype in LIST_TYPES:
            apply_list(recipe, LIST_TYPES[rtype], ops)
        else:
            raise SystemExit(f"{tier}: {src} has unhandled type {rtype}")
        dest = os.path.join(out, ns, "recipe", *path.split("/")) + ".json"
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8", newline="\n") as f:
            json.dump(recipe, f, indent=2)
            f.write("\n")
        written.append((tier, f"{ns}:{path}"))
    return written


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mods", required=True, help="folder with the pack's mod jars")
    ap.add_argument("--out", default="kubejs/data")
    a = ap.parse_args()
    for tier, rid in build(a.mods, a.out):
        print(f"{tier:4} {rid}")


if __name__ == "__main__":
    main()
