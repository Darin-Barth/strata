"""Build an index of registry IDs from mod jars (read-only).

- items: an item model (assets/<ns>/models/item/<path>.json) or a lang key
  item.<ns>.<path> / block.<ns>.<path>
- entities: lang key entity.<ns>.<path>
- dimensions, structures, biomes, advancements: data/<ns>/<kind>/<path>.json
Jars inside jars (META-INF/jarjar) are scanned too. The vanilla 1.21.1 client
jar supplies minecraft: IDs.

Usage: python -I tools/quests/item_index.py [--mods DIR ...] [--vanilla JAR] --out FILE
"""
import argparse
import io
import json
import os
import re
import sys
import zipfile

MODEL_RE = re.compile(r"^assets/([a-z0-9_.-]+)/models/item/([a-z0-9_./-]+)\.json$")
LANG_RE = re.compile(r"^assets/([a-z0-9_.-]+)/lang/en_us\.json$")
KEY_RE = re.compile(r'"(item|block|entity)\.([a-z0-9_-]+)\.([a-z0-9_./-]+)"\s*:\s*"((?:[^"\\]|\\.)*)"')
DATA_RE = re.compile(
    r"^data/([a-z0-9_.-]+)/(dimension|worldgen/structure|worldgen/biome|advancement)/([a-z0-9_./-]+)\.json$")
DATA_KIND = {"dimension": "dimensions", "worldgen/structure": "structures",
             "worldgen/biome": "biomes", "advancement": "advancements"}

HOME = os.path.expanduser("~")
REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
# Darin's client profile has every client+both mod; server/mods adds the server-only ones.
DEFAULT_MODS = [
    os.path.join(os.environ.get("APPDATA", ""), "ModrinthApp", "profiles", "Strata-0.1.1", "mods"),
    os.path.join(REPO, "server", "mods"),
]
DEFAULT_VANILLA = os.path.join(HOME, "curseforge", "minecraft", "Install", "versions", "1.21.1", "1.21.1.jar")
BUILTIN_DIMENSIONS = ["minecraft:overworld", "minecraft:the_nether", "minecraft:the_end"]


def scan_zip(zf, source, idx):
    for n in zf.namelist():
        m = MODEL_RE.match(n)
        if m:
            idx["items"].setdefault(f"{m.group(1)}:{m.group(2)}", source)
            continue
        m = DATA_RE.match(n)
        if m:
            idx[DATA_KIND[m.group(2)]].setdefault(f"{m.group(1)}:{m.group(3)}", source)
            continue
        if LANG_RE.match(n):
            text = zf.read(n).decode("utf-8", "replace")
            for kind, ns, path, val in KEY_RE.findall(text):
                if "." in path:  # item.ns.foo.tooltip and similar sub-keys
                    continue
                iid = f"{ns}:{path}"
                bucket = "entities" if kind == "entity" else "items"
                idx[bucket].setdefault(iid, source)
                idx["names"].setdefault(iid, val)
        elif n.endswith(".jar") and n.startswith("META-INF/"):
            try:
                with zipfile.ZipFile(io.BytesIO(zf.read(n))) as inner:
                    scan_zip(inner, source, idx)
            except zipfile.BadZipFile:
                pass


KJS_ID_RE = re.compile(r"(?:create\(|frame:|igniter:)\s*'([a-z0-9_]+:[a-z0-9_/]+)'")


def scan_kubejs(root, idx):
    """The pack's own KubeJS items/blocks (startup scripts) and datapack files (kubejs/data)."""
    for dirpath, _, files in os.walk(root):
        for f in files:
            full = os.path.join(dirpath, f)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            m = DATA_RE.match(rel)
            if m:
                idx[DATA_KIND[m.group(2)]].setdefault(f"{m.group(1)}:{m.group(3)}", "kubejs")
            elif rel.startswith("startup_scripts/") and f.endswith(".js"):
                with open(full, encoding="utf-8") as fh:
                    for iid in KJS_ID_RE.findall(fh.read()):
                        idx["items"].setdefault(iid, "kubejs")


def build(mods_dirs, vanilla):
    idx = {k: {} for k in ("items", "entities", "dimensions", "structures", "biomes", "advancements", "names")}
    seen, jars = set(), 0
    for d in mods_dirs:
        if not os.path.isdir(d):
            continue
        for j in sorted(os.listdir(d)):
            if not j.endswith(".jar") or j in seen:
                continue
            seen.add(j)
            jars += 1
            with zipfile.ZipFile(os.path.join(d, j)) as zf:
                scan_zip(zf, j, idx)
    if vanilla and os.path.exists(vanilla):
        with zipfile.ZipFile(vanilla) as zf:
            scan_zip(zf, "minecraft", idx)
    scan_kubejs(os.path.join(REPO, "kubejs"), idx)
    for dim in BUILTIN_DIMENSIONS:
        idx["dimensions"].setdefault(dim, "minecraft")
    idx["jars"] = jars
    return idx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mods", action="append", default=None)
    ap.add_argument("--vanilla", default=DEFAULT_VANILLA)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    idx = build(a.mods or DEFAULT_MODS, a.vanilla)
    if not idx["jars"]:
        sys.exit("no mod jars found; pass --mods")
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(idx, f)
    print(f"{idx['jars']} jars: " + ", ".join(f"{len(idx[k])} {k}" for k in
                                             ("items", "entities", "dimensions", "structures", "biomes")))


if __name__ == "__main__":
    main()
