"""Import a registry dump (from registry_dump.js) into tools/quests/registry.json.

The jar scan in item_index.py can't see items a mod disables or only registers under some
conditions (they still ship a model and a lang entry), so check_ids.py treats this dump as the
authority for items, entities, structures, biomes and dimensions when it exists.

To refresh it after mod changes:
1. Copy registry_dump.js into a server's kubejs/server_scripts/ (scratch copy, not the shipped pack).
2. Start the server once; it logs "STRATAREG <kind> <id>" lines to logs/kubejs/server.log.
3. python -I tools/quests/import_registry.py <path to that server.log>
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "registry.json")
LINE_RE = re.compile(r"STRATAREG (items|entities|structures|biomes|dimensions) (\S+)")


def main(argv):
    if not argv:
        sys.exit(__doc__)
    reg = {k: set() for k in ("items", "entities", "structures", "biomes", "dimensions")}
    with open(argv[0], encoding="utf-8", errors="replace") as f:
        for line in f:
            m = LINE_RE.search(line)
            if m:
                reg[m.group(1)].add(m.group(2))
    if not reg["items"]:
        sys.exit("no STRATAREG lines found")
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump({k: sorted(v) for k, v in reg.items()}, f, indent=0)
    print(", ".join(f"{len(v)} {k}" for k, v in reg.items()), "->", OUT)


if __name__ == "__main__":
    main(sys.argv[1:])
