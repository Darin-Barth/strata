"""Print the heaviest self-time stacks (leaf first) for threads matching a filter, to see what dominates."""
import sys, os, heapq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spark_blame import fields, parse_thread  # noqa: E402
data = open(sys.argv[1], "rb").read(); filt = sys.argv[2].lower(); top = []
for num, _, v in fields(data):
    if num != 2: continue
    t = parse_thread(v)
    if filt not in t["name"].lower(): continue
    nodes = t["nodes"]; tot = lambda n: sum(n["times"])
    stack = [(r, ()) for r in t["roots"]]
    while stack:
        i, path = stack.pop(); n = nodes[i]
        p = path + (f"{n['cls'].rsplit('.',1)[-1]}.{n['meth']}",)
        st = tot(n) - sum(tot(nodes[c]) for c in n["kids"])
        if st > 0: heapq.heappush(top, (st, t["name"], p[::-1][:9])); top = heapq.nlargest(12, top)
        stack += [(c, p) for c in n["kids"]]
for st, name, p in sorted(top, reverse=True):
    print(f"{st/1000:8.1f}s {name}\n    " + "\n    ".join(p))
