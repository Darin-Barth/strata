# The Abyssal Plain: mod research

Research for `strata:abyssal_plain` (our own datapack dimension, entered by portal): water from a rock ceiling down to a deep seafloor with plains, trenches, hydrothermal vents and ruins. The feel is Subnautica-like. Create: Deep Seas is the core mod. Deep-sea mobs should spawn only here. Ordinary ocean life may spawn anywhere.

Method (Oct 26, 2026):
- Builds come from the Modrinth API (`/v2/project/<slug>/version?loaders=["neoforge"]&game_versions=["1.21.1"]`). Every candidate worth a row was on Modrinth. cfwidget was used once, to confirm that the original Alex's Caves has no 1.21.1 build.
- Spawn and placement facts come from the jars. New jars were downloaded to `C:\Users\darin\AppData\Local\Temp\claude\C--ClaudeProjects-strata\6cda4669-d9d2-4cc1-9cd6-2942705e8977\scratchpad\abyss-research\dl\`. Jars already in the pack were read from `ModrinthApp\profiles\Strata-0.2.1\mods\`. I read biome modifiers, biome tags, structure JSON, lang files and class-file strings. No jar was run.
- "Side" in the tables is Modrinth's client/server flag, where c = client and s = server. "In" means the mod is already in `mods/`.

## Key findings that shape the design

1. **Deep Seas already ships its own abyss dimension, and it is switched off.** The 3.4.5 jar contains `create_abyss:abyss`: a fixed-biome noise dimension (min_y -1200, height 1200, no skylight, ambient light 0) with an `abyss_ceiling` block and an experimental "tectonic" variant (`abyss_plains`, `abyss_shallows`, `abyss_continental_shelf`). All of it sits behind the `enableAbyssDimension` condition, and the code contains the string "Create Abyss is in development, content disabled in production". So in a release jar, the isopod, pelican eel, cookiecutter shark, cuttlefish, amphistium, magmatic snail, vents, lianas, creepvine and PDA are probably not usable yet. Test that with `/summon create_abyss:isopod` and `/give @s create_abyss:geothermal_vent` before we plan around any of them. For now, plan the Abyssal Plain to work without them and add them when they ship.
2. **Deep Seas measures pressure from the top of the water column, not from Y.** Its classes use `surfaceY` and `measureSurfaceY`. Under a rock ceiling, depth should therefore count from the underside of the ceiling. That is a likely reading of the class strings, not something I checked in-game, so test it. The full copper suit holds to 280 m; without it, pressure hurts past 120 m. Hull implosion depth is set in config. Design the depth bands around these numbers: shallows 0-120 m below the ceiling, the plain around 120-280 m, and trenches deeper than 280 m, where only submarines can go.
3. **Deep Seas has a "Deeper Oceans" switch that reshapes the Overworld.** It is a lithostitched `wrap_density_function` on `minecraft:overworld/offset`, behind `enableDeeperOceans`. Set it to `false` explicitly in our config; it would fight Tectonic and leave seams in existing chunks.
4. **A rock ceiling breaks heightmap placement.** `OCEAN_FLOOR_WG` and `WORLD_SURFACE` find the ceiling, not the seafloor. Any placed feature that uses `minecraft:heightmap` (all vanilla ocean flora, most mod flora) and any structure with `project_start_to_heightmap` (Moog's, many jigsaws) will try to build on top of the ceiling. This is probably why Deep Seas' own abyss biome has `"features": []`. Workarounds:
   - Features: write our own `placed_feature` JSONs that reuse the mods' `configured_feature` ids, with nether-style placement (`count`, `in_square`, `height_range`, then `environment_scan` downward to a solid block, then `block_predicate_filter`).
   - Structures: copy the structure JSON into `strata:` with an absolute `start_height` and no heightmap projection, or accept that some structures won't work. Cataclysm's `sunken_city` uses its own structure type with `start_height` 0, so it needs an in-game test.
5. **Set `sea_level` in our noise settings to the ceiling's underside, and use a `fixed_time` dimension type.** Many aquatic mobs check spawn height against `level.getSeaLevel()`: in Hybrid Aquatic (colossal squid, giant squid, firefly squid, dragonfish, oarfish, umbrella octopus, hagfish and more), Naturalist (anglerfish, giant isopod), Alex's Mobs (hammerhead, mantis shrimp, mimic octopus, orca, cachalot) and Upgrade Aquatic (jellyfish). Several Hybrid Aquatic mobs also check `isDay`. A fixed-time dimension always reports not-day, which makes it permanent night: the bioluminescent mobs come out and act as they do at night.
6. **Abyssal biomes must not carry `#minecraft:is_ocean`, `#minecraft:is_deep_ocean`, `#c:is_ocean` or `#minecraft:is_overworld`.** If they did, every ocean mod would bring its surface content in: Seven Seas ships, rafts, drowned, shipwrecks at "sea level", and Naturalist and Hybrid Aquatic spawns everywhere. Opt each mod in through its own tags instead (`#hapi:*`, `#naturalist:has_*`, `#upgrade_aquatic:has_spawn/*`, `#joshie:has_structure/*`, `#cataclysm:has_structure/*`, and so on). For Naturalist, Unusual Fish and Myths of the Sea, overriding their tags or modifiers with `"replace": true` is also how we keep the deep species out of the Overworld.
7. **Many items already give free breathing, which undercuts Deep Seas' oxygen loop:** Aquamirae Oxygen Tank and Salvager suit, Aquaculture Neptunium, Create's backtank, Ars and Iron's water-breathing spells, conduits and potions. Pressure still applies, because only the full copper suit or a hull protects against it, so depth stays gated. Decide whether the Abyssal Plain needs extra rules (for example a KubeJS check that removes water breathing in `strata:abyssal_plain`). Avoid adding more breathing gear.

