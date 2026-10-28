"""Generate the recipe side of Strata's balance patch (docs/balance-patch.md, Darin's answers Oct 27)
as datapack overrides in kubejs/data/... Each recipe is read from its mod jar, changed, and written
at the SAME path so it replaces the mod's own file. Removals are in
kubejs/server_scripts/strata_balance.js; config-only changes ship in config/.

  D2 Theurgy liquefaction of metal ores: 5 sulfur -> 3 (raw ore 3 -> 2, rich raw 5 -> 3), so its
     ore doubling sits below Mekanism's 5x instead of matching it from stone-age machines. Gems,
     coal, uraninite and other non-metal results keep their counts.
  G1 Bountiful rewards: kept, but the top rewards are rarer and cost more. Netherite armor, diamond
     gear, Mending, the Totem of Undying and the ominous trial key are worth 1.5x as much (a bigger
     bounty to pay one out) and come up a quarter as often. (3x worth was too much: Bountiful then
     can't build a bounty big enough for netherite armor, so it would never show up.)

Run from the repo root (re-run after a Theurgy or Bountiful update):
  python -I tools/build_balance.py --mods <mods dir> --out kubejs/data
"""
import argparse
import json
import os
import re
import zipfile

THEURGY = "theurgy-"
BOUNTIFUL = "bountiful-"
BOUNTIFUL_POOLS = ["armorer_rews", "toolsmith_rews", "cleric_rews", "_all_rews"]
BOUNTIFUL_TOP = re.compile(r"netherite|diamond|mending|totem_of_undying|ominous_trial_key")
# liquefaction ingredient tag prefix -> {old count: new count}
THEURGY_SCALE = {"c:ores/": {5: 3}, "c:raw_materials/": {3: 2, 5: 3}}


def jar(mods, prefix):
    for j in sorted(os.listdir(mods)):
        if j.lower().startswith(prefix):
            return zipfile.ZipFile(os.path.join(mods, j))
    raise SystemExit(f"no jar starting with {prefix} in {mods}")


def write(out, rel, data):
    path = os.path.join(out, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def theurgy(mods, out):
    z = jar(mods, THEURGY)
    n = 0
    for name in z.namelist():
        if not (name.startswith("data/theurgy/recipe/liquefaction/") and name.endswith(".json")):
            continue
        r = json.loads(z.read(name))
        tag = r.get("ingredient", {}).get("tag", "")
        if not r.get("result", {}).get("id", "").startswith("theurgy:alchemical_sulfur_"):
            continue
        for prefix, scale in THEURGY_SCALE.items():
            # metal ores only: gem, coal and other ores have their own (non-5/3) counts
            if tag.startswith(prefix) and r["result"].get("count") in scale:
                r["result"]["count"] = scale[r["result"]["count"]]
                write(out, name[len("data/"):], r)
                n += 1
    return n


def bountiful(mods, out):
    z = jar(mods, BOUNTIFUL)
    n = 0
    for pool in BOUNTIFUL_POOLS:
        name = f"data/bountiful/bounty_pools/bountiful/{pool}.json"
        d = json.loads(z.read(name))
        for key, entry in d["content"].items():
            if BOUNTIFUL_TOP.search(json.dumps(entry)):
                entry["unitWorth"] = round(entry["unitWorth"] * 1.5)
                entry["weightMult"] = round(entry.get("weightMult", 1.0) / 4, 4)
                n += 1
        write(out, name[len("data/"):], d)
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mods", required=True)
    ap.add_argument("--out", default="kubejs/data")
    a = ap.parse_args()
    print(f"D2 Theurgy liquefaction: {theurgy(a.mods, a.out)} recipes scaled")
    print(f"G1 Bountiful: {bountiful(a.mods, a.out)} top rewards made rarer and pricier")


if __name__ == "__main__":
    main()
