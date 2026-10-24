# Strata — Phase 1 report

Pack: packwiz project `Strata` 0.1.0, Minecraft 1.21.1, NeoForge 21.1.264.
Contents: 239 mods (Keep mods plus the libraries they need), 1 resource pack (Fresh Animations), 1 shader pack (Complementary Reimagined).
Every Keep/Maybe row was checked against the Modrinth API, and through packwiz against CurseForge for anything missing on Modrinth. Results are in `docs/strata-mod-tracker.xlsx`: column G was updated and a new column J, "Phase 1 lookup", says where each build was found.
Mods come from Modrinth where possible. 23 projects that only exist on CurseForge (or only have a build there) come from CurseForge.

## Claude Code picks
- **Gravestone: GraveStone Mod** (henkelmax). It has the most downloads of the 1.21.1 NeoForge options (12.6M), release builds (updated Aug 2026), and no required dependencies. Its author also maintains Corpse and Simple Voice Chat. Corail Tombstone was rejected because its extras include grave teleport and recall features, which break the no-free-teleport rule. Corpse is a fine alternative if you'd rather have a corpse entity with a death-history screen.
- **Dynamic lighting: LambDynamicLights**. It is the reference mod (64M downloads, updated Aug 2026) and has official NeoForge support. Its API is what other mods integrate with. Sodium Dynamic Lights is a port that was last updated in Jan 2025. RyoamicLights is still alpha. LambDynamicLights ships one multi-loader jar whose metadata lists Fabric API as required. That is only needed on Fabric, so I declined it. Confirm it in the launch test.

## Keep mods with no 1.21.1 NeoForge build (not added)
| Mod | Notes |
| --- | --- |
| Botania | No 1.21.1 build (latest is 1.20.1). **Ars Botania has a build, but it requires Botania, so it isn't added either** |
| Drive By Wire | Original is Forge-only. The fork **Drive-By-Wire with Sable** (395k downloads) has a build |
| Domestication Innovation | Abandoned (2023). The fork **Redomesticate** has a 1.21.1 NeoForge build |
| No Mons In My World | Fabric-only (MIT), no NeoForge port. We recreate it when building the Pokémon world; options are recorded in the design doc (Pokémon world, step 2) |

Maybe rows with no build: Blue Skies, Dimension Gated Difficulty (the fallback isn't needed, because Majrusz's Continued has a build), Diet, and the original Alex's Mobs and Bosses of Mass Destruction. Alex's Mobs Continued and the Bosses of Mass Destruction Forge port do have builds.

## Names that matched more than one project
- **Create Thrusters**: no mod has exactly this name. The candidates are Create Aeronautics: Gadgets & Gizmos (formerly Thrusters'n'Things, 1M+ downloads), Create: Simulated Thrusters and Create: Linked Thrusters. **Not added; you need to pick one.**
- **Discord bridge mod**: not named, and Discord Integration (dcintegration) has no 1.21.1 NeoForge build. Not added.
- **FTB Quests / FTB Ultimine**: on Modrinth these names hit a translation pack and a fork (Ultimine Rewind). I used the official CurseForge projects.
- **Noisium**: the original (used), NoisiumForked and Noisiumed all exist.
- **Bloodlines**: the bare CurseForge slug hit a different project. The real one is "Bloodlines - A Vampirism Addon".
- **Falling Leaves**: CurseForge has two projects with this name. I used the Forge/NeoForge one (fallingleaves 2.6.0).
- **Friends & Foes**: there are separate Fabric and Forge/NeoForge projects. I used the NeoForge one.
- **ExtendedAE** vs ExtendedAE-Plus (a separate add-on), **Polymorph** vs Polymorph+, **Cosmetic Armor Reworked** (original on CF, used) vs a Modrinth fork, **Twilight Forest** (Modrinth only has an unofficial Fabric port; used the official CF project), **Every Compat** (Wood Good, used; Stone Zone and others are sister mods), **Incendium** (now titled "Incendium Legacy"; same project), **Tide** (titled "Tide 2").
- **Create Offroad** is bundled inside Create Aeronautics, so there's nothing separate to add.
- **Farmer's Delight + add-ons**: Farmer's Delight is added, but no add-ons are named yet (Vampire's Delight and Slice & Dice are already in).

## Known conflicts and risks
- **Create: Steam 'n' Rails is the unofficial port** "Steam 'n' Rails Neoforge" (0.3.0-beta.2, Modrinth `create-steam-n-rails-1.21.1`). The official mod is still 1.20.1-only. The port requires Create ≥ 6.0.7 and NeoForge ≥ 21.1.233, which we meet. Known bug: weather on snow-paved tracks can crash singleplayer and kick everyone from a server (port issue #361; one-line fix in PR #372, not merged). Serene Seasons winters make this more likely. See test 10 in the design doc.
- **Continuity was removed.** Its only NeoForge path is Sinytra Connector plus Forgified Fabric API, a layer for running Fabric mods. That's a crash risk in a pack this size. Fusion (native) plus Athena (pulled in by Chipped) cover connected textures. Re-add it if you want it anyway.
- **Create Aeronautics** lists "visual issues with Iris shaders" as a known incompatibility. This matches test 2 in the plan.
- **Just Enough Resources** is a JEI plugin, and JEI is not in the pack (we chose EMI). Either add JEI alongside EMI (EMI handles JEI plugins) or drop JER. Check this at first launch.
- **Integrated Cataclysm** pulls in **Quark + Zeta** as required dependencies. Quark isn't in the tracker, so it may need config to stay in scope.
- Modrinth-declared incompatibilities among the 217 Modrinth-sourced projects: **none found** (`tools/check_conflicts.py`).
- The design's existing risks stand: Iron & Nouveau's listing says it works alongside Ars 'n Spells (test 4), and Vampirism plus Majrusz plus Apotheosis scaling (test 6).
- Several mods are beta builds: Crafts & Additions, Industrial Foregoing, Relics, Functional Storage, Serene Seasons, Bountiful, Iris, Simple Voice Chat, and others.

## Sides
Packwiz took sides from Modrinth. I then applied the tracker: Xaero's maps, Distant Horizons, Complementary, Fresh Animations, Sound Physics and Falling Leaves are client-only. Chunky, Simple Backups, Noisium, Let Me Despawn, Nullscape and CobbleStructures are server-only. Incendium stays on both sides because it adds items and mobs.

## Decisions for you
1. Thrusters: which mod is "Create Thrusters"?
2. Drive By Wire → the Sable fork? Domestication Innovation → Redomesticate?
3. Botania and Ars Botania are out until a build exists. Keep the Ars↔Botania bridge on the to-do list?
4. ~~Wild-spawn blocking~~ Deferred to the Pokémon world build (options in the design doc).
5. JER: add JEI, or drop JER?
6. Discord bridge mod, Farmer's Delight add-ons, and the still-open Maybes.
