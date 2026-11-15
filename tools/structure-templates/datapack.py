"""Finish or check the server-only `strata_templates` datapack (pre-upgraded structure templates).

Usage:
  python -I tools/structure-templates/datapack.py finish <strata_templates dir> <mods dir>
  python -I tools/structure-templates/datapack.py check  <strata_templates dir> <mods dir>

`finish` writes pack.mcmeta and manifest.json (for every upgraded template: the mod jar it came from, the sha1 of
the original file and its old DataVersion). `check` compares the manifest with the mod jars and lists templates
whose original changed or disappeared, or that a jar now ships in an old format without an upgraded copy: any
output means the datapack must be regenerated (README.md here), or the stale copies would override the mod's new
pieces. Sources are the mod jars plus the repo's own kubejs/data; vanilla's own old templates (Minecraft's jar) are
recorded without a hash.
"""
import hashlib
import json
import pathlib
import sys
import zipfile

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
KEY = b'\x03\x00\x0bDataVersion'


def data_version(raw):
    import zlib
    try:
        data = zlib.decompressobj(31).decompress(raw)  # tolerant of trailing junk, like the game's reader
    except zlib.error:
        data = raw
    i = data.find(KEY)
    return int.from_bytes(data[i + len(KEY):i + len(KEY) + 4], 'big') if i >= 0 else 500


def sources(mods):
    """id path ('data/<ns>/structure/...nbt') -> list of (source name, bytes loader)."""
    out = {}
    for jar in sorted(pathlib.Path(mods).glob('*.jar')):
        try:
            z = zipfile.ZipFile(jar)
        except zipfile.BadZipFile:
            continue
        for n in z.namelist():
            parts = n.split('/')
            if len(parts) > 3 and parts[0] == 'data' and parts[2] == 'structure' and n.endswith('.nbt'):
                out.setdefault(n, []).append((jar.name, lambda z=z, n=n: z.read(n)))
    for f in (REPO / 'kubejs/data').glob('*/structure/**/*.nbt'):
        n = 'data/' + f.relative_to(REPO / 'kubejs/data').as_posix()
        out.setdefault(n, []).append(('kubejs/data', lambda f=f: f.read_bytes()))
    return out


def main():
    if len(sys.argv) != 4 or sys.argv[1] not in ('finish', 'check'):
        sys.exit(__doc__)
    pack, src = pathlib.Path(sys.argv[2]), sources(sys.argv[3])
    files = sorted(p.relative_to(pack).as_posix() for p in (pack / 'data').rglob('*.nbt'))
    if sys.argv[1] == 'finish':
        manifest, missing = {}, []
        for n in files:
            if n not in src:
                if n.startswith('data/minecraft/'):  # vanilla's own templates (Minecraft's jar, never changes)
                    manifest[n] = {'source': 'minecraft', 'sha1': None, 'data_version': None, 'others': []}
                else:
                    missing.append(n)
                continue
            name, load = src[n][-1]
            raw = load()
            manifest[n] = {'source': name, 'sha1': hashlib.sha1(raw).hexdigest(), 'data_version': data_version(raw),
                           'others': [s for s, _ in src[n][:-1]]}
        (pack / 'pack.mcmeta').write_text(json.dumps({'pack': {'pack_format': 48, 'description':
            'Strata: structure templates pre-upgraded to 1.21.1 (server only; tools/structure-templates)'}}, indent=2) + '\n')
        (pack / 'manifest.json').write_text(json.dumps(manifest, indent=0, sort_keys=True) + '\n')
        size = sum((pack / n).stat().st_size for n in files)
        print(f'{len(files)} templates, {size / 1e6:.0f} MB; {len(missing)} without a source in the jars')
        for n in missing[:20]:
            print('  no source:', n)
        return
    manifest = json.loads((pack / 'manifest.json').read_text())
    stale = []
    for n, m in manifest.items():
        hashes = {hashlib.sha1(load()).hexdigest() for _, load in src.get(n, [])}
        if m['source'] == 'minecraft' and not hashes:
            continue
        if m['sha1'] not in hashes:
            stale.append(('changed or removed', n))
    for n in set(manifest) ^ set(files):
        stale.append(('manifest and files differ', n))
    for n, lst in src.items():
        if n not in manifest and data_version(lst[-1][1]()) < 3955:
            stale.append(('old format, no upgraded copy', n))
    for why, n in sorted(stale):
        print(f'{why}: {n}')
    print(f'{len(stale)} problem(s) in {len(manifest)} templates' if stale else f'up to date: {len(manifest)} templates')
    sys.exit(1 if stale else 0)


if __name__ == '__main__':
    main()
