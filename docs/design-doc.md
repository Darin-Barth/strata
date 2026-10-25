# Strata — Design Doc

Oct 23, 2026 · @Darin

## Overview

The pack is named Strata, tagline "Build. Fly. Explore." It targets **Minecraft 1.21.1 on NeoForge**, because Create Aeronautics only exists there. It is a kitchen-sink pack in the 500–600 mod range, built around three pillars and a lot of world-filling content.

| Item | Decision |
| --- | --- |
| Minecraft / loader | 1.21.1 / NeoForge (newest version Create Aeronautics supports) |
| Size | No hard ceiling; MC Eternal 2 (\~600 mods) runs on everyone's PCs today |
| Players | 5–6 friends, mixed PC specs; two newer players who prefer exploring and cute content |
| Hosting | treehouse (Ryzen 5 3600, 32 GB RAM, Debian 13 + Docker, itzg image) |
| Pillars | 1. Technology and automation (Create, Mekanism) · 2. Magic · 3. Exploration, bosses, dungeons |
| Structure | Sandbox with FTB Quests chapters per mod and boss (middle ground between ATM and MC Eternal) |
| Feel | A "full" world: wildlife, ambience, structures and visuals so it never feels empty |

Guiding test for every mod: keep it when it adds a different way to play; question it when it does the same job as something already in.

## Core rules

Travel and logistics must cost something, so trains, airships and power grids stay worth building.

**Teleporting**

- No free commands for players: no `/home`, `/back`, `/rtp`, `/tpa` (leave out FTB Essentials or disable these for non-ops).
- Waystones allowed, with an XP cost that scales with distance and an extra cost across dimensions; warp scrolls and warp stones removed from loot.
- Earned teleporting is fine: Mekanism Teleporters (power + fixed points), Ars Nouveau warp, short-range blink spells, Vampirism's vampire teleport skill, the Royal Telelocator (breaks, repaired with Royal Ender Pearls).

**Flight: it has to cost something** (fuel, power, mana, stamina, durability). Free creative-style flight is out.

| Source | Verdict |
| --- | --- |
| Mekanism jetpack (hydrogen), PneumaticCraft Jet Boots (air) | Allowed |
| Ars Nouveau / Iron's flight (mana) | Allowed |
| Cobblemon riding, including flying Pokémon (stamina), in every dimension | Allowed |
| Elytra (rockets, durability), airships | Allowed |
| MekaSuit flight module | Allowed as a late-game reward |
| Inventory Pets Cloud pet | Test: out unless feeding is a real cost (or raise its cost with KubeJS) |
| Excessive Utilities angel-ring style items | Remove or tie to a cost (XP or power) |
| Any "wear it and fly free" item | Same treatment as the Cloud pet |

**Wireless items and power come in tiers**

1. Early: cables, pipes, belts, trains, IE power lines. No wireless.
2. Mid (after entering the Nether or the first major boss): wireless within one dimension — Flux Networks, AE2 wireless terminals, Mekanism quantum entangloporters.
3. Late: cross-dimension wireless — AE2 Quantum Network Bridge. Until then, moving goods between dimensions takes a train or airship.

## Progression and difficulty

Challenge is there for anyone who wants it, but the world stays friendly for builders and newer players.