## 1. Deep-sea creatures and ocean fauna (new mods)

| Mod | Build | Side | Deps | What it adds for the abyss | How it spawns, can it be confined | Risks |
|---|---|---|---|---|---|---|
| **Hybrid Aquatic** `hybrid-aquatic` | mc1.21.1-1.7.4-neoforge, release, 2026-10-04, ARR | c+s | lithostitched (in), geckolib (in), kotlin-for-forge (in), **hybrid-api** (new, MIT, 1.1.3 release 2026-10-04), curios (opt) | About 140 entities. Deep species: anglerfish, barreleye, dragonfish, fangtooth, viperfish, hatchetfish, lantern shark, goblin shark, frilled/sixgill/sleeper shark, colossal and giant squid, vampire squid, firefly squid, umbrella octopus, oarfish, giant isopod, tripod fish, snailfish, scalyfoot snail, yeti crab, hagfish, ratfish, coelacanth, and the Karkinos miniboss. | Spawns use NeoForge `add_spawns` biome modifiers on **tags**: `#hapi:all_trenches`, `#hapi:has_thermal_vents`, and per-temperature trench tags. Adding our biomes to those tags confines deep species to trenches plus our dimension. Its Overworld trench and reef biomes come in through lithostitched `biome_injector`s gated by `hybrid_aquatic:biome_enabled`, which a config switch (`enableBiomes`) controls. | Diving Suit, Reinforced Diving Suit and Glowing Diving Suit probably add breathing on top of Deep Seas; gate or remove them with KubeJS. Ordinary fish are added to vanilla oceans (acceptable). Heavy entity count. ARR (Modrinth CDN download is fine). |
| Alex's Caves Continued `alexs-caves-continued` | 1.1.3+neoforge-1.21.1, release, 2026-10-19, LGPL-3.0 | c+s | codxlib (in) | Its Abyssal Chasm biome fits the abyss very well: the Hullbreaker (a leviathan), lanternfish swarms, tripodfish, sea pigs, gossamer worms, Deep Ones (3 kinds), mine guardians, abyssmarine blocks, black vents, tube worms, mussels, anemones, whalefall and deep-one ruins. It also has its own submarine and diving suit. | The biome JSON spawners (including the custom category `alexscaves:deep_sea_creature`) can be copied into our biomes, and features referenced by id (`alexscaves:black_vent`, `whalefall`, `deep_one_ruins`, `tube_worm`, `abyssal_boulder`). Overworld placement is set per biome in `config/alexscaves_biome_generation/<biome>.json`, which has `disabledCompletely` and `dimensions` fields. | 75 MB, with 5 other cave biomes and a whole progression (nuclear, magnetic, candy). Its submarine and diving suit duplicate Deep Seas. Taking it only for the Chasm is a big addition, so this is Darin's call. Don't also install `alexs-caves-unofficial-port`. |
| Unusual Fish `unusual-fish` | 1.21.1-1.1.13, release, 2026-06-26, custom licence | c+s | geckolib (in) | Fictional fish: volt anglerfish, gnasher, ripper, blind sailfin, demon herring, crowned sea spider, celestial fish, mana jellyfish, trumpet and crimsonshell squid, deep crawler. | Plain `add_spawns` modifiers with explicit biome lists (for example `volt_angler` → `deep_cold_ocean`). To confine, override those JSONs. `deep_crawler` targets `#minecraft:is_overworld`. | Cartoony style next to Hybrid Aquatic's realism. Read the custom licence before adding. |
| Myths of the Sea `myths-of-the-sea` | 1.3.0, release, 2026-07-13, ARR | c+s | none | Kraken (200 hp, grabs), Leviathan (one-shots unarmoured players), Hippocampus (rideable), Abaia, Bake Kujira, Bunyip. | `add_spawns` with explicit vanilla biome lists. Override them to point at our biomes. | One build, no source. The Leviathan one-shot is harsh. We already have plenty of big creatures (see below). |
| Sea Life `new-sea-life` | 21.1.0, release, 2026-05-21, MIT | c+s | puzzles-lib (in) | 32 fish, including anglerfish, manta and electric ray, lamprey and stargazer. | A code biome modifier (`sealife:biome_modifications`, no JSON), so it can't be pointed at our biomes without In Control!. | Mostly ordinary fish, and it overlaps Aquaculture and Hybrid Aquatic. |
| Whaleborne `whaleborne` | 1.21.1-1.2.5, release, 2026-09-18, MIT | c+s | none | Hullback whale that you build a ship on (sails, helm, cannons). | `whaleborne:configurable_spawns` on `#minecraft:is_deep_ocean`. | A surface ship, which is pointless under a ceiling. |
| Ben's Sharks `bens-sharks` | 1.2.5, release, 2025-04-02, LGPL | c+s | geckolib | Sharks. | Biome modifiers. | Duplicates Naturalist, Alex's Mobs and Hybrid Aquatic sharks. |

