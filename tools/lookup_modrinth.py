"""Look up every tracker query on Modrinth and record whether a 1.21.1 NeoForge build exists.

Writes tools/lookup-results.json. Usage: python -I tools/lookup_modrinth.py
"""
import difflib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from queries import QUERIES  # noqa: E402

API = "https://api.modrinth.com/v2"
UA = "Strata-modpack-builder/0.1 (packwiz setup)"
OUT = Path(__file__).parent / "lookup-results.json"
# Loaders that count as "works on 1.21.1 NeoForge" per Modrinth project type.
OK_LOADERS = {"mod": {"neoforge"}, "resourcepack": {"minecraft"}, "shader": {"iris", "optifine"},
              "datapack": {"datapack", "neoforge"}}


def get(path, **params):
    url = API + path
    if params:
        url += "?" + urllib.parse.urlencode({k: json.dumps(v) if isinstance(v, list) else v
                                              for k, v in params.items()})
    for attempt in range(5):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code == 429:
                time.sleep(10)
                continue
            raise
    raise RuntimeError(url)


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower().replace("&", "and"))


def build_for(project_id, project_type):
    vers = get(f"/project/{project_id}/version", game_versions=["1.21.1"]) or []
    ok = OK_LOADERS.get(project_type, {"neoforge"})
    good = [v for v in vers if ok & set(v["loaders"])]
    if not good:
        return None
    v = good[0]
    return {"version": v["version_number"], "type": v["version_type"], "date": v["date_published"][:10],
            "loaders": v["loaders"]}


def candidates(term):
    if term.startswith("slug:"):
        p = get(f"/project/{term[5:]}")
        return [{"slug": p["slug"], "title": p["title"], "id": p["id"], "type": p["project_type"],
                 "downloads": p["downloads"], "author": None, "sim": 1.0}] if p else []
    res = get("/search", query=term, limit=10)["hits"]
    out = []
    for h in res:
        sim = difflib.SequenceMatcher(None, norm(term), norm(h["title"])).ratio()
        out.append({"slug": h["slug"], "title": h["title"], "id": h["project_id"], "type": h["project_type"],
                    "downloads": h["downloads"], "author": h["author"], "sim": round(sim, 2)})
    return sorted(out, key=lambda c: (-c["sim"], -c["downloads"]))


def main():
    results = {}
    for row, terms in QUERIES.items():
        results[row] = []
        for term in terms:
            cands = candidates(term)
            # Check builds for the closest few so ambiguous names can be compared.
            for c in cands[:4]:
                if c["sim"] >= 0.6:
                    c["build"] = build_for(c["id"], c["type"])
            results[row].append({"term": term, "candidates": cands[:6]})
            print(f"{row[:40]:40} {term[:30]:30} -> " +
                  (f"{cands[0]['slug']} ({cands[0]['sim']}) build={bool(cands[0].get('build'))}" if cands else "none"),
                  flush=True)
    OUT.write_text(json.dumps(results, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
