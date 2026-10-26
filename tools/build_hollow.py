"""Generate The Hollow's datapack (kubejs/data/...) for Strata.

The Hollow (strata:hollow) is an opt-in horror dimension: permanent night, dark fog, grimstone
underground, and every horror mob in the pack confined to it (docs/hollow-design.md). This writes:

  * strata:hollow dimension + dimension type (fixed night, not "natural" so compasses spin)
  * terrain: the Pokemon world's vanilla terrain router (copies under pokeworld:, so Tectonic's
    overrides don't reach it) with Grim & Bleak's Soulsrealm materials and surface rule (grimstone
    underground), plus a surface rule for our copied biomes (grass/dirt/mud on top)
  * strata:hollow_<name> copies of vanilla, Vanilla Backport and Regions Unexplored biomes with the
    Hollow's atmosphere (fog, sky, particles, sounds, music) and no animals; Grim & Bleak's 8
    Soulsrealm biomes are used as they are (they exist only in its own dimension)
  * a multi-noise biome layout and biome tags (#strata:hollow_biomes and subsets); the biomes are
    in no vanilla or c: tags, so Overworld mobs and structures stay out and Hollow ones stay in
  * overrides that point the horror mods' spawns and structures at the Hollow only

Inputs: the repo's Pokemon-world biome copies (kubejs/data/pokeworld/worldgen/biome) and three jars.
Run from the repo root:
  python -I tools/build_hollow.py --backport <VanillaBackport jar> --ru <regions-unexplored jar> \
      --grim <grim_and_bleak jar> --out kubejs/data
"""
import argparse
import copy
import json
import os
import zipfile

NS = "strata"
GB = "grim_and_bleak"

# Copied biomes: id -> (source, path inside source). "poke" = repo pokeworld copy of vanilla.
COPIES = {
    "hollow_dark_forest": ("poke", "dark_forest"),
    "hollow_taiga": ("poke", "old_growth_spruce_taiga"),
    "hollow_swamp": ("poke", "swamp"),
    "hollow_mangrove": ("poke", "mangrove_swamp"),
    "hollow_black_sea": ("poke", "deep_ocean"),
    "hollow_deep_dark": ("poke", "deep_dark"),
    "hollow_dripstone": ("poke", "dripstone_caves"),
    "hollow_pale_garden": ("backport", "data/minecraft/worldgen/biome/pale_garden.json"),
    "hollow_ashen_woodland": ("ru", "data/regions_unexplored/worldgen/biome/ashen_woodland.json"),
    "hollow_blackwood_taiga": ("ru", "data/regions_unexplored/worldgen/biome/blackwood_taiga.json"),
    "hollow_fungal_fen": ("ru", "data/regions_unexplored/worldgen/biome/fungal_fen.json"),
}
GRIM = ["bleakplains", "eerie_forest", "sparse_eerie_forest", "grim_taiga", "grimplains",
        "grimstone_plains", "grimstone_mountains", "snowy_plains"]


def c(name):
    return f"{NS}:{name}"


def g(name):
    return f"{GB}:{name}"


# Biome groups (used for tags that horror mods' spawns and structures are pointed at).
FORESTS = [c("hollow_dark_forest"), c("hollow_pale_garden"), c("hollow_taiga"), c("hollow_blackwood_taiga"),
           c("hollow_ashen_woodland"), g("eerie_forest"), g("sparse_eerie_forest"), g("grim_taiga")]
PLAINS = [g("grimplains"), g("bleakplains"), g("grimstone_plains"), g("snowy_plains")]
WET = [c("hollow_swamp"), c("hollow_mangrove"), c("hollow_fungal_fen")]
SNOWY = [g("snowy_plains"), g("grim_taiga")]
TAIGA = [c("hollow_taiga"), c("hollow_blackwood_taiga"), g("grim_taiga")]
SEA = [c("hollow_black_sea")]
MOUNTAINS = [g("grimstone_mountains")]
CAVES = [c("hollow_deep_dark"), c("hollow_dripstone")]
SURFACE = FORESTS + PLAINS + WET + MOUNTAINS + SEA
ALL = SURFACE + CAVES