## 2. Underwater flora, blocks and biomes

| Mod | Build | Side | Deps | What it adds | Placement, confinement | Risks |
|---|---|---|---|---|---|---|
| **Hybrid Aquatic** (see above) | | | | Thermal vent and giant thermal vent, tube worm, glass, harp, tube and ping-pong sponges, brine pools and brinestone (3 colours), sulfur deposits, glowing plankton, glowslime, deep-sea vegetation, 12 new corals plus bleached variants, anemones, giant clams, and a whale-fall structure. | Features are tag-driven (`thermal_vent_trenches_all_trenches` → `#hapi:all_trenches`, `glass_sponge_patch_all_trenches`, and so on). Its placed features use heightmaps, so for our biomes reuse the configured features with our own scan-down placement (finding 4). | As above. |
| Alex's Caves Continued (see above) | | | | Abyssmarine, black vents, tube worms, mussels, ping-pong sponge, dusk, twilight and midnight anemones, whalefall. | Features referenced by id. | As above. |
| Luminous Blocks `luminous-blocks` | v1.3.0, release, 2025-08-15, Modvane Public Mod License | c+s | none | Glowing glass and panes in 3 light levels, for hull windows and base lighting. | Crafted only. | Small. Read the licence. |
| Glow Sticks `glow-sticks` | 7.5.1, release, 2026-09-19, MIT | c+s | none | Throwable, timed coloured lights that work underwater, so you can mark paths and drop lights down trenches. | Crafted only. | None noted. |
| Deeper Oceans `deeper-oceans` | 2.0.1, release, 2026-06-28, MIT | c+s | lithostitched | Deepens Overworld oceans. | Global. | Reject: changes the Overworld, and Deep Seas has the same option. |
| NeoReefRedux `neoreefredux` | 1.0, release, 2026-03-03, GPL | s | none | Rocky coral reefs in the Overworld. | Global. | Reject: nothing for the abyss. |
| Abyssal Decor `abyssal-decor` | 0.11.0, beta, 2026-08-17, CC0 | c+s | none | Victorian and Lovecraftian decorative blocks. | Crafted. | Reject: WIP, placeholder recipes, and its page still says "Forge only". |

