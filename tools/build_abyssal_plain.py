"""Generate the Abyssal Plain's datapack (kubejs/data/...) for Strata.

The Abyssal Plain (strata:abyssal_plain) is a fully underwater dimension with no surface
(docs/abyssal-plain-design.md): a rock ceiling around Y 560, water below it, and a seafloor in
three depth bands that line up with Create: Deep Seas' pressure limits:
  shelves   floor ~Y 479   (~80 m below the ceiling)    plain gear
  the plain floor ~Y 314   (~245 m)                     copper diving suit
  trenches  floor ~Y 14    (~545 m)                     submarines
The whole column sits above Y -54 on purpose: the standard noise generator hard-codes lava below
Y -54 in every dimension (NoiseBasedChunkGenerator's fluid picker), whatever the sea level.
This writes:
  * the dimension type (no skylight, permanent dark, beds set spawn) and dimension
  * noise settings built from density functions: floor height = plain base + shelf mask - trench
    mask + detail, ceiling = rough cap; no aquifers, sea level above the ceiling's underside so
    every open block below it is water
  * five biomes (shelf, plain, hydrothermal field, bioluminescent garden, trench) placed by the
    same noises the terrain uses, with dark water, underwater ambience and their creatures
  * placed features that scan DOWN to the seafloor (the ceiling breaks every heightmap-based
    placement, so mods' own placements can't be used; their configured features can)
  * biome tags; our biomes are in no vanilla or c: ocean tag, and each mod is opted in through
    its own tags (Hybrid Aquatic trenches, Naturalist, Upgrade Aquatic) or config (Alex's Mobs)

Noises come from the Pokemon world's vanilla copies (pokeworld:*), so Tectonic's overrides of
minecraft:* noises don't reach this dimension. Run from the repo root:
  python -I tools/build_abyssal_plain.py --out kubejs/data
"""
import argparse
import json
import os

NS = "strata"
DIM = f"{NS}:abyssal_plain"
CEILING_Y = 560         # underside of the rock cap (roughly)
SEA_LEVEL = 568         # above the cap's underside: every open block below it fills with water
MIN_Y, HEIGHT = -48, 640   # never below Y -54 (hard-coded lava level)
PLAIN_Y, SHELF_RISE, TRENCH_DROP = 314, 165, 300

BIOMES = ["abyssal_shelf", "abyssal_plain", "hydrothermal_field", "bioluminescent_garden", "the_trench"]
FLOOR_BAND = {  # Y range to start the downward scan from; the scan reaches 32 blocks (vanilla's cap) below it
    "abyssal_shelf": (474, 514), "abyssal_plain": (309, 349), "hydrothermal_field": (309, 349),
    "bioluminescent_garden": (309, 349), "the_trench": (9, 49),
}


def c(n):
    return f"{NS}:{n}"


def noise(nid, xz, y=0.0):
    return {"type": "minecraft:noise", "noise": nid, "xz_scale": xz, "y_scale": y}


def flat(f):
    return {"type": "minecraft:flat_cache", "argument": {"type": "minecraft:cache_2d", "argument": f}}


def add(a, b):
    return {"type": "minecraft:add", "argument1": a, "argument2": b}


def mul(a, b):
    return {"type": "minecraft:mul", "argument1": a, "argument2": b}


def clamp(f, lo, hi):
    return {"type": "minecraft:clamp", "input": f, "min": lo, "max": hi}


def absf(f):
    return {"type": "minecraft:abs", "argument": f}


# Climate noises, shared by the terrain and the biome layout so biomes follow the terrain.
CONT = flat(noise("pokeworld:continentalness", 0.5))       # shelves where high
RIDGE = flat(noise("pokeworld:ridge", 0.45))               # trench lines where |ridge| ~ 0
VENT = flat(noise("pokeworld:erosion", 1.2))               # hydrothermal fields where high
GARDEN = flat(noise("pokeworld:vegetation", 1.2))          # bioluminescent gardens where high
DETAIL = flat(noise("pokeworld:surface", 3.0))             # small floor relief