# The Hollow's atmosphere for copied biomes. Grim & Bleak's biomes keep their own (already eerie).
FOG, SKY, WATER, WATER_FOG = 0x101318, 0x050608, 0x1E2A2C, 0x070B0D
GRASS, FOLIAGE = 0x4B5A47, 0x3C4A3A
AMBIENT_LOOP = "minecraft:ambient.soul_sand_valley.loop"
ADDITIONS = {"sound": "minecraft:ambient.soul_sand_valley.additions", "tick_chance": 0.0111}
MOOD = {"sound": "minecraft:ambient.cave", "tick_delay": 2400, "block_search_extent": 8, "offset": 2.0}
MUSIC = {"sound": "minecraft:music.overworld.deep_dark", "min_delay": 6000, "max_delay": 18000,
         "replace_current_music": False}
PARTICLES = {
    "hollow_dark_forest": ("minecraft:white_ash", 0.004),
    "hollow_taiga": ("minecraft:white_ash", 0.003),
    "hollow_blackwood_taiga": ("minecraft:ash", 0.006),
    "hollow_ashen_woodland": ("minecraft:ash", 0.01),
    "hollow_pale_garden": ("minecraft:white_ash", 0.006),
    "hollow_swamp": ("minecraft:spore_blossom_air", 0.002),
    "hollow_mangrove": ("minecraft:spore_blossom_air", 0.002),
    "hollow_fungal_fen": ("minecraft:spore_blossom_air", 0.008),
}


def read_json_from(source, path, args):
    if source == "poke":
        with open(os.path.join("kubejs/data/pokeworld/worldgen/biome", path + ".json"), encoding="utf-8") as f:
            return json.load(f)
    jar = {"backport": args.backport, "ru": args.ru}[source]
    with zipfile.ZipFile(jar) as z:
        return json.loads(z.read(path))


def hollow_biome(name, src):
    b = copy.deepcopy(src)
    # Pokemon-world copies carry Cobblemon's features; the Hollow doesn't want them.
    b["features"] = [[f for f in step if not f.startswith("pokeworld:")] for step in b["features"]]
    e = b["effects"]
    keep_grass = name in ("hollow_pale_garden",)  # the Pale Garden's own grey palette fits already
    e.update({"fog_color": FOG, "sky_color": SKY, "water_color": WATER, "water_fog_color": WATER_FOG,
              "ambient_sound": AMBIENT_LOOP, "additions_sound": ADDITIONS, "mood_sound": MOOD, "music": MUSIC})
    if not keep_grass:
        e["grass_color"], e["foliage_color"] = GRASS, FOLIAGE
    if name in PARTICLES:
        p, chance = PARTICLES[name]
        e["particle"] = {"options": {"type": p}, "probability": chance}
    # No animals: the Hollow is hostile country. Keep monsters, bats, and water life.
    sp = b.setdefault("spawners", {})
    sp["creature"] = []
    sp["axolotls"] = []
    b["spawn_costs"] = {k: v for k, v in b.get("spawn_costs", {}).items()}
    return b


