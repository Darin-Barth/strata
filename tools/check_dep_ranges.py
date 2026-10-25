"""Check every mod jar's required NeoForge dependency version ranges against the versions actually installed.

Server boots only exercise server-side mods, so client-only conflicts (e.g. WaterFrames needing WaterMedia 2.1.x
while 3.0 was installed, Oct 25) slip through. Run it on a client instance's mods folder.
Usage: python tools/check_dep_ranges.py <mods-dir> [--override modid=version ...]
"""
import re
import sys
import tomllib
import zipfile
from pathlib import Path

SKIP = {"minecraft", "neoforge", "forge", "java"}


def version_key(v):
    v = re.sub(r"^\d+\.\d+(\.\d+)?-(?=\d)", "", v) if re.match(r"^1\.2\d", v) and "-" in v else v  # '1.21.1-93-NEOFORGE' -> '93-NEOFORGE'
    v = v.split("+")[0]
    parts = re.split(r"[.\-]", v)
    key = []
    for p in parts:
        key.append((0, int(p), "") if p.isdigit() else (1, 0, p))
    return key


def cmp(a, b):
    ka, kb = version_key(a), version_key(b)
    return (ka > kb) - (ka < kb)


def in_range(version, rng):
    """Maven range check: '[1.0,2.0)', '[1.0,)', '1.0' (minimum), '*' or ''. Comma-joined unions supported.
    Also npm-style '>=1.1.20 <1.2.0' (SuperMartijn642's mods) and the literal 'TODO' some jars ship."""
    rng = rng.strip()
    if rng in ("", "*", "TODO"):
        return True
    if re.match(r"^[<>=]", rng):
        ok = True
        for op, v in re.findall(r"(>=|<=|>|<|=)\s*([^\s]+)", rng):
            c = cmp(version, v)
            ok &= {">=": c >= 0, "<=": c <= 0, ">": c > 0, "<": c < 0, "=": c == 0}[op]
        return ok
    for part in re.findall(r"[\[\(][^\]\)]*[\]\)]|[^,\[\(]+", rng):
        part = part.strip()
        if not part:
            continue
        if part[0] not in "[(":
            if cmp(version, part) >= 0:
                return True
            continue
        lo, _, hi = part[1:-1].partition(",")
        if "," not in part:  # [1.0] exact
            if cmp(version, lo) == 0:
                return True
            continue
        ok_lo = not lo.strip() or (cmp(version, lo.strip()) >= 0 if part[0] == "[" else cmp(version, lo.strip()) > 0)
        ok_hi = not hi.strip() or (cmp(version, hi.strip()) <= 0 if part[-1] == "]" else cmp(version, hi.strip()) < 0)
        if ok_lo and ok_hi:
            return True
    return False


def read_jar(path):
    with zipfile.ZipFile(path) as z:
        return read_zip(z)


def read_zip(z):
    nested = []
    for n in z.namelist():
        if n.startswith("META-INF/jarjar/") and n.endswith(".jar"):
            import io
            try:
                m, _ = read_zip(zipfile.ZipFile(io.BytesIO(z.read(n))))
                nested += m
            except zipfile.BadZipFile:
                pass
    if True:
        try:
            meta = tomllib.loads(z.read("META-INF/neoforge.mods.toml").decode("utf-8", "replace"))
        except (KeyError, tomllib.TOMLDecodeError):
            return nested, {}
        manifest = ""
        try:
            manifest = z.read("META-INF/MANIFEST.MF").decode("utf-8", "replace")
        except KeyError:
            pass
        impl = re.search(r"Implementation-Version:\s*(\S+)", manifest)
        mods = []
        for m in meta.get("mods", []):
            v = str(m.get("version", ""))
            if "${" in v:
                v = impl.group(1) if impl else ""
            mods.append((m.get("modId"), v))
        return mods + nested, meta.get("dependencies", {})


def main():
    mods_dir = Path(sys.argv[1])
    overrides = dict(a.split("=", 1) for a in sys.argv[2:] if "=" in a)
    provided, deps = {}, []
    for jar in sorted(mods_dir.glob("*.jar")):
        mods, dep_tables = read_jar(jar)
        for mod_id, v in mods:
            provided[mod_id] = v
        if not isinstance(dep_tables, dict):  # a few jars write [[dependencies]] without the mod id key
            dep_tables = {mods[0][0] if mods else "?": dep_tables}
        for owner, lst in dep_tables.items():
            for d in lst if isinstance(lst, list) else []:
                kind = str(d.get("type", "required" if d.get("mandatory", True) else "optional")).lower()
                deps.append((jar.name, owner, d.get("modId"), kind, str(d.get("versionRange", ""))))
    provided.update(overrides)
    problems = 0
    for jar, owner, dep, kind, rng in deps:
        if dep in SKIP:
            continue
        have = provided.get(dep)
        if have is None:
            if kind == "required":
                print(f"MISSING  {owner} ({jar}) requires {dep} {rng}")
                problems += 1
            continue
        if kind in ("required", "optional") and have and not in_range(have, rng):
            print(f"RANGE    {owner} ({jar}) wants {dep} {rng}, installed {have} [{kind}]")
            problems += 1
        if kind == "incompatible" and have and in_range(have, rng):
            print(f"CONFLICT {owner} ({jar}) is incompatible with installed {dep} {have}")
            problems += 1
    print(f"{len(provided)} mods, {len(deps)} declared dependencies, {problems} problems")


if __name__ == "__main__":
    main()
