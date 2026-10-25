# Strata — mod gap analysis (Oct 24, 2026)

What the current list (~310 mods in `mods/`) covers well, where it is thin, and mods that would fill the gaps. Darin picks; nothing here has been added.

**How builds were checked (Oct 24, 2026):** every suggestion was checked against the Modrinth API (`/v2/project/<slug>/version?game_versions=["1.21.1"]&loaders=["neoforge"]`). CurseForge-only mods were added to a throwaway packwiz pack outside the repo; `packwiz cf export` raised no "downloads disabled" warning for any of them. Version numbers are the newest 1.21.1 NeoForge build at check time.

**Worldgen key** (the seed is chosen last, after all worldgen changes; pregeneration comes after that):
- **Biomes (OW)**: adds Overworld biomes, reshapes the world. None of the picks below do this.
- **Structures**: adds structures; decide before pregeneration; check Lootr (vanilla chests) and rarity, like the Inventory Pets pass.
- **Other-dim worldgen**: biomes/structures in the Nether, End or Aether only; decide before pregenerating that dimension.
- **None**: no worldgen.

Not re-suggested (in the pack or already decided against): MCA Reborn, Small Ships, Immersive Aircraft, The Bumblezone, Alex's Caves, Epic Fight, C2ME, Moonrise, Terralith, Dynamic Trees, MineColonies, Majrusz's, T.O Magic 'n Extras (= Traveloptics), Frieren Flight, FTB Essentials (Cut), Born in Chaos and Mutant Monsters (horror dimension).

## Decision (Oct 24, 2026): approved list

Darin approved the recommendations, with these choices: MVS (not Repurposed Structures), Simply Swords only (no Spartan Weaponry, Silent Gear or Immersive Armors), no sixth magic mod, Let's Do Vinery only (not Farm & Charm). Defaults where the doc said "one or the other": Moog's Nether Structures over Formations Nether, Croptopia over Expanded Delight.

