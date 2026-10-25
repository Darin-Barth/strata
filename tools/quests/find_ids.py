"""Search the ID index (built by check_ids.py) by regex on the ID or its English name.

Usage: python -I tools/quests/find_ids.py [-items|-entities|-dimensions|-structures|-biomes|-advancements] REGEX...
Example: python -I tools/quests/find_ids.py "^mekanism:.*(infuser|alloy)" "Jetpack"
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_ids  # noqa: E402


def main(argv):
    kind = "items"
    if argv and argv[0].startswith("-"):
        kind, argv = argv[0][1:], argv[1:]
    idx = check_ids.load_index()
    names = idx["names"]
    for pat in argv:
        rx = re.compile(pat, re.I)
        hits = sorted(k for k in idx[kind] if rx.search(k) or rx.search(names.get(k, "")))
        print(f"## {pat} ({len(hits)}{', first 150 shown' if len(hits) > 150 else ''})")
        print("  ".join(k + (f"[{names[k]}]" if names.get(k) else "") for k in hits[:150]))


if __name__ == "__main__":
    main(sys.argv[1:])