def biome_layout():
    """Multi-noise entries. Surface biomes appear at depth 0 and 1 like vanilla's list."""
    T = [[-1.0, -0.45], [-0.45, -0.15], [-0.15, 0.2], [0.2, 0.55], [0.55, 1.0]]
    H_LO, H_HI, W_LO, W_HI = [-1.0, 0.0], [0.0, 1.0], [-1.0, 0.0], [0.0, 1.0]
    ANY = [-1.0, 1.0]
    out = []

    def add(biome, t=ANY, h=ANY, cont=ANY, e=ANY, w=ANY, depths=(0.0, 1.0)):
        for d in depths:
            out.append({"biome": biome, "parameters": {"temperature": t, "humidity": h, "continentalness": cont,
                                                       "erosion": e, "weirdness": w, "depth": d, "offset": 0.0}})

    OCEAN, COAST, INLAND = [-1.2, -0.455], [-0.455, -0.19], [-0.19, 1.0]
    add(c("hollow_black_sea"), cont=OCEAN)
    add(g("grimstone_plains"), t=[-1.0, -0.15], cont=COAST)
    add(c("hollow_swamp"), t=T[2], cont=COAST)
    add(c("hollow_mangrove"), t=[0.2, 1.0], cont=COAST)
    add(g("grimstone_mountains"), cont=[0.3, 1.0], e=[-1.0, -0.375])
    lowlands = [-0.375, 1.0]
    add(g("snowy_plains"), t=T[0], h=H_LO, cont=INLAND, e=lowlands)
    add(g("grim_taiga"), t=T[0], h=H_HI, cont=INLAND, e=lowlands)
    add(c("hollow_taiga"), t=T[1], h=H_LO, cont=INLAND, e=lowlands)
    add(c("hollow_blackwood_taiga"), t=T[1], h=H_HI, cont=INLAND, e=lowlands)
    add(g("eerie_forest"), t=T[2], h=H_LO, cont=INLAND, e=lowlands, w=W_LO)
    add(g("sparse_eerie_forest"), t=T[2], h=H_LO, cont=INLAND, e=lowlands, w=W_HI)
    add(c("hollow_dark_forest"), t=T[2], h=H_HI, cont=INLAND, e=lowlands, w=W_LO)
    add(c("hollow_pale_garden"), t=T[2], h=H_HI, cont=INLAND, e=lowlands, w=W_HI)
    add(g("grimplains"), t=T[3], h=H_LO, cont=INLAND, e=lowlands, w=W_LO)
    add(g("bleakplains"), t=T[3], h=H_LO, cont=INLAND, e=lowlands, w=W_HI)
    add(c("hollow_ashen_woodland"), t=T[3], h=H_HI, cont=INLAND, e=lowlands)
    add(g("grimstone_plains"), t=T[4], h=H_LO, cont=INLAND, e=lowlands)
    add(c("hollow_fungal_fen"), t=T[4], h=H_HI, cont=INLAND, e=lowlands)
    # Caves, placed by depth like vanilla's dripstone caves and deep dark.
    add(c("hollow_dripstone"), cont=[0.8, 1.0], depths=([0.2, 0.9],))
    add(c("hollow_deep_dark"), e=[-1.0, -0.375], depths=(1.1,))
    return out


def surface_rule(grim_rule):
    """Our copied biomes get grass/dirt (mud in wet ones) at the surface; caves and the rest fall
    through to Grim & Bleak's rule (bedrock, grimstone, its own biomes)."""
    def biome_is(ids):
        return {"type": "minecraft:biome", "biome_is": ids}

    def floor(depth_extra):
        return {"type": "minecraft:stone_depth", "surface_type": "floor", "add_surface_depth": depth_extra,
                "secondary_depth_range": 0, "offset": 0}

    def block(name):
        return {"type": "minecraft:block", "result_state": {"Name": name}}

    def top(top_block):
        return {"type": "minecraft:sequence", "sequence": [
            {"type": "minecraft:condition", "if_true": floor(False), "then_run": {"type": "minecraft:sequence", "sequence": [
                {"type": "minecraft:condition", "if_true": {"type": "minecraft:water", "offset": -1,
                                                            "surface_depth_multiplier": 0, "add_stone_depth": False},
                 "then_run": block(top_block)},
                block("minecraft:dirt")]}},
            {"type": "minecraft:condition", "if_true": floor(True), "then_run": block("minecraft:dirt")}]}

    ours_dry = [c(n) for n in COPIES if n not in ("hollow_mangrove", "hollow_swamp", "hollow_black_sea",
                                                    "hollow_deep_dark", "hollow_dripstone")]
    ours = {"type": "minecraft:condition", "if_true": {"type": "minecraft:above_preliminary_surface"},
            "then_run": {"type": "minecraft:sequence", "sequence": [
                {"type": "minecraft:condition", "if_true": biome_is(ours_dry), "then_run": top("minecraft:grass_block")},
                {"type": "minecraft:condition", "if_true": biome_is([c("hollow_mangrove"), c("hollow_swamp")]),
                 "then_run": top("minecraft:mud")},
            ]}}
    return {"type": "minecraft:sequence", "sequence": [ours, grim_rule]}


