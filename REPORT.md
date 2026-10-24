# Strata — Phase 1 report

Pack: packwiz project `Strata` 0.1.0, Minecraft 1.21.1, NeoForge 21.1.264.
Contents: 261 mods (Keep mods plus the libraries they need), 1 resource pack (Fresh Animations), 1 shader pack (Complementary Reimagined).
Every Keep/Maybe row was checked against the Modrinth API, and through packwiz against CurseForge for anything missing on Modrinth. Results are in `docs/strata-mod-tracker.xlsx`: column G was updated and a new column J, "Phase 1 lookup", says where each build was found.
Mods come from Modrinth where possible. 23 projects that only exist on CurseForge (or only have a build there) come from CurseForge.

## Claude Code picks
- **Gravestone: GraveStone Mod** (henkelmax). It has the most downloads of the 1.21.1 NeoForge options (12.6M), release builds (updated Aug 2026), and no required dependencies. Its author also maintains Corpse and Simple Voice Chat. Corail Tombstone was rejected because its extras include grave teleport and recall features, which break the no-free-teleport rule. Corpse is a fine alternative if you'd rather have a corpse entity with a death-history screen.
- **Dynamic lighting: LambDynamicLights**. It is the reference mod (64M downloads, updated Aug 2026) and has official NeoForge support. Its API is what other mods integrate with. Sodium Dynamic Lights is a port that was last updated in Jan 2025. RyoamicLights is still alpha. LambDynamicLights ships one multi-loader jar whose metadata lists Fabric API as required. That is only needed on Fabric, so I declined it. Confirm it in the launch test.

## Keep mods with no 1.21.1 NeoForge build
| Mod | Outcome |
| --- | --- |
| Botania, Ars Botania | Cut. Ars Botania requires Botania, which has no 1.21.1 build. No replacement: Ars, Iron's, Occultism, Vampirism and Neo Vitae cover magic |
| Drive By Wire | Replaced by the fork **Drive-By-Wire with Sable** |
| Domestication Innovation | Replaced by the fork **Redomesticate** |
| No Mons In My World | Fabric-only (MIT), no NeoForge port. We recreate it when we build the Pokémon world; options are in the design doc (Pokémon world, step 2) |

Maybe rows with no build: Blue Skies and Dimension Gated Difficulty (both cut) and Diet (Spice of Life: Onion was chosen instead).

## Names that matched more than one project
- **Create Thrusters**: no mod has exactly this name. Resolved as **Create Aeronautics: Gadgets & Gizmos**, pinned to 1.2.10, the last stable 1.x build: 2.0 has had six pre-releases and betas in ten days, and the pre-releases are tagged as full releases. Create Propulsion: Simulated stays in too.
- **FTB Quests / FTB Ultimine**: on Modrinth these names hit a translation pack and a fork (Ultimine Rewind). I used the official CurseForge projects.
- **Noisium**: the original (used), NoisiumForked and Noisiumed all exist.
- **Bloodlines**: the bare CurseForge slug hit a different project. The real one is "Bloodlines - A Vampirism Addon".
- **Falling Leaves**: CurseForge has two projects with this name. I used the Forge/NeoForge one (fallingleaves 2.6.0).
- **Friends & Foes**: there are separate Fabric and Forge/NeoForge projects. I used the NeoForge one.
- **ExtendedAE** vs ExtendedAE-Plus (a separate add-on), **Polymorph** vs Polymorph+, **Cosmetic Armor Reworked** (original on CF, used) vs a Modrinth fork, **Twilight Forest** (Modrinth only has an unofficial Fabric port; used the official CF project), **Every Compat** (Wood Good, used; Stone Zone and others are sister mods), **Incendium** (now titled "Incendium Legacy"; same project), **Tide** (titled "Tide 2").
- **Create Offroad** is bundled inside Create Aeronautics, so there's nothing separate to add.

