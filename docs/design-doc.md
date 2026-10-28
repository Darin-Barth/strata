# Strata design doc

## Overview

The pack is named Strata, tagline "Build. Fly. Explore." It targets **Minecraft 1.21.1 on NeoForge**, because Create Aeronautics only exists there. It is a kitchen-sink pack in the 500–600 mod range, built around three pillars and a lot of world-filling content.

| Item | Decision |
| --- | --- |
| Minecraft / loader | 1.21.1 / NeoForge (newest version Create Aeronautics supports) |
| Size | 500–600 mods; no hard ceiling |
| Players | 5–6, mixed PC specs; includes newer players who prefer exploration and cozy content |
| Hosting | treehouse (Ryzen 5 3600, 32 GB RAM, Debian 13 + Docker, itzg image) |
| Pillars | 1. Technology and automation (Create, Mekanism) · 2. Magic · 3. Exploration, bosses, dungeons |
| Structure | Sandbox with FTB Quests chapters per mod and boss |
| Feel | A "full" world: wildlife, ambience, structures and visuals so it never feels empty |

Guiding test for every mod: keep it when it adds a different way to play; question it when it does the same job as something already in.

## Core rules

Travel and logistics must cost something, so trains, airships and power grids stay worth building. Item-by-item rulings are in `docs/gate-map.md` section 5.

**Teleporting:**
- One `/home` per player with a 10-second cooldown (`kubejs/server_scripts/strata_home.js`). Non-ops have no `/back`, `/rtp` or `/tpa`.
- Waystones cost XP by distance, with an extra cost across dimensions. Waystones' warp scrolls and stones are removed from loot.
- Ars Nouveau's single-use Warp Scroll (same dimension) stays as shipped. Its reusable, cross-dimension Stabilized Warp Scroll needs 2 echo shards (gate M21).
- Earned teleporting is fine: Mekanism teleporters, Ars, blink spells, the Vampirism skill, Iron's Portal spell, the Oritech portal augment.
- Removed (`server_scripts/strata_removed_items.js`): Iron's Recall spell, all Draconic dislocators, Helium Flamingo, Wind Staff and Forsaken Relics' Linking Book.
- Corail Tombstone: its teleport tablets are off (`config/tombstone-server.toml`) and its teleport commands are ops-only (`server_scripts/strata_tombstone.js`). The Grave's Key teleport to your grave stays.
- MineColonies: the allied Town Hall teleport is off.

**Flight:** no easy "creative" flight. Flight is fine when it takes real effort to get (boss materials, late-game tiers, taming a dragon) or has an ongoing cost (fuel, power, mana, XP, food for pets, stamina). Every current flight source passes, for example: the Angel Ring needs Grid Power, Inventory Pets' Flying Saddle and Cloud pets must be fed, the Excelsius chestplate needs Cataclysm boss materials. Only something that is both cheap to get and free to run gets gated.

**Wireless: no tiers.** Flux Networks, Mekanism entangloporters, AE2 wireless and Mighty Mail work across dimensions as the mods ship them; AE2's Quantum Network Bridge keeps its own recipe cost. Wireless is never boss-gated. Power still has a ladder (see Tech pillar).

## Progression and difficulty

Challenge is there for anyone who wants it, but the world stays friendly for builders and newer players.

- **Difficulty is per player.** Players progress at very different paces, so there are no server-wide difficulty stages. Difficulty comes from Apotheosis World Tiers (each player picks their own), dimension danger (the Hollow), and bosses with designed stats.
- **Bosses keep their designed stats.**
- **Apotheosis:** randomized gear, gems, elite mobs. Elites are rare near spawn and more common in the Nether, End and far out.
- **Boss gating:** tech, magic and gear tiers need boss drops, Hollow Embers or Abyssal Pearls (`docs/gate-map.md`). Magic gets more and earlier road blocks than tech.
- **Other scalers:** Vampirism scales its own mobs to nearby player level.
- **Safety nets:** Corail Tombstone so death doesn't scatter items; Redomesticate so pets aren't lost for good.
- **Combat feel:** Better Combat + Apothic Combat + Combat Roll.

## Tech pillar

Tech is the heaviest pillar: Create plus its add-on ecosystem, Mekanism, AE2, and several big tech mods that each bring a different way to play.

**Power progression**