def floor_height_over_64():
    shelf = clamp(mul(add(CONT, -0.35), 4.0), 0.0, 1.0)
    trench = clamp(mul(add(absf(RIDGE), -0.08), -12.5), 0.0, 1.0)
    h = add(PLAIN_Y / 64, mul(shelf, SHELF_RISE / 64))
    h = add(h, mul(trench, -TRENCH_DROP / 64))
    return add(h, mul(DETAIL, 0.2))


def final_density():
    # d_floor > 0 below the floor height: Hf/64 - y/64.
    d_floor = add({"type": "minecraft:y_clamped_gradient", "from_y": MIN_Y, "to_y": MIN_Y + HEIGHT,
                   "from_value": -MIN_Y / 64, "to_value": -(MIN_Y + HEIGHT) / 64}, floor_height_over_64())
    rough = mul(noise("pokeworld:cave_cheese", 1.0, 1.0), 0.12)   # overhangs and ledges near the floor
    d_floor = add(d_floor, rough)
    # d_ceil > 0 above the cap's underside: (y - Hc)/16, Hc = CEILING_Y +- ~6.
    d_ceil = add({"type": "minecraft:y_clamped_gradient", "from_y": MIN_Y, "to_y": MIN_Y + HEIGHT,
                  "from_value": MIN_Y / 16, "to_value": (MIN_Y + HEIGHT) / 16}, -CEILING_Y / 16)
    d_ceil = add(d_ceil, mul(flat(noise("pokeworld:surface", 2.0)), 0.4))
    return {"type": "minecraft:interpolated", "argument": {"type": "minecraft:max", "argument1": d_floor, "argument2": d_ceil}}


def noise_settings():
    zero = 0.0
    dens = final_density()
    return {
        "sea_level": SEA_LEVEL, "disable_mob_generation": False, "aquifers_enabled": False,
        "ore_veins_enabled": False, "legacy_random_source": False,
        "default_block": {"Name": "minecraft:deepslate", "Properties": {"axis": "y"}},
        "default_fluid": {"Name": "minecraft:water", "Properties": {"level": "0"}},
        "noise": {"min_y": MIN_Y, "height": HEIGHT, "size_horizontal": 1, "size_vertical": 2},
        "noise_router": {
            "barrier": zero, "fluid_level_floodedness": zero, "fluid_level_spread": zero, "lava": zero,
            "temperature": zero, "vegetation": GARDEN, "continents": CONT, "erosion": absf(RIDGE),
            "depth": zero, "ridges": VENT,
            # 0 like the Nether: the preliminary-surface estimate would otherwise be the ceiling, and
            # surface rules only run down to it, leaving the seafloor bare deepslate.
            "initial_density_without_jaggedness": zero, "final_density": dens,
            "vein_toggle": zero, "vein_ridged": zero, "vein_gap": zero,
        },
        "spawn_target": [],
        "surface_rule": surface_rule(),
    }


def block(name, props=None):
    d = {"Name": name}
    if props: d["Properties"] = props
    return {"type": "minecraft:block", "result_state": d}


def cond(test, run):
    return {"type": "minecraft:condition", "if_true": test, "then_run": run}


def floor(depth=False, secondary=0):
    return {"type": "minecraft:stone_depth", "surface_type": "floor", "add_surface_depth": depth,
            "secondary_depth_range": secondary, "offset": 0}


def biome_is(*names):
    return {"type": "minecraft:biome", "biome_is": [c(n) for n in names]}


def surface_rule():
    bedrock_floor = cond({"type": "minecraft:vertical_gradient", "random_name": "minecraft:bedrock_floor",
                          "true_at_and_below": {"above_bottom": 0}, "false_at_and_above": {"above_bottom": 5}},
                         block("minecraft:bedrock"))
    bedrock_roof = cond({"type": "minecraft:not", "invert": {
        "type": "minecraft:vertical_gradient", "random_name": "minecraft:bedrock_roof",
        "true_at_and_below": {"below_top": 5}, "false_at_and_above": {"below_top": 0}}}, block("minecraft:bedrock"))
    ceiling = cond({"type": "minecraft:stone_depth", "surface_type": "ceiling", "add_surface_depth": False,
                    "secondary_depth_range": 0, "offset": 0}, block("minecraft:tuff"))
    # No floor rules: surface rules count depth from the topmost air, and water doesn't reset that
    # count, so in a world with no air the "surface" is the top of the cap. Seafloor sediment is
    # laid down as disk features instead (SEDIMENT below).
    return {"type": "minecraft:sequence", "sequence": [bedrock_floor, bedrock_roof, ceiling]}


