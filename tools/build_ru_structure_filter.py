"""Regions Unexplored features without Lithostitched's `in_structure` filter.

Some Regions Unexplored placed features (cave bioshrooms, dropleaf, redstone
buds and bulbs, prismarite, lava falls, overworld lava deltas, Inferno ash
vents) skip spots near structures with a `not lithostitched:in_structure`
block predicate. That predicate (Lithostitched 1.8.1) ignores the generation
region it is given and calls ServerLevel.getChunk(..., STRUCTURE_REFERENCES)
from the world-generation thread, which hands the request to the main thread
and blocks until it is answered. On the live server (Nov 12) a world-gen worker
sat in that wait for minutes, the chunks around it never finished, the main
thread spun on their unloads, and players nearby saw land stop loading.

This copies each affected placed feature from the Regions Unexplored jar with
that filter removed, into kubejs/data/regions_unexplored/worldgen/placed_feature/.
Trade-off: these small decorations can now also generate inside structures.

Usage: python -I tools/build_ru_structure_filter.py <mods dir>
Re-run after a Regions Unexplored update.
"""
import json
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'kubejs', 'data', 'regions_unexplored', 'worldgen', 'placed_feature')
PREFIX = 'data/regions_unexplored/worldgen/placed_feature/'


def uses_filter(node):
    if isinstance(node, dict):
        return node.get('type') == 'lithostitched:in_structure' or any(uses_filter(v) for v in node.values())
    if isinstance(node, list):
        return any(uses_filter(v) for v in node)
    return False


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    mods = sys.argv[1]
    jars = [f for f in os.listdir(mods) if f.startswith('regions-unexplored') and f.endswith('.jar')]
    if len(jars) != 1:
        sys.exit(f'expected one Regions Unexplored jar in {mods}, found {jars}')
    z = zipfile.ZipFile(os.path.join(mods, jars[0]))
    written = []
    for name in sorted(z.namelist()):
        if not (name.startswith(PREFIX) and name.endswith('.json')):
            continue
        feature = json.loads(z.read(name))
        if not uses_filter(feature):
            continue
        kept = [p for p in feature['placement'] if not uses_filter(p)]
        if uses_filter(kept) or len(kept) != len(feature['placement']) - 1:
            sys.exit(f'{name}: expected exactly one top-level placement step with the filter')
        out = {'neoforge:conditions': [{'type': 'neoforge:mod_loaded', 'modid': 'regions_unexplored'}]}
        out.update(feature)
        out['placement'] = kept
        path = os.path.join(OUT, *name[len(PREFIX):].split('/'))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(out, f, indent=2)
            f.write('\n')
        written.append(name[len(PREFIX):-len('.json')])
    if not written:
        sys.exit('no Regions Unexplored placed feature uses lithostitched:in_structure any more; remove this generator')
    print(f'{len(written)} placed features -> {os.path.relpath(OUT, ROOT)}: {", ".join(written)}')


if __name__ == '__main__':
    main()
