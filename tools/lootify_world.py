"""Find already-generated chests that still hold a structure template's baked-in items.

Reads a world copy's region files (read-only) and lists every chest/trapped chest/barrel with no
LootTable whose contents match a signature in tools/lootify_index.json (written by
lootify_structures.py). Matching on exact contents means player-made chests are never touched,
and chests someone has already taken from no longer match. The result is a list of commands to
run on the live server (forceload, swap items for the loot table, unload); Lootr converts the
chest the next time it loads.

Usage: python -I tools/lootify_world.py <world copy dir> <out commands.txt>
"""
import io
import json
import struct
import sys
import zlib
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import nbtlib

ROOT = Path(__file__).resolve().parent.parent
INDEX = json.load(open(ROOT / "tools" / "lootify_index.json"))
CONTAINERS = {"minecraft:chest", "minecraft:trapped_chest", "minecraft:barrel"}
DIMS = {"region": "minecraft:overworld", "DIM-1/region": "minecraft:the_nether", "DIM1/region": "minecraft:the_end"}


def signature(items):
    return json.dumps(sorted([str(i["id"]), int(i.get("count", i.get("Count", 1)))] for i in items))


def scan_region(path):
    hits = []
    data = Path(path).read_bytes()
    if len(data) < 8192:
        return hits
    for i in range(1024):
        off = struct.unpack(">I", data[i * 4:i * 4 + 4])[0]
        if not off:
            continue
        start = (off >> 8) * 4096
        length, comp = struct.unpack(">IB", data[start:start + 5])
        raw = data[start + 5:start + 4 + length]
        try:
            buf = zlib.decompress(raw) if comp == 2 else raw
            chunk = nbtlib.File.parse(io.BytesIO(buf))
        except Exception:
            continue
        for be in chunk.get("block_entities", []):
            if str(be.get("id")) not in CONTAINERS or "LootTable" in be or "Items" not in be or not be["Items"]:
                continue
            table = INDEX.get(signature(be["Items"]))
            if table:
                hits.append((int(be["x"]), int(be["y"]), int(be["z"]), table))
    return hits


def main():
    world, out = Path(sys.argv[1]), Path(sys.argv[2])
    jobs = []
    for region_dir in sorted(world.rglob("region")):
        rel = region_dir.relative_to(world).as_posix()
        dim = DIMS.get(rel) or ":".join(rel.split("/")[1:3])  # dimensions/<ns>/<path>/region
        jobs += [(dim, str(p)) for p in region_dir.glob("*.mca")]
    commands, found = [], {}
    with ProcessPoolExecutor() as pool:
        for (dim, _), hits in zip(jobs, pool.map(scan_region, [p for _, p in jobs], chunksize=4)):
            for x, y, z, table in hits:
                found[dim] = found.get(dim, 0) + 1
                cx, cz = x >> 4 << 4, z >> 4 << 4
                commands += [
                    f"execute in {dim} run forceload add {cx} {cz}",
                    f"execute in {dim} run data remove block {x} {y} {z} Items",
                    f'execute in {dim} run data modify block {x} {y} {z} LootTable set value "{table}"',
                    f"execute in {dim} run forceload remove {cx} {cz}",
                ]
    out.write_text("\n".join(commands) + "\n")
    print("matched chests per dimension:", found, "| commands:", len(commands))


if __name__ == "__main__":
    main()