def write(out, rel, data):
    path = os.path.join(out, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def tag(values):
    return {"replace": True, "values": values}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backport", required=True)
    ap.add_argument("--ru", required=True)
    ap.add_argument("--grim", required=True)
    ap.add_argument("--out", default="kubejs/data")
    args = ap.parse_args()
    out = args.out

    # Biomes
    for name, (source, path) in COPIES.items():
        write(out, f"{NS}/worldgen/biome/{name}.json", hollow_biome(name, read_json_from(source, path, args)))

    # Terrain: Grim & Bleak's Soulsrealm settings on our vanilla density-function copies.
    with zipfile.ZipFile(args.grim) as z:
        realm = json.loads(z.read(f"data/{GB}/dimension/soulsrealm.json"))
    settings = realm["generator"]["settings"]
    settings.pop("name", None)
    # Terrain shape: the Pokemon world's router (vanilla density functions and noises copied under
    # pokeworld:, so Tectonic's overrides don't apply). Materials and surface: Grim & Bleak's.
    with open("kubejs/data/pokeworld/worldgen/noise_settings/pokeworld.json", encoding="utf-8") as f:
        poke = json.load(f)
    for key in ("noise_router", "noise", "spawn_target", "sea_level", "aquifers_enabled"):
        settings[key] = poke[key]
    settings["surface_rule"] = surface_rule(settings["surface_rule"])
    write(out, f"{NS}/worldgen/noise_settings/hollow.json", settings)

    write(out, f"{NS}/dimension_type/hollow.json", {
        "ultrawarm": False, "natural": False, "piglin_safe": False, "respawn_anchor_works": False,
        "bed_works": True, "has_raids": False, "has_skylight": True, "has_ceiling": False,
        "coordinate_scale": 1.0, "ambient_light": 0.0, "fixed_time": 18000,
        "infiniburn": "#minecraft:infiniburn_overworld", "min_y": -64, "height": 384, "logical_height": 384,
        "monster_spawn_light_level": {"type": "minecraft:uniform", "min_inclusive": 0, "max_inclusive": 7},
        "monster_spawn_block_light_limit": 0, "effects": "minecraft:overworld"})
    write(out, f"{NS}/dimension/hollow.json", {
        "type": c("hollow"),
        "generator": {"type": "minecraft:noise", "settings": c("hollow"),
                      "biome_source": {"type": "minecraft:multi_noise", "biomes": biome_layout()}}})

    # Biome tags
    groups = {"hollow_biomes": ALL, "hollow_forests": FORESTS, "hollow_plains": PLAINS, "hollow_wet": WET,
              "hollow_snowy": SNOWY, "hollow_taiga": TAIGA, "hollow_sea": SEA, "hollow_mountains": MOUNTAINS,
              "hollow_caves": CAVES, "hollow_surface": SURFACE, "none": []}
    for name, vals in groups.items():
        write(out, f"{NS}/tags/worldgen/biome/{name}.json", tag(vals))
    hb = f"#{NS}:hollow_biomes"

    # --- Horror mods: spawns and structures in the Hollow only ---
    # Whispering Spirits, The Ravenous: their spawn files target every biome. The Ravenous' own spawn
    # check also wants #minecraft:is_overworld, which Hollow biomes never get, so these two
    # never fire; server_scripts/hollow_ravenous.js spawns it instead.
    write(out, "whispering_spirits/neoforge/biome_modifier/whispering_spirit_biome_modifier.json", {
        "type": "neoforge:add_spawns", "biomes": f"#{NS}:hollow_surface",
        "spawners": {"type": "whispering_spirits:whispering_spirit", "weight": 8, "minCount": 1, "maxCount": 1}})
    for mob, weight in (("the_ravenous", 1), ("the_screecher", 2)):
        write(out, f"the_ravenous/neoforge/biome_modifier/{mob}_biome_modifier.json", {
            "type": "neoforge:add_spawns", "biomes": f"#{NS}:hollow_surface",
            "spawners": {"type": f"the_ravenous:{mob}", "weight": weight, "minCount": 1, "maxCount": 1}})
    # Weeping Angels: spawn and catacombs tags; snow angels nowhere.
    write(out, "weeping_angels/tags/worldgen/biome/spawns/weeping_angels.json",
          tag([f"#{NS}:hollow_forests", f"#{NS}:hollow_snowy", f"#{NS}:hollow_caves"]))
    write(out, "weeping_angels/tags/worldgen/biome/has_structure/catacombs.json", tag([f"#{NS}:hollow_forests"]))
    write(out, "weeping_angels/neoforge/biome_modifier/snow_angel.json", {
        "type": "weeping_angels:snow_angels", "biomes": f"#{NS}:none", "features": "weeping_angels:snow_angel",
        "step": "raw_generation"})
    # Mutant Monsters: its config spawn weights are 0; these are the Hollow's own (rare) spawns.
    write(out, f"{NS}/neoforge/biome_modifier/hollow_mutants.json", {
        "type": "neoforge:add_spawns", "biomes": f"#{NS}:hollow_surface", "spawners": [
            {"type": "mutantmonsters:mutant_zombie", "weight": 2, "minCount": 1, "maxCount": 1},
            {"type": "mutantmonsters:mutant_skeleton", "weight": 1, "minCount": 1, "maxCount": 1},
            {"type": "mutantmonsters:mutant_creeper", "weight": 1, "minCount": 1, "maxCount": 1},
            {"type": "mutantmonsters:mutant_enderman", "weight": 1, "minCount": 1, "maxCount": 1}]})
    # Grim & Bleak: its two portal ruins that sit in Overworld biomes, and its any-biome ore.
    with zipfile.ZipFile(args.grim) as z:
        for s in ("grim_portal_2", "grim_portal_4"):
            st = json.loads(z.read(f"data/{GB}/worldgen/structure/{s}.json"))
            st["biomes"] = f"#{NS}:none"
            write(out, f"{GB}/worldgen/structure/{s}.json", st)
    write(out, f"{GB}/neoforge/biome_modifier/raw_darksteel_block_biome_modifier.json", {
        "type": "neoforge:add_features", "biomes": hb, "features": f"{GB}:raw_darksteel_block",
        "step": "underground_ores"})
    # The Graveyard: every mob spawn tag and structure tag (config decides weights/chances).
    for mob in ("acolyte", "corrupted_evoker", "corrupted_pillager", "corrupted_vindicator", "ghoul", "nightmare",
                "reaper", "revenant", "skeleton_creeper", "tormented_villager", "wraith"):
        write(out, f"graveyard/tags/worldgen/biome/{mob}_spawns.json", tag([f"#{NS}:hollow_surface"]))
    for bird in ("crow", "magpie", "raven"):
        write(out, f"graveyard/tags/worldgen/biome/{bird}_spawns.json", tag([f"#{NS}:hollow_forests"]))
    structures = {
        "altar": [f"#{NS}:hollow_snowy"], "crypt": [f"#{NS}:hollow_surface"],
        "dead_tree": [f"#{NS}:hollow_forests", f"#{NS}:hollow_wet"], "giant_mushroom": [c("hollow_fungal_fen")],
        "haunted_house": [f"#{NS}:hollow_forests"], "large_graveyard": [f"#{NS}:hollow_taiga"],
        "lich_prison": [f"#{NS}:hollow_sea"], "medium_graveyard": [f"#{NS}:hollow_forests"],
        "memorial_tree": [f"#{NS}:hollow_forests"], "mushroom_grave": [f"#{NS}:hollow_wet"],
        "overrun_plains_village": [g("grimplains"), g("bleakplains")], "overrun_taiga_village": [f"#{NS}:hollow_taiga"],
        "overrun_snowy_village": [g("snowy_plains")], "ruins": [f"#{NS}:hollow_forests"],
        "small_grave": [f"#{NS}:hollow_forests", f"#{NS}:hollow_plains"], "small_graveyard": [f"#{NS}:hollow_plains"],
        "small_mountain_grave": [f"#{NS}:hollow_mountains"],
        "overrun_desert_village": [], "overrun_savanna_village": [], "small_desert_grave": [],
        "small_desert_graveyard": [], "small_savanna_grave": [],
    }
    for s, vals in structures.items():
        write(out, f"graveyard/tags/worldgen/biome/has_structure/{s}.json", tag(vals))
    # Hollow Ember in the Hollow's structure chests (NeoForge global loot modifiers, like the
    # Pokemon world's Bell Fragment). Chance per chest; Lootr rolls each chest once per player.
    write(out, f"{NS}/loot_table/inject/hollow_ember.json", {"type": "minecraft:chest", "pools": [{
        "rolls": 1, "entries": [{"type": "minecraft:item", "name": c("hollow_ember"), "functions": [
            {"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": 1, "max": 2}}]}]}]})
    ember_chests = {
        # Grim & Bleak's ruined portals use this minecraft-namespaced table of its own (not vanilla's
        # ruined_portal); its abandonned_tower_loot table is used by no structure.
        "minecraft:chests/ruinedportalloot": 0.4, "grim_and_bleak:chests/cabinloot": 0.25,
        "grim_and_bleak:chests/small_tent_loot": 0.15, "graveyard:chests/great_crypt_loot": 0.75,
        "graveyard:chests/crypt_loot": 0.4, "graveyard:chests/large_graveyard_loot": 0.4,
        "graveyard:chests/medium_graveyard_loot": 0.25, "graveyard:chests/swamp_graveyard_loot": 0.25,
        "graveyard:chests/small_graveyard_loot": 0.15, "graveyard:chests/large_loot": 0.25,
        "graveyard:chests/medium_loot": 0.15, "graveyard:chests/small_loot": 0.1,
        "weeping_angels:chests/catacombs": 0.3,
    }
    entries = []
    for table, chance in ember_chests.items():
        ns, path = table.split(":")
        name = f"hollow_ember/{ns}/{path.split('/')[-1]}"
        write(out, f"{NS}/loot_modifiers/{name}.json", {"type": "neoforge:add_table", "conditions": [
            {"condition": "neoforge:loot_table_id", "loot_table_id": table},
            {"condition": "minecraft:random_chance", "chance": chance}], "table": c("inject/hollow_ember")})
        entries.append(c(name))
    glm_path = os.path.join(out, "neoforge/loot_modifiers/global_loot_modifiers.json")
    with open(glm_path, encoding="utf-8") as f:
        glm = json.load(f)
    glm["entries"] = [e for e in glm["entries"] if not e.startswith(f"{NS}:hollow_ember/")] + entries
    write(out, "neoforge/loot_modifiers/global_loot_modifiers.json", glm)

    print(f"The Hollow: {len(COPIES)} biome copies + {len(GRIM)} Grim & Bleak biomes, "
          f"{len(biome_layout())} layout entries, written to {out}")


if __name__ == "__main__":
    main()