1. Early: Create rotation → Crafts & Additions alternator. Compact but lossy; alternator FE output is lowered in config so free water-wheel power doesn't make Mekanism generators pointless.
2. Mid: Create: New Age multiblock coil/magnet generators, clearly more efficient than the alternator.
3. Late: New Age nuclear heat into Create steam engines, alongside Mekanism fission and fusion.

**The grid**

- Crafts & Additions hanging wires for local runs around factories.
- Immersive Engineering LV/MV/HV lines for long distance between buildings, with transformers at substations. Both carry FE and meet at an FE block (for example an accumulator).
- New Age's Electrical Connector is removed with KubeJS (`strata_power.js`); its generators, motors and nuclear stay.
- Inside bases, Mekanism universal cables; Flux Networks for wireless power (no wireless tiers).

**Mod groups** (full list in the tracker)

- Create + flight, power, processing, trains/logistics/trading, building and vehicle add-ons, plus Create Big Cannons.
- Mekanism + Generators, Tools, Applied Mekanistics.
- AE2 + ExtendedAE, Applied Flux.
- Immersive Engineering, Industrial Foregoing, PneumaticCraft: Repressurized, Powah, Extreme Reactors, Integrated Dynamics, LaserIO, Excessive Utilities, Oritech.
- Resource automation: Mystical Agriculture, Productive Bees, Mob Grinding Utils.
- **Almost Unified** collapses the many copper/tin/steel variants to one.

## Magic pillar

Ars Nouveau is the hub; the other magic mods connect to it through bridge mods so the systems work together.

| Connection | Bridge mod | Notes |
| --- | --- | --- |
| Ars ↔ Iron's Spells | Ars 'n Spells (+ Iron & Nouveau) | Shared mana pool and progression. Test rituals early. |
| Ars ↔ Occultism | Ars Ocultas | Spirits work from Ars Containment Jars |
| Ars ↔ AE2 | Ars Énergistique |  |
| Ars ↔ Create | Ars Creo |  |
| Iron's ↔ Apotheosis | Apotheosis x Iron's Spellbooks Compat |  |
| Vampirism ↔ Iron's | Vampirism Iron's Spells Compatibility | Blood spells drain Vampirism blood; holy damage vs vampires |

Fifth magic mod: Neo Vitae (Blood Magic continuation).

**Vampirism** is opt-in per player: vampire, hunter, or ignore it. Add-ons: Vampirism Integrations, Werewolves, Vampire's Delight, Vampires Need Umbrellas, Vampiric Ageing and Bloodlines. PvP is between factions only (config). Test vampires against the food variety mod.

## Exploration pillar

The world is built for long-distance travel: big terrain, lots of structures, real bosses, and reasons to keep looting all game.

