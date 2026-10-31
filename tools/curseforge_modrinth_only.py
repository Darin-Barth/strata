"""Mark the Modrinth-only files (tools/curseforge-manual.json, "_modrinth_only") as server-only before
`packwiz cf export`, so the CurseForge zip leaves them out instead of copying them into its overrides.
Run on a throwaway checkout (the CurseForge Action does), then `packwiz refresh`; never commit the result.

Usage: python -I tools/curseforge_modrinth_only.py     (from the repo root)
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = json.load(open(os.path.join(ROOT, "tools", "curseforge-manual.json"), encoding="utf-8"))["_modrinth_only"]["files"]
for f in files:
    p = os.path.join(ROOT, f)
    t = open(p, encoding="utf-8").read()
    open(p, "w", encoding="utf-8", newline="").write(re.sub(r'^side = "\w+"', 'side = "server"', t, count=1, flags=re.M))
    print(f"left out of the CurseForge zip: {f}")
