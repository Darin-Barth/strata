"""Generate the Pokémon world datapack (kubejs/data/...) for Strata.

The Pokémon world is a "vanilla + Cobblemon" dimension, pokeworld:pokeworld. This script
builds it from vanilla 1.21.1 worldgen data plus the mod jars, so the result can be
regenerated after a Cobblemon or structure-mod update:

  * pokeworld:pokeworld dimension type, noise settings, density functions and noises
    (deep copies of vanilla, so Tectonic's overrides of minecraft:overworld/* don't apply)
  * a pokeworld:<name> copy of every vanilla Overworld biome, wired into an explicit
    multi-noise biome list (TerraBlender / Regions Unexplored only touch the Overworld)
  * Cobblemon's code-injected placed features: the originals are neutered (count 0)
    everywhere, and pokeworld:cobblemon/<path> copies are listed directly in the matching
    pokeworld biomes (same biome tags Cobblemon uses, mapped from vanilla biome to copy)
  * pokeworld biomes added to Cobblemon's own biome tags (spawn conditions, evolutions)
  * Cobblemon + Cobblemon structure-mod structures retargeted to pokeworld-only biome tags
  * vanilla Overworld structures copied as pokeworld:<name> (villages use jigsaw pool
    aliases so their houses pool keeps Cobblemon's Pokécenters)

Inputs (see docs/design-doc.md, "Pokémon world"):
  --vanilla  extracted misode/mcmeta tag 1.21.1-data (the folder that contains data/)
  --params   biome_parameters/minecraft/overworld.json from the vanilla server's
             data generator (java -DbundlerMainClass=net.minecraft.data.Main -jar
             server.jar --reports)
  --mods     folder with the pack's mod jars (e.g. a test server's mods/)
  --neoforge the NeoForge universal jar (for the c: biome tags)
  --cobblemon-features  JSON list of {feature, step, tag} that Cobblemon injects in code
             (tools/pokeworld/cobblemon_injected.json, read from Cobblemon's bytecode)
  --out      kubejs/data

Run from the repo root:  python tools/build_pokeworld.py --vanilla ... --out kubejs/data
"""
import argparse
import copy
import json
import os
import re
import shutil
import zipfile
from collections import defaultdict

NS = 'pokeworld'
DIM = f'{NS}:{NS}'
STEPS = ['raw_generation', 'lakes', 'local_modifications', 'underground_structures',
         'surface_structures', 'strongholds', 'underground_ores', 'underground_decoration',
         'fluid_springs', 'vegetal_decoration', 'top_layer_modification']
# Structure mods whose structures move to the Pokémon world (plus Cobblemon itself).
STRUCTURE_MODS = ['cobblemon', 'integrated_cobblemon', 'cobblestructures',
                  'cobblemon_simple_center', 'cobblemonextrastructures']
# Vanilla structures left out of the Pokémon world.
SKIP_VANILLA_STRUCTURES = {'stronghold'}
VILLAGE_TYPES = ['plains', 'desert', 'savanna', 'snowy', 'taiga']


def rl(s):
    return s if ':' in s else 'minecraft:' + s


def path_of(s):
    return rl(s).split(':', 1)[1]