## 3. Underwater gameplay (gear, scanning, vehicles, bases)

| Mod | Build | Side | Deps | What it adds | Notes, confinement | Risks or conflict with Deep Seas |
|---|---|---|---|---|---|---|
| **Create: Deep Seas** `create-deep-seas` (core) | Latest release 3.3.0 (2026-10-02). Latest overall 3.4.5 **beta** (2026-10-22). ARR | c+s | create, sable, create-aeronautics (all in). iris-flw-compat is **required in 3.3.0** and optional in 3.4.5. Embeds fusion-connected-textures (in) | Physics submarines, pressure (Classic, Hybrid or Realistic model), copper diving suit, pressure goggles, decompression chamber and airlocks, electrolyzer, oxygen diffuser, pressurized glass, ballast, thrusters, mines, industrial alarm, High Seas sailboats. | Since 3.4.1 it officially supports Photon, BSL, Bliss and Complementary shaders, and it uses its own lighting engine that works with Sodium and Iris. | Set `enableDeeperOceans = false`. The abyss content is gated off (finding 1). Pick 3.3.0 release or 3.4.5 beta. 3.3.0 also pulls in Iris & Oculus Flywheel Compat (`iris-flw-compat`, client, CC0, recommended anyway). |
| Create: Deep Seas – Lava Fix `create-deep-seas-lava-fix` | 1.0.1, release, 2026-06-15, MIT | c+s | none | Stops fire and lava damage to players inside a sealed submarine. | Relevant if the vents have magma. | Check whether Deep Seas 3.4.x already fixed this before adding it. |
| **Scannable** `scannable` | MC1.21.1-neoforge-1.8.1, release, 2026-10-12, MIT | c+s | architectury (in) | A scanner with modules (entity, specific entity, block, fluid, ores, range). FE-powered, with in-world highlight overlays. The closest match to Subnautica's scanner. | Scanning runs client-side, so it doesn't load the server. | Ore modules make prospecting easier. Restrict them by recipe or config if needed. |
| **Field Guide** `field-guide` | 1.22.4+1.21.1-neoforge, release, 2026-10-24, MIT | c+s | **immersive-overlays** (MIT, client-only) and **item-descriptions** (MIT, client-only); emi and kubejs optional | Scan creatures and plants with a spyglass to unlock encyclopedia entries, with progress saved per server. This is the Subnautica databank. Works with modded entities without setup; Naturalist and Spawn integrate with it. | Hidden entries could become FTB Quests goals ("scan 10 abyssal species"). | 2 extra client libs. Immersive Overlays adds HUD overlays that may need config. |
| Sable: Water Pressure `sable-water-pressure` | 1.0.0, beta, 2026-07-21, ARR | c+s | create-ironworks, sable, create | Depth damage. | | **Conflicts** with Deep Seas pressure. Reject. |
| Simple Dive Gear `simple-dive-gear` | 10.0.0, release, 2025-01-09, CC0 | c+s | none | Subnautica-style oxygen tanks. | | **Conflicts** with Deep Seas backtank and oxygen. Reject. |
| Bottled Air `bottled-air` | 1.21.1-2.6, release, 2026-10-02, ARR | s | collective | Breathe from empty bottles. | | Cheap air. Reject. |
| Deep Diving Gear `deep-diving-gear` | 1.2.1, release, 2026-08-31, MIT | c+s | deeperdarker (in), create | Upgrades Create netherite diving gear with echo shards. | | Deep Seas' pressure suit is its own copper suit, so this adds little. Reject. |
| Permanent Sponges `permanent-sponges` | v21.1.0, release, 2024-09-18, MPL-2.0 | c+s | puzzles-lib | Sponges that keep an area permanently dry. | | Bypasses Deep Seas airlocks and sealed rooms. Reject. |
| S.O.N.A.R `s.o.n.a.r` / Echo Sense `echo-sense` | 1.0.5 ARR / 1.0.0 MIT | c+s | none | Scanners. | | Scannable is more mature. Reject. |
| Yellow Submarine `yellow_submarine` | 1.0.0, release, 2025-05-09, MIT | c+s | none | Joke submarine entity. | | Duplicates Deep Seas. Reject. |
| CC: Deep Seas, Cosmonautics: Deep Air | | | cc-tweaked / Cosmonautics | Add-ons. | | Their required mods are not in the pack. Reject. |