- **Staged difficulty, like MC Eternal:** our own KubeJS script (phase 2) — Normal at start, Expert after the first Nether visit, Master after the Ender Dragon, as a server-wide stage. Replaces Majrusz's Progressive Difficulty Continued, which was dropped on Oct 24, 2026: it can't be auto-downloaded (CurseForge API opt-out), it starts Expert on entering *any* modded dimension, and it brings extra systems (bleeding, Undead Army, Enderium tier). See docs/difficulty-options.md.
- **Avoid MC Eternal 2's stacking problem:** bosses keep their designed stats; the progressive mod is the only thing scaling regular mobs. Keep the Nether step modest so newer players aren't overwhelmed; put the bigger jumps in dangerous dimensions.
- **Apotheosis:** randomized gear, gems, elite mobs. Configure elites to be rare near spawn and more common in the Nether, End and far out.
- **Boss gating:** quests and KubeJS recipes require boss drops for late tiers (for example Cataclysm drops for top Mekanism/AE2 parts and cross-dimension wireless).
- **Other scalers to watch:** Vampirism scales its own mobs to nearby player level — include it in the Nether-jump play test.
- **Safety nets:** GraveStone Mod so death doesn't scatter items; Redomesticate (Domestication Innovation fork) so pets aren't lost for good.
- **Combat feel:** Better Combat + Apothic Combat + Combat Roll (not Epic Fight).

## Tech pillar

Tech is the heaviest pillar: Create plus its add-on ecosystem, Mekanism, AE2, and several big tech mods that each bring a different way to play.

**Power progression**

1. Early: Create rotation → Crafts & Additions alternator. Compact but lossy; alternator FE output lowered in config so free water-wheel power doesn't make Mekanism generators pointless.
2. Mid: Create: New Age multiblock coil/magnet generators, clearly more efficient than the alternator.
3. Late: New Age nuclear heat into Create steam engines, alongside Mekanism fission and fusion.

**The grid**

- Crafts & Additions hanging wires for local runs around factories.
- Immersive Engineering LV/MV/HV lines for long distance between buildings, with transformers at substations. Both carry FE and meet at an FE block (for example an accumulator).
- New Age's wire recipes removed with KubeJS; its generators, motors and nuclear stay.
- Inside bases, Mekanism universal cables; Flux Networks later per the wireless tiers.

**Mod groups** (full list in the tracker)

- Create + flight, power, processing, trains/logistics/trading, building and vehicle add-ons, plus Create Big Cannons.
- Mekanism + Generators, Tools, Applied Mekanistics.
- AE2 + ExtendedAE, Applied Flux.
- Immersive Engineering, Industrial Foregoing, PneumaticCraft: Repressurized, Powah, Extreme Reactors, Integrated Dynamics, Laser IO, Excessive Utilities, one of Modern Industrialization / Oritech.
- Resource automation: Mystical Agriculture, Productive Bees, Mob Grinding Utils.
- **Almost Unified** is required so the many copper/tin/steel variants collapse to one.

## Magic pillar

Ars Nouveau is the hub; the other magic mods connect to it through bridge mods so the systems work together.

| Connection | Bridge mod | Notes |
| --- | --- | --- |
| Ars ↔ Iron's Spells | Ars 'n Spells (+ Iron & Nouveau) | Shared mana pool and progression. Newer mod with recent ritual fixes — test early. Do not also add Ars ↔ Iron Mana Bridge. |
| Ars ↔ Occultism | Ars Ocultas | Spirits work from Ars Containment Jars |
| ~~Ars ↔ Botania~~ | ~~Ars Botania~~ | Cut: Botania has no 1.21.1 build. Ars, Iron's, Occultism, Vampirism and Neo Vitae cover magic |
| Ars ↔ AE2 | Ars Énergistique | Verify 1.21.1 |
| Ars ↔ Create | Ars Creo | Verify 1.21.1 |
| Iron's ↔ Apotheosis | Apotheosis x Iron's Spellbooks Compat |  |
| Vampirism ↔ Iron's | Vampirism Iron's Spells Compatibility | Blood spells drain Vampirism blood; holy damage vs vampires |

Fifth magic mod: Neo Vitae (Blood Magic continuation), in now that Botania is out.

**Vampirism** is opt-in per player: vampire, hunter, or ignore it. Include Vampirism Integrations, Werewolves, Vampire's Delight, and if 1.21.1 builds exist, Vampires Need Umbrellas, Vampiric Ageing and Bloodlines. Godly Vampirism and the Mekanism x Vampirism MekaSuit mod (1.20.1 only) are out. Factions-only PvP via config. Test vampires against the food variety mod.

