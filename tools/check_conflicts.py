"""Report declared incompatibilities between mods in the pack (Modrinth metadata only).

Reads mods/*.pw.toml, fetches each Modrinth file's version and lists "incompatible" dependencies
that point at another project already in the pack. Usage: python -I -X utf8 tools/check_conflicts.py
"""
import json
import tomllib
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "Strata-modpack-builder/0.1"}


def get(path):
    req = urllib.request.Request("https://api.modrinth.com/v2" + path, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    by_project, versions = {}, []
    for f in sorted(ROOT.glob("*/*.pw.toml")):
        meta = tomllib.loads(f.read_text(encoding="utf-8"))
        mr = meta.get("update", {}).get("modrinth")
        if mr:
            by_project[mr["mod-id"]] = meta["name"]
            versions.append(mr["version"])
    hits = []
    for i in range(0, len(versions), 100):
        ids = json.dumps(versions[i:i + 100])
        for v in get("/versions?ids=" + urllib.parse.quote(ids)):
            for d in v["dependencies"]:
                if d["dependency_type"] == "incompatible" and d.get("project_id") in by_project:
                    hits.append((by_project[v["project_id"]], by_project[d["project_id"]]))
    print(f"{len(by_project)} Modrinth projects checked")
    for a, b in sorted(set(hits)):
        print(f"INCOMPATIBLE: {a} declares {b}")


if __name__ == "__main__":
    main()