## 4. Atmosphere

Most of this needs no mod. Biome `effects` (`water_color`, `water_fog_color`, `fog_color`, `ambient_sound`, `mood_sound`, `additions_sound`, `music`) and the dimension type (`ambient_light`, `fixed_time`, `effects`) cover fog colour, darkness and sound. Deep Seas' own abyss uses water fog `#001030`-ish (4144), water colour 12140, and `ambient.underwater.loop`.

| Mod | Build | Side | Deps | What it adds | Notes | Risks |
|---|---|---|---|---|---|---|
| AmbientSounds (in) | 6.3.11 | c | creativecore | Already has `ocean_deep` and `underwater` regions. It also supports per-dimension definitions (`assets/ambientsounds/basic/dimensions/*.json` with `dimension-names`, `regions`, `sound-collections`). | Add a `strata_abyssal_plain` dimension file through a client resource pack, using the "dark/suspense" collections and underwater regions. | Check whether `dimension-names` matches our dimension's id or its display name. |
| Sound Physics Remastered (in) | | c | | Underwater muffling and reverb. | Nothing to do. | |
| Make Bubbles Pop `make_bubbles_pop` | 0.4.0-beta.2, beta, 2026-09-05, custom licence | c | yacl (opt) | Bubble particles rise to the surface and pop. | Optional client extra. | Beta. Under a ceiling the bubbles may rise and pop at the ceiling, which needs a look. |
| Particular ✨ Reforged `particular-reforged` | 1.5.7, release, 2026-08-16, LGPL | c | create, sable, aeronautics, iris (opt) | Bubbles from underwater chests, splashes, cascades, cave dust. | Optional client extra. Overlaps a little with Subtle Effects (in). | |
| Drown Panic `drown-panic` | 1.0.0, release, 2026-08-02, MIT | c | none | Tunnel-vision vignette when air runs low. | Adds tension. Optional. | May stack with Deep Seas' own pressure vignette and heartbeat. |
| Water Depth Fog `water-depth-fog` | 1.0.0, beta, 2026-07-21, ARR | c | none | Darker, closer fog with depth below a fixed `seaLevel` Y (default 62). Skips Sable sub-levels. | Not dimension-aware: one `seaLevel` applies everywhere, so it would darken deep Overworld water too. Biome `water_fog_color` per abyss biome does the same job. | Reject, or at most optional for players. |
| Clear Water, Simple Fog, Clearviews | | c | | Remove or adjust water fog. | | These work against the mood. Don't add them, but players may. |

## 5. Structures