## Exploration pillar

The world is built for long-distance travel: big terrain, lots of structures, real bosses, and reasons to keep looting all game.

- **Terrain and biomes:** Tectonic (terrain shape) + Regions Unexplored 6.0 (main biome mod, ATM10 Aeronautics' pick) + Streams Reflowing. Terralith decided out — stacking two big biome mods mostly adds worldgen cost.
- **Structures:** YUNG's suite, Towns and Towers, When Dungeons Arise, Dungeons and Taverns, Integrated Dungeons and Structures, Explorify. Lootr so every player gets their own loot.
- **Bosses:** L\_Ender's Cataclysm + Integrated Cataclysm (Create doors, puzzles, traps), Mowzie's Mobs, Bosses of Mass Destruction (NeoForge port "Bosses of Mass Destruction Forge").
- **Dimensions:** Twilight Forest, Deeper and Darker, The Aether (a sky dimension fits the flying theme). Undergarden out for now (beta; revisit later); Blue Skies out (no 1.21.1 build). Nether: Incendium (not compatible with Amplified Nether). End: Nullscape.
- **Reasons to keep exploring:** Apotheosis gear and gems; boss drops gating progression; Relics/Artifacts accessories.
- **Making airships matter:** limited teleporting (Core rules), loot on high peaks and sky islands, Explorer's Compass / Nature's Compass to plan trips.
- **Pregenerate** the world with Chunky before anyone joins; heavy worldgen is the main server performance risk. Decided Oct 24 (see docs/worldgen-profile.md):
  1. **Seed chosen (Oct 24):** `1121906793898615393`, spawn at the meadow village X 24031, Y 111, Z −26565 (see docs/seed-scouting.md). Pregeneration is centered there.
  2. **Finish every worldgen-affecting change before pregenerating.** Pregenerated chunks never pick up later worldgen changes. That includes Cobblemon worldgen moving to the Pokémon world (apricorns, evolution-stone ores, Integrated Cobblemon gyms and Pokécenters), the Artifacts/IDAS chest fixes, and any ore or structure configs.
  3. **Pregenerate on Darin's desktop** (i5-13600K, much faster than treehouse), **5,000-block radius** in the Overworld, plus the Nether, End and Aether at sizes to decide. Use the same settings as the server, then copy the world to treehouse.
  4. **Server settings:** 12 GB, `-XX:+UseZGC -XX:+ZGenerational`, `sync-chunk-writes=false` (itzg: `MEMORY=12G`, `JVM_XX_OPTS`, `SYNC_CHUNK_WRITES=false`). Chunky keeps expanding the border in the background after launch if needed.

## Pokémon world

Cobblemon lives in its own "vanilla + Cobblemon" dimension reached by a portal; players can bring their Pokémon anywhere. Built after the base pack is stable.

1. **Dimension:** datapack with copies of the vanilla noise settings and biomes under our own namespace (for example `pokeworld:plains`), so Tectonic, Terralith, Streams Reflowing and the Overworld structure mods don't apply there.
2. **Spawns:** add the copied biomes to Cobblemon's biome tags. Wild spawns must be off in every other dimension while owned Pokémon still work everywhere. No Mons In My World is Fabric-only (checked Oct 23, 2026; MIT license, no NeoForge port or equivalent), so we build our own when we get here. Options, in the order to try:
   1. **KubeJS:** cancel Cobblemon's natural-spawn event unless the dimension is the Pokémon world. That event only covers natural spawns, so sent-out, trainer (Radical Cobblemon Trainers) and battle Pokémon are unaffected. Unverified: whether KubeJS can subscribe to Cobblemon's Kotlin events.
   2. **Small NeoForge mod:** the same hook, with a config list of dimensions where spawning is allowed. About 50 lines. The most robust option, but it needs a Java build setup and ongoing maintenance.
   3. **Datapack only:** replace Cobblemon's biome tags so they contain only our Pokémon world biomes. No code, but it leaks: some spawn files use other tags or name biomes directly, and biome mods add themselves to Cobblemon's tags. It has to be re-checked on every Cobblemon update.
   - Avoid blocking every ownerless Pokémon entity as it joins a world: NPC trainers' Pokémon have no owner, so trainer battles would likely break.
3. **Cobblemon worldgen moves there:** apricorns, evolution-stone ores and other Cobblemon features generate only in the Pokémon world, so trips there are how you get Poké Ball materials.
4. **Structures (targeted at our biomes only):** Integrated Cobblemon (18 gyms + Pokécenters; needs Radical Cobblemon Trainers), CobbleStructures, Cobblemon: Simple Pokecenters, Cobblemon Extra Structures, plus vanilla villages. Cobblemon Additions is Fabric-only, so it's out.
5. **Portal:** a NeoForge portal mod or a KubeJS-scripted portal (to be chosen).
6. **Riding:** allowed in every dimension (flying Pokémon use stamina).
7. **Pokémon only shows up in the Pokémon world** (from the first client test, Oct 24): no starter prompt on first join and no Cobblemon party HUD in the other dimensions.
   - Starter: turn off Cobblemon's on-join starter prompt (`exportStarterConfig` in `config/cobblemon/main.json` writes the starter config; then disable the on-join prompt there; key names to verify). Use KubeJS to run Cobblemon's `/openstarterscreen <player>` the first time a player enters the Pokémon world.
   - Party HUD: Cobblemon has a "Hide Party" keybind. Hiding it automatically outside the Pokémon world needs a client-side KubeJS script or a tiny mod (to research). The fallback is shipping it hidden by default.

Later option: the Cobblemon Kanto map (FireRed/LeafGreen recreation, 1.21.1) as a second portal — needs testing on NeoForge, claim protection, and a license check.

## Horror dimension (proposal, Oct 24)
A separate opt-in dimension for the group's horror fan: horror mods active **only there**, like the Pokémon world.
- **Biomes:** our own dimension, using biomes by reference or copied under our namespace: Vampirism's vampire forest (stays in the Overworld too; removing it there would reshuffle Overworld biomes and break the chosen seed), dark forest, swamp and similar, plus a Pale Garden if a 1.21.1 backport can be **kept out of the Overworld**. The ones checked (Perfect Parity Neo: Pale Garden Awakens, Another Pale Garden Backport) add a TerraBlender Overworld region, which would reshape the Overworld; needs a config switch or a test before using.
- **Mobs:** prefer horror mods that spawn through biome modifiers (retargeted to our biomes). Stalker-type mods (The Knocker, The Obsessed, Cave Dweller ReEvolved, Kenny...) use their own spawn logic and need a dimension whitelist in their config or a KubeJS block outside the dimension. Candidates with 1.21.1 NeoForge builds include ArPhEx, The Obsessed, The Knocker, The Boy and the Bath, Face of Horror, Kenny, Hollow Steve, Cave Dweller ReEvolved, Zombie Nightmare Expansions and Server-Side Horror (ambient).
  - **Reserved (Oct 24, wave 3):** Born in Chaos and Mutant Monsters are picked for this dimension only. Both spawn through biome modifiers, so their spawns get retargeted to the horror dimension's biomes; neither is in the pack yet (added when the dimension is built).
- **Entry: a resin portal** (Darin's idea, Oct 24). A portal frame of **resin bricks/blocks** (the orange "amber" block from the Pale Garden), using the same portal tech as the Pokémon world. Both checked backports include resin blocks and bricks, chiseled resin bricks and the Creaking Heart.
  - **Chicken-and-egg:** if Pale Gardens only exist inside the horror dimension, players need resin from somewhere else first. Preferred: craft resin clumps from **Vampirism's vampire forest** materials (KubeJS recipe; vampire forests stay in the Overworld), so the cursed forest is the gateway. Alternatives: Wandering Trader trade, rare Overworld loot, or a boss drop.
  - **Decision update (Oct 24, later): Pale Gardens go IN the Overworld.** Darin prefers the progression: find a Pale Garden in the Overworld, harvest resin from Creaking Hearts, build the resin portal into the horror dimension. Vanilla Backport ships with **everything on, including all three biomes** (Pale Garden, Dappled Forest, Sulfur Caves); resin shortcuts are off (`resin_loot = false`, `pale_trades = false`) so the Overworld Pale Garden is the only source. This reshapes the Overworld, so **the seed is re-scouted** (the earlier seed 1121906793898615393 is retired). The test notes below still describe what the biome toggles do.
  - **Earlier test (Oct 24): Vanilla Backport with its biomes off.** Its config has `pale_garden`, `has_dappled_forest` and `has_sulfur_caves`. Tested with the chosen seed (1,730 chunks around spawn): defaults changed 19.4% of surface biomes (nearby vampire forests vanished); with those three set to `false` the biomes were **identical to the baseline (0% changed)**. The `minecraft:pale_garden` biome, resin blocks, the Creaking and the Creaking Heart still exist for the horror dimension. Built-in resin sources: Woodland Mansion loot (`resin_loot`) and Wandering Trader trades (`pale_trades`). Vanilla Backport also backports many other features, all on by default; which to keep is still to decide. The Happy Ghast (`dried_ghasts`) is a free-flight mount and must be off or cost-gated.
- Difficulty-script multiplier can be high there.
- Status: idea; research per-mod spawn control and the Pale Garden test before committing.

## Life, building and the cozy side

The pack has to work for players who never touch a machine, so there's a full layer of farming, pets, decorating and gentle goals.

- **Food and farming:** Farmer's Delight + add-ons tied to other mods (Ender's Delight, Twilight's Flavor & Delight, Ars Nouveau's Flavors & Delight, L_Ender's Cataclysm Delight, Aether's Delight, Vampire's Delight), Create Slice & Dice and Central Kitchen, Serene Seasons, Spice of Life: Onion (Diet has no 1.21.1 build).
- **Pets and critters:** Inventory Pets (Cloud and other teleport/free-flight pets disabled or re-gated), Redomesticate, Naturalist, Friends & Foes, Creatures and Beasts: Continued, Critters and Companions, Creeper/Enderman Overhaul, Illager Invasion, Aquaculture 2, Alex's Mobs Continued, Royal Variations.
- **Cozy activities:** Tide (fishing journal), Bountiful (village bounty boards), a short "cozy" FTB Quests chapter (tame a pet, cook five dishes, decorate a house, find a pet dungeon).
- **Building:** Handcrafted, Chipped, Macaw's suite, Supplementaries, Every Compat, Another Furniture, a plushie mod if one exists, Cosmetic Armor Reworked.
- **Storage:** Sophisticated Backpacks + Storage, Functional Storage, Tom's Simple Storage, AE2.
- **Accessories:** Curios is the standard slot system (Accessories Compatibility Layer only if a mod needs it). Artifacts, Relics, Reliquified Artifacts, Forsaken Relics. Reliquified Cataclysm left out (needs a fan fix to work).
- **QoL:** EMI (+ JEI alongside, so JEI plugins like JER work), Jade, AppleSkin, Inventory Profiles Next (sort button), FTB Ultimine, FallingTree, Polymorph, Controlling, Just Enough Resources, Carry On, Mouse Tweaks, Xaero's maps, FTB Chunks + FTB Teams (claims, chunk loading), Simple Voice Chat, Comforts.
- **Skipped on purpose:** Dynamic Trees, MineColonies.

## Visuals and performance

Every heavy visual is client-side and optional, so weaker PCs turn it off and nothing changes for anyone else.

**Visuals (client)**

- Shaders via Iris: Complementary Reimagined as the default (low-to-high presets); Bliss or Photon for strong PCs.
- Distant Horizons (optional per player) — big payoff for airship flight.
- Fresh Animations + Entity Model Features + Entity Texture Features; Fusion for connected textures (Continuity cut: on NeoForge it needs Sinytra Connector).
- Atmospherics (per-biome fog, sky, clouds, stars); mostly replaced when shaders are on, so it mainly helps non-shader players. Check its biome-teleport menu is op-only.
- Sound Physics Remastered, AmbientSounds, Falling Leaves, Camera Overhaul, dynamic lighting.
- Not included: Smooth Loading Screen (Fabric-only); Diorama (no 1.21.1 NeoForge build) — Xaero's instead.

**Performance**

| Where | Mods |
| --- | --- |
| Client | Sodium (not Embeddium), ModernFix, FerriteCore, ImmediatelyFast, Entity Culling, BadOptimizations, AllTheLeaks |
| Server | Lithium, Noisium, Chunky (pregen), Clumps, Let Me Despawn, Spark |
| Skip | C2ME (prone to break with heavy worldgen) |

Ship recommended RAM and Java flags with the pack; tune treehouse's garbage collector settings once the pack is up. Set up automatic world backups before day one.

## KubeJS and config to-do

These are the tweaks that make the pack feel designed rather than piled together.

- [ ] Remove Create: New Age wire recipes (keep Crafts & Additions + IE wires)
- [ ] Lower Crafts & Additions alternator FE output; keep it below New Age generators
- [ ] Gate wireless: same-dimension wireless behind the Nether or first major boss; AE2 Quantum Network Bridge behind a late boss drop
- [ ] Gate top-tier Mekanism / AE2 parts behind boss drops
- [ ] Waystones: distance-scaled XP cost, extra cost across dimensions; remove warp scrolls/stones from loot
- [ ] Disable or re-gate Inventory Pets that teleport or give free flight (Cloud, Nether Portal, Ender Chest — review the rest)
- [ ] Excessive Utilities: remove or cost-gate any free-flight item
- [ ] Player commands: no `/home`, `/back`, `/rtp`, `/tpa` for non-ops
- [ ] Progressive difficulty KubeJS script: server-wide stage (Normal → Expert on the first Nether entry → Master on the first Dragon kill), stored in server persistent data. On spawn, scale health/damage/armor of regular hostile mobs by stage × per-dimension multiplier (modest Nether step; bigger in the End, Twilight Forest, Deeper and Darker, Cataclysm areas; none in the Pokémon world). Skip bosses (`c:bosses` tag + an explicit list: Cataclysm, Mowzie's, BoMD, Twilight bosses, Wither, Dragon, Warden). Op commands to view/set the stage. Tested in test 6
- [ ] Apotheosis: elite mobs rare near spawn, more common far out and in other dimensions
- [ ] Create Big Cannons: limit block damage; FTB Chunks claims block explosions
- [ ] Vampirism: PvP between factions only
- [ ] Almost Unified: pick preferred ores/ingots
- [ ] Pokémon world datapack (see Pokémon world section)
- [ ] Ice and Fire CE dragon riding is free flight: decide how it fits the flight rule (earned only, e.g. a fully grown tamed dragon, and/or a stamina or food cost). Dragon Meal Taming was not added.
- [ ] Create Stuff & Additions jetpacks and Building Gadgets 2 copy-paste: check against the flight rule and set a sane block limit.
- [ ] ChoiceTheorem's Overhauled Village and Aquamirae add structures: settle their configs before pregeneration.
- [ ] Happy Ghast (Vanilla Backport, `dried_ghasts`): a free-flight mount, so cost-gate it (e.g. an expensive harness recipe and/or harness durability) to fit the flight rule.
- [x] Inventory Pets structures made rare (Oct 24): their chests have items baked in (no loot table), so Lootr can't make them per-player, and they were everywhere (24 tree tops near spawn). Overrides in `kubejs/data/inventorypets/`: tree top 24-chunk spacing, underground dungeon/Nether/End dungeons 40, sea cave 48. **Sky dungeons only generate in the Aether** (24 spacing; they sit on island tops at about Y 132). Measured nearest-structure distances from five points: tree top 0.5–3.8 km, underground 0.6–3.2 km, sea cave 1.3–2.8 km, Nether 0.4–1.9 km (Nether blocks), End 0.3–0.9 km, Aether sky dungeon 0.06–0.9 km.

## Test plan and open questions

Test with the whole group early, before writing quests, so heavy mods are found by name instead of guessed at.

**Tests**

1. Launch everything together in a creative world; fix load crashes.
2. Shaders + Distant Horizons with Aeronautics ships in flight (Flywheel rendering is the likeliest break).
3. Create Tweaked Controllers vs Aeronautics' own controls.
4. Ars 'n Spells rituals and shared mana.
5. Wire comparison in creative: Crafts & Additions vs IE (range, throughput, looks).
6. The Nether difficulty jump with progressive difficulty + Apotheosis + Vampirism together.
7. Vampires vs Spice of Life: Onion.
8. Cloud pet upkeep cost.
9. Group play test on treehouse: several airships in the air, players spread out, Spark running.
10. Steam 'n' Rails (unofficial 1.21.1 port, beta) on treehouse: lay snow-paved tracks, let it snow (and a Serene Seasons winter), run trains; watch for the crash/kick from port issue #361 (fix proposed in PR #372, not merged). Also check assembled trains with shaders on, plus couplers and Conductor Whistle.
11. Bosses of Mass Destruction (NeoForge port): summon each boss, check drops, and confirm the bosses keep their designed stats (progressive difficulty and Apotheosis must not scale them).
12. Quark: after first launch, confirm config/quark-common.toml kept our disabled modules (sorting, easy transferring, tool restock, Pathfinder Maps, Ancient Tomes, Glimmering Weald) and look for other overlaps.
13. Maps: Xaero's Minimap + World Map are the map mods. FTB Chunks has its own minimap and large map; turn the FTB minimap off in its client settings (and ship that as a default), then check that claims are still easy to see and manage from FTB Chunks' map. TeamPins (CurseForge, 1.21.1 NeoForge) is an option if we want claims shown on Xaero's maps.
14. Client comfort and performance defaults (from the first client test): Camera Overhaul ships **off** (its camera roll and sway caused motion sickness while flying; players can turn it on), and Distant Horizons ships at 128 chunks, 4 threads and `PRE_EXISTING_ONLY` (no LOD worldgen; its `FEATURES` default caused 48 s freezes and an out-of-memory crash in singleplayer). Both files are `preserve = true`, so player changes survive updates. Check that both feel right.

**Open questions**

- Decided: EMI as the recipe viewer (JEI installed alongside for its plugins), Terralith out; gravestone = GraveStone Mod, dynamic lighting = LambDynamicLights.
- Modern Industrialization or Oritech? Decide during the creative test.
- ~~Spice of Life or Diet?~~ Spice of Life: Onion.
- Remaining choices are settled during testing (below).
- Which portal method for the Pokémon world?
- ~~Neo Vitae in?~~ In.

## Next steps in Claude Code

The build moves to Claude Code, using the mod tracker as the input list.

1. Set up the pack as a git repo with packwiz, pulling mods from CurseForge and Modrinth.
2. Verify every "verify" mod in the tracker against the CurseForge/Modrinth APIs for a 1.21.1 NeoForge build; packwiz fails loudly on any mod without one.
3. Resolve the open questions above as mods are added.
4. Write the KubeJS scripts and configs from the to-do list.
5. Stand up a test server on treehouse (itzg/minecraft-server) with backups and the Discord bridge (Simple Discord Link); pregenerate with Chunky.
6. Run the test plan, then write FTB Quests chapters.
7. Build the Pokémon world datapack and portal once the base pack is stable.
