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

**Teleporting and flight:** the current rules are in CLAUDE.md ("Limited teleport", "No easy creative flight"), and the item-by-item rulings are in `docs/gate-map.md` section 5. In short: one `/home` per player with a 10-second cooldown (`kubejs/server_scripts/strata_home.js`); no `/back`, `/rtp` or `/tpa`; Waystones cost XP by distance (more across dimensions); earned teleporting is fine; flight is fine when it's hard to get or costs something to run (Darin's Oct 25 review passed every current source). Removed Oct 26: Iron's Recall, Draconic dislocators, Helium Flamingo, Wind Staff, Linking Book.

**Wireless: no tiers** (Darin, Oct 25; confirmed Oct 26). Flux Networks, Mekanism entangloporters, AE2 wireless and Mighty Mail work across dimensions as the mods ship them; AE2's Quantum Network Bridge keeps its own recipe cost. Power still has a ladder (CLAUDE.md).

## Progression and difficulty

Challenge is there for anyone who wants it, but the world stays friendly for builders and newer players.

- **Dropped (Oct 26): no server-wide difficulty stages.** Darin: the group plays at very different paces (one player is already in the Nether while others have barely started), so a world that hardens on the first Nether visit or Dragon kill would punish the newer players. Difficulty stays per player (Apotheosis World Tiers, which each player picks; dimensions like the Hollow). Original plan kept below for reference.
- ~~**Staged difficulty, like MC Eternal:** our own KubeJS script (phase 2) — Normal at start, Expert after the first Nether visit, Master after the Ender Dragon, as a server-wide stage. Replaces Majrusz's Progressive Difficulty Continued, which was dropped on Oct 24, 2026: it can't be auto-downloaded (CurseForge API opt-out), it starts Expert on entering *any* modded dimension, and it brings extra systems (bleeding, Undead Army, Enderium tier). See docs/difficulty-options.md.~~
- **Avoid MC Eternal 2's stacking problem:** bosses keep their designed stats; the progressive mod is the only thing scaling regular mobs. Keep the Nether step modest so newer players aren't overwhelmed; put the bigger jumps in dangerous dimensions.
- **Apotheosis:** randomized gear, gems, elite mobs. Configure elites to be rare near spawn and more common in the Nether, End and far out.
- **Boss gating:** quests and KubeJS recipes require boss drops for late tiers (for example Cataclysm drops for top Mekanism/AE2 parts and cross-dimension wireless).
- **Other scalers to watch:** Vampirism scales its own mobs to nearby player level — include it in the Nether-jump play test.
- **Safety nets:** Corail Tombstone (replaced GraveStone Mod, Oct 27) so death doesn't scatter items; Redomesticate (Domestication Innovation fork) so pets aren't lost for good.
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
- Inside bases, Mekanism universal cables; Flux Networks for wireless power (no wireless tiers).

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
  1. **Seed chosen (Oct 25, final):** `-1678324137078475659`, spawn at -358, 77, -3260 beside the tavern of an Integrated Villages Tavern village (see docs/seed-scouting.md). The Oct 24 seed `1121906793898615393` is retired. Pregeneration is centered at the spawn: `tools/start_pregen.sh` boots container `strata-world` with the world in `server/` (git- and packwiz-ignored), sets the spawn and runs Chunky (Overworld, circle, 5,000-block radius). Started Oct 25 on Darin's desktop. The Overworld was finished with **C2ME as a pregen-only tool** (~50 vs ~11 chunks/s; checked clean against a normal run, see docs/worldgen-profile.md); the Nether (1,250 radius) was done without it, and C2ME is removed before the End/Aether/Pokémon world pregens and before play. **Done Oct 25:** Overworld 5,000 (circle, 1 h 03 with C2ME after one out-of-memory crash at 29%: C2ME parallelism lowered to 6 and `lowMemoryMode` on in the server's `config/c2me.toml`), then without C2ME (`tools/pregen_dimensions.sh`, two dimensions at a time): Nether 1,250 around -45/-408, End 2,000 around 0/0, Pokémon world 2,000, Twilight Forest 1,500 and Aether 1,000 around spawn. World 5.6 GB. Lessons: long runs build up a scheduler/heap backlog (rate drops to 1–2 chunks/s); a clean restart clears it and Chunky resumes. `/sable paused true` during pregen (Sable's physics thread competes for the main thread); **`/sable paused` with no argument toggles it**, so always pass true/false; it was set back to false. **Aether trap:** the Aether's `DungeonBlacklistFilter` placement filter calls `Level.getChunk` from inside worldgen and deadlocked the pregen around chunk -73,-281 (≈ block -1168,-4496); the Aether is therefore pregenerated to 1,000 blocks (concentric), and that spot generates on demand. Watch for a stall if someone flies there. Still open before players join: Nether/End/Aether/Pokémon world pregeneration sizes.
  2. **Finish every worldgen-affecting change before pregenerating.** Pregenerated chunks never pick up later worldgen changes. That includes Cobblemon worldgen moving to the Pokémon world (apricorns, evolution-stone ores, Integrated Cobblemon gyms and Pokécenters), the Artifacts/IDAS chest fixes, and any ore or structure configs.
  3. **Pregenerate on Darin's desktop** (i5-13600K, much faster than treehouse), **5,000-block radius** in the Overworld, plus the Nether, End and Aether at sizes to decide. Use the same settings as the server, then copy the world to treehouse.
  4. **Server settings:** 12 GB, `-XX:+UseZGC -XX:+ZGenerational`, `sync-chunk-writes=false` (itzg: `MEMORY=12G`, `JVM_XX_OPTS`, `SYNC_CHUNK_WRITES=false`). Chunky keeps expanding the border in the background after launch if needed.

## Pokémon world

**Player-facing name: the Kakuto Region** (Darin, Oct 26; *kaku* = square, like the blocks). The title banner, quest book and portal docs use it; IDs stay `pokeworld:*` so built worlds keep working. Portal look: "Unown Drift" texture, bell/hum/wind/Unown sounds and glyph particles (`startup_scripts/portal_ambience.js`).

Cobblemon lives in its own "vanilla + Cobblemon" dimension, `pokeworld:pokeworld`, reached by a portal. Players can bring their Pokémon anywhere, and riding (flying Pokémon use stamina) is allowed in every dimension. Built Oct 24, 2026 (branch `claude/pokemon-world-1d29ea`). Everything ships through KubeJS (`kubejs/data`, `kubejs/*_scripts`) and `config/`. Most of the datapack is generated by `tools/build_pokeworld.py`. Re-run it after a Cobblemon or structure-mod update (inputs are listed at the top of the script).

1. **Dimension:** `pokeworld:pokeworld` uses its own dimension type, noise settings, density functions and noises, all deep copies of vanilla 1.21.1. Tectonic overrides `minecraft:overworld/*` density functions and noises, so referencing vanilla IDs would have pulled Tectonic in. The 53 vanilla Overworld biomes are copied as `pokeworld:<name>` and placed by an explicit multi-noise list (vanilla's own parameters). TerraBlender/Regions Unexplored only inject into `minecraft:overworld`. Streams Reflowing attaches to every noise dimension, so `config/streamsreflowing.properties` sets `streamBiomeBlacklist=pokeworld:*`: no streams or lakes start in Pokémon-world biomes, and Overworld streams are unchanged. It applies to newly generated land only, so it must ship before pregeneration. The copies are in no vanilla or `c:` biome tags, so Overworld feature, ore and structure mods don't reach them. Exceptions found by the script's leak check: IE mineral veins (virtual, harmless) and a few Quark/vanilla mob spawns added by code.
2. **Wild spawns only in the Pokémon world:** `kubejs/server_scripts/pokeworld_spawns.js` fills Cobblemon's `worldSpawningBlocklist` with every loaded dimension except `pokeworld:pokeworld` at server start, so dimensions added later are covered too. The first version used a Cobblemon spawn rule (`location` component), but in Cobblemon 1.8.2 that component fails before evaluating its expression and blocked spawns everywhere (found in Darin's client test, Oct 24). The blocklist only affects the natural spawner. Sent-out, NPC-trainer and battle Pokémon don't go through it. The pokeworld biomes are added to all 155 of Cobblemon's own biome tags, so spawn conditions, regional evolutions and Vivillon patterns work there. Radical Cobblemon Trainers' wandering trainers spawn only there too (`dimensionWhitelist` in `config/rctmod-server.toml`). That list doesn't affect trainers placed by gym structures.
3. **Cobblemon worldgen moved there:** Cobblemon adds about 96 placed features from code (apricorns, mints, saccharine trees and medicinal leeks in *every* biome; berry groves, type gems, big roots, treasure hoards and lost ruins in `#minecraft:is_overworld`; evolution-stone ores, fossils and habitats by Cobblemon tags). Tags can't move them, so the originals are overridden to `count 0` everywhere, and `pokeworld:cobblemon/<path>` copies are listed directly in the matching pokeworld biomes (88 copies; the Nether/End-only ones have no pokeworld biome). The list is read from Cobblemon's bytecode (`tools/pokeworld/parse_cobblemon_features.py` → `cobblemon_injected.json`).
4. **Structures:** the structures of Cobblemon, Integrated Cobblemon (gyms + Pokécenters), CobbleStructures, Cobblemon: Simple Pokecenters and Cobblemon Extra Structures are overridden to `#pokeworld:has_structure/...` tags (the pokeworld copies of their original biomes). Integrated Cobblemon's fire gym (Nether) and psychic/dragon gyms (End) stay in the Nether and End (Darin, Oct 24). Vanilla Overworld structures are copied as `pokeworld:<name>` (villages, outposts, temples, monuments, mansions, shipwrecks, ruins, trial chambers, ancient cities, mineshafts; no stronghold). The copies are added to the vanilla structure tags (`#minecraft:village` etc.). The 26 Cobblemon spawn files that name a vanilla structure directly (e.g. Qwilfish avoiding `minecraft:monument`) are overridden with the `pokeworld:` copy added next to it (generated; re-run the script after a Cobblemon update).
   - Villages: Cobblemon adds Pokécenters, berry farms and habitats to the vanilla village house pools, both in a data file and in code at server start. `kubejs/startup_scripts/pokeworld_village_pools.js` strips every `cobblemon:` piece from the five `minecraft:village/*/houses` pools (lowest priority on ServerAboutToStart, before any chunk generates). Pokémon world villages use jigsaw pool aliases to a copy with Cobblemon's buildings (`pokeworld:village/*/houses`). Other mods' village additions (Waystones, Bountiful, Farmer's Delight, ...) stay in Overworld villages. CobbleDollars (2.0.0-beta-6.1) checked: its Cobble Merchant village code never runs, its `minecraft:<type>/villagers.json` copies sit at a path nothing references, and the jar ships no merchant template. So it adds nothing to villages anywhere; Cobble Merchants only appear when a villager takes their job block. The startup script filters `cobbledollars:` pieces from the villager pools too, in case a later version turns that on.
5. **Starter:** `config/cobblemon/main.json` sets `exportStarterConfig: true` so Cobblemon reads `config/cobblemon/starters.json`, which has `allowStarterOnJoin: false` and Cobblemon's own default starter list with `useConfigStarters: true` (with `false`, Cobblemon 1.8.2 opens an empty starter screen, because no datapack starters exist; found in the Oct 25 in-game test). That leaves no prompt on join, and the starter is locked for new players. `kubejs/server_scripts/pokeworld_starter.js` runs `/openstarterscreen <player>` when a player without a starter is in the Pokémon world. It runs at most once per login, so closing the screen without picking brings it back next time; Cobblemon's own "starter selected" flag stops it for good. Verified in game on Oct 25: the categories show, and picking Charmander works.
6. **Party HUD:** `kubejs/client_scripts/pokeworld_party_hud.js` sets Cobblemon's Hide Party toggle (`HidePartyBinding.setShouldHide`) on every dimension change: hidden outside the Pokémon world, shown inside. The Hide Party key still works in between.
7. **Portal:** BBL Portals (MIT; standalone fork of Custom Portal API + PortalJS with their Sodium/flint-and-steel fixes), set up in `kubejs/startup_scripts/pokeworld_portal.js`. The portal list there is easy to copy for the horror dimension. Darin's design (Oct 24): no pre-built portal; players make their own. A nether-portal-shaped frame of **Alph Stone** (block id `pokeworld:poke_portal_frame`; ancient carved sandstone after the Ruins of Alph, Oct 26; 8 per craft from 8 chiseled sandstone around a diamond) is lit with the **Johto Bell**. The frame blocks connect into one carved border through Fusion (already in the pack for Rechiseled, `pieced` layout) and pick a random variant per block: every block carved with Unown (each with its eye): one big (O, A, !) or two small (I + U, O + A), cracked and/or mossy. The portal glows Ultra Wormhole cyan. The Bell is crafted from a vanilla Bell, 3 gold ingots and a **Bell Fragment**, and is reusable (BBL Portals never uses up the igniter; the fragment's rarity is the gate). Bell Fragments are rare chest loot in Overworld structures, via NeoForge global loot modifiers in `kubejs/data/pokeworld/loot_modifiers`. Chances per chest; Lootr rolls each chest once per player: dungeon 8%, mineshaft 3%, desert pyramid 6%, jungle temple 8%, ancient city 12%, woodland mansion 20%, trial vault 6% / ominous vault 20%, YUNG's dungeons 5–8%, YUNG's desert tomb 8%, YUNG's jungle treasure 10%. The link stays 1:1 X/Z, and the portal on the other side leads back to the Overworld. World Portal (datapack-defined, server-only) was tried first and crashes the server at boot: its `EntityLMixin` can't inject into `Entity.getRelativePortalPosition`, which another mod already changes.

**Verified on a Docker test server (Oct 24, seed 1121906793898615393, spawn 24031 / −26565):**
- `/locate structure` for all 105 overridden structures from the spawn: none found in the Overworld; 103 found in the Pokémon world. The two cave ruins (crumbling arch, rooted arch) come from feature copies, not structure sets.
- Chunky, 600-block radius around spawn in both dimensions, then a region scan (`tools/pokeworld/scan_regions.py`): Overworld 6,267 chunks with **0** `cobblemon:` blocks, including two villages. Pokémon world 8,417 chunks, 6,460 with Cobblemon blocks: evolution-stone ores, apricorn trees, big roots, type gems, berries, revival herbs, Pokécenters (healing machines, PCs).
- Pokémon-world villages get Cobblemon's Pokécenters through the pool alias. Five placed villages all had healing machines. The KubeJS hook logged removing 1,730 Cobblemon pool entries (repeated by weight) from the Overworld village pools.
- A command-spawned Pikachu and a summoned RCT trainer (Youngster Joey) work in the Overworld.
- Portal (second boot, Oct 24): BBL Portals registered the Poké Portal Frame as its frame block. Both recipes loaded with 0 failures. 100 woodland-mansion loot rolls gave 18 Bell Fragments (20% expected).
- Mobs in the other direction: no Pokémon reach other dimensions. The spawn rule blocks the Cobblemon spawner outside `pokeworld:pokeworld`, and nothing else spawns wild Pokémon. Only Pokémon spawn there (Darin, Oct 26: "I ONLY want pokemon in that dimension"): In Control! allows natural spawns from Cobblemon and Radical Cobblemon Trainers in `pokeworld:pokeworld` and denies everything else (`config/incontrol/spawn.json`). Village villagers placed with structures stay.
- After merging waves 4 and 5 (396 mods, Oct 25): the leak check found nothing new. `/locate` for all 890 non-Cobblemon structures in every mod, Ice and Fire included, found none in the Pokémon world (4 are disabled or replaced by IDAS). Wild spawns are blocked in 24 dimensions. Async Locator (wave 4) makes `/locate` asynchronous: over RCON the reply is empty and the result is in the server log.
- In-game test (Oct 25, computer-use session with Darin's client): the portal, the HUD hiding and showing, wild spawns (Pokémon world 49 in 2 min, Overworld 0) and an Overworld trainer battle all pass. The starter screen opened empty at first; with the default list it shows every category and a starter can be picked (retest passed).
- Not verifiable without a player client (test 15 below): natural spawns, the starter screen, the party HUD, the portal, and a trainer battle.

Later option: the Cobblemon Kanto map (FireRed/LeafGreen recreation, 1.21.1) as a second portal. It needs testing on NeoForge, claim protection, and a license check.

## Horror dimension: The Hollow (built Oct 26)
Built as **The Hollow** (`strata:hollow`); the current design and what was built are in `docs/hollow-design.md` (mod research: `docs/hollow-mod-research.md`). The notes below are the original Oct 24 proposal.

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

- [x] New Age wiring removed (Oct 26, `kubejs/server_scripts/strata_power.js`): the Electrical Connector recipe (and the Street Light, which needs one) are gone; wires stay craftable because copper wire goes into New Age's copper circuit. New Age generators hand FE to C&A and IE through their carbon brushes.
- [x] Crafts & Additions alternator lowered to 240 FE at max RPM (`config/createaddition-common.toml`, Oct 26), half of New Age's.
- [x] ~~Gate wireless~~: dropped (Darin, Oct 25 and again Oct 26): no wireless tiers; see CLAUDE.md
- [ ] Gate top-tier Mekanism / AE2 parts behind boss drops: proposal in `docs/gate-map.md` (T1–T10), waiting for Darin.
- [x] Waystones: distance XP cost is the mod default (0.01 XP per block, 27 levels across dimensions); no loot table contains warp scrolls or stones (audit Oct 26). Warp scrolls and warp plates now pay the same XP as waystones (Darin, Oct 26; `config/waystones-common.toml`).
- [x] Inventory Pets: flight pets settled (must be fed; CLAUDE.md). House and End Portal pets disabled (Darin, Oct 26; `config/inventorypets-common.toml`); Nether Portal and Enderman pets stay; the Nether Portal pet only works after you've entered the Nether yourself (Darin, Oct 27; `strata_pets.js`). Pets are found, not crafted (Darin, Oct 27): every pet recipe and the Petrifier are removed (`strata_pets.js`); pets drop from structure chests in three tiers (`tools/build_pet_loot.py`: common in dungeons/temples, rare in strongholds/mansions/fortresses, legendary in End cities/ancient cities/bastion treasure). Strong pets stay but are weaker: Juggernaut and Illuminati cooldowns 10 min, Pac-Man's damage bonus grows 1 per kill instead of 3, Pingot finds ore but no longer extracts it, and costlier upkeep food for Juggernaut, Illuminati, Wither, Sun, Black Hole, Loot, Pixie, Silverfish, Quantum Crystal Monster, Pac-Man and Anvil.
- [x] Excessive Utilities flight: settled by the Oct 25 flight review (Angel Ring needs Grid Power).
- [x] Player commands: `/home` + `/sethome` only (`strata_home.js`, 9a6507f); no Essentials-type mod.
- [x] ~~Progressive difficulty KubeJS script~~ (dropped Oct 26, see Progression and difficulty): server-wide stage (Normal → Expert on the first Nether entry → Master on the first Dragon kill), stored in server persistent data. On spawn, scale health/damage/armor of regular hostile mobs by stage × per-dimension multiplier (modest Nether step; bigger in the End, Twilight Forest, Deeper and Darker, Cataclysm areas; none in the Pokémon world). Skip bosses (`c:bosses` tag + an explicit list: Cataclysm, Mowzie's, BoMD, Twilight bosses, Wither, Dragon, Warden). Op commands to view/set the stage. Tested in test 6
- [x] Apotheosis elites and invaders rare near spawn (Oct 26, `kubejs/server_scripts/strata_elites.js`): 10% kept at world spawn, all by 2,000 blocks; Overworld only.
- [x] Create Big Cannons: `NO_EXPLOSIVE_DAMAGE` (Darin, Oct 26); FTB Chunks claims already block explosions (default).
- [x] Vampirism: PvP between factions only (Darin, Oct 26; `config/vampirism-server.toml`), on top of the team protection.
- [x] Almost Unified: default priority (minecraft > kubejs > create > IE > mekanism) shipped in `config/almostunified/` (Darin, Oct 26).
- [x] CobblemonOptimizer 5.0.0 added, server-only (Oct 26; loads clean, TPS threshold 18).
- [x] Ice and Fire dragon riding: settled by the Oct 25 flight review (taming a dragon is real effort). Optional: `flightStamina` is still off.
- [x] Create Stuff & Additions jetpacks: settled (they burn fuel). Building Gadgets 2 copy-paste: defaults kept (50 FE per block, about 20k blocks per charge, and it uses your own blocks).
- [x] ChoiceTheorem's Overhauled Village and Aquamirae configs: moot; the world was pregenerated and went live Oct 25 (changes would only reach chunks past 5,000 blocks).
- [ ] Wave 4 checks. Done or settled: End Remastered eyes (in-game pass Oct 25), Ars Elemental Air focus and Ars Additions warp (mana, earned), TorchMaster (default 64, in the quest book), difficulty skip list (moot), Lootr (39c5841). Horseman horn capped at 128 blocks (`config/horseman-server.toml`); Mega Torches can't be placed in the Hollow (`hollow_rules.js`); Legendary Monsters' only natural Overworld spawn, the desert Bomber, cut from weight 75 to 10 (`kubejs/data/legendary_monsters/`) (all Oct 26). *Open:* Extended Crafting endgame (gate map T10). Rarity pass for new structures: low value now the world is pregenerated.
- [ ] Wave 5 checks. Done or settled: Ad Astra oxygen and launch rules (defaults), Create Jetpack air (ongoing cost), In Control! for the Hollow (00757be), LootJS strip script (`strata_removed_items.js`). *Open:* Ad Astra rocket gates (gate map T7/T8), Ad Astra Overworld ores (check), Structurify spacing (probably drop: world pregenerated), Immersive Optimization test with farms, contraptions and Cobblemon (work).
- [ ] In-game test notes (Oct 25): Lootr confirmed; Seven Seas junk in icebergs is cosmetic (ignore); client heap 79–94% of 16 GB (watch). Pregenerated: Overworld, Nether, End, Aether, Kakuto, Twilight (d91b9e3). *Open, work:* pregenerate the Hollow, the Abyssal Plain and Crystal Chronicles' dimension; log errors checked Oct 26: `byg:emeraldite_shards` / `create:crushed_gold_ore` come from IDAS sunken ship and ancient mine chests that name items from mods we don't have (those slots stay empty, harmless); Ice and Fire attachments and Blueprint's repaletter are only DEBUG lines on the live server; Grim & Bleak's torch and withered-stick recipes fail to load (its own bad recipes, harmless). *Open:* Immersive Optimization test in play. Report: side-session notes `main-ingame-test-results.md`.
- [ ] Wave 6 checks. Done or settled: Apocalyptic Bosses loot and density (8fb8e2a), skip list (moot), Oritech flight (research cost; gate map §5), WaterFrames (URL whitelist is image and video hosts only); Oritech over Modern Industrialization, Cobblemon Kanto and Wings of Fire left out. *Open:* Apocalyptic ultimate ingot (gate map G6), Draconic tiers (T9), Oritech flight dragon heart (G5) and an in-game check that the exosuit jetpack drains power, Crystal Chronicles: pregenerate and check its End sub-biome against Nullscape (work).
- [x] Happy Ghast: settled by the Oct 25 flight review. Optional: a harness cost if it ever feels cheap.
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
15. Pokémon world with a client: craft Alph Stone and a Johto Bell (`/give` a Bell Fragment), build and light a portal, and travel both ways. The starter screen should open on first arrival and never on join. The party HUD should hide in the Overworld and show in the Pokémon world. Wild Pokémon should spawn only in the Pokémon world (stand around in an Overworld plains for a few minutes). A wandering RCT trainer and a gym battle should work, and a trainer summoned in the Overworld should still battle.

**Open questions**

- Decided: EMI as the recipe viewer (JEI installed alongside for its plugins), Terralith out; gravestone = GraveStone Mod (replaced by Corail Tombstone, Oct 27), dynamic lighting = LambDynamicLights.
- ~~Modern Industrialization or Oritech?~~ Oritech (wave 6, Oct 25).
- ~~Spice of Life or Diet?~~ Spice of Life: Onion.
- Remaining choices are settled during testing (below).
- ~~Which portal method for the Pokémon world?~~ BBL Portals (KubeJS): Alph Stone frame + Johto Bell; World Portal crashes.
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