| Mod | Build | Side | Deps | What it adds | Placement, confinement | Risks |
|---|---|---|---|---|---|---|
| **Sunken Spires** `sunken-spires` | 1.0+mod, release, 2025-10-19, ARR | s (c optional) | none | 11 ruins of a vanished advanced prismarine civilisation: sunken city, colosseum (miniboss), prismarine trial chamber (15 trial spawners, miniboss), prismarine forge (Elder Guardian), ocean temple, conduit ruins, floating spikes, fossils, trident shrine. Includes archaeology. | Tag-driven: `#joshie:has_structure/<name>`, defaulting to `#minecraft:is_ocean` plus other mods' ocean tags. Override with `replace: true` to move the structures into our biomes only, or add our biomes so they appear in both. | Heightmap projection (finding 4). Same author and namespace (`joshie`) as Tidal Towns, which is fine. |
| **MOS – Moog's Ocean Structures** `mos-moogs-ocean-structures` | 1.1.1, release, 2026-09-17, LGPL code / ARR structures | s only | moogs-structure-lib (in) | 26 structures: Atlantis ruins and tribune, sunken ships and wrecks, sea-dragon skeleton, underwater garden and shrine, ruined church and castle, magma ravine, buried treasure. | Tag-driven (`#mos:is_deep_ocean`, etc.), and configurable through Moog's Structure Lib datapacks. Add our biomes only to the seafloor structures' tags, not to rafts or travel ships. | Uses `project_start_to_heightmap: OCEAN_FLOOR_WG`, so the ceiling problem applies. Copy the structures into `strata:` with an absolute height. |
| Aures – Sea Dwellers `aures-sea-dwellers` | 1.0.0, release, 2026-05-18, ARR | c+s | geckolib | Underwater villages with sea traders. | Not inspected. | Could be "inhabited outpost" flavour. One build. Maybe. |
| Hopo Better Underwater Ruins `hopo-better-underwater-ruins` | 1.2.1b, release, 2025-04-13, LGPL | s | none | New ocean ruins. | Not inspected. | Probably changes Overworld ruins too. Maybe. |
| Revamped Shipwrecks / Unwrecked Ships | 1.1.0 (2024-12) / 2.0.5 (2024-12) | s | | Replace vanilla shipwrecks. | Global. | Reject: global and old. |
| Awesome Dungeon Ocean, Underwater Village, Unnamed Sea, Buried Wrecks, statue mods | various ARR | | | Ocean structures. | | Reject: duplicates of Sunken Spires, MOS and what we already have. |

## Already in the pack: reusable content

Check these before adding anything new. Each entry gives the ids and how to put them in the Abyssal Plain.

- **Upgrade Aquatic 7.0.2**
  - Mobs: `upgrade_aquatic:thrasher` and `great_thrasher` (a deep-sea predator that uses sonar), plus `nautilus`, `lionfish`, `box_jellyfish`, `cassiopea_jellyfish` and `immortal_jellyfish`. Thrasher, nautilus and lionfish spawn through biome-tag modifiers, so add our biomes to `#upgrade_aquatic:has_spawn/thrasher` (and `nautilus`, `lionfish`). The jellyfish have no add_spawn modifier in this version, so put them in our biome `spawners`.
  - Flora and terrain: `upgrade_aquatic:prismarine_coral` (elder and prismarine coral, coral showers) through `#upgrade_aquatic:has_feature/prismarine_coral`. The carver `upgrade_aquatic:underwater_canyon` comes through `#upgrade_aquatic:has_carver/underwater_canyon` and is good for trenches.
  - Blocks: 7 jelly-torch colours (bioluminescent lighting), luminous prismarine, coralstone in every coral colour, tooth blocks and tooth lantern, embedded ammonite ore.
- **Alex's Mobs Continued 2.2.4**
  - Mobs: `alexsmobs:frilled_shark`, `giant_squid`, `cachalot_whale`, `comb_jelly`, `blobfish`, `mimic_octopus`, `lobster`, `mantis_shrimp`, `hammerhead_shark`, `orca`, `devils_hole_pupfish`.
  - Spawns are set per mob in `config/alexsmobs/<mob>_spawns.json`, using `BIOME_TAG` or `REGISTRY_NAME` conditions. Frilled shark and giant squid default to `minecraft:is_deep_ocean`, and comb jelly already lists `alexscaves:abyssal_chasm`. Replace or add `{"type":"REGISTRY_NAME","value":"strata:abyssal_..."}`. Weights are in the common config.
- **Naturalist 2.0.7**
  - Mobs: `naturalist:anglerfish`, `giant_isopod`, `jellyfish`, `whale`, `great_white_shark`, `blobfish`, `ray`, `starfish`, `clam`, `crab`.
  - Spawns are code-based but read biome tags: `#naturalist:has_<mob>` minus `#naturalist:blacklist/blacklist_<mob>` (default `#minecraft:is_ocean`, `#c:is_ocean`). Override `has_anglerfish` and `has_giant_isopod` with `replace: true` and our biomes, which makes them abyss-only. The `*_removed` switches are in `naturalist-server.toml`.