**Add (Keep):** (added to the pack Oct 24, wave 4)
- Overworld: Ember's Floating Islands, Sky Whale Ship, MVS – Moog's Voyager Structures, Kobolds, Hopo Better Ruined Portals
- Oceans: When Dungeons Arise: Seven Seas, Integrated Seven Seas, Upgrade Aquatic (+ Blueprint), Tidal Towns, Ocean's Delight, Illager Warship, Illager War Trireme
- Nether: MNS – Moog's Nether Structures, Nether Depths Upgrade, My Nether's Delight, Eternal Nether (check Incendium overlap on first boot)
- End: MES – Moog's End Structures, End Remastered
- Aether: Aether Villages, Aether Addon: Treasure Reforging
- Travel: Horseman (turn off any long-range horse summon), Horse Expert, Xaero's Minimap & World Map – Waystones Compatibility
- Combat / late game: Simply Swords, Extended Crafting, Legendary Monsters (Maybe → Keep; tune Overworld spawns)
- Tech: Create Ore Excavation
- Magic: Ars Elemental (CurseForge), Ars Additions, Theurgy
- Food: Croptopia (CurseForge, + EpheroLib), Brewin' and Chewin', [Let's Do] Vinery
- Building: Amendments
- QoL: Enchantment Descriptions, TorchMaster, Crafting Tweaks, Jade Addons, Crash Assistant (client)
- Social: Ping Wheel, Ping to Map: Xaero's Minimap (client)
- Server: Neruina, Packet Fixer
- Performance: Structure Layout Optimizer, Async Locator Refined, FastSuite, Dynamic FPS (client), More Culling (client), Sodium Extra (client)

**Hold for a test first:** Unusual End (End biomes; boot with Nullscape and look at the End before keeping it). Draconic Evolution (beta; only if the Mekanism/AE2 endgame feels short).

**Not added:** Repurposed Structures, Formations Nether, Enderscape, Expanded Delight, Farm & Charm, Spartan Weaponry, Silent Gear, Immersive Armors, Malum, Eidolon, Forbidden & Arcanus, Ars Technica, Emotecraft (Quark has emotes), LuckPerms and FTB Ranks (no command mod needs them). Sparse Structures stays on standby in case structure density is too high.

## Gaps at a glance

| Area | Covered by | Verdict |
| --- | --- | --- |
| Overworld structures | YUNG's suite, Towns and Towers, When Dungeons Arise, Dungeons and Taverns, IDAS, Explorify, Integrated Villages, ChoiceTheorem's villages, Cataclysm, Bosses'Rise, Qliphoth | **Well covered** on land. Thin: **sky structures** (the "Fly" in "Build. Fly. Explore." has little to fly *to*), small ruins between the big set pieces |
| Oceans | Aquamirae, YUNG's monuments, Aquaculture 2, Tide 2, Alex's Mobs | **Thin.** Few ocean structures, little underwater life beyond vanilla, no ocean food add-on |
| Nether | Incendium, YUNG's fortresses, Cataclysm Nether bosses | **Thin** for a dimension that is the Expert-stage gate: few structures, nothing in the lava seas, no Nether food |
| End | Nullscape, YUNG's End Island, End's Delight, Cataclysm End bosses | **Thin**: big terrain, little in it. End cities are the only common structure |
| Aether | Aether, Deep Aether, Aether's Delight, Inventory Pets sky dungeons | **OK.** Aether Redux and Lost Content have no 1.21.1 NeoForge build; only small add-ons available |
| Early-game travel | Horses, boats, Waystones (XP cost), Create trains later | **Slightly thin** until trains/airships; horses could matter more |
| Combat and gear variety | Apotheosis, Better Combat, Apothic Combat, Combat Roll, Mekanism Tools, Artifacts, Relics, Ice and Fire gear, Iron's armor | **Thin on weapon types**: Better Combat has few weapon shapes to animate |
| Bosses and late game | Cataclysm, Mowzie's, BoMD, Bosses'Rise, Qliphoth, Ice and Fire, Twilight, Aquamirae | Bosses **well covered**. Thin: a **post-boss "big build" goal** for the tech side |
| Tech | Create + many add-ons, Mekanism, AE2, IE, IF, PneumaticCraft, Powah, Extreme Reactors, ID, LaserIO | **Very well covered.** Only open item: MI vs Oritech (still Maybe) |
| Magic | Ars + 7 add-ons/bridges, Iron's, Occultism, Neo Vitae, Vampirism | **Well covered.** Ars has no elemental/school add-on; one more distinct magic style is optional |
| Farming and food | Farmer's Delight + 7 add-ons, Slice & Dice, Central Kitchen, Serene Seasons, Spice of Life | Covered, but **crop variety is low** for Spice of Life (only vanilla + FD crops); no drinks/brewing |
| Building and decoration | Macaw's suite, Handcrafted, Chipped, Rechiseled, FramedBlocks, Supplementaries, Another Furniture, Create Deco, building gadgets | **Fully covered.** Don't add more |
| QoL | EMI/JEI, Jade, AppleSkin, IPN, Ultimine, FallingTree, Polymorph, Carry On, Xaero's, Sophisticated, Locked In Slots | Mostly covered. Small gaps: enchantment descriptions (Apotheosis has many), crafting-grid buttons, base mob-proofing, crash help |
| Multiplayer / social | Voice Chat, WATUT, Mighty Mail, FTB Teams/Chunks, Numismatics, Trading Floor, PlayerRevive, Discord link | Covered. Small gap: **pinging** a spot for friends |
| Server admin | Simple Backups, spark, Chunky, Simple Discord Link, Let Me Despawn | **Gaps**: crash protection for the world, permissions, big-packet fixes |
| Performance | Sodium, Lithium, ModernFix, FerriteCore, ImmediatelyFast, Entity Culling, BadOptimizations, AllTheLeaks, Noisium, Clumps | Good base. **Gaps for a structure-heavy pack**: jigsaw structure generation (pregen time), async structure locating (Explorer's Compass, maps, dolphins) |

## Recommendations by area

### Overworld exploration and structures

| Mod | Source / build | What it adds | Rules / worldgen |
| --- | --- | --- | --- |
| **Ember's Floating Islands** | Modrinth `embers-floating-islands` 1.5.3 (release, Aug 2026); server-only | Structures floating in the sky | Structures. Best fit for the airship theme: loot you need a ship or elytra to reach |
| **Sky Whale Ship** | Modrinth `sky-whale-ship` 1.0.3 (release, Nov 2025; 1 build, small) | A whale-ship structure in the sky | Structures. Small one-off; low maintenance risk, low update activity |
| **MVS – Moog's Voyager Structures** | Modrinth `moogs-voyager-structures` 5.1.3 (release, Sep 2026); server-only | 130+ vanilla-style structures (ruins, towers, camps, ocean pieces) to fill gaps between big set pieces | Structures. Many; set spacing with Sparse Structures or its config |
| **Repurposed Structures** | Modrinth `repurposed-structures-forge` 7.5.22 (release, Aug 2026); server-only | Biome variants of vanilla structures (jungle fortress, Nether/End variants, more villages, wells, shipwrecks) | Structures in all three dimensions. Overlaps a bit with YUNG's and Integrated Villages; disable its village/mineshaft/stronghold variants in config so YUNG's stays in charge |
| Kobolds | Modrinth `kobolds` 4.0.2 (release, Oct 2026) | Small friendly lizard villagers with dens and trades | Structures + mobs. "Cute" content for the newer players |
| Hopo Better Ruined Portals | Modrinth 1.4.4b (release, Apr 2025) | Nicer ruined portals | Structures (replaces vanilla). Optional |

Tool if structure density gets out of hand: **Sparse Structures** (`sparsestructures` 3.0, server-only) spreads all structures out by one multiplier.

### Oceans

| Mod | Source / build | What it adds | Rules / worldgen |
| --- | --- | --- | --- |
| **When Dungeons Arise: Seven Seas** | Modrinth 1.0.4 (release, Oct 2025); server-only | Large ships and sea fortresses, same author as WDA (already in) | Structures. Optional **Integrated Seven Seas** (1.1.0) adds puzzles like Integrated Cataclysm/Villages, 5 deps |
| **Upgrade Aquatic** | Modrinth 7.0.2 (release, Sep 2026); needs Blueprint (8.2.0) | Ocean life: new fish, jellyfish, thrashers, coral/kelp/driftwood blocks, beachgrass | Features + mobs. Not seen to add biomes in its description; confirm in the seed-scouting test |
| **Tidal Towns** | Modrinth 2.0 (release, Sep 2026) | Floating driftwood villages on the ocean | Structures |
| **Ocean's Delight** | Modrinth 1.0.4 (release, Apr 2026) | Farmer's Delight recipes for ocean foods | None. Gives fishers (Tide/Aquaculture) a food use |
| Illager Warship / Illager War Trireme | Modrinth 1.0.1 each (release, Aug 2025) | One giant illager warship structure (oceans); a trireme in warm oceans | Structures. Both are static ocean structures, not flying |

### Nether (Expert-stage gate)

| Mod | Source / build | What it adds | Rules / worldgen |
| --- | --- | --- | --- |
| **MNS – Moog's Nether Structures** | Modrinth 3.1.1 (release, Sep 2026); server-only | Many vanilla-style Nether structures | Other-dim structures. Works with Incendium (different structures, no biomes) |
| **Nether Depths Upgrade** | Modrinth 3.3 (release, Sep 2026) | Lava fish, lava fishing, plants in the lava seas | Other-dim features. Pairs with Tide |
| **My Nether's Delight** | Modrinth 1.10.4.1 (release, Sep 2026) | Farmer's Delight Nether crops and food | Light Nether features. Vampire players benefit (Nether food) — check vs Vampire's Delight in test 7 |
| Formations Nether | Modrinth 1.0.5b (release, Sep 2026) | Small Nether structures | Other-dim structures. Alternative to MNS, not both |
| Eternal Nether | Modrinth 21.1.3 (release, Jul 2025) | Bygone Nether continuation: new mobs and structures | Other-dim structures + mobs. New mobs fall under the difficulty script; check Incendium overlap first. Lower priority |

### End

| Mod | Source / build | What it adds | Rules / worldgen |
| --- | --- | --- | --- |
| **MES – Moog's End Structures** | Modrinth 2.1.1 (release, Sep 2026); server-only | Vanilla-style structures across the outer End | Other-dim structures. No biomes, so it is safe with Nullscape |
| **End Remastered** | Modrinth 6.3.0 (release, Jul 2026) | 16 special Eyes found in structures/bosses to open the End portal | Structures (eye shrines). A real **exploration goal before the Dragon**; can be tied to our boss gating. Makes the Master stage later; check it fits the quest pacing |
| Unusual End | Modrinth 2.3.1b (release, Sep 2026) | New End biomes, mobs, blocks | Other-dim **biomes**. Not documented as Nullscape-compatible; test together before deciding |
| Enderscape | Modrinth 1.0.9 (**beta**, Aug 2025) | Full End overhaul with biomes and mobs | Other-dim biomes. Beta and likely to clash with Nullscape. Not recommended |

### The Aether

The big Aether add-ons (Aether Redux, Lost Content, Genesis) have **no 1.21.1 NeoForge build**. Available:

| Mod | Source / build | What it adds | Rules / worldgen |
| --- | --- | --- | --- |
| **Aether Villages** | Modrinth 1.0.8 (release, Nov 2024; 1 build) | Temples and villages in the Aether | Other-dim structures. Old single build; test it with Deep Aether |
| Aether Addon: Treasure Reforging | Modrinth 1.0.1 (release, Dec 2024) | Melt dungeon gear down and reforge it | None. Small, official Aether team add-on |

### Early-game travel

| Mod | Source / build | What it adds | Rules |
| --- | --- | --- | --- |
| **Horseman** | Modrinth 1.5.13 (release, Aug 2026) | Better horses: smoother riding, faster hitching, QoL | Fits "travel costs something". Check its horse-summon/whistle feature and turn it off if it calls a horse from any distance (counts as a soft teleport) |
| Horse Expert | Modrinth v21.1.0 (release, Sep 2024) | Shows horse stats | Client-useful, none. Small |
| Xaero's Minimap & World Map – Waystones Compatibility | Modrinth 2.1.0 (release, Apr 2026) | Activated waystones become Xaero waypoints | QoL only; no free travel |

### Combat and gear variety

| Mod | Source / build | What it adds | Rules |
| --- | --- | --- | --- |
| **Simply Swords** | Modrinth 1.70.2 (release, Aug 2026); 3 deps | Spears, glaives, katanas, greathammers, rapiers + unique loot weapons | Has Better Combat animations. Unique weapons spawn in loot (fits Apotheosis). Optional `simplycataclysm` add-on exists |
| **Immersive Armors** | Modrinth 1.7.6 (release, May 2026) | Many armor sets with set effects | None. Check no set grants flight (none known) |
| Spartan Weaponry Unofficial | Modrinth 1.2.3 (release, Aug 2026) | Classic weapon types per material, incl. Mekanism/modded metals | Unofficial port. Pick Simply Swords **or** this, not both |
| Silent Gear | Modrinth 4.2.1.1 (release, May 2026) | Part-based tools/armor you design | A different way to play, but overlaps Apotheosis gear and Mekanism Tools. Tinkers' Construct has **no** 1.21.1 NeoForge build (CF check; only a tiny unofficial port) |

### Bosses and late-game goals

| Mod | Source / build | What it adds | Rules |
| --- | --- | --- | --- |
| **Extended Crafting** | Modrinth 7.0.9 (release, Sep 2026) | Big crafting tables (up to 9×9), combination crafting | None. The usual "final craft" tool for a pack-made endgame item (boss drops + every tech mod). Recipes are ours in KubeJS |
| Draconic Evolution | Modrinth 3.1.4.633 (**beta**, Sep 2026); 2 deps | Endgame tech, Chaos Guardian boss, armor with **flight** | Beta. Its armor flight is power-costed, but it is another top-tier tech line next to Mekanism; boss stats and flight need review. Only if Mek/AE2 endgame feels short |
| Legendary Monsters | Modrinth 2.2.4 (release, Oct 2026) | Early/mid/late bosses in 13 structures | Already a **Maybe** in the friend list (Overworld spawns to tune). Still the strongest boss pick left |

### Tech

Very well covered; nothing is missing. One idea that adds a different way to play:

| Mod | Source / build | What it adds | Rules |
| --- | --- | --- | --- |
| Create Ore Excavation | Modrinth 1.6.8 (release, Nov 2025) | Hidden infinite ore veins mined by Create drills | No worldgen blocks (veins are data). Gives Create a reason to set up remote mining outposts reached by train or airship |
| Modern Industrialization / Oritech | MI 2.5.11, Oritech 1.2.13 (both release, Oct 2026) | Still an open Maybe (pick one in the creative test) | Oritech has flight items (jetpack, exosuit); check costs |

### Magic

| Mod | Source / build | What it adds | Rules |
| --- | --- | --- | --- |
| **Ars Elemental** | CurseForge only, `ars_elemental-1.21.1-0.7.10.4` | Elemental schools, focuses and armor for Ars | The standard Ars add-on and missing here. Check the Air focus (fall-damage/levitation help, not free flight) |
| Ars Additions | Modrinth 21.3.0 (release, Feb 2026) | Small Ars QoL and tweaks | None. Check any warp-related additions against the teleport rule |
| Theurgy | Modrinth 1.78.0 (release, Oct 2026) | Alchemy: replicate and transmute matter | A different style (alchemy) that connects to the resource side; overlaps a little with Mystical Agriculture |
| Malum / Eidolon: Repraised / Forbidden & Arcanus | Malum 1.8.2, Eidolon 0.5.0.7, F&A 2.6.1 (all release) | Dark/soul magic; necromancy; magic + building blocks | All have builds, but magic already has five systems. Only if the group wants a sixth. Eidolon is an unofficial port. Ars Technica (CF, 2.7.6) overlaps Ars Creo |

### Farming and food

| Mod | Source / build | What it adds | Rules |
| --- | --- | --- | --- |
| **Croptopia** | CurseForge only, `croptopia-neoforge-1.21.1-4.2.4` (needs EpheroLib) | 60+ crops and hundreds of foods | Adds wild crop features in biomes; check Lootr/worldgen (features only, no biomes). Biggest help for Spice of Life variety. Optional bridge `farmers-croptopia` on Modrinth |
| **Brewin' and Chewin'** | Modrinth 4.5.0 (release, Jun 2026) | Fermented drinks and cheeses for Farmer's Delight | None. Fills the drinks gap |
| Expanded Delight | Modrinth 0.1.4 (**beta**, Jan 2026) | More FD crops (cinnamon, peanuts, chili…) | Features. Beta; take Croptopia **or** this |
| [Let's Do] Vinery / Farm & Charm | Modrinth 1.5.6 / 1.1.29 (release, Oct 2026) | Vineyards and wine; farmhouse cooking | Cozy content. Let's Do Bakery/Brewery are archived (no 1.21.1). Overlaps Farmer's Delight style; one at most |

### Building and decoration

Fully covered; no picks. **Amendments** (Modrinth 1.21-2.2.0, by the Supplementaries author) is the only small one worth a look (vanilla block tweaks: hanging signs, cauldron dyes, lanterns on walls).

### QoL

| Mod | Source / build | What it adds | Rules |
| --- | --- | --- | --- |
| **Enchantment Descriptions** | Modrinth 21.1.11 (release); client-required | Tooltip text for every enchantment | Big help with Apothic Enchanting's many enchants |
| **TorchMaster** | Modrinth 21.1.13 (release, Sep 2026) | Mega Torch stops hostile spawns in a radius | Supports "friendly near spawn" and builders. Mega Torch radius in config; doesn't touch the difficulty script |
| **Crafting Tweaks** | Modrinth 21.1.11 (release) | Rotate/balance/clear crafting grid buttons | None. Check overlap with IPN |
| Jade Addons | Modrinth 6.1.2 (release, Oct 2026) | Jade info for more mods | None |
| Crash Assistant | Modrinth 1.11.12 (release, Aug 2026); client-only | Crash screen that points to the right log | Helps 5–6 players report crashes. Client-only, optional |

### Multiplayer / social

| Mod | Source / build | What it adds | Rules |
| --- | --- | --- | --- |
| **Ping Wheel** | Modrinth 1.12.2 (**beta**, Apr 2026); both sides | Ping a spot or mob for friends | Small and widely used despite the beta tag. `ping-to-map-xaeros` shows pings on Xaero's |
| Emotecraft | Modrinth 2.4.12 (release, Aug 2025); server optional | Player emotes | Quark already has an emotes module. Only if Quark's is turned off |

### Server admin

| Mod | Source / build | What it adds | Rules |
| --- | --- | --- | --- |
| **Neruina** | Modrinth 3.3.5 (release, Oct 2026) | Stops a crashing entity/block entity from bricking the world | Strong pick for a 300+ mod server |
| **Packet Fixer** | Modrinth 3.3.1 (release, Nov 2025) | Raises packet/NBT limits, fixes timeouts and kicks | Big packs often hit packet limits (large backpacks, Create contraptions) |
| LuckPerms | Modrinth v5.4.140-neoforge (release, **Aug 2024**; newer builds on luckperms.net) | Permission groups | Only needed if a command mod with permission nodes comes in |
| FTB Ranks | CurseForge only, `ftb-ranks-neoforge-2101.1.5` | Rank-based permissions for FTB mods and commands | Same as above |

**On `/home`, `/back`, `/rtp`, `/tpa`:** the pack has no mod that adds them (FTB Essentials is Cut), so players already can't use them and vanilla `/tp` is op-only. Nothing to add unless ops want those commands for admin work; then the route would be FTB Essentials + FTB Ranks with the commands restricted to an op rank, which reverses a Cut decision. Recommended: leave it as is.

### Performance

| Mod | Source / build | What it adds | Rules |
| --- | --- | --- | --- |
| **Structure Layout Optimizer** | Modrinth 1.0.12 (release, Jan 2026); server-only | Faster jigsaw/NBT structure generation | Directly cuts pregeneration time with this many structure mods. No worldgen change (same structures, faster) |
| **Async Locator Refined** | Modrinth 1.6.0 (release, Jul 2026); server-only | Structure searches off the main thread | Explorer's Compass, treasure maps, dolphins and `/locate` freeze servers in structure-heavy packs |
| FastSuite | Modrinth 6.0.7 (release, Jun 2026) | Faster recipe lookups (crafting, furnaces, machines) | None |
| Dynamic FPS | Modrinth 3.11.4 (release); client-only | Lowers FPS when tabbed out or idle | Optional client |
| More Culling / Sodium Extra | Modrinth 1.0.10 / 0.9.4 (release); client-only | More culling; extra Sodium video options | Optional client. Test with Iris and Distant Horizons |

## Top picks

If Darin takes only a short list, these fill the clearest gaps with the least risk (all release builds unless noted):

1. **Ember's Floating Islands** + **Sky Whale Ship**: things to fly to (structures).
2. **When Dungeons Arise: Seven Seas** + **Upgrade Aquatic** + **Ocean's Delight**: the ocean gap (structures; Upgrade Aquatic needs Blueprint).
3. **MNS – Moog's Nether Structures** + **Nether Depths Upgrade**: the Nether gap (Nether structures/features).
4. **MES – Moog's End Structures**: the End gap; safe with Nullscape (End structures).
5. **Simply Swords**: weapon variety that uses Better Combat.
6. **Ars Elemental** (CurseForge): the missing core Ars add-on.
7. **Croptopia** (CurseForge) + **Brewin' and Chewin'**: food variety for Spice of Life.
8. **Enchantment Descriptions** + **TorchMaster**: QoL and friendly-near-spawn.
9. **Neruina** + **Packet Fixer**: server stability.
10. **Structure Layout Optimizer** + **Async Locator Refined**: structure-heavy pack performance and pregen speed.

Worth a deliberate yes/no: **End Remastered** (changes how the End opens), **Legendary Monsters** (existing Maybe), **Extended Crafting** (endgame craft), **MVS** or **Repurposed Structures** (more Overworld fill; pick at most one).

## If any are added

- Everything marked Structures or Other-dim worldgen: decide before pregeneration, and before the seed is re-scouted if the change could move features near spawn.
- New mobs and bosses (Kobolds, Eternal Nether, Legendary Monsters, Upgrade Aquatic thrashers): add bosses to the difficulty script's skip list; check regular mobs at the Expert/Master stages.
- New structures: Lootr check and a rarity pass.
- Flight check: Draconic Evolution armor, Oritech exosuit/jetpack, Ars Elemental Air focus, Immersive Armors sets.
- Teleport check: Horseman horse summon, Ars Additions.