class Data:
    """Merged view of data/ files from vanilla + jars."""

    def __init__(self):
        self.tags = defaultdict(list)   # (registry, id) -> [values]
        self.files = {}                 # (kind, id) -> json, first-come (vanilla first)
        self.jar_files = defaultdict(dict)  # jar name -> {(kind, id): json}

    def add_tag(self, registry, tag_id, j):
        vals = j.get('values', [])
        if j.get('replace'):
            self.tags[(registry, tag_id)] = []
        self.tags[(registry, tag_id)].extend(vals)

    def load_dir(self, root):
        for dp, _, fns in os.walk(root):
            for fn in fns:
                if not fn.endswith('.json'):
                    continue
                full = os.path.join(dp, fn)
                rel = os.path.relpath(full, root).replace(os.sep, '/')
                self._add(rel, lambda f=full: json.load(open(f, encoding='utf-8')), None)

    def load_jar(self, jar):
        name = os.path.basename(jar)
        with zipfile.ZipFile(jar) as z:
            for n in z.namelist():
                if n.startswith('data/') and n.endswith('.json'):
                    self._add(n, lambda n=n: json.loads(z.read(n).decode('utf-8-sig')), name)

    def _add(self, rel, loader, jar):
        m = re.match(r'data/([^/]+)/(.+)\.json$', rel)
        if not m:
            return
        ns, p = m.groups()
        tm = re.match(r'tags/(worldgen/biome|worldgen/structure)/(.+)$', p)
        try:
            if tm:
                self.add_tag(tm.group(1), f'{ns}:{tm.group(2)}', loader())
                return
            km = re.match(r'(worldgen/[a-z_]+|dimension_type|dimension|neoforge/biome_modifier|'
                          r'lithostitched/worldgen_modifier)/(.+)$', p)
            if km:
                j = loader()
                key = (km.group(1), f'{ns}:{km.group(2)}')
                self.files.setdefault(key, j)
                if jar:
                    self.jar_files[jar][key] = j
        except (ValueError, UnicodeDecodeError):
            pass

    def resolve_tag(self, registry, tag_id, seen=None):
        seen = seen or set()
        if (registry, tag_id) in seen:
            return set()
        seen.add((registry, tag_id))
        out = set()
        for v in self.tags.get((registry, tag_id), []):
            vid = v['id'] if isinstance(v, dict) else v
            if vid.startswith('#'):
                out |= self.resolve_tag(registry, rl(vid[1:]), seen)
            else:
                out.add(rl(vid))
        return out

    def resolve_holderset(self, hs, universe, registry='worldgen/biome'):
        if hs is None:
            return set()
        if isinstance(hs, str):
            return self.resolve_tag(registry, rl(hs[1:])) if hs.startswith('#') else {rl(hs)}
        if isinstance(hs, list):
            out = set()
            for x in hs:
                out |= self.resolve_holderset(x, universe, registry)
            return out
        t = hs.get('type')
        if t == 'neoforge:any':
            return set(universe)
        if t == 'neoforge:and':
            sets = [self.resolve_holderset(v, universe, registry) for v in hs['values']]
            return set.intersection(*sets) if sets else set()
        if t == 'neoforge:or':
            out = set()
            for v in hs['values']:
                out |= self.resolve_holderset(v, universe, registry)
            return out
        if t == 'neoforge:not':
            return set(universe) - self.resolve_holderset(hs['value'], universe, registry)
        return set()


class Writer:
    def __init__(self, out):
        self.out = out
        self.count = 0

    def write(self, ns, path, obj):
        f = os.path.join(self.out, ns, path)
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, 'w', encoding='utf-8', newline='\n') as fh:
            json.dump(obj, fh, indent=2, ensure_ascii=False)
            fh.write('\n')
        self.count += 1