- **L_Ender's Cataclysm 3.33**
  - The Leviathan boss and its `cataclysm:sunken_city` structure, through `#cataclysm:has_structure/sunken_city_biomes` plus `required_sunken_city_surrounding`. Also `deepling`, `deepling_brute`, `deepling_angler`, `deepling_priest`, `deepling_warlock`, `coral_golem`, `coralssus`, `lionfish`, `urchinkin`.
  - Moving the Sunken City to the Abyssal Plain makes the Leviathan the dimension's boss, and its drops could gate late Deep Seas or Mekanism tiers, which fits the boss-gating rule. The structure type is custom, so test where it places under a ceiling.
- **Ice and Fire CE 2.1.4**: `iceandfire:sea_serpent` (a leviathan-class creature). It spawns from a worldgen feature (`iceandfire:spawn_sea_serpent`) added through `#iceandfire:entity_gen/sea_serpent`; add our biomes there. That placed feature may use a heightmap, so test it. Sirens are beach-only (`#c:is_beach`), so skip them.
- **Aquamirae 7.2.13**
  - Mobs: `aquamirae:anglerfish`, `maw`, `eel`, `abyssal_scyphoid`, `spinefish`, `shellback`, `maze_mother`, `captain_cornelia`. Spawns come from its own spawner tied to `#aquamirae:ice_maze` (CommonConfig, `BiomeSpawnerMode`).
  - **Don't** add our biomes to that tag: the same tag drives the ice-wall and cracked-ice surface features. If we want these mobs, add them through our biome `spawners` (if their spawn rules allow it) or through In Control!.
  - The `luminescent_lamp` block is a good light.
