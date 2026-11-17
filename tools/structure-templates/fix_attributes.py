"""Fix structure templates saved in Minecraft 1.21.2 or later for use on 1.21.1.

Usage: python tools/structure-templates/fix_attributes.py <output dir> <mod jar> [<mod jar> ...]

1.21.2 renamed every attribute (`minecraft:generic.max_health` became `minecraft:max_health`, and so on). A
template saved in a newer version keeps the new names, 1.21.1 does not know them, and it silently drops them:
mobs lose their designed health, damage and size ("Ignoring unknown attribute" warnings) and their gear loses its
bonuses ("Tried to load invalid item" errors). Sunken Spires 1.0 ships four such templates (data version 4189):
its Colosseum guardian came out with 20 health instead of 180 (Nov 17).

This writes corrected copies of the affected templates only, under <output dir>/data/<namespace>/structure/.
They go into the server-only `strata_templates` datapack (see README.md), never into the pack or this repo when
the mod is All Rights Reserved. Needs nbtlib (`pip install nbtlib`). Structures already generated keep the
broken mobs: only newly generated ones are fixed.
"""
import gzip, io, sys, zipfile, pathlib, collections
import nbtlib
G = 'armor armor_toughness attack_damage attack_knockback attack_speed flying_speed follow_range knockback_resistance luck max_absorption max_health movement_speed safe_fall_distance scale step_height gravity jump_strength fall_damage_multiplier burning_time explosion_knockback_resistance movement_efficiency oxygen_bonus water_movement_efficiency'.split()
P = 'block_interaction_range entity_interaction_range block_break_speed mining_efficiency sneaking_speed submerged_mining_speed sweeping_damage_ratio'.split()
MAP = {f'minecraft:{n}': f'minecraft:generic.{n}' for n in G}
MAP.update({f'minecraft:{n}': f'minecraft:player.{n}' for n in P})
MAP['minecraft:spawn_reinforcements'] = 'minecraft:zombie.spawn_reinforcements'

def fix(tag, counts, where=''):
    if isinstance(tag, dict):
        for k in list(tag.keys()):
            v = tag[k]
            if k in ('type', 'id') and isinstance(v, nbtlib.String) and str(v) in MAP and ('attribute' in where or 'modifiers' in where):
                counts[str(v)] += 1
                tag[k] = nbtlib.String(MAP[str(v)])
            else:
                fix(v, counts, where + '/' + k)
    elif isinstance(tag, list):
        for v in tag: fix(v, counts, where)

def fix_bytes(raw):
    f = nbtlib.File.parse(io.BytesIO(gzip.decompress(raw)))
    counts = collections.Counter()
    fix(f, counts)
    out = io.BytesIO()
    f.write(out)
    return gzip.compress(out.getvalue()), counts, int(f.get('DataVersion', 0))

if __name__ == '__main__':
    outdir = pathlib.Path(sys.argv[1])
    for jar in sys.argv[2:]:
        z = zipfile.ZipFile(jar)
        n_all = 0
        for name in z.namelist():
            if not name.endswith('.nbt') or '/structure/' not in name: continue
            n_all += 1
            data, counts, dv = fix_bytes(z.read(name))
            if counts:
                p = outdir / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(data)
                print(f'{pathlib.Path(jar).name}: {name} (DataVersion {dv}): {dict(counts)}')
        print(f'{pathlib.Path(jar).name}: {n_all} templates scanned')