def biome_layout():
    full = [-1.0, 1.0]
    out = []

    def addb(b, cont=full, ero=(0.05, 1.0), weird=full, hum=full):
        out.append({"biome": c(b), "parameters": {"temperature": full, "humidity": list(hum), "continentalness": list(cont),
                                                  "erosion": list(ero), "weirdness": list(weird), "depth": 0.0, "offset": 0.0}})
    addb("the_trench", ero=(0.0, 0.05))
    addb("abyssal_shelf", cont=(0.4, 1.0))
    addb("hydrothermal_field", cont=(-1.0, 0.4), weird=(0.5, 1.0))
    addb("bioluminescent_garden", cont=(-1.0, 0.4), weird=(-1.0, 0.5), hum=(0.45, 1.0))
    addb("abyssal_plain", cont=(-1.0, 0.4), weird=(-1.0, 0.5), hum=(-1.0, 0.45))
    return out


def scan_down(feature, biome, count, extra_y=1):
    lo, hi = FLOOR_BAND[biome]
    if biome in WIDE:
        (lo, hi), mult = WIDE[biome]
        count *= mult
    return {"feature": feature, "placement": [
        {"type": "minecraft:count", "count": count},
        {"type": "minecraft:in_square"},
        {"type": "minecraft:height_range", "height": {"type": "minecraft:uniform",
                                                      "min_inclusive": {"absolute": lo}, "max_inclusive": {"absolute": hi}}},
        {"type": "minecraft:environment_scan", "direction_of_search": "down", "max_steps": 32,
         "target_condition": {"type": "minecraft:solid"},
         "allowed_search_condition": {"type": "minecraft:matching_fluids", "fluids": ["minecraft:water"]}},
        {"type": "minecraft:random_offset", "xz_spread": 0, "y_spread": extra_y},
        {"type": "minecraft:biome"}]}


def ceiling_scan(feature, count):
    return {"feature": feature, "placement": [
        {"type": "minecraft:count", "count": count}, {"type": "minecraft:in_square"},
        {"type": "minecraft:height_range", "height": {"type": "minecraft:uniform",
                                                      "min_inclusive": {"absolute": CEILING_Y - 30}, "max_inclusive": {"absolute": CEILING_Y - 4}}},
        {"type": "minecraft:environment_scan", "direction_of_search": "up", "max_steps": 32,
         "target_condition": {"type": "minecraft:solid"},
         "allowed_search_condition": {"type": "minecraft:matching_fluids", "fluids": ["minecraft:water"]}},
        {"type": "minecraft:random_offset", "xz_spread": 0, "y_spread": -1},
        {"type": "minecraft:biome"}]}