- **Terrain and biomes:** Tectonic (terrain shape) + Regions Unexplored (main biome mod) + Streams Reflowing.
- **Structures:** YUNG's suite, Towns and Towers, When Dungeons Arise, Dungeons and Taverns, Integrated Dungeons and Structures, Explorify. Lootr so every player gets their own loot.
- **Bosses:** L\_Ender's Cataclysm + Integrated Cataclysm (Create doors, puzzles, traps), Mowzie's Mobs, Bosses of Mass Destruction (NeoForge port "Bosses of Mass Destruction Forge").
- **Dimensions:** Twilight Forest, Deeper and Darker, The Aether (a sky dimension fits the flying theme). Nether: Incendium. End: Nullscape.
- **Reasons to keep exploring:** Apotheosis gear and gems; boss drops gating progression; Relics/Artifacts accessories.
- **Making airships matter:** limited teleporting (Core rules), loot on high peaks and sky islands, Explorer's Compass / Nature's Compass to plan trips.
- **Pregenerate** the world with Chunky before anyone joins; heavy worldgen is the main server performance risk (see `docs/worldgen-profile.md`).
  1. **Seed:** `-1678324137078475659`, spawn at -358, 77, -3260 beside the tavern of an Integrated Villages Tavern village.
     - **How it runs:** pregeneration is centered at the spawn. `tools/start_pregen.sh` boots container `strata-world` with the world in `server/` (git- and packwiz-ignored), sets the spawn and runs Chunky (Overworld, circle, 5,000-block radius). Other dimensions use `tools/pregen_dimensions.sh` (two dimensions at a time).
     - **Done:** Overworld 5,000 (circle); Nether 1,250 around -45/-408; End 2,000 around 0/0; Pokémon world 2,000; Twilight Forest 1,500 and Aether 1,000 around spawn. World size 5.6 GB.
     - **Notes:** long runs build up a scheduler/heap backlog (rate drops to 1–2 chunks/s); a clean restart clears it and Chunky resumes. Run `/sable paused true` during pregen (Sable's physics thread competes for the main thread). **`/sable paused` with no argument toggles it**, so always pass true/false; set it back to false after pregen.
     - **Aether trap:** the Aether's `DungeonBlacklistFilter` placement filter calls `Level.getChunk` from inside worldgen and deadlocks the pregen around chunk -73,-281 (≈ block -1168,-4496). The Aether is therefore pregenerated to 1,000 blocks (concentric), and that spot generates on demand. Watch for a stall if someone flies there.
  2. **Finish every worldgen-affecting change before pregenerating.** Pregenerated chunks never pick up later worldgen changes. That includes the Pokémon world's Cobblemon worldgen (apricorns, evolution-stone ores, Integrated Cobblemon gyms and Pokécenters), the Artifacts/IDAS chest fixes, and any ore or structure configs.
  3. **Pregenerate on a fast desktop** (i5-13600K, much faster than treehouse) with the same settings as the server, then copy the world to treehouse.
  4. **Server settings:** 12 GB, `-XX:+UseZGC -XX:+ZGenerational`, `sync-chunk-writes=false` (itzg: `MEMORY=12G`, `JVM_XX_OPTS`, `SYNC_CHUNK_WRITES=false`). Chunky keeps expanding the border in the background after launch if needed.

## Pokémon world

**Player-facing name: the Kakuto Region** (*kaku* = square, like the blocks). The title banner, quest book and portal docs use it; IDs stay `pokeworld:*` so built worlds keep working. Portal look: "Unown Drift" texture, bell/hum/wind/Unown sounds and glyph particles (`startup_scripts/portal_ambience.js`).

Status: built. Cobblemon lives in its own "vanilla + Cobblemon" dimension, `pokeworld:pokeworld`, reached by a portal. Players can bring their Pokémon anywhere, and riding (flying Pokémon use stamina) is allowed in every dimension. Everything ships through KubeJS (`kubejs/data`, `kubejs/*_scripts`) and `config/`. Most of the datapack is generated by `tools/build_pokeworld.py`. Re-run it after a Cobblemon or structure-mod update (inputs are listed at the top of the script).

1. **Dimension:** `pokeworld:pokeworld` uses its own dimension type, noise settings, density functions and noises, all deep copies of vanilla 1.21.1. Tectonic overrides `minecraft:overworld/*` density functions and noises, so referencing vanilla IDs would pull Tectonic in. The 53 vanilla Overworld biomes are copied as `pokeworld:<name>` and placed by an explicit multi-noise list (vanilla's own parameters). TerraBlender/Regions Unexplored only inject into `minecraft:overworld`. Streams Reflowing attaches to every noise dimension, so `config/streamsreflowing.properties` sets `streamBiomeBlacklist=pokeworld:*`: no streams or lakes start in Pokémon-world biomes, and Overworld streams are unchanged. It applies to newly generated land only, so it must ship before pregeneration. The copies are in no vanilla or `c:` biome tags, so Overworld feature, ore and structure mods don't reach them. Exceptions found by the script's leak check: IE mineral veins (virtual, harmless) and a few Quark/vanilla mob spawns added by code.
2. **Wild spawns only in the Pokémon world:** `kubejs/server_scripts/pokeworld_spawns.js` fills Cobblemon's `worldSpawningBlocklist` with every loaded dimension except `pokeworld:pokeworld` at server start, so dimensions added later are covered too. A Cobblemon spawn rule (`location` component) is not usable: in Cobblemon 1.8.2 that component fails before evaluating its expression and blocks spawns everywhere. The blocklist only affects the natural spawner. Sent-out, NPC-trainer and battle Pokémon don't go through it. The pokeworld biomes are added to all 155 of Cobblemon's own biome tags, so spawn conditions, regional evolutions and Vivillon patterns work there. Radical Cobblemon Trainers' wandering trainers spawn only there too (`dimensionWhitelist` in `config/rctmod-server.toml`). That list doesn't affect trainers placed by gym structures.
3. **Cobblemon worldgen lives there:** Cobblemon adds about 96 placed features from code (apricorns, mints, saccharine trees and medicinal leeks in *every* biome; berry groves, type gems, big roots, treasure hoards and lost ruins in `#minecraft:is_overworld`; evolution-stone ores, fossils and habitats by Cobblemon tags). Tags can't move them, so the originals are overridden to `count 0` everywhere, and `pokeworld:cobblemon/<path>` copies are listed directly in the matching pokeworld biomes (88 copies; the Nether/End-only ones have no pokeworld biome). The list is read from Cobblemon's bytecode (`tools/pokeworld/parse_cobblemon_features.py` → `cobblemon_injected.json`).
4. **Structures:** the structures of Cobblemon, Integrated Cobblemon (gyms + Pokécenters), CobbleStructures, Cobblemon: Simple Pokecenters and Cobblemon Extra Structures are overridden to `#pokeworld:has_structure/...` tags (the pokeworld copies of their original biomes). Integrated Cobblemon's fire gym (Nether) and psychic/dragon gyms (End) stay in the Nether and End. Vanilla Overworld structures are copied as `pokeworld:<name>` (villages, outposts, temples, monuments, mansions, shipwrecks, ruins, trial chambers, ancient cities, mineshafts; no stronghold). The copies are added to the vanilla structure tags (`#minecraft:village` etc.). The 26 Cobblemon spawn files that name a vanilla structure directly (e.g. Qwilfish avoiding `minecraft:monument`) are overridden with the `pokeworld:` copy added next to it (generated; re-run the script after a Cobblemon update).
   - Villages: Cobblemon adds Pokécenters, berry farms and habitats to the vanilla village house pools, both in a data file and in code at server start. `kubejs/startup_scripts/pokeworld_village_pools.js` strips every `cobblemon:` piece from the five `minecraft:village/*/houses` pools (lowest priority on ServerAboutToStart, before any chunk generates). Pokémon world villages use jigsaw pool aliases to a copy with Cobblemon's buildings (`pokeworld:village/*/houses`). Other mods' village additions (Waystones, Bountiful, Farmer's Delight, ...) stay in Overworld villages. CobbleDollars (2.0.0-beta-6.1): its Cobble Merchant village code never runs, its `minecraft:<type>/villagers.json` copies sit at a path nothing references, and the jar ships no merchant template. So it adds nothing to villages anywhere; Cobble Merchants only appear when a villager takes their job block. The startup script filters `cobbledollars:` pieces from the villager pools too, in case a later version turns that on.
5. **Starter:** `config/cobblemon/main.json` sets `exportStarterConfig: true` so Cobblemon reads `config/cobblemon/starters.json`, which has `allowStarterOnJoin: false` and Cobblemon's own default starter list with `useConfigStarters: true` (with `false`, Cobblemon 1.8.2 opens an empty starter screen, because no datapack starters exist). That leaves no prompt on join, and the starter is locked for new players. `kubejs/server_scripts/pokeworld_starter.js` runs `/openstarterscreen <player>` when a player without a starter is in the Pokémon world. It runs at most once per login, so closing the screen without picking brings it back next time; Cobblemon's own "starter selected" flag stops it for good. Verified in game: the categories show, and picking Charmander works.
6. **Party HUD:** `kubejs/client_scripts/pokeworld_party_hud.js` sets Cobblemon's Hide Party toggle (`HidePartyBinding.setShouldHide`) on every dimension change: hidden outside the Pokémon world, shown inside. The Hide Party key still works in between.
7. **Portal:** BBL Portals (MIT; standalone fork of Custom Portal API + PortalJS with their Sodium/flint-and-steel fixes), set up in `kubejs/startup_scripts/pokeworld_portal.js`. There is no pre-built portal; players make their own.
   - **Frame:** a nether-portal-shaped frame of **Alph Stone** (block id `pokeworld:poke_portal_frame`; ancient carved sandstone after the Ruins of Alph; 8 per craft from 8 chiseled sandstone around a diamond), lit with the **Johto Bell**. The frame blocks connect into one carved border through Fusion (in the pack for Rechiseled, `pieced` layout) and pick a random variant per block: every block carved with Unown (each with its eye): one big (O, A, !) or two small (I + U, O + A), cracked and/or mossy. The portal glows Ultra Wormhole cyan.
   - **Igniter:** the Bell is crafted from a vanilla Bell, 3 gold ingots and a **Bell Fragment**, and is reusable (BBL Portals never uses up the igniter; the fragment's rarity is the gate). Bell Fragments are rare chest loot in Overworld structures, via NeoForge global loot modifiers in `kubejs/data/pokeworld/loot_modifiers`. Chances per chest (Lootr rolls each chest once per player): dungeon 8%, mineshaft 3%, desert pyramid 6%, jungle temple 8%, ancient city 12%, woodland mansion 20%, trial vault 6% / ominous vault 20%, YUNG's dungeons 5–8%, YUNG's desert tomb 8%, YUNG's jungle treasure 10%.
   - **Link:** 1:1 X/Z, and the portal on the other side leads back to the Overworld.

**Verification (Docker test server):**
- `/locate structure` for all 105 overridden structures from the spawn: none found in the Overworld; 103 found in the Pokémon world. The two cave ruins (crumbling arch, rooted arch) come from feature copies, not structure sets.
- Chunky, 600-block radius around spawn in both dimensions, then a region scan (`tools/pokeworld/scan_regions.py`): Overworld 6,267 chunks with **0** `cobblemon:` blocks, including two villages. Pokémon world 8,417 chunks, 6,460 with Cobblemon blocks: evolution-stone ores, apricorn trees, big roots, type gems, berries, revival herbs, Pokécenters (healing machines, PCs).
- Pokémon-world villages get Cobblemon's Pokécenters through the pool alias. Five placed villages all had healing machines. The KubeJS hook logged removing 1,730 Cobblemon pool entries (repeated by weight) from the Overworld village pools.
- A command-spawned Pikachu and a summoned RCT trainer (Youngster Joey) work in the Overworld.
- Portal: BBL Portals registers the Poké Portal Frame as its frame block. Both recipes load with 0 failures. 100 woodland-mansion loot rolls gave 18 Bell Fragments (20% expected).
- Mobs in the other direction: no Pokémon reach other dimensions. The spawn blocklist keeps the Cobblemon spawner out of every dimension except `pokeworld:pokeworld`, and nothing else spawns wild Pokémon. Only Pokémon spawn in the Pokémon world: In Control! allows natural spawns from Cobblemon and Radical Cobblemon Trainers in `pokeworld:pokeworld` and denies everything else (`config/incontrol/spawn.json`). Village villagers placed with structures stay.
- Full-pack check (396 mods): the leak check found nothing new. `/locate` for all 890 non-Cobblemon structures in every mod, Ice and Fire included, found none in the Pokémon world (4 are disabled or replaced by IDAS). Wild spawns are blocked in 24 dimensions. Async Locator makes `/locate` asynchronous: over RCON the reply is empty and the result is in the server log.
- In-game test with a player client: the portal, the HUD hiding and showing, wild spawns (Pokémon world 49 in 2 min, Overworld 0), an Overworld trainer battle and the starter screen (every category shows and a starter can be picked) all pass.

**Open items**
- Cobblemon Kanto map (FireRed/LeafGreen recreation, 1.21.1) as a second portal: still planned? It needs testing on NeoForge, claim protection, and a license check. To decide when the Pokémon world is extended.

## Horror dimension: The Hollow

Status: built as **The Hollow** (`strata:hollow`), an opt-in dimension where every horror mod in the pack is confined. The full design is in `docs/hollow-design.md`.

- **Entry:** a resin-brick portal (BBL Portals, same setup as the Pokémon world) lit with the Pale Lantern.
- **Resin source:** Vanilla Backport runs with all its biomes on (Pale Garden, Dappled Forest, Sulfur Caves) in the Overworld. Its resin shortcuts are off (`resin_loot = false`, `pale_trades = false` in `config/vanillabackport-common.toml`), so Overworld Pale Gardens are the only resin source.

## Life, building and the cozy side

The pack has to work for players who never touch a machine, so there's a full layer of farming, pets, decorating and gentle goals.

- **Food and farming:** Farmer's Delight + add-ons tied to other mods (Ender's Delight, Twilight's Flavor & Delight, Ars Nouveau's Flavors & Delight, L_Ender's Cataclysm Delight, Aether's Delight, Vampire's Delight), Create Slice & Dice and Central Kitchen, Serene Seasons, Spice of Life: Onion.
- **Pets and critters:** Inventory Pets (House and End Portal pets disabled; flight pets must be fed), Redomesticate, Naturalist, Friends & Foes, Creatures and Beasts: Continued, Critters and Companions, Creeper/Enderman Overhaul, Illager Invasion, Aquaculture 2, Alex's Mobs Continued, Royal Variations.
- **Cozy activities:** Tide (fishing journal), Bountiful (village bounty boards), a short "cozy" FTB Quests chapter (tame a pet, cook five dishes, decorate a house, find a pet dungeon).
- **Building:** Handcrafted, Chipped, Macaw's suite, Supplementaries, Every Compat, Another Furniture, Plushie Mod, Cosmetic Armor Reworked.
- **Storage:** Sophisticated Backpacks + Storage, Functional Storage, Tom's Simple Storage, AE2.
- **Accessories:** Curios is the standard slot system. Artifacts, Relics, Reliquified Artifacts, Forsaken Relics.
- **QoL:** EMI as the only recipe viewer, with EMI Ores, Advanced Loot Info and Just Enough Breeding; Jade, AppleSkin, Inventory Profiles Next (sort button), FTB Ultimine, FallingTree, Polymorph, Controlling, Carry On, Mouse Tweaks, Xaero's maps, FTB Chunks + FTB Teams (claims, chunk loading), Simple Voice Chat, Comforts.

## Visuals and performance

Every heavy visual is client-side and optional, so weaker PCs turn it off and nothing changes for anyone else.

**Visuals (client)**

- Shaders via Iris: Complementary Reimagined as the default (low-to-high presets).
- Distant Horizons (optional per player): big payoff for airship flight.
- Fresh Animations + Entity Model Features + Entity Texture Features; Fusion for connected textures.
- Atmospherics (per-biome fog, sky, clouds, stars); mostly replaced when shaders are on, so it mainly helps non-shader players. Check its biome-teleport menu is op-only.
- Sound Physics Remastered, AmbientSounds, Falling Leaves, Camera Overhaul, LambDynamicLights. Xaero's for maps.

**Performance**

| Where | Mods |
| --- | --- |
| Client | Sodium, ModernFix, FerriteCore, ImmediatelyFast, Entity Culling, BadOptimizations, AllTheLeaks |
| Server | Lithium, Noisium, Chunky (pregen), Clumps, Let Me Despawn, Spark |

Ship recommended RAM and Java flags with the pack; tune treehouse's garbage collector settings once the pack is up. Set up automatic world backups before day one.

## KubeJS and config to-do

These are the tweaks that make the pack feel designed rather than piled together.

- [x] New Age wiring removed (`kubejs/server_scripts/strata_power.js`): the Electrical Connector recipe (and the Street Light, which needs one) are gone; wires stay craftable because copper wire goes into New Age's copper circuit. New Age generators hand FE to C&A and IE through their carbon brushes.
- [x] Crafts & Additions alternator at 240 FE at max RPM (`config/createaddition-common.toml`), half of New Age's.
- [x] Wireless: not gated; no wireless tiers (see Core rules).
- [x] Gate top-tier Mekanism / AE2 parts behind boss drops: built from `docs/gate-map.md` (T1–T10).
- [x] Waystones: distance XP cost is the mod default (0.01 XP per block, 27 levels across dimensions); no loot table contains warp scrolls or stones (audited). Warp scrolls and warp plates pay the same XP as waystones (`config/waystones-common.toml`).
- [x] Inventory Pets:
  - Flight pets settled (must be fed; see Core rules).
  - House and End Portal pets disabled (`config/inventorypets-common.toml`). Nether Portal and Enderman pets stay; the Nether Portal pet only works after you've entered the Nether yourself (`strata_pets.js`).
  - Pets are found, not crafted: every pet recipe and the Petrifier are removed (`strata_pets.js`). Pets drop from structure chests in tiers (`tools/build_pet_loot.py`): common in dungeons/temples, rare in strongholds/mansions/fortresses, the Nether Portal pet in Nether fortresses and bastions, legendary (2.5%) in End cities/ancient cities/bastion treasure/ominous vaults. Five legendary pets also drop from a boss (15% per player): Cloud from the Sun Spirit, Sun from Ignis, Wither from the Harbinger, Black Hole from the Ender Guardian, Pufferfish from Scylla or the Leviathan. The Slime pet (cheat-death) is chest-only.
  - Boss loot bags (`kubejs/server_scripts/strata_boss_bags.js`, item `strata:boss_bag`): when a boss in `#strata:boss_bags` dies, every player who hit it in the last 10 minutes gets a bag with their own full roll of its loot table; nothing drops on the floor. The killing blow's player gets the actual drops (so death-time drops added by other mods still land); everyone else gets a fresh roll with themselves as the killer. Loot modifiers (pets, gate drops) apply to every roll. Bosses that move their loot into their own chest (Twilight Forest) keep doing that for the main player. Each boss has its own bag texture (`tools/build_boss_bags.py`: colours from the boss's entity texture or a hand-picked palette, a themed emblem; selected by `custom_model_data` from the generated `strata_boss_bag_models.js`).
  - Strong pets stay but are weaker: Juggernaut and Illuminati cooldowns 10 min, Pac-Man's damage bonus grows 1 per kill, Pingot finds ore but doesn't extract it, and costlier upkeep food for Juggernaut, Illuminati, Wither, Sun, Black Hole, Loot, Pixie, Silverfish, Quantum Crystal Monster, Pac-Man and Anvil.
- [x] Excessive Utilities flight: passes the flight rule (Angel Ring needs Grid Power).
- [x] Player commands: `/home` + `/sethome` only (`strata_home.js`, 9a6507f).
- [x] Apotheosis elites and invaders rare near spawn (`kubejs/server_scripts/strata_elites.js`): 10% kept at world spawn, all by 2,000 blocks; Overworld only.
- [x] Create Big Cannons: `NO_EXPLOSIVE_DAMAGE`; FTB Chunks claims already block explosions (default).
- [x] Vampirism: PvP between factions only (`config/vampirism-server.toml`), on top of the team protection.
- [x] Almost Unified: default priority (minecraft > kubejs > create > IE > mekanism) shipped in `config/almostunified/`.
- [x] CobblemonOptimizer 5.0.0, server-only (loads clean, TPS threshold 18).
- [x] Ice and Fire dragon riding: passes the flight rule (taming a dragon is real effort). Optional: `flightStamina` is off.
- [x] Create Stuff 'N Additions jetpacks: settled (they burn fuel). Building Gadgets 2 copy-paste: defaults kept (50 FE per block, about 20k blocks per charge, and it uses your own blocks).
- [x] ChoiceTheorem's Overhauled Village and Aquamirae configs: moot; the world is pregenerated and live (changes would only reach chunks past 5,000 blocks).
- [ ] Wave 4 checks.
  - Done or settled: End Remastered eyes (in-game pass), Ars Elemental Air focus and Ars Additions warp (mana, earned), TorchMaster (default 64, in the quest book), Lootr (39c5841). Horseman horn capped at 128 blocks (`config/horseman-server.toml`); Mega Torches can't be placed in the Hollow (`hollow_rules.js`); Legendary Monsters' only natural Overworld spawn, the desert Bomber, is at weight 10 (`kubejs/data/legendary_monsters/`).
  - *Open:* Extended Crafting endgame (gate map T10). Rarity pass for new structures: low value now the world is pregenerated.
- [ ] Wave 5 checks.
  - Done or settled: Ad Astra oxygen and launch rules (defaults), Create Jetpack air (ongoing cost), In Control! for the Hollow (00757be), LootJS strip script (`strata_removed_items.js`).
  - *Open:* Ad Astra rocket gates (gate map T7/T8), Ad Astra Overworld ores (check), Structurify spacing (probably skip: world pregenerated), Immersive Optimization test with farms, contraptions and Cobblemon (work).
- [ ] In-game test notes.
  - Lootr confirmed; Seven Seas junk in icebergs is cosmetic (ignore); client heap 79–94% of 16 GB (watch).
  - Pregenerated: Overworld, Nether, End, Aether, Kakuto, Twilight (d91b9e3).
  - Log errors checked: `byg:emeraldite_shards` / `create:crushed_gold_ore` come from IDAS sunken ship and ancient mine chests that name items from mods not in the pack (those slots stay empty, harmless); Ice and Fire attachments and Blueprint's repaletter are only DEBUG lines on the live server; Grim & Bleak's torch and withered-stick recipes fail to load (its own bad recipes, harmless).
  - *Open, work:* pregenerate the Hollow, the Abyssal Plain and Crystal Chronicles' dimension. *Open:* Immersive Optimization test in play. Report: `main-ingame-test-results.md`.
- [ ] Wave 6 checks.
  - Done or settled: Apocalyptic Bosses loot and density (8fb8e2a), Oritech flight (research cost; gate map §5), WaterFrames (URL whitelist is image and video hosts only).
  - *Open:* Apocalyptic ultimate ingot (gate map G6), Draconic tiers (T9), Oritech flight dragon heart (G5) and an in-game check that the exosuit jetpack drains power, Crystal Chronicles: pregenerate and check its End sub-biome against Nullscape (work).
- [x] Happy Ghast: passes the flight rule. Optional: a harness cost if it ever feels cheap.
- [x] Inventory Pets structures made rare: their chests have items baked in (no loot table), so Lootr can't make them per-player. Overrides in `kubejs/data/inventorypets/`: tree top 24-chunk spacing, underground dungeon/Nether/End dungeons 40, sea cave 48. **Sky dungeons only generate in the Aether** (24 spacing; they sit on island tops at about Y 132). Measured nearest-structure distances from five points: tree top 0.5–3.8 km, underground 0.6–3.2 km, sea cave 1.3–2.8 km, Nether 0.4–1.9 km (Nether blocks), End 0.3–0.9 km, Aether sky dungeon 0.06–0.9 km.

## Test plan

Test with all players early, before writing quests, so heavy mods are found by name instead of guessed at.

1. Launch everything together in a creative world; fix load crashes.
2. Shaders + Distant Horizons with Aeronautics ships in flight (Flywheel rendering is the likeliest break).
3. Create Tweaked Controllers vs Aeronautics' own controls.
4. Ars 'n Spells rituals and shared mana.
5. Wire comparison in creative: Crafts & Additions vs IE (range, throughput, looks).
6. Vampires vs Spice of Life: Onion.
7. Cloud pet upkeep cost.
8. Multiplayer play test on treehouse: several airships in the air, players spread out, Spark running.
9. Steam 'n' Rails (unofficial 1.21.1 port, beta) on treehouse: lay snow-paved tracks, let it snow (and a Serene Seasons winter), run trains; watch for the crash/kick from port issue #361 (fix proposed in PR #372, not merged). Also check assembled trains with shaders on, plus couplers and Conductor Whistle.
10. Bosses of Mass Destruction (NeoForge port): summon each boss, check drops, and confirm the bosses keep their designed stats (Apotheosis must not scale them).
11. Quark: after first launch, confirm config/quark-common.toml kept the disabled modules (sorting, easy transferring, tool restock, Pathfinder Maps, Ancient Tomes, Glimmering Weald) and look for other overlaps.
12. Maps: Xaero's Minimap + World Map are the map mods. FTB Chunks has its own minimap and large map; turn the FTB minimap off in its client settings (and ship that as a default), then check that claims are still easy to see and manage from FTB Chunks' map.
13. Client comfort and performance defaults: Camera Overhaul ships **off** (its camera roll and sway cause motion sickness while flying; players can turn it on), and Distant Horizons ships at 128 chunks, 4 threads and `PRE_EXISTING_ONLY` (no LOD worldgen; its `FEATURES` default causes 48 s freezes and an out-of-memory crash in singleplayer). Both files are `preserve = true`, so player changes survive updates. Check that both feel right.
14. Pokémon world with a client: craft Alph Stone and a Johto Bell (`/give` a Bell Fragment), build and light a portal, and travel both ways. The starter screen should open on first arrival and never on join. The party HUD should hide in the Overworld and show in the Pokémon world. Wild Pokémon should spawn only in the Pokémon world (stand around in an Overworld plains for a few minutes). A wandering RCT trainer and a gym battle should work, and a trainer summoned in the Overworld should still battle.

## Decisions

- Recipe viewer: EMI only.
- Grave mod: Corail Tombstone.
- Dynamic lighting: LambDynamicLights.
- Big tech mod: Oritech.
- Food variety: Spice of Life: Onion.
- Portal method for the Pokémon world: BBL Portals (KubeJS), Alph Stone frame + Johto Bell.
- Neo Vitae: in.
- Remaining choices are settled during testing (see Test plan).

## Build phases

The build uses the mod tracker (`docs/strata-mod-tracker.xlsx`) as the input list.

1. Set up the pack as a git repo with packwiz, pulling mods from CurseForge and Modrinth.
2. Verify every "verify" mod in the tracker against the CurseForge/Modrinth APIs for a 1.21.1 NeoForge build; packwiz fails loudly on any mod without one.
3. Resolve open decisions as mods are added.
4. Write the KubeJS scripts and configs from the to-do list.
5. Stand up a test server on treehouse (itzg/minecraft-server) with backups and the Discord bridge (Simple Discord Link); pregenerate with Chunky.
6. Run the test plan, then write FTB Quests chapters.
7. Build the Pokémon world datapack and portal once the base pack is stable.