## Known conflicts and risks
- **Create: Steam 'n' Rails is the unofficial port** "Steam 'n' Rails Neoforge" (0.3.0-beta.2, Modrinth `create-steam-n-rails-1.21.1`). The official mod is still 1.20.1-only. The port requires Create ≥ 6.0.7 and NeoForge ≥ 21.1.233, which we meet. Known bug: weather on snow-paved tracks can crash singleplayer and kick everyone from a server (port issue #361; one-line fix in PR #372, not merged). Serene Seasons winters make this more likely. See test 10 in the design doc.
- **Continuity was removed.** Its only NeoForge path is Sinytra Connector plus Forgified Fabric API, a layer for running Fabric mods. That's a crash risk in a pack this size. Fusion (native) plus Athena (pulled in by Chipped) cover connected textures. Re-add it if you want it anyway.
- **Create Aeronautics** lists "visual issues with Iris shaders" as a known incompatibility. This matches test 2 in the plan.
- **JEI** is now installed alongside EMI so JEI plugins like Just Enough Resources work. EMI stays the main recipe viewer.
- **Quark + Zeta** stay (required by Integrated Cataclysm), with overlapping modules turned off (see below).
- Modrinth-declared incompatibilities among the 237 Modrinth-sourced projects: **none found** (`tools/check_conflicts.py`).
- The design's existing risks stand: Iron & Nouveau's listing says it works alongside Ars 'n Spells (test 4), and Vampirism plus the difficulty script plus Apotheosis scaling (test 6).
- Several mods are beta builds: Crafts & Additions, Industrial Foregoing, Relics, Functional Storage, Serene Seasons, Bountiful, Iris, Simple Voice Chat, and others.

## Sides
Packwiz took sides from Modrinth. I then applied the tracker: Xaero's maps, Distant Horizons, Complementary, Fresh Animations, Sound Physics and Falling Leaves are client-only. Chunky, Simple Backups, Noisium, Let Me Despawn, Nullscape and CobbleStructures are server-only. Incendium stays on both sides because it adds items and mobs.

## Round 1 decisions applied (from docs/open-questions.md)
**Added:** Create Aeronautics: Gadgets & Gizmos 1.2.10 (pinned), Drive-By-Wire with Sable, Redomesticate, JEI, Spice of Life: Onion, Neo Vitae, The Aether, Alex's Mobs Continued, Bosses of Mass Destruction Forge (test 11), Plushie Mod.
**Cut:** Botania, Ars Botania, Blue Skies, Dimension Gated Difficulty, Continuity. **Still Maybe:** Modern Industrialization vs Oritech (decide in the creative test), Undergarden (beta; revisit), Create: Better Motors, Accessories.

**Farmer's Delight add-ons added** (each ties into a mod already in the pack, all with 1.21.1 NeoForge builds):
| Add-on | Ties into | Notes |
| --- | --- | --- |
| Ender's Delight 1.3.1 | The End | Picked over End's Delight, whose 1.21.1 build is still beta |
| Twilight's Flavor & Delight 3.2.8 | Twilight Forest | |
| Ars Nouveau's Flavors & Delight 2.2.5 | Ars Nouveau | Same team as Twilight's Flavor |
| L_Ender's Cataclysm Delight 1.0.10b | Cataclysm | Boss-drop foods |
| Aether's Delight 0.1.4.2 | The Aether | Beta, last updated Oct 2025 |

Vampire's Delight, Create Slice & Dice and Central Kitchen were already in. Other candidates I left out: My Nether's Delight (Nether), Ocean's Delight, Expanded Delight, Chef's Delight (villagers).

**Quark modules disabled** (`config/quark-common.toml`; module names checked against the Quark 4.1-487 jar):
| Module | Overlaps with |
| --- | --- |
| Inventory Sorting | Inventory Profiles Next |
| Easy Transferring | Mouse Tweaks + Inventory Profiles Next |
| Automatic Tool Restock | Inventory Profiles Next (auto-refill) |
| Pathfinder Maps | Explorer's Compass / Nature's Compass |
| Ancient Tomes | Apotheosis enchanting |
| Glimmering Weald (+ Quark's TerraBlender region) | Regions Unexplored as the only biome mod |
| Pistons Move Tile Entities (already off by default; pinned off) | Create / Mekanism / AE2 block entities (dupe/crash risk) |

Quark 4.1 no longer has Matrix Enchanting, Backpacks or Totem of Holding, so those overlaps don't exist. Quark's building blocks, mobs and worldgen features stay on. The file sets only these keys and Quark fills in the rest on first launch; test 12 checks the values survive.

**Discord bridge: options with 1.21.1 NeoForge builds** (all server-only):
| Mod | Size | Downloads | Notes |
| --- | --- | --- | --- |
| **Simple Discord Link** (`sdlink`) | ~10 MB + CraterLib | 82k | **Recommended.** MIT, open source, updated Sep 2026, two-way chat, optional whitelist linking |
| Mc2Discord | ~25 MB | 33k | Apache-2.0, open source; bundles a large Discord library |
| Discord Integration (DI) | ~11 MB | 9k | All rights reserved; Discord commands for server info |
| MC-Sync | ~0.4 MB | 6k | Smallest jar, but closed source, low adoption, sides not declared |
| Discord & Chat Images | ~19 MB | 58k | Optional client part for chat images; heavier than needed |

Simple Discord Link is the lightest option that's open source, server-only and widely used. MC-Sync is smaller on disk, but I wouldn't trust it on a server yet. **Added** (server-only, + CraterLib). It needs a Discord bot token and channel ID in its config when we set up the server.

## First launch test: dedicated server (Oct 24, 2026)
Run in Docker with the itzg image (`java21`), NeoForge 21.1.264, 8 GB, with the pack installed from `packwiz serve`. This is the same install path treehouse will use.

**Result: the server boots.** 237 server-side jars loaded (the client-only mods are skipped on a server), "Done" in 22 s, the spawn area generated, and it shut down cleanly. Client-only mods (Sodium, Iris, LambDynamicLights, maps, shaders) still need a real client launch.

Fixes found and applied:
- **Kambrik** (needed by Bountiful) and **TerraBlender** (needed by YUNG's Cave Biomes) were missing. Their Modrinth listings don't declare these dependencies. Both are added.
- **Majrusz's Progressive Difficulty Continued is excluded from the CurseForge API.** The author opted out of third-party downloads, so packwiz can't install it, and the test ran without it. This will block treehouse and packwiz-based player installs too. **Decided Oct 24: dropped.** Staged difficulty becomes a KubeJS script in phase 2 (see docs/difficulty-options.md).

Log findings (no action needed to boot):
- Most of the ~300 ERROR lines are optional compatibility for mods we don't have (Botany Pots, ComputerCraft, BYG/BOP biomes, Hexcasting, FramedBlocks) and client classes the server skips. That's normal.
- Small bugs in other mods: an Ender's Delight recipe (`chorus_pie_slice`) and a Create Deco recipe (`placard`) fail to parse, and Sable logs 14 physics-tag warnings for a Copycats+ block (`copycat_catwalk`). Worth reporting upstream.
- **Every Compat** warns that its generated blocks are over a third of all blocks, mostly from Macaw's Furniture (2,741). Trim that in the phase 2 configs to save memory and load time.
- Simple Discord Link disables itself until it has a bot token (expected).

## Client test 1 (Oct 24, 2026): Modrinth App, RTX 4080, 6 GB
- Reached the title screen; Sodium, Iris and the other client mods loaded, and the game used the NVIDIA GPU.
- **Crashed with `OutOfMemoryError: Java heap space` on creating a singleplayer world.** The instance had 6 GB.
- Fix: ModernFix `mixin.perf.dynamic_resources=true` (shipped in `config/modernfix-mixins.properties`) to load models on demand, and 8 GB for the retest. Every Compat (2,741 Macaw's Furniture variants, a third of all blocks) is the next lever if memory is still tight. Trimming it is a content decision for phase 2.
- Quark kept every disabled module (test 12, partly confirmed). "Terrablender Add Region" doesn't exist in Quark 4.1, so it was removed from our config.

## Client test 2 (Oct 24, 2026): 8 GB + ModernFix dynamic resources
- The world loads and is playable, but laggy: seven server-tick stalls (one of 48 s) and a second `OutOfMemoryError` (in an IO thread, while saving).
- **Cause: Distant Horizons defaults.** `chunkGeneratorMode = FEATURES` makes DH run full worldgen (all 260 mods) to build distant terrain, out to 256 chunks, on 10 threads. DH logged its own warning that its presets were too high.
- Fixes shipped (also applied to the test instance; its originals are saved as `*.before-strata`):
  - Distant Horizons: `PRE_EXISTING_ONLY`, 128 chunks, 4 threads (`preserve = true`).
  - Camera Overhaul off by default (`preserve = true`). Its turning roll and idle sway caused motion sickness while flying. Fresh Animations only animates mobs, so it wasn't the cause.
  - Quark `Replace Worldgen Chests = false`. Quark was swapping structure chests for wood-variant chests that Lootr can't convert (25 found).
- The "sky dungeon" is Inventory Pets' `sky_dungeon`. Its chests have items baked into the structure (no loot table), so Lootr can't make them per-player. **Fixed:** all Inventory Pets structures are now rare (datapack overrides in `kubejs/data/inventorypets/`), and sky dungeons only generate in the Aether. Verified with `/locate` on the test server (see the design doc's KubeJS/config list).
- Pokémon UI and starters in the Pokémon world only: added to the Pokémon world plan.

## Client test 3 (Oct 24, 2026): 8 GB, new world, Chunky pregen in singleplayer
- No out-of-memory errors, but AllTheLeaks warned **"You reached 90% memory usage"** while terrain generated. Five server stalls (2–12 s) while flying through new terrain; smoother after pregenerating with Chunky. Generation itself is slow (about 260 mods' worldgen).
- Next levers: 10 GB for singleplayer testing, generational ZGC (`-XX:+UseZGC -XX:+ZGenerational`) to cut collector pauses, and profiling worldgen on the test server to find the heaviest mods. Multiplayer clients won't generate terrain (treehouse is pregenerated), so they need less.
- **Overlap found:** Iron & Nouveau's in-game notice says Ars 'n Spells 3.4.0+ includes its own Iron's Spells glyphs, so the two overlap. Options: keep Ars 'n Spells only, or set Iron & Nouveau's `enable_iron_glyphs = false` and `enable_glyph_press = false` (per-world server config). **Decision needed.**

## Worldgen profile (Oct 24, 2026)
Chunky + Spark on the Docker server, decoded locally: see `docs/worldgen-profile.md`. Pregeneration ran at about 6.8 chunks/s. The **main server thread** (chunk unload/save) and **G1 GC (~30% of CPU)** are the bottleneck, not mod worldgen; worker threads were mostly idle. The heaviest worldgen is Tectonic's terrain (via Lithostitched, 24%), then Quark's features (7%). **Run 2 with 12 GB + generational ZGC:** 17% faster (8.2 chunks/s), GC CPU down from ~30% to ~8%, worst stall 5.9 s → 3.5 s. Recommended: server 12 GB, singleplayer 10 GB, multiplayer clients 8 GB, all with `-XX:+UseZGC -XX:+ZGenerational`.

## Still open
- Iron & Nouveau vs Ars 'n Spells glyph overlap (see client test 3).
1. Maps: FTB Chunks' own minimap overlaps Xaero's; turn it off client-side (test 13).
2. Modern Industrialization vs Oritech: during the creative test.
3. Pokémon world portal, and the Kanto map license: when we build the Pokémon world.