# Per biome: (placed feature name, configured feature, count). Vanilla's kelp, seagrass, sea pickle
# and coral features find their own height from the OCEAN_FLOOR heightmap (the top of our cap), so
# they're rebuilt as our own simple features (CUSTOM). Hybrid Aquatic's patches and Alex's Caves'
# mussels and black vents place fine; its boulders, tube worms and anemones don't (they expect its
# chasm biome), so they're left out.
FEATURES = {
    "abyssal_shelf": [("kelp", c("abyssal/kelp"), 24), ("seagrass", c("abyssal/seagrass"), 40),
                      ("sea_pickle", c("abyssal/sea_pickle"), 6), ("coral", c("abyssal/coral"), 10),
                      ("anemones", "hybrid_aquatic:anemones", 3)],
    "abyssal_plain": [("glass_sponges", "hybrid_aquatic:glass_sponge_patch", 3), ("harp_sponges", "hybrid_aquatic:harp_sponge_patch", 2),
                      ("mussels", "alexscaves:mussel", 3), ("sea_pickle", c("abyssal/sea_pickle"), 2)],
    "hydrothermal_field": [("black_vents", "alexscaves:black_vent", 6), ("thermal_vents", "hybrid_aquatic:thermal_vent_patch", 4),
                           ("brine_pools", "hybrid_aquatic:brine_pool", 1), ("magma", "minecraft:underwater_magma", 4)],
    "bioluminescent_garden": [("glow_kelp", c("abyssal/kelp"), 10), ("sea_pickle", c("abyssal/sea_pickle"), 16),
                              ("anemones", "hybrid_aquatic:anemones", 6), ("ping_pong_sponges", "hybrid_aquatic:ping_pong_sponge_patch", 3),
                              ("seagrass", c("abyssal/seagrass"), 12)],
    "the_trench": [("black_vents", "alexscaves:black_vent", 6), ("glass_sponges", "hybrid_aquatic:glass_sponge_patch", 3),
                   ("mussels", "alexscaves:mussel", 4)],
}
CORALS = ["tube", "brain", "bubble", "fire", "horn"]
CUSTOM = {
    "kelp": {"type": "minecraft:block_column", "config": {"direction": "up", "allowed_placement": {
        "type": "minecraft:matching_blocks", "blocks": ["minecraft:water"]}, "prioritize_tip": True, "layers": [
        {"height": {"type": "minecraft:uniform", "min_inclusive": 2, "max_inclusive": 14},
         "provider": {"type": "minecraft:simple_state_provider", "state": {"Name": "minecraft:kelp_plant"}}},
        {"height": 1, "provider": {"type": "minecraft:simple_state_provider", "state": {"Name": "minecraft:kelp", "Properties": {"age": "20"}}}}]}},
    "seagrass": {"type": "minecraft:simple_block", "config": {"to_place": {"type": "minecraft:simple_state_provider",
                                                                          "state": {"Name": "minecraft:seagrass"}}}},
    "sea_pickle": {"type": "minecraft:simple_block", "config": {"to_place": {"type": "minecraft:weighted_state_provider", "entries": [
        {"weight": 1, "data": {"Name": "minecraft:sea_pickle", "Properties": {"pickles": str(n), "waterlogged": "true"}}} for n in (1, 2, 3, 4)]}}},
    "coral": {"type": "minecraft:simple_block", "config": {"to_place": {"type": "minecraft:weighted_state_provider", "entries": (
        [{"weight": 2, "data": {"Name": f"minecraft:{k}_coral", "Properties": {"waterlogged": "true"}}} for k in CORALS] +
        [{"weight": 2, "data": {"Name": f"minecraft:{k}_coral_fan", "Properties": {"waterlogged": "true"}}} for k in CORALS] +
        [{"weight": 1, "data": {"Name": f"minecraft:{k}_coral_block"}} for k in CORALS])}}},
}
CEILING_FEATURES = {"bioluminescent_garden": [("glow_lichen", "minecraft:glow_lichen", 30)],
                    "abyssal_shelf": [("glow_lichen", "minecraft:glow_lichen", 10)],
                    "abyssal_plain": [("glow_lichen", "minecraft:glow_lichen", 6)]}
RARE = {  # big one-offs: (placed name, configured, rarity 1-in-N chunks)
    "abyssal_plain": [("whalefall", "alexscaves:whalefall", 18), ("deep_one_ruins", "alexscaves:deep_one_ruins", 30)],
    "the_trench": [("whalefall", "alexscaves:whalefall", 14), ("deep_one_ruins", "alexscaves:deep_one_ruins", 10)],
    "bioluminescent_garden": [("whalefall", "alexscaves:whalefall", 24)],
}
# The trench (walls and floor) and shelf (slopes) span tall height ranges: scan from anywhere in
# them, with more attempts, since only starts within 32 blocks above the floor find it.
WIDE = {"the_trench": ((9, 300), 4), "abyssal_shelf": ((330, 500), 3)}


def rare_scan(feature, biome, chance):
    p = scan_down(feature, biome, 1, extra_y=0)
    p["placement"].insert(0, {"type": "minecraft:rarity_filter", "chance": chance})
    return p


