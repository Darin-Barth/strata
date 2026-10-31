"""Check every registry ID in the FTB Quests files against the mod jars.

Scans the SNBT files (so it also catches edits made with the in-game editor) for item IDs
(`id: "ns:path"`, in tasks, rewards, icons and reward tables) and for entity, dimension,
structure, biome and advancement IDs, and looks each up in the index built by item_index.py.

Usage: python -I tools/quests/check_ids.py [QUESTS_DIR] [--rebuild]
The index is cached in tools/quests/.cache/index.json and rebuilt when a jar is newer.
"""
import difflib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import item_index  # noqa: E402

REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
CACHE = os.path.join(HERE, ".cache", "index.json")
DEFAULT_DIR = os.path.join(REPO, "config", "ftbquests", "quests")

PATTERNS = {
    "items": re.compile(r'\bid: "([a-z0-9_.-]+:[a-z0-9_./-]+)"'),
    "entities": re.compile(r'\bentity: "([a-z0-9_.-]+:[a-z0-9_./-]+)"'),
    "dimensions": re.compile(r'\bdimension: "([a-z0-9_.-]+:[a-z0-9_./-]+)"'),
    "structures": re.compile(r'\bstructure: "([a-z0-9_.-]+:[a-z0-9_./-]+)"'),
    "biomes": re.compile(r'\bbiome: "([a-z0-9_.-]+:[a-z0-9_./-]+)"'),
    "advancements": re.compile(r'\badvancement: "([a-z0-9_.-]+:[a-z0-9_./-]+)"'),
}


def newest_jar():
    t = 0
    for d in item_index.DEFAULT_MODS:
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.endswith(".jar"):
                    t = max(t, os.path.getmtime(os.path.join(d, f)))
    return t


REGISTRY = os.path.join(HERE, "registry.json")


def load_index(rebuild=False):
    if rebuild or not os.path.exists(CACHE) or os.path.getmtime(CACHE) < newest_jar():
        idx = item_index.build(item_index.DEFAULT_MODS, item_index.DEFAULT_VANILLA)
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        with open(CACHE, "w", encoding="utf-8") as f:
            json.dump(idx, f)
    else:
        with open(CACHE, encoding="utf-8") as f:
            idx = json.load(f)
    # A registry dump from a running server (import_registry.py) is the authority where it exists:
    # the jar scan also sees disabled items that still ship a model and a lang entry.
    idx["source"] = "jar scan"
    if os.path.exists(REGISTRY):
        with open(REGISTRY, encoding="utf-8") as f:
            reg = json.load(f)
        for kind, ids in reg.items():
            if ids:
                idx[kind] = {i: "registry" for i in ids}
        idx["source"] = "registry dump + jar scan (advancements)"
    return idx


def main(argv):
    rebuild = "--rebuild" in argv
    dirs = [a for a in argv if not a.startswith("--")] or [DEFAULT_DIR]
    idx = load_index(rebuild)
    found = {k: {} for k in PATTERNS}  # kind -> id -> first file
    for root in dirs:
        for dirpath, _, files in os.walk(root):
            for f in files:
                if not f.endswith(".snbt") or dirpath.endswith("lang"):
                    continue
                path = os.path.join(dirpath, f)
                text = open(path, encoding="utf-8").read()
                for kind, rx in PATTERNS.items():
                    for v in rx.findall(text):
                        found[kind].setdefault(v, os.path.relpath(path, root))
    bad = 0
    for kind, ids in found.items():
        for v, where in sorted(ids.items()):
            if v not in idx[kind]:
                bad += 1
                near = difflib.get_close_matches(v, idx[kind].keys(), n=3, cutoff=0.75)
                print(f"UNKNOWN {kind[:-1]} {v} ({where})" + (f"  did you mean {', '.join(near)}?" if near else ""))
    total = sum(len(v) for v in found.values())
    print(f"checked {total} distinct IDs ({', '.join(f'{len(v)} {k}' for k, v in found.items())}) "
          f"against the {idx['source']} ({idx['jars']} jars): {'OK' if not bad else f'{bad} unknown'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
