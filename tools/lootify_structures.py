"""Turn pre-filled structure chests into loot-table chests, so Lootr can give every player their own loot.

Some mods ship structure templates whose chests have their items baked in (no LootTable). Lootr only
handles loot-table containers, so those chests are first-come-first-served. For each such chest this
writes an exact loot table (one pool per stack) and a patched copy of the template whose chest uses
that loot table instead of the items. The patched templates override the mod's own through KubeJS data.

It also writes tools/lootify_index.json: a signature of each original chest's contents -> loot table,
used by tools/lootify_world.py to convert chests that were already generated into the world.

Usage: python -I tools/lootify_structures.py <namespace>=<mod jar> [<namespace>=<mod jar> ...]
Item ids are checked against tools/quests/registry.json (a dump from a running server).
"""
import gzip
import io
import json
import sys
import zipfile
from pathlib import Path

import nbtlib

ROOT = Path(__file__).resolve().parent.parent
OUT_DATA = ROOT / "kubejs" / "data"
INDEX = ROOT / "tools" / "lootify_index.json"
REGISTRY = set(json.load(open(ROOT / "tools" / "quests" / "registry.json"))["items"])


def signature(items):
    """Order-independent description of a chest's contents, shared with lootify_world.py."""
    return json.dumps(sorted([str(i["id"]), int(i["count"])] for i in items))


def old_item(it):
    """Item from a 1.20.1-format stack (id, Count, tag) -> (id, count, tag dict)."""
    return str(it["id"]), int(it.get("Count", it.get("count", 1))), it.get("tag") or {}


def entry_for(item_id, count, tag):
    functions = [{"function": "minecraft:set_count", "count": count}]
    enchants = {}
    for key in ("Enchantments", "StoredEnchantments"):
        for e in tag.get(key, []):
            enchants[str(e["id"])] = int(e["lvl"])
    if enchants:
        functions.append({"function": "minecraft:set_enchantments", "enchantments": enchants})
    name = tag.get("display", {}).get("Name")
    if name:
        functions.append({"function": "minecraft:set_name", "name": json.loads(str(name)), "target": "custom_name"})
    return {"rolls": 1, "entries": [{"type": "minecraft:item", "name": item_id, "functions": functions}]}


def main():
    index = json.load(open(INDEX)) if INDEX.exists() else {}
    for arg in sys.argv[1:]:
        ns, jar = arg.split("=", 1)
        z = zipfile.ZipFile(jar)
        for name in sorted(n for n in z.namelist() if n.startswith(f"data/{ns}/structure/") and n.endswith(".nbt")):
            struct = name[len(f"data/{ns}/structure/"):-4]
            f = nbtlib.File.parse(gzip.GzipFile(fileobj=io.BytesIO(z.read(name))))
            changed = 0
            for b in f["blocks"]:
                nb = b.get("nbt")
                if nb is None or "Items" not in nb or "LootTable" in nb or len(nb["Items"]) == 0:
                    continue
                stacks = [old_item(it) for it in nb["Items"]]
                unknown = [i for i, _, _ in stacks if i not in REGISTRY]
                for u in unknown:
                    print(f"  WARN {ns}:{struct}: {u} isn't registered on 1.21.1, dropped")
                kept = [s for s in stacks if s[0] in REGISTRY]
                table = f"strata:lootified/{ns}/{struct}/{changed}"
                path = OUT_DATA / "strata" / "loot_table" / "lootified" / ns / struct / f"{changed}.json"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps({"type": "minecraft:chest", "pools": [entry_for(*s) for s in kept]}, indent=2) + "\n", newline="\n")
                index[signature([{"id": i, "count": c} for i, c, _ in stacks])] = table
                del nb["Items"]
                nb["LootTable"] = nbtlib.String(table)
                changed += 1
            if changed:
                out = OUT_DATA / ns / "structure" / f"{struct}.nbt"
                out.parent.mkdir(parents=True, exist_ok=True)
                f.save(out, gzipped=True)
                print(f"{ns}:{struct}: {changed} chest(s) -> loot tables")
    INDEX.write_text(json.dumps(index, indent=1, sort_keys=True) + "\n", newline="\n")
    print(f"index: {len(index)} chest signatures in {INDEX.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