# Seafloor sediment: overlapping disks over the deepslate floor, per biome (block, count/chunk, radius).
SEDIMENT = {
    "abyssal_shelf": [("minecraft:sand", 18, 5), ("minecraft:gravel", 6, 3)],
    "abyssal_plain": [("minecraft:clay", 16, 6), ("minecraft:mud", 8, 4)],
    "bioluminescent_garden": [("minecraft:mud", 16, 6), ("minecraft:moss_block", 4, 3)],
    "hydrothermal_field": [("minecraft:blackstone", 16, 6), ("minecraft:magma_block", 6, 2)],
    "the_trench": [("alexscaves:abyssmarine", 18, 6), ("minecraft:tuff", 6, 4)],
}


def disk(block_id, radius):
    return {"type": "minecraft:disk", "config": {
        "state_provider": {"fallback": {"type": "minecraft:simple_state_provider", "state": {"Name": block_id}}, "rules": []},
        "target": {"type": "minecraft:matching_blocks", "blocks": ["minecraft:deepslate", "minecraft:tuff", "minecraft:clay",
                                                                   "minecraft:mud", "minecraft:sand", "minecraft:blackstone"]},
        "radius": {"type": "minecraft:uniform", "min_inclusive": max(1, radius - 2), "max_inclusive": radius},
        "half_height": 1}}


# Effects and creatures per biome.
EFFECTS = {
    "abyssal_shelf": (0x1A3F6B, 0x0B2A50, "minecraft:music.under_water", None),
    "abyssal_plain": (0x0B1A3A, 0x041028, "minecraft:music.under_water", None),
    "hydrothermal_field": (0x2A1A14, 0x1A0C08, "minecraft:music.under_water", None),
    "bioluminescent_garden": (0x0A2A3A, 0x062030, "minecraft:music.under_water", ("minecraft:glow", 0.002)),
    "the_trench": (0x02060F, 0x01030A, "alexscaves:abyssal_chasm_music", None),
}


def spawn(t, w, lo, hi):
    return {"type": t, "weight": w, "minCount": lo, "maxCount": hi}


SPAWNS = {
    "abyssal_shelf": {"water_ambient": [spawn("minecraft:cod", 10, 3, 6), spawn("minecraft:tropical_fish", 15, 4, 8)],
                      "water_creature": [spawn("minecraft:squid", 4, 1, 3)],
                      "underground_water_creature": [spawn("minecraft:glow_squid", 6, 2, 4)]},
    "abyssal_plain": {"water_ambient": [spawn("alexscaves:lanternfish", 60, 10, 16)],
                      "alexscaves:deep_sea_creature": [spawn("alexscaves:tripodfish", 40, 1, 2), spawn("alexscaves:sea_pig", 50, 3, 4)],
                      "underground_water_creature": [spawn("minecraft:glow_squid", 4, 1, 3)]},
    "hydrothermal_field": {"water_ambient": [spawn("alexscaves:lanternfish", 30, 6, 10)],
                           "alexscaves:deep_sea_creature": [spawn("alexscaves:sea_pig", 40, 2, 4), spawn("alexscaves:gossamer_worm", 20, 1, 1)]},
    "bioluminescent_garden": {"water_ambient": [spawn("alexscaves:lanternfish", 80, 12, 20)],
                              "underground_water_creature": [spawn("minecraft:glow_squid", 12, 2, 4)],
                              "alexscaves:deep_sea_creature": [spawn("alexscaves:gossamer_worm", 30, 1, 2)]},
    "the_trench": {"monster": [spawn("alexscaves:deep_one", 8, 1, 1), spawn("alexscaves:deep_one_knight", 4, 1, 1),
                               spawn("alexscaves:deep_one_mage", 2, 1, 1)],
                   "underground_water_creature": [spawn("alexscaves:hullbreaker", 4, 1, 1)],
                   "water_ambient": [spawn("alexscaves:lanternfish", 40, 8, 12)],
                   "alexscaves:deep_sea_creature": [spawn("alexscaves:tripodfish", 40, 1, 2), spawn("alexscaves:gossamer_worm", 20, 1, 1)]},
}