def deep_copy_noise(vanilla, w):
    """Copy overworld noise settings with every density function / noise it uses."""
    dfs, noises = {}, {}

    def load(kind, i):
        f = os.path.join(vanilla, 'data', 'minecraft', 'worldgen', kind, path_of(i) + '.json')
        return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else None

    def remap(o, key=None):
        if isinstance(o, dict):
            return {k: remap(v, k) for k, v in o.items()}
        if isinstance(o, list):
            return [remap(v, key) for v in o]
        if isinstance(o, str) and o.startswith('minecraft:') and key != 'type':
            if key == 'noise':
                if load('noise', o) is not None:
                    if o not in noises:
                        noises[o] = None
                        noises[o] = load('noise', o)
                    return f'{NS}:{path_of(o)}'
            elif load('density_function', o) is not None:
                if o not in dfs:
                    dfs[o] = None
                    dfs[o] = remap(load('density_function', o))
                return f'{NS}:{path_of(o)}'
        return o

    ns_settings = remap(load('noise_settings', 'minecraft:overworld'))
    w.write(NS, 'worldgen/noise_settings/pokeworld.json', ns_settings)
    for i, j in dfs.items():
        w.write(NS, f'worldgen/density_function/{path_of(i)}.json', j)
    for i, j in noises.items():
        w.write(NS, f'worldgen/noise/{path_of(i)}.json', j)
    return len(dfs), len(noises)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--vanilla', required=True)
    ap.add_argument('--params', required=True)
    ap.add_argument('--mods', required=True)
    ap.add_argument('--neoforge', required=True)
    ap.add_argument('--cobblemon-features', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    # Clean previous output of this script (only folders it owns; pokeworld/spawn_rules and
    # pokeworld/worldportal are hand-written).
    for sub in [f'{NS}/worldgen', f'{NS}/dimension', f'{NS}/dimension_type', f'{NS}/tags',
                'cobblemon/worldgen/placed_feature', 'cobblemon/tags/worldgen/biome',
                'cobblemon/worldgen/structure', 'integrated_cobblemon/worldgen/structure',
                'cobblestructures/worldgen/structure', 'cobblemon_simple_center/worldgen/structure',
                'cobblemonextrastructures/worldgen/structure', 'minecraft/tags/worldgen/structure']:
        shutil.rmtree(os.path.join(a.out, sub), ignore_errors=True)

    d = Data()
    d.load_dir(a.vanilla)
    d.load_jar(a.neoforge)
    jars = sorted(f for f in os.listdir(a.mods) if f.endswith('.jar'))
    for j in jars:
        d.load_jar(os.path.join(a.mods, j))
    w = Writer(a.out)
    vroot = os.path.join(a.vanilla, 'data', 'minecraft')

    def vjson(kind, i):
        return json.load(open(os.path.join(vroot, kind, path_of(i) + '.json'), encoding='utf-8'))

    # --- biomes list -------------------------------------------------------------
    params = json.load(open(a.params, encoding='utf-8'))['biomes']
    vbiomes = sorted({p['biome'] for p in params})
    universe = set(vbiomes)
    to_pw = {b: f'{NS}:{path_of(b)}' for b in vbiomes}

    def map_hs(hs):
        """Pokeworld biomes whose vanilla original is in holder set hs."""
        return sorted(to_pw[b] for b in d.resolve_holderset(hs, universe) if b in to_pw)

    # --- dimension ---------------------------------------------------------------
    w.write(NS, 'dimension_type/pokeworld.json', vjson('dimension_type', 'minecraft:overworld'))
    ndf, nnoise = deep_copy_noise(a.vanilla, w)
    w.write(NS, 'dimension/pokeworld.json', {
        'type': DIM,
        'generator': {
            'type': 'minecraft:noise',
            'settings': DIM,
            'biome_source': {'type': 'minecraft:multi_noise',
                             'biomes': [{'biome': to_pw[p['biome']], 'parameters': p['parameters']}
                                        for p in params]},
        },
    }, compact=True)  # 7,593 biome entries

    # --- Cobblemon features ------------------------------------------------------
    injected = json.load(open(a.cobblemon_features, encoding='utf-8'))
    per_biome = defaultdict(lambda: defaultdict(list))  # pw biome -> step -> [feature]
    copied = []
    for f in injected:
        fid = f['feature']
        orig = d.files.get(('worldgen/placed_feature', fid))
        if orig is None:
            print('WARN missing placed feature', fid)
            continue
        # Neuter the original everywhere (Overworld, Nether, End, modded dimensions).
        w.write('cobblemon', f'worldgen/placed_feature/{path_of(fid)}.json',
                {'feature': orig['feature'], 'placement': [{'type': 'minecraft:count', 'count': 0}]})
        targets = sorted(to_pw.values()) if f['tag'] is None else map_hs('#' + f['tag'])
        if not targets:
            continue
        cid = f'{NS}:cobblemon/{path_of(fid)}'
        w.write(NS, f'worldgen/placed_feature/cobblemon/{path_of(fid)}.json', orig)
        copied.append(cid)
        for b in targets:
            per_biome[b][f['step']].append(cid)
    # Injected IDs must not be referenced from inside other features (they are neutered).
    injected_ids = {f['feature'] for f in injected}
    for (kind, i), j in d.files.items():
        if kind in ('worldgen/configured_feature', 'worldgen/placed_feature') and i.startswith('cobblemon:'):
            s = json.dumps(j)
            for x in injected_ids:
                if f'"feature": "{x}"' in s and i != x:
                    print('WARN', i, 'references neutered', x)

    # --- biomes ------------------------------------------------------------------
    for b in vbiomes:
        j = vjson('worldgen/biome', b)
        feats = j.get('features', [])
        feats = [list(s) for s in feats] + [[] for _ in range(len(STEPS) - len(feats))]
        for step, lst in per_biome[to_pw[b]].items():
            feats[STEPS.index(step)].extend(lst)
        j['features'] = feats
        w.write(NS, f'worldgen/biome/{path_of(b)}.json', j)
    w.write(NS, 'tags/worldgen/biome/is_pokeworld.json', {'values': sorted(to_pw.values())})

    # --- Cobblemon biome tags: add the pokeworld copies --------------------------
    ntags = 0
    for (reg, tid) in list(d.tags):
        if reg != 'worldgen/biome' or not tid.startswith('cobblemon:'):
            continue
        vals = map_hs('#' + tid)
        if vals:
            w.write('cobblemon', f'tags/worldgen/biome/{path_of(tid)}.json', {'replace': False, 'values': vals})
            ntags += 1

    # --- Cobblemon + structure-mod structures -> pokeworld biomes ----------------
    report = []
    for (kind, sid), j in sorted(d.files.items()):
        if kind != 'worldgen/structure' or sid.split(':')[0] not in STRUCTURE_MODS:
            continue
        vals = map_hs(j.get('biomes'))
        if not vals:
            # Nether / End structures (Integrated Cobblemon's fire, psychic and dragon gyms)
            # stay where their mod puts them; only Overworld structures move.
            report.append((sid, 0))
            continue
        tag = f'{NS}:has_structure/{sid.replace(":", "/")}'
        w.write(NS, f'tags/worldgen/biome/has_structure/{sid.replace(":", "/")}.json', {'values': vals})
        nj = copy.deepcopy(j)
        nj['biomes'] = '#' + tag
        ns, p = sid.split(':')
        w.write(ns, f'worldgen/structure/{p}.json', nj)
        report.append((sid, len(vals)))

    # --- vanilla structures -> pokeworld copies ----------------------------------
    vstruct_dir = os.path.join(vroot, 'worldgen', 'structure')
    vcopied = {}
    for fn in sorted(os.listdir(vstruct_dir)):
        sid = 'minecraft:' + fn[:-5]
        if fn[:-5] in SKIP_VANILLA_STRUCTURES:
            continue
        j = vjson('worldgen/structure', sid)
        vals = map_hs(j.get('biomes'))
        if not vals:
            continue  # Nether / End structures
        name = fn[:-5]
        pid = f'{NS}:{name}'
        w.write(NS, f'tags/worldgen/biome/has_structure/minecraft/{name}.json', {'values': vals})
        nj = copy.deepcopy(j)
        nj['biomes'] = f'#{NS}:has_structure/minecraft/{name}'
        if name.startswith('village_'):
            vt = name[len('village_'):]
            nj['pool_aliases'] = [{'type': 'minecraft:direct',
                                   'alias': f'minecraft:village/{vt}/houses',
                                   'target': f'{NS}:village/{vt}/houses'}]
        w.write(NS, f'worldgen/structure/{name}.json', nj)
        vcopied[sid] = pid
    # Village houses pools for the Pokémon world = Cobblemon's version (with Pokécenters).
    for vt in VILLAGE_TYPES:
        pool = None
        for jar, files in d.jar_files.items():
            if jar.lower().startswith('cobblemon-') and ('worldgen/template_pool', f'minecraft:village/{vt}/houses') in files:
                pool = files[('worldgen/template_pool', f'minecraft:village/{vt}/houses')]
        if pool is None:
            pool = vjson('worldgen/template_pool', f'minecraft:village/{vt}/houses')
            print('WARN no Cobblemon houses pool for', vt)
        w.write(NS, f'worldgen/template_pool/village/{vt}/houses.json', pool)
    # Structure sets.
    sset_dir = os.path.join(vroot, 'worldgen', 'structure_set')
    copied_sets = {}
    for fn in sorted(os.listdir(sset_dir)):
        j = vjson('worldgen/structure_set', 'minecraft:' + fn[:-5])
        entries = [dict(e, structure=vcopied[e['structure']]) for e in j['structures'] if e['structure'] in vcopied]
        if entries:
            copied_sets['minecraft:' + fn[:-5]] = (j, entries)
    for sid, (j, entries) in copied_sets.items():
        nj = copy.deepcopy(j)
        nj['structures'] = entries
        ez = nj['placement'].get('exclusion_zone')
        if ez:
            if ez['other_set'] in copied_sets:
                ez['other_set'] = f'{NS}:{path_of(ez["other_set"])}'
            else:
                del nj['placement']['exclusion_zone']
        w.write(NS, f'worldgen/structure_set/{path_of(sid)}.json', nj)
    # Vanilla structure tags (village, shipwreck, on_treasure_maps, ...) get the copies too.
    for (reg, tid) in list(d.tags):
        if reg != 'worldgen/structure' or not tid.startswith('minecraft:') or tid == 'minecraft:eye_of_ender_located':
            continue
        members = d.resolve_tag(reg, tid)
        vals = sorted(vcopied[m] for m in members if m in vcopied)
        if vals:
            w.write('minecraft', f'tags/worldgen/structure/{path_of(tid)}.json', {'replace': False, 'values': vals})

    # --- report + leak check -----------------------------------------------------
    print(f'{w.count} files; {len(vbiomes)} biomes, {ndf} density functions, {nnoise} noises, '
          f'{len(copied)} Cobblemon feature copies, {ntags} Cobblemon tags, '
          f'{len(vcopied)} vanilla structures, {len(copied_sets)} structure sets')
    for sid, n in report:
        if n == 0:
            print('  kept in its own dimension (no Overworld biomes):', sid)
    # Which other structures / biome modifiers would reach pokeworld biomes, given the
    # Cobblemon tags now contain them?
    for (reg, tid) in list(d.tags):
        if reg == 'worldgen/biome' and tid.startswith('cobblemon:'):
            d.tags[(reg, tid)].extend(map_hs('#' + tid))
    pw = set(to_pw.values())
    pw_universe = universe | pw
    for (kind, i), j in sorted(d.files.items()):
        if i.split(':')[0] in STRUCTURE_MODS + [NS] and kind == 'worldgen/structure':
            continue
        hs = None
        if kind == 'worldgen/structure':
            hs = j.get('biomes')
        elif kind == 'neoforge/biome_modifier':
            hs = j.get('biomes')
        elif kind == 'lithostitched/worldgen_modifier':
            hs = j.get('biomes')
        if hs is None:
            continue
        hit = d.resolve_holderset(hs, pw_universe) & pw
        if hit:
            print(f'  LEAK {kind} {i} reaches {len(hit)} pokeworld biomes')


if __name__ == '__main__':
    main()
