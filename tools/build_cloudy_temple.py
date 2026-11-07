"""Legendary Monsters Cloudy Temple: place its Stratlings from the main thread (Nov 6, 2026).

A Stratling fills its trade list whenever it is loaded (StratlingEntity.readAdditionalSaveData -> populateTrades ->
createRandomEnchantedBook), and that draws from the *level's* random generator. When world generation places a
Cloudy Temple piece, the entity is loaded on a world-generation thread, so it uses the level's random at the same time
as the server thread does: "Accessing LegacyRandomSource from multiple threads" crashed the server on Nov 6.

This copies the temple pieces that hold Stratlings into kubejs/data (same IDs, so they override the mod's) with every
Stratling replaced by a minecraft:marker tagged "strata_stratling". kubejs/server_scripts/strata_stratling.js turns
each marker back into a Stratling on the server thread when the chunk enters the world. Temples generated before this
are unchanged (their Stratlings already exist).

Usage: python -I tools/build_cloudy_temple.py <path to the Legendary Monsters jar>
Re-run after a Legendary Monsters update (it reports the pieces it rewrote).
"""
import gzip
import io
import struct
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "kubejs" / "data" / "legendary_monsters" / "structure"
TAG = "strata_stratling"
STRATLING = "legendary_monsters:stratling"


# Minimal typed NBT reader/writer: every value is kept as (type id, value) so a rewrite keeps the original types.
def read_payload(f, t):
    if t == 1: return struct.unpack(">b", f.read(1))[0]
    if t == 2: return struct.unpack(">h", f.read(2))[0]
    if t == 3: return struct.unpack(">i", f.read(4))[0]
    if t == 4: return struct.unpack(">q", f.read(8))[0]
    if t == 5: return struct.unpack(">f", f.read(4))[0]
    if t == 6: return struct.unpack(">d", f.read(8))[0]
    if t == 7:
        n = struct.unpack(">i", f.read(4))[0]
        return f.read(n)
    if t == 8:
        n = struct.unpack(">H", f.read(2))[0]
        return f.read(n).decode("utf-8")
    if t == 9:
        et = f.read(1)[0]
        n = struct.unpack(">i", f.read(4))[0]
        return (et, [read_payload(f, et) for _ in range(n)])
    if t == 10:
        d = {}
        while True:
            tt = f.read(1)[0]
            if tt == 0:
                return d
            n = struct.unpack(">H", f.read(2))[0]
            key = f.read(n).decode("utf-8")  # read the name first (Python evaluates an assignment's value before its key)
            d[key] = (tt, read_payload(f, tt))
    if t == 11:
        n = struct.unpack(">i", f.read(4))[0]
        return list(struct.unpack(">%di" % n, f.read(4 * n)))
    if t == 12:
        n = struct.unpack(">i", f.read(4))[0]
        return list(struct.unpack(">%dq" % n, f.read(8 * n)))
    raise ValueError("bad tag %d" % t)


def write_payload(out, t, v):
    if t == 1: out.write(struct.pack(">b", v))
    elif t == 2: out.write(struct.pack(">h", v))
    elif t == 3: out.write(struct.pack(">i", v))
    elif t == 4: out.write(struct.pack(">q", v))
    elif t == 5: out.write(struct.pack(">f", v))
    elif t == 6: out.write(struct.pack(">d", v))
    elif t == 7:
        out.write(struct.pack(">i", len(v))); out.write(v)
    elif t == 8:
        b = v.encode("utf-8"); out.write(struct.pack(">H", len(b))); out.write(b)
    elif t == 9:
        et, items = v
        out.write(bytes([et if items else (et or 0)])); out.write(struct.pack(">i", len(items)))
        for item in items:
            write_payload(out, et, item)
    elif t == 10:
        for k, (tt, vv) in v.items():
            out.write(bytes([tt])); kb = k.encode("utf-8")
            out.write(struct.pack(">H", len(kb))); out.write(kb)
            write_payload(out, tt, vv)
        out.write(b"\x00")
    elif t == 11:
        out.write(struct.pack(">i", len(v))); out.write(struct.pack(">%di" % len(v), *v))
    elif t == 12:
        out.write(struct.pack(">i", len(v))); out.write(struct.pack(">%dq" % len(v), *v))
    else:
        raise ValueError("bad tag %d" % t)


def load(data):
    f = io.BytesIO(gzip.decompress(data))
    t = f.read(1)[0]
    n = struct.unpack(">H", f.read(2))[0]
    name = f.read(n).decode("utf-8")
    return t, name, read_payload(f, t)


def dump(t, name, root):
    out = io.BytesIO()
    out.write(bytes([t])); nb = name.encode("utf-8")
    out.write(struct.pack(">H", len(nb))); out.write(nb)
    write_payload(out, t, root)
    return gzip.compress(out.getvalue(), mtime=0)


def marker(nbt):
    """A marker at the Stratling's spot, keeping its position and facing."""
    keep = {k: nbt[k] for k in ("Pos", "Rotation") if k in nbt}
    m = {"id": (8, "minecraft:marker"), "Tags": (9, (8, [TAG]))}
    m.update(keep)
    return m


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    jar = zipfile.ZipFile(sys.argv[1])
    prefix = "data/legendary_monsters/structure/"
    written = []
    for name in sorted(jar.namelist()):
        if not (name.startswith(prefix) and name.endswith(".nbt")):
            continue
        t, rname, root = load(jar.read(name))
        et, ents = root.get("entities", (9, (10, [])))[1]
        count = 0
        for e in ents:
            nbt = e["nbt"][1]
            if nbt.get("id", (8, ""))[1] == STRATLING:
                e["nbt"] = (10, marker(nbt))
                count += 1
        if count:
            dest = OUT / name[len(prefix):]
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(dump(t, rname, root))
            written.append((name[len(prefix):], count))
    for n, c in written:
        print("%s: %d Stratling(s) -> marker" % (n, c))
    if not written:
        print("No Stratlings found: the mod changed; check whether this override is still needed.")


if __name__ == "__main__":
    main()
