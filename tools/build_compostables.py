"""Composting fix: mod items that only register in vanilla's old compost list.

NeoForge 1.21.1's composter reads only the `neoforge:compostables` data map
(ComposterBlock.getValue). Some mods still put their items into the old
`ComposterBlock.COMPOSTABLES` map, which nothing in the game reads any more
(EMI does, so it shows a chance the composter then refuses). This writes those
items into the data map, with the same chances the mods use.

Found by scanning every mod jar for writes to the old map (Nov 10). Covered on
their own: mods that also ship the data map (Ars Nouveau, Immersive Engineering,
Integrated Dynamics, Regions Unexplored) and Let's Do Vinery (its Foundation
library patches the composter itself).

Usage: python -I tools/build_compostables.py <mods dir>
Re-run after a Croptopia, Alex's Mobs, Friends & Foes, Critters and Companions
or Naturalist update.
"""
import json
import os
import re
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'kubejs', 'data', 'neoforge', 'data_maps', 'item', 'compostables.json')

# Fixed lists, read from each mod's registration code (chances as the mod sets them).
FIXED = {
    'alexsmobs': {'banana': 0.65, 'banana_peel': 1.0, 'acacia_blossom': 0.65, 'gongylidia': 0.9},
    'friendsandfoes': {'buttercup': 0.65},
    'crittersandcompanions': {'acorn': 0.3},
    # Naturalist ships its data map at data/naturalist/neoforge/..., a path NeoForge never reads.
    'naturalist': {'snail_shell': 0.65},
}


def croptopia(mods_dir):
    """Croptopia's Composter.init(): crops 0.65 and seeds 0.3, tree fruits 0.65 and saplings 0.5."""
    jars = [f for f in os.listdir(mods_dir) if f.startswith('croptopia') and f.endswith('.jar')]
    if len(jars) != 1:
        sys.exit(f'expected one Croptopia jar in {mods_dir}, found {jars}')
    names = zipfile.ZipFile(os.path.join(mods_dir, jars[0])).namelist()
    items = {m.group(1) for n in names if (m := re.fullmatch(r'assets/croptopia/models/item/([a-z0-9_]+)\.json', n))}
    out = {}
    for item in sorted(items):
        if item.endswith('_seed'):
            out[item] = 0.3
            out[item[:-len('_seed')]] = 0.65
        elif item.endswith('_sapling'):
            out[item] = 0.5
            if item[:-len('_sapling')] in items:  # apple_sapling grows vanilla apples
                out[item[:-len('_sapling')]] = 0.65
    missing = [i for i in out if i not in items]
    if missing:
        sys.exit(f'Croptopia items not found: {missing}')
    return out


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    lists = dict(FIXED)
    lists['croptopia'] = croptopia(sys.argv[1])
    values = {}
    for modid in sorted(lists):
        for item, chance in sorted(lists[modid].items()):
            values[f'{modid}:{item}'] = {
                'neoforge:conditions': [{'type': 'neoforge:mod_loaded', 'modid': modid}],
                'neoforge:value': {'chance': chance},
            }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'values': values}, f, indent=2)
        f.write('\n')
    counts = ', '.join(f'{m} {len(v)}' for m, v in sorted(lists.items()))
    print(f'{len(values)} items -> {os.path.relpath(OUT, ROOT)} ({counts})')


if __name__ == '__main__':
    main()