- **Critters and Companions 2.7.0**: `crittersandcompanions:dumbo_octopus` (a real deep-sea species) and `sea_bunny`. Their `biome_spec` entries are in `crittersandcompanions-common.json5`; add our biome ids.
- **Regions Unexplored 0.6.3**: the `hyacinth_deeps` underwater flora. Placed features `regions_unexplored:hyacinth_flowers`, `hyacinth_plants`, `hyacinth_rocks` and `tall_hyacinth_stock` (use their configured features with our placement), plus `rocky_reef` and `rocky_reef_rocks`.
- **Aquaculture 2.7.21**: `aquaculture:jellyfish`, `tuna`, `red_grouper` and others through per-mob `add_spawns` files (for example `aquaculture:jellyfish_spawn`). This is ordinary life, so leaving it where it is works.
- **Structures already in**
  - `betteroceanmonuments:ocean_monument` (YUNG's): a guardian fortress, usable as a mid-tier dungeon if its biome tag includes ours.
  - `mvs:prismarine_house_1` and `_2`, `mvs:ocean_tower`, `mvs:statue_ruins` (Moog's Voyager).
  - Skip `aquamirae:shipwreck` (it belongs to the frozen region) and Seven Seas and Tidal Towns, which are surface builds.
- **Deep Seas' own blocks, once its abyss is enabled**: `create_abyss:geothermal_vent`, `deepslate_geothermal_vent`, `foam_rock_geothermal_vent`, `burning_sand`, `magma` (Magma Flow), `submarine_liana`, `creepvine_seed`, `abyss_ceiling`. There is also a `GeothermalBreathing` system, possibly air from vents; check it in-game.
- **Other**: LambDynamicLights (in) already lights a held torch or jelly torch underwater. In Control! (in) can confine any code-spawned mob to `strata:abyssal_plain`.

Big creatures already available without a new mod: Cataclysm Leviathan (boss), Ice and Fire sea serpent, Alex's Mobs giant squid and cachalot, and Naturalist whale. Hybrid Aquatic would add the colossal squid and Karkinos, and Alex's Caves the Hullbreaker.

## Recommended set (6 new mods plus 3 libraries)

1. **Create: Deep Seas** (the core), with `iris-flw-compat` (client) if we take 3.3.0. Prefer 3.3.0 release unless 3.4.x fixes something we need. Set `enableDeeperOceans=false`.
2. **Hybrid Aquatic** plus **Hybrid API**. This is the main deep-sea fauna and terrain kit: vents, brine pools, glass sponges, trench predators and bioluminescent fish. It is driven by tags, and its Overworld biomes have a config switch. Remove or gate its diving suits.
3. **Scannable**: the Subnautica scanner, FE-powered, which fits the tech pillar.
4. **Field Guide** plus **Immersive Overlays** and **Item Descriptions** (client libraries): a spyglass scan → databank loop, a ready source of FTB Quests goals, and works with all modded mobs.
5. **Sunken Spires**: tag-driven ancient-civilisation ruins with minibosses and a prismarine trial chamber. These are the "ruins" in the brief.
6. **MOS – Moog's Ocean Structures**: Atlantis ruins, wrecks and skeletons. Server-only, and its library is already in.
7. Optional: **Glow Sticks** (underwater path lighting) and **Create: Deep Seas – Lava Fix**, if vents keep hurting players inside subs.

Then reuse what is already in: Upgrade Aquatic thrashers and jelly torches, Naturalist anglerfish and isopods (confined), Alex's Mobs frilled shark and giant squid, Critters' dumbo octopus, Regions Unexplored hyacinths, and the Cataclysm Sunken City with the Leviathan as the dimension boss.

Separate decision for Darin: **Alex's Caves Continued**. Its Abyssal Chasm is the best ready-made abyss content, but it is a 75 MB mod. Its other cave biomes would need `disabledCompletely`, and its submarine and diving suit duplicate Deep Seas.

## Rejected (one line each)

- Sable: Water Pressure: a second pressure system that conflicts with Deep Seas.
- Simple Dive Gear, Bottled Air: cheap air that undercuts Deep Seas oxygen.
- Permanent Sponges: dry bases without airlocks.
- Deep Diving Gear, Create: Better Utils: upgrade Create diving gear, which Deep Seas' copper suit replaces for pressure.
- Deeper Oceans, NeoReefRedux: change Overworld oceans globally and add nothing here.
- Spawn (`spawn-mod`): a 74 MB Overworld wilderness overhaul with island biomes; its sea life duplicates Naturalist and Hybrid Aquatic.
- Sea Life: code-only spawns that can't be targeted, and ordinary fish we already have.
- Fish of Thieves: adds a tropical-island biome; mainly fishing.
- Whaleborne: a surface whale-ship, useless under a ceiling.
- Myths of the Sea: ARR, single build, one-shot Leviathan; we already have enough leviathans.
- Ben's Sharks, Apex Waters, Animal Garden Bull Shark and Narwhal, Complementary Nautilus, Krakentilus, Kraken Mod: single-species duplicates or one-build ARR mods.
- Creatures of SonariaCraft, Jurassic Reborn, Rocket Squids, Aquatic Creepers: tone doesn't fit, or they're off-theme.
- Aquatic Fauna Expansion (beta 2025), Aquatic Frontiers (2024), Oceanlife: stale or thin.
- Ocean Giants: rescales Alex's Mobs and other existing mobs globally (bosses and mobs keep their designed stats).
- Abyssal Corrupter: a one-build ritual boss; the Cataclysm Leviathan fills that role.
- Ocean World Dimension, Abyssborne, Deep Waters, Abyss (`deepabyss`), Dive Into the Abyss, Lost River, Subnautica After Zero, Subnautica Internal Modules, Beyond the Ocean: whole dimensions or story mods that compete with our own dimension.
- Water Depth Fog: not dimension-aware; biome water-fog colour does the job.
- Clear Water, Simple Fog: remove the mood.
- Abyssal Decor: WIP with placeholder recipes.
- S.O.N.A.R, Echo Sense: weaker than Scannable.
- Yellow Submarine, CC: Deep Seas, Cosmonautics: Deep Air: duplicates, or need mods we don't run.
- Revamped Shipwrecks, Unwrecked Ships, Awesome Dungeon Ocean, Unnamed Sea, Underwater Village, Buried Wrecks, statue mods: global changes, old, or duplicates.
- Alex's Caves (original, `alexs-caves`): 1.20.1 only. Alex's Caves Unofficial Port: use Continued instead (newer, and its codxlib is already in).
