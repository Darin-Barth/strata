"""Generate Strata's magic gates (docs/gate-map.md sections 1 and 3) as data overrides.

Each gate reads the mod's original JSON from its jar, applies one small change (add an ingredient,
swap the least important one when the recipe has no free slot, or disable the recipe with a
NeoForge false condition) and writes an override at the SAME path under kubejs/data/<ns>/..., so a
mod update can't silently undo it: re-run this after updating any of the mods below.

Writes:
  * section 1 fixes: Theurgy nether star and calorite sulfur reformation routes disabled; netherite
    sulfur reformation +1 strata:hollow_ember (M11); Occultism possess_warden +1 hollow_ember
  * section 3 rows M1-M21 (recipe overrides and Vampirism lord-task overrides)
  * item tags strata:dragon_bloods, strata:dragon_hearts, strata:lich_relics (any-of ingredients)
M6 (Iron's allow_crafting=false) lives in config/irons_spellbooks_spell_config/, not here.

Run from the repo root:
  python -I tools/gates/build_magic.py --mods <mods dir> --out kubejs/data
"""
import argparse
import copy
import glob
import json
import os
import zipfile

EMBER = "strata:hollow_ember"
PEARL = "strata:abyssal_pearl"

TAGS = {
    "dragon_bloods": ["iceandfire:fire_dragon_blood", "iceandfire:ice_dragon_blood",
                      "iceandfire:lightning_dragon_blood"],
    "dragon_hearts": ["iceandfire:fire_dragon_heart", "iceandfire:ice_dragon_heart",
                      "iceandfire:lightning_dragon_heart"],
    # Twilight Lich drops: its trophy or any of its scepters.
    "lich_relics": ["twilightforest:lich_trophy", "twilightforest:twilight_scepter",
                    "twilightforest:lifedrain_scepter", "twilightforest:zombie_scepter",
                    "twilightforest:fortification_scepter"],
}

# jar glob per namespace (first match in --mods)
JARS = {
    "theurgy": "theurgy-*.jar",
    "occultism": "occultism-*.jar",
    "ars_nouveau": "ars_nouveau-*.jar",
    "ars_elemental": "ars_elemental-*.jar",
    "irons_nouveau": "irons-nouveau-*.jar",
    "irons_spellbooks": "irons_spellbooks-*.jar",
    "neovitae": "neovitae-*.jar",
    "vampirism": "Vampirism-*.jar",
}


def item(i):
    return {"item": i}


def tag(t):
    return {"tag": t}


class Builder:
    def __init__(self, mods, out):
        self.mods = mods
        self.out = out
        self.written = []

    def read(self, ns, path):
        jars = sorted(glob.glob(os.path.join(self.mods, JARS[ns])))
        if not jars:
            raise SystemExit(f"no jar for {ns} ({JARS[ns]}) in {self.mods}")
        with zipfile.ZipFile(jars[0]) as z:
            return json.loads(z.read(f"data/{ns}/{path}"))

    def write(self, ns, path, data, note):
        dest = os.path.join(self.out, ns, *path.split("/"))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        self.written.append((f"{ns}/{path}", note))

    def edit(self, ns, name, fn, note):
        """Recipe override: data/<ns>/recipe/<name>.json, changed by fn(recipe)."""
        path = f"recipe/{name}.json"
        data = copy.deepcopy(self.read(ns, path))
        fn(data)
        self.write(ns, path, data, note)

    def disable(self, ns, name, note):
        path = f"recipe/{name}.json"
        orig = self.read(ns, path)
        self.write(ns, path, {"neoforge:conditions": [{"type": "neoforge:false"}], "type": orig["type"]},
                   note)


# ---- change helpers -------------------------------------------------------------------------

def append(key, ing):
    def fn(r):
        r[key].append(ing)
    return fn


def swap(key, old, new, last=True):
    """Replace one ingredient equal to `old` (the last match by default) in list r[key]."""
    def fn(r):
        idx = [i for i, x in enumerate(r[key]) if x == old]
        if not idx:
            raise SystemExit(f"swap: {old} not found in {key}")
        r[key][idx[-1] if last else idx[0]] = new
    return fn