def biome_json(b):
    water, fog, music, particle = EFFECTS[b]
    eff = {"fog_color": 0x050A14, "sky_color": 0, "water_color": water, "water_fog_color": fog,
           "ambient_sound": "alexscaves:abyssal_chasm_ambience" if b == "the_trench" else "minecraft:ambient.underwater.loop",
           "additions_sound": {"sound": "minecraft:ambient.underwater.loop.additions.rare", "tick_chance": 0.012},
           "mood_sound": {"sound": "minecraft:ambient.cave", "tick_delay": 3000, "block_search_extent": 8, "offset": 2.0},
           "music": {"sound": music, "min_delay": 6000, "max_delay": 18000, "replace_current_music": False}}
    if particle:
        eff["particle"] = {"options": {"type": particle[0]}, "probability": particle[1]}
    steps = [[] for _ in range(11)]
    for name, _, _ in FEATURES[b]: steps[9].append(c(f"abyssal/{b}/{name}"))
    for name, _, _ in CEILING_FEATURES.get(b, []): steps[9].append(c(f"abyssal/{b}/ceiling_{name}"))
    for name, _, _ in RARE.get(b, []): steps[4].append(c(f"abyssal/{b}/{name}"))
    for blk, _, _ in SEDIMENT[b]: steps[2].append(c(f"abyssal/{b}/sediment_{blk.split(':')[1]}"))
    spawners = {k: [] for k in ("monster", "creature", "ambient", "axolotls", "underground_water_creature",
                                "water_creature", "water_ambient", "misc")}
    spawners.update(SPAWNS[b])
    return {"has_precipitation": False, "temperature": 0.5, "downfall": 0.5, "effects": eff,
            "spawners": spawners, "spawn_costs": {}, "carvers": {}, "features": steps}


