"""Decode a .sparkprofile (spark_sampler.proto SamplerData) and rank mods by self time.

Each stack node's self time (its time minus its children's) is credited to the nearest frame,
from that node up toward the thread root, whose class (or class.method, for mixin-injected
methods) maps to a mod in class_sources / method_sources. Frames with no mod are "minecraft/neoforge/jdk".
Usage: python spark_blame.py <file.sparkprofile> [thread-name-substring ...]
"""
import collections
import struct
import sys


def fields(buf):
    i, n = 0, len(buf)
    while i < n:
        key, i = varint(buf, i)
        num, wt = key >> 3, key & 7
        if wt == 0:
            v, i = varint(buf, i)
        elif wt == 1:
            v, i = buf[i:i + 8], i + 8
        elif wt == 2:
            ln, i = varint(buf, i)
            v, i = buf[i:i + ln], i + ln
        elif wt == 5:
            v, i = buf[i:i + 4], i + 4
        else:
            raise ValueError(f"wire type {wt}")
        yield num, wt, v


def varint(buf, i):
    r = s = 0
    while True:
        b = buf[i]; i += 1
        r |= (b & 0x7F) << s; s += 7
        if not b & 0x80:
            return r, i


def packed_doubles(v):
    return list(struct.unpack(f"<{len(v) // 8}d", v))


def packed_varints(v):
    out, i = [], 0
    while i < len(v):
        x, i = varint(v, i); out.append(x)
    return out


def parse_map(v):
    k = val = ""
    for num, _, x in fields(v):
        if num == 1: k = x.decode("utf8", "replace")
        elif num == 2: val = x.decode("utf8", "replace")
    return k, val


def parse_node(v):
    node = {"cls": "", "meth": "", "times": [], "kids": []}
    for num, wt, x in fields(v):
        if num == 3: node["cls"] = x.decode("utf8", "replace")
        elif num == 4: node["meth"] = x.decode("utf8", "replace")
        elif num == 8: node["times"] += packed_doubles(x) if wt == 2 else [struct.unpack("<d", x)[0]]
        elif num == 9: node["kids"] += packed_varints(x) if wt == 2 else [x]
    return node


def parse_thread(v):
    t = {"name": "", "nodes": [], "times": [], "roots": []}
    for num, wt, x in fields(v):
        if num == 1: t["name"] = x.decode("utf8", "replace")
        elif num == 3: t["nodes"].append(parse_node(x))
        elif num == 4: t["times"] += packed_doubles(x) if wt == 2 else [struct.unpack("<d", x)[0]]
        elif num == 5: t["roots"] += packed_varints(x) if wt == 2 else [x]
    return t


def main():
    data = open(sys.argv[1], "rb").read()
    filters = [f.lower() for f in sys.argv[2:]]
    threads, class_src, method_src = [], {}, {}
    for num, _, v in fields(data):
        if num == 2: threads.append(parse_thread(v))
        elif num == 3: k, s = parse_map(v); class_src[k] = s
        elif num == 4: k, s = parse_map(v); method_src[k] = s

    def mod_of(n):
        return method_src.get(f"{n['cls']}.{n['meth']}") or class_src.get(n["cls"])

    IDLE = ("Unsafe.park", "LockSupport.park", "Object.wait", "Thread.sleep", "Thread.onSpinWait", "EPoll", "epoll",
            "ForkJoinPool.awaitWork", "SelectorImpl", "Thread.yield", "WatchService", "LinkedBlockingQueue.take",
            "managedBlock", "BlockableEventLoop.waitForTasks", "MinecraftServer.waitUntilNextTick", "MinecraftServer.waitForTasks", "sable_rapier")
    def is_idle(n):
        sig = f"{n['cls']}.{n['meth']}"
        return any(k in sig for k in IDLE)
    STAGE_CLS = ("ChunkStatusTasks", "ChunkGenerator", "NoiseBasedChunkGenerator", "LevelLightEngine", "ChunkMap", "ChunkStorage", "RegionFile", "StructureStart", "StructureManager")
    def stage_of(n):
        c = n["cls"].rsplit(".", 1)[-1]
        if any(c == k or c.startswith(k + "$") for k in STAGE_CLS):
            return f"{c.split('$')[0]}.{n['meth']}"
        return None
    stages = collections.Counter()
    blame, per_thread, top_frames = collections.Counter(), collections.Counter(), collections.defaultdict(collections.Counter)
    grand = 0.0
    for t in threads:
        if filters and not any(f in t["name"].lower() for f in filters):
            continue
        nodes = t["nodes"]
        tot = lambda n: sum(n["times"])
        per_thread[t["name"]] += sum(t["times"])
        stack = [(r, None, None) for r in t["roots"]]
        while stack:
            idx, inherited, stage = stack.pop()
            n = nodes[idx]
            if is_idle(n):
                continue
            owner = mod_of(n) or inherited
            stage = stage or stage_of(n)
            self_t = tot(n) - sum(tot(nodes[c]) for c in n["kids"])
            if self_t > 0:
                stages[stage or "(other)"] += self_t
                key = owner or "minecraft/neoforge/jdk"
                blame[key] += self_t; grand += self_t
                top_frames[key][f"{n['cls'].rsplit('.', 1)[-1]}.{n['meth']}"] += self_t
            for c in n["kids"]:
                stack.append((c, owner, stage))

    print(f"threads analysed: {len(per_thread)}; total sampled time {grand / 1000:.1f} s")
    groups = collections.Counter()
    for name, v in per_thread.items():
        groups[name.rstrip("0123456789-# ").strip() or name] += v
    print("by thread group:", ", ".join(f"{k}: {v / 1000:.0f}s" for k, v in groups.most_common(8)))
    print("\nbusy time by outermost worldgen/chunk step:")
    for st, v in stages.most_common(16):
        print(f"  {100 * v / grand:5.1f}%  {st}")
    print("\nhottest frames overall:")
    allf = collections.Counter()
    for fr in top_frames.values():
        allf.update(fr)
    for f, v in allf.most_common(15):
        print(f"  {100 * v / grand:5.1f}%  {f}")
    print("\nself time by mod (nearest mod frame):")
    for mod, v in blame.most_common(25):
        frames = ", ".join(f for f, _ in top_frames[mod].most_common(3))
        print(f"  {100 * v / grand:5.1f}%  {mod:28}  e.g. {frames}")


if __name__ == "__main__":
    main()
