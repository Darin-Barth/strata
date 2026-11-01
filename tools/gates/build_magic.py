"""Generate Strata's magic gates (docs/gate-map.md sections 1 and 3) as data overrides.

Each gate reads the mod's original JSON from its jar, applies one small change (add an ingredient,
swap the least important one when the recipe has no free slot, or disable the recipe with a
NeoForge false condition) and writes an override at the SAME path under kubejs/data/<ns>/..., so a
mod update can't silently undo it: re-run this after updating any of the mods below.

Writes:
  * section 1 fixes: Theurgy nether star and calorite sulfur reformation routes disabled; netherite
    sulfur reformation +1 strata:hollow_ember (M11); Occultism possess_warden +1 hollow_ember
  * section 3: only M21 (Ars stabilized warp scroll, the teleport rule); the magic road blocks
    M1-M20 were dropped Oct 31 (Darin)

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

# jar glob per namespace (first match in --mods)
JARS = {
    "theurgy": "theurgy-*.jar",
    "occultism": "occultism-*.jar",
    "ars_nouveau": "ars_nouveau-*.jar",
}


def item(i):
    return {"item": i}


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


def build(b):
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
    # The magic road blocks (M1-M20) were dropped Oct 31 (Darin): magic recipes are back to the mods'
    # own. M21 stays because it's the teleport rule, not balance.
    # M21 Ars stabilized warp scroll: reusable, cross-dimension and free to use, so it costs echo
    # shards (ancient cities); the single-use warp scroll stays as it is.
    b.edit("ars_nouveau", "stable_warp_scroll",
           lambda r: r["pedestalItems"].extend([item("minecraft:echo_shard")] * 2),
           "M21: +2 echo_shard pedestals")


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
