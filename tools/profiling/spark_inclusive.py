"""Inclusive (self + children) busy time per method on matching threads, counted once per stack path."""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spark_blame import fields, parse_thread, parse_map  # noqa: E402
IDLE = ("Unsafe.park", "LockSupport.park", "Object.wait", "Thread.sleep", "EPoll", "awaitWork", "waitForTasks", "waitUntilNextTick", "sable_rapier", "managedBlock")
data = open(sys.argv[1], "rb").read(); filt = sys.argv[2].lower()
inc = collections.Counter(); grand = 0.0; class_src = {}; method_src = {}
for num, _, v in fields(data):
    if num == 3: k, s = parse_map(v); class_src[k] = s
    elif num == 4: k, s = parse_map(v); method_src[k] = s
mods_inc = collections.Counter()
for num, _, v in fields(data):
    if num != 2: continue
    t = parse_thread(v)
    if filt not in t["name"].lower(): continue
    nodes = t["nodes"]; tot = lambda n: sum(n["times"])
    stack = [(r, frozenset(), frozenset()) for r in t["roots"]]
    while stack:
        i, seen, mods = stack.pop(); n = nodes[i]
        sig = f"{n['cls']}.{n['meth']}"
        if any(k in sig for k in IDLE): continue
        short = f"{n['cls'].rsplit('.',1)[-1]}.{n['meth']}"
        st = tot(n) - sum(tot(nodes[c]) for c in n["kids"])
        m = method_src.get(sig) or class_src.get(n["cls"])
        seen2 = seen | {short}; mods2 = mods | ({m} if m else set())
        if st > 0:
            grand += st
            for s_ in seen2: inc[s_] += st
            for m_ in mods2: mods_inc[m_] += st
        stack += [(c, seen2, mods2) for c in n["kids"]]
print(f"busy time on '{filt}': {grand/1000:.0f} s")
print("\nmods anywhere on the busy stack (inclusive):")
for m, v in mods_inc.most_common(20): print(f"  {100*v/grand:5.1f}%  {m}")
print("\nhot methods (inclusive):")
for k, v in inc.most_common(int(sys.argv[3]) if len(sys.argv) > 3 else 45): print(f"  {100*v/grand:5.1f}%  {k}")