def set_key(key, value):
    def fn(r):
        if key not in r:
            raise SystemExit(f"set_key: {key} missing")
        r[key] = value
    return fn


def shaped_swap(row, col, letter, ing):
    """Shaped crafting: put a new key letter at pattern[row][col]."""
    def fn(r):
        p = list(r["pattern"][row])
        p[col] = letter
        r["pattern"][row] = "".join(p)
        assert letter not in r["key"]
        r["key"][letter] = ing
    return fn


def task_item(item_id, name, count):
    ns, p = item_id.split(":")
    return {
        "type": "vampirism:item",
        "description": {"translate": f"item.{ns}.{p}", "fallback": name},
        "id": item_id,
        "item": {"count": count, "id": item_id},
    }


def build(b):
    # ---- tags ----
    for name, values in TAGS.items():
        b.write("strata", f"tags/item/{name}.json", {"replace": False, "values": values},
                "any-of tag for gate ingredients")

    # ---- section 1: bypasses ----
    for n in ["reformation/alchemical_sulfur_nether_star_from_alchemical_niter_mobs_precious",
              "reformation/alchemical_sulfur_calorite_from_alchemical_niter_metals_precious",
              "reformation/alchemical_sulfur_calorite_from_alchemical_sulfurs_metals_precious"]:
        b.disable("theurgy", n, "S1: disabled (niter/sulfur -> nether star or calorite sulfur)")
    ember_src = {"count": 1, "ingredient": item(EMBER)}
    for n in ["reformation/alchemical_sulfur_netherite_from_alchemical_niter_metals_precious",
              "reformation/alchemical_sulfur_netherite_from_alchemical_sulfurs_metals_precious"]:
        b.edit("theurgy", n, append("sources", ember_src), "M11: +1 hollow_ember source")
    b.edit("occultism", "ritual/possess_warden", append("ingredients", item(EMBER)),
           "S1: +1 hollow_ember")

    # ---- section 3 ----
    # M18 Ars apprentice book: 9/9 slots, swap one quartz block for a naga scale.
    b.edit("ars_nouveau", "apprentice_book_upgrade",
           swap("ingredients", item("minecraft:quartz_block"), item("twilightforest:naga_scale")),
           "M18: one quartz_block -> naga_scale (slots full)")
    # M19 Iron's diamond spellbook: 3x3 full, one of the 4 diamonds -> Lich trophy or scepter.
    b.edit("irons_spellbooks", "diamond_spell_book",
           shaped_swap(2, 0, "L", tag("strata:lich_relics")),
           "M19: bottom-left diamond -> #strata:lich_relics (grid full)")
    # M20 Occultism djinni tier: every djinni ritual needs a Book of Binding (Djinni), crafted once
    # and kept (chalk is used up, so gating chalk would cost a boss kill per stick).
    b.edit("occultism", "crafting/book_of_binding_djinni",
           shaped_swap(2, 0, "E", item("bosses_of_mass_destruction:blazing_eye")),
           "M20: +1 blazing_eye in an empty slot")
    b.edit("occultism", "crafting/book_of_binding_djinni_from_empty",
           shaped_swap(0, 0, "E", item("bosses_of_mass_destruction:blazing_eye")),
           "M20: +1 blazing_eye in an empty slot")
    # M1 Ars tier-3 mage armor upgrade.
    b.edit("ars_nouveau", "second_armor_upgrade",
           append("pedestalItems", item("bosses_of_mass_destruction:ancient_anima")),
           "M1: +1 ancient_anima pedestal")
    # M21 Ars stabilized warp scroll: reusable, cross-dimension and free to use, so it costs echo
    # shards (ancient cities); the single-use warp scroll stays as it is.
    b.edit("ars_nouveau", "stable_warp_scroll",
           lambda r: r["pedestalItems"].extend([item("minecraft:echo_shard")] * 2),
           "M21: +2 echo_shard pedestals")
    # M5 Iron's legendary ink: amethyst -> any dragon blood.
    b.edit("irons_spellbooks", "alchemist_cauldron/brew_legendary_ink",
           set_key("input", tag("strata:dragon_bloods")), "M5: amethyst -> #strata:dragon_bloods")
    # M8 / M9 Occultism afrit and marid tiers.
    b.edit("occultism", "ritual/summon_unbound_afrit", append("ingredients", item(EMBER)),
           "M8: +1 hollow_ember")
    b.edit("occultism", "ritual/summon_unbound_marid", append("ingredients", item(PEARL)),
           "M9: +1 abyssal_pearl")
    # M10 miner djinni and dimensional mineshaft.
    for n in ["ritual/craft_miner_djinni_ores", "ritual/craft_dimensional_mineshaft"]:
        b.edit("occultism", n, append("ingredients", item("deeperdarker:warden_carapace")),
               "M10: +1 warden_carapace")
    # M15 Neo Vitae teleposition reagent (alchemy table, 4 of 6 slots used).
    b.edit("neovitae", "alchemytable/reagent_teleposition",
           append("input", item("legendary_monsters:portal_shard")), "M15: +1 portal_shard")
    # M2 Ars Elemental Mark of Mastery: 8/8 pedestals, manipulation essence -> dragon heart.
    b.edit("ars_elemental", "mark_of_mastery",
           swap("pedestalItems", item("ars_nouveau:manipulation_essence"), tag("strata:dragon_hearts")),
           "M2: manipulation_essence pedestal -> #strata:dragon_hearts (pedestals full)")
    # M3 Iron & Nouveau legendary-spell glyphs.
    for s in ["black_hole", "starfall", "sculk_tentacles", "dragon_breath"]:
        b.edit("irons_nouveau", f"glyph_{s}", append("inputs", item(EMBER)), "M3: +1 hollow_ember")
    # M4 Ars archmage book: one ender pearl -> abyssal pearl.
    b.edit("ars_nouveau", "archmage_book_upgrade",
           swap("ingredients", tag("c:ender_pearls"), item(PEARL)),
           "M4: one #c:ender_pearls -> abyssal_pearl")
    # M12 Neo Vitae crystal cluster (hellfire forge, 4/4 slots): sculk -> obsidian heart.
    b.edit("neovitae", "hellfire_forge/crystal_cluster",
           swap("inputs", item("minecraft:sculk"), item("bosses_of_mass_destruction:obsidian_heart")),
           "M12: sculk -> obsidian_heart (slots full)")
    # M14 Neo Vitae diamond meteor: catalyst diamond -> abyssal pearl.
    b.edit("neovitae", "meteor/diamond", set_key("input", item(PEARL)),
           "M14: input #c:gems/diamond -> abyssal_pearl")
    # M7 Iron's netherite spellbook: 3x3 full, bottom-right magic cloth -> void worm mandible.
    b.edit("irons_spellbooks", "netherite_spell_book",
           shaped_swap(2, 2, "V", item("alexsmobs:void_worm_mandible")),
           "M7: bottom-right magic_cloth -> void_worm_mandible (grid full)")
    # M13 Neo Vitae prismatic gem (athanor; 5 inputs is the most any athanor recipe uses).
    b.edit("neovitae", "athanor/orb/prismatic_spiritus_gem",
           swap("inputs", tag("c:gems/diamond"), item(PEARL)),
           "M13: one #c:gems/diamond -> abyssal_pearl (5-input max)")

    # M16 / M17 Vampirism lord levels 3 and 5.
    for side in ["vampire", "hunter"]:
        for lvl, (iid, name, m) in {3: (EMBER, "Hollow Ember", "M16"),
                                    5: (PEARL, "Abyssal Pearl", "M17")}.items():
            path = f"vampirism/tasks/{side}_lord{lvl}.json"
            data = copy.deepcopy(b.read("vampirism", path))
            data["requirements"]["requirements"].append(task_item(iid, name, 2))
            b.write("vampirism", path, data, f"{m}: +2 {iid.split(':')[1]}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mods", required=True, help="server mods directory (jars)")
    ap.add_argument("--out", default="kubejs/data")
    a = ap.parse_args()
    b = Builder(a.mods, a.out)
    build(b)
    for p, note in b.written:
        print(f"{p}: {note}")
    print(f"{len(b.written)} files written under {a.out}")


if __name__ == "__main__":
    main()
