"""Add CurseForge IDs to the Modrinth-sourced files so `packwiz cf export` builds a proper CurseForge zip.

The pack stays Modrinth-first: each mod keeps its Modrinth download, and gets an `[update.curseforge]`
section naming the same file on CurseForge. `packwiz cf export` lists a mod with a CurseForge ID in
manifest.json (the CurseForge app downloads it); one without is copied into the zip's overrides, which
CurseForge only accepts for its approved non-CurseForge mods (tools/curseforge-manual.json says which).

How it matches: the jars are fingerprinted with `packwiz cf detect`, so an ID is only added when
CurseForge hosts the byte-identical file. A few authors upload separate builds of the same version to
each site; those are listed by hand in tools/curseforge-manual.json (keyed by our filename, so a mod
update drops the mapping until it is checked again).

Re-run after every mod update or add (the release checklist does): it rewrites every generated
section, so stale IDs never survive.

Usage: python -I tools/curseforge_ids.py     (from the repo root; needs packwiz on PATH or in ~/go/bin)
"""
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDERS = ["mods", "resourcepacks", "shaderpacks"]
MANUAL = os.path.join(ROOT, "tools", "curseforge-manual.json")
CACHE = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~/.cache")), "packwiz", "cache")
CF_SECTION = re.compile(r"\n\[update\.curseforge\]\n(?:[^\[\n].*\n?)*")


def packwiz():
    for p in [shutil.which("packwiz"), os.path.expanduser("~/go/bin/packwiz.exe"), os.path.expanduser("~/go/bin/packwiz")]:
        if p and os.path.exists(p):
            return p
    sys.exit("packwiz not found")


def field(text, name):
    m = re.search(rf'^{name} = "(.*)"', text, re.M)
    return m.group(1) if m else None


def modrinth_files():
    """Every metadata file downloaded from Modrinth: path -> (text, filename, sha512, url)."""
    out = {}
    for folder in FOLDERS:
        for p in sorted(glob.glob(os.path.join(ROOT, folder, "*.pw.toml"))):
            t = open(p, encoding="utf-8").read()
            if "[update.modrinth]" in t:
                out[p] = (t, field(t, "filename"), field(t, "hash"), field(t, "url"))
    return out


def gather(files, dest):
    """Copy each file's jar into dest (from packwiz's cache, else downloaded). Returns sha1 -> path."""
    want = {sha512: p for p, (_, _, sha512, _) in files.items()}
    found = {}
    if os.path.isdir(CACHE):
        for d, _, names in os.walk(CACHE):
            for n in names:
                src = os.path.join(d, n)
                data = open(src, "rb").read()
                h = hashlib.sha512(data).hexdigest()
                if h in want and want[h] not in found:
                    found[want[h]] = data
    for p, (_, fn, sha512, url) in files.items():
        if p not in found:
            req = urllib.request.Request(url, headers={"User-Agent": "strata-modpack (github.com/Darin-Barth/strata)"})
            found[p] = urllib.request.urlopen(req).read()
    by_sha1 = {}
    for p, data in found.items():
        name = os.path.basename(p).replace(".pw.toml", "") + "__" + files[p][1]
        if not name.endswith((".jar", ".zip")):
            name += ".jar"
        open(os.path.join(dest, name), "wb").write(data)
        by_sha1[hashlib.sha1(data).hexdigest()] = p
    return by_sha1


def detect(work, pw):
    """Run `packwiz cf detect` in a throwaway pack; returns sha1 -> (project-id, file-id)."""
    shutil.copy(os.path.join(ROOT, "pack.toml"), os.path.join(work, "pack.toml"))
    pack = open(os.path.join(work, "pack.toml"), encoding="utf-8").read()
    pack = re.sub(r'(\[index\][^\[]*?)\nhash = "[^"\n]*"', r"\1", pack)
    open(os.path.join(work, "pack.toml"), "w", encoding="utf-8").write(pack)
    open(os.path.join(work, "index.toml"), "w", encoding="utf-8").write('hash-format = "sha256"\n')
    subprocess.run([pw, "refresh"], cwd=work, capture_output=True)
    r = subprocess.run([pw, "cf", "detect"], cwd=work, capture_output=True, text=True)
    m = re.search(r"Successfully matched (\d+) files", r.stdout + r.stderr)
    if not m:
        sys.exit("packwiz cf detect failed:\n" + r.stdout + r.stderr)
    ids = {}
    for p in glob.glob(os.path.join(work, "mods", "*.pw.toml")):
        t = open(p, encoding="utf-8").read()
        ids[field(t, "hash")] = (int(re.search(r"project-id = (\d+)", t).group(1)),
                                 int(re.search(r"file-id = (\d+)", t).group(1)))
    return ids


def main():
    pw = packwiz()
    files = modrinth_files()
    manual = {k: v for k, v in json.load(open(MANUAL, encoding="utf-8")).items() if not k.startswith("_")}
    with tempfile.TemporaryDirectory() as work:
        os.makedirs(os.path.join(work, "mods"))
        by_sha1 = gather(files, os.path.join(work, "mods"))
        detected = detect(work, pw)
    ids = {by_sha1[s]: v for s, v in detected.items() if s in by_sha1}
    changed, missing = 0, []
    for p, (t, fn, _, _) in files.items():
        new = CF_SECTION.sub("\n", t).rstrip("\n") + "\n"
        entry = ids.get(p)
        if entry is None and fn in manual:
            entry = (manual[fn]["project-id"], manual[fn]["file-id"])
        if entry:
            new += f"[update.curseforge]\nfile-id = {entry[1]}\nproject-id = {entry[0]}\n"
        elif field(t, "side") != "server":     # server-only files never go into the players' zip
            missing.append(fn)
        if new != t:
            open(p, "w", encoding="utf-8", newline="").write(new)
            changed += 1
    stale = [k for k in manual if k not in {v[1] for v in files.values()}]
    print(f"{len(files)} Modrinth files: {len(ids)} matched on CurseForge, "
          f"{sum(1 for v in files.values() if v[1] in manual)} from curseforge-manual.json, "
          f"{len(missing)} players need without one; {changed} rewritten")
    for fn in missing:
        print(f"  no CurseForge file (goes into the zip's overrides): {fn}")
    for k in stale:
        print(f"  curseforge-manual.json entry no longer used (mod updated? check it): {k}")
    print("Now run `packwiz refresh`.")


if __name__ == "__main__":
    main()