def write(out, rel, data):
    path = os.path.join(out, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def tag(values, replace=True):
    return {"replace": replace, "values": values}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="kubejs/data")
    out = ap.parse_args().out

    write(out, f"{NS}/dimension_type/abyssal_plain.json", {
        "ultrawarm": False, "natural": False, "piglin_safe": False, "respawn_anchor_works": False, "bed_works": True,
        "has_raids": False, "has_skylight": False, "has_ceiling": True, "coordinate_scale": 1.0, "ambient_light": 0.0,
        "fixed_time": 18000, "infiniburn": "#minecraft:infiniburn_overworld", "min_y": MIN_Y, "height": HEIGHT,
        "logical_height": HEIGHT, "monster_spawn_light_level": {"type": "minecraft:uniform", "min_inclusive": 0, "max_inclusive": 7},
        "monster_spawn_block_light_limit": 0, "effects": "minecraft:overworld"})
    write(out, f"{NS}/worldgen/noise_settings/abyssal_plain.json", noise_settings())
    write(out, f"{NS}/dimension/abyssal_plain.json", {"type": DIM, "generator": {
        "type": "minecraft:noise", "settings": DIM, "biome_source": {"type": "minecraft:multi_noise", "biomes": biome_layout()}}})

    for name, conf in CUSTOM.items():
        write(out, f"{NS}/worldgen/configured_feature/abyssal/{name}.json", conf)
    for b in BIOMES:
        write(out, f"{NS}/worldgen/biome/{b}.json", biome_json(b))
        for name, feat, count in FEATURES[b]:
            write(out, f"{NS}/worldgen/placed_feature/abyssal/{b}/{name}.json", scan_down(feat, b, count))
        for name, feat, count in CEILING_FEATURES.get(b, []):
            write(out, f"{NS}/worldgen/placed_feature/abyssal/{b}/ceiling_{name}.json", ceiling_scan(feat, count))
        for name, feat, chance in RARE.get(b, []):
            write(out, f"{NS}/worldgen/placed_feature/abyssal/{b}/{name}.json", rare_scan(feat, b, chance))
        for blk, count, radius in SEDIMENT[b]:
            name = blk.split(":")[1]
            write(out, f"{NS}/worldgen/configured_feature/abyssal/{b}/sediment_{name}.json", disk(blk, radius))
            # Disks are placed at the floor block itself (no +1 offset).
            write(out, f"{NS}/worldgen/placed_feature/abyssal/{b}/sediment_{name}.json",
                  scan_down(c(f"abyssal/{b}/sediment_{name}"), b, count, extra_y=0))

    deep = [c(b) for b in BIOMES if b != "abyssal_shelf"]
    write(out, f"{NS}/tags/worldgen/biome/abyssal_plain_biomes.json", tag([c(b) for b in BIOMES]))
    write(out, f"{NS}/tags/worldgen/biome/abyssal_deep.json", tag(deep))
    # Hybrid Aquatic: its deep species follow these tags (spawn config); its own trench biomes are
    # switched off (config/hybrid_aquatic.json enableBiomes = false), so they live only here.
    for t, vals in {"all_trenches": deep, "temperate_trench": [c("abyssal_plain"), c("hydrothermal_field")],
                    "cold_trench": [c("the_trench")], "frozen_trench": [c("the_trench")],
                    "warm_trench": [c("hydrothermal_field")], "lukewarm_trench": [c("bioluminescent_garden")],
                    "has_thermal_vents": [c("hydrothermal_field")]}.items():
        write(out, f"hapi/tags/worldgen/biome/{t}.json", tag(vals))
    # ...but its trench decorations use heightmap placement, which would land on top of our
    # ceiling: those modifiers target nothing, and we place the same features ourselves.
    for m, feat, step in (("thermal_vent_trenches_all_trenches", "hybrid_aquatic:thermal_vent_trenches", "local_modifications"),
                          ("trench_brine_pools_all_trenches", "hybrid_aquatic:trench_brine_pools", "local_modifications"),
                          ("glass_sponge_patch_all_trenches", "hybrid_aquatic:glass_sponge_patch", "vegetal_decoration"),
                          ("harp_sponge_patch_all_trenches", "hybrid_aquatic:harp_sponge_patch", "vegetal_decoration"),
                          ("ping_pong_sponge_patch_all_trenches", "hybrid_aquatic:ping_pong_sponge_patch", "vegetal_decoration")):
        write(out, f"hybrid_aquatic/neoforge/biome_modifier/{m}.json",
              {"type": "neoforge:add_features", "biomes": f"#{NS}:none", "features": feat, "step": step})
    write(out, f"{NS}/tags/worldgen/biome/none.json", tag([]))
    # Ordinary deep-sea animals also live here (they stay in Overworld oceans too).
    write(out, "naturalist/tags/worldgen/biome/has_anglerfish.json", tag(deep, replace=False))
    write(out, "naturalist/tags/worldgen/biome/has_giant_isopod.json", tag(deep, replace=False))
    write(out, "upgrade_aquatic/tags/worldgen/biome/has_spawn/thrasher.json", tag([c("abyssal_shelf"), c("abyssal_plain")], replace=False))
    # Abyssal Pearls in the Deep One ruins' chests (Alex's Caves), like the Hollow's Ember.
    write(out, f"{NS}/loot_table/inject/abyssal_pearl.json", {"type": "minecraft:chest", "pools": [{
        "rolls": 1, "entries": [{"type": "minecraft:item", "name": c("abyssal_pearl"), "functions": [
            {"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": 1, "max": 2}}]}]}]})
    pearl_chests = {"alexscaves:chests/abyssal_ruins": 0.35}
    entries = []
    for table, chance in pearl_chests.items():
        ns, path = table.split(":")
        name = f"abyssal_pearl/{ns}/{path.split('/')[-1]}"
        write(out, f"{NS}/loot_modifiers/{name}.json", {"type": "neoforge:add_table", "conditions": [
            {"condition": "neoforge:loot_table_id", "loot_table_id": table},
            {"condition": "minecraft:random_chance", "chance": chance}], "table": c("inject/abyssal_pearl")})
        entries.append(c(name))
    glm_path = os.path.join(out, "neoforge/loot_modifiers/global_loot_modifiers.json")
    with open(glm_path, encoding="utf-8") as f:
        glm = json.load(f)
    glm["entries"] = [e for e in glm["entries"] if not e.startswith(f"{NS}:abyssal_pearl/")] + entries
    write(out, "neoforge/loot_modifiers/global_loot_modifiers.json", glm)

    print(f"Abyssal Plain: {len(BIOMES)} biomes, {sum(len(v) for v in FEATURES.values())} floor features, written to {out}")


if __name__ == "__main__":
    main()
