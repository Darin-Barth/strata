# Strata quest book — plan (draft for Darin)

FTB Quests 2101.1.37. Generated from Python sources in `tools/quests/` → `config/ftbquests/quests/`
(chapter SNBT + text in `lang/en_us.snbt`, the format the in-game editor writes). Every item ID is checked
against the mod jars by `tools/quests/check_ids.py`.

## Style
- Each chapter opens with a short "What is this mod?" quest (checkmark), then quests that teach by doing:
  craft the key block, use it, make the next tier. Descriptions: 2–4 short lines, friendly, with the
  key controls/tips ("Press U on an item in EMI to see what it's used for").
- Chapters end with a "Where next?" quest pointing to related chapters.
- Rewards stay modest: XP, a few useful items, and loot bags (Common / Uncommon / Rare reward tables).
  No flight items, no teleport items, no wireless items as rewards.
- Quest order follows the design-doc gates: same-dimension wireless (Flux, AE2 wireless, entangloporters)
  only after "Into the Nether"; cross-dimension (Quantum Network Bridge), late Mekanism/AE2, Draconic and
  Extended Crafting finals after boss quests (Cataclysm). Quests only order things; KubeJS does the real
  recipe gating (phase 2).

## Starter flow (chapter "Welcome to Strata")
1. **Welcome to Strata** — Build. Fly. Explore. How the quest book works.
2. **A Tavern Town** — you spawn by a tavern; villagers, Bountiful board, Guard Villagers.
3. **What's That Recipe?** — EMI (R = recipe, U = uses), JEI/JER for drops and ore heights.
4. **Find Your Way** — Xaero's minimap/world map, waypoints, Ping Wheel.
5. **Timber!** — logs (FallingTree, FTB Ultimine with the ` key).
6. **A Bag for Everything** — Sophisticated Backpack.
7. **Home Sweet Claim** — FTB Teams (make a team) + FTB Chunks claims from the map.
8. **When Things Go Wrong** — Corail Tombstone, PlayerRevive, Redomesticate (pets come back).
9. **Rules of the Road** — no /home, /back, /tpa; flight costs fuel/power/mana/stamina.
10. **Waystones** — find or craft one; XP cost grows with distance, more across dimensions.
11. **Iron Age** — iron tools and armor, Apotheosis gear and Better Combat basics.
12. **The World Gets Harder** — staged difficulty: Normal → Expert after the first Nether visit → Master
    after the Dragon. Bosses keep their own stats.
13. **Pick a Path** — branches to: Tech (Create), Magic (Ars Nouveau), Exploration, Life & Cozy,
    Pokémon World. Nothing is locked; all chapters stay visible.

## Chapters (groups → chapters)
**Start here:** Welcome to Strata

**Tech**
1. Create: Getting Moving — rotation, andesite alloy, press/mixer/fan, belts, depots, Ore Excavation.
2. Create: Power & Wires — water wheels → C&A alternator → New Age generators → nuclear; C&A wires
   locally, IE wires long distance; Diesel Generators.
3. Create: Trains & Trade — Steam 'n' Rails, Numismatics, Trading Floor, Additional Logistics.
4. Create: Airships — Aeronautics, Propulsion, Aeroworks, Tweaked Controllers, Create Jetpack (air cost).
5. Create: Extras — Enchantment Industry, Big Cannons, Slice & Dice / Central Kitchen, Deco/Copycats.
6. Immersive Engineering — hammer, coke oven, blast furnace, wires & transformers, Excavator.
7. Mekanism — metallurgic infuser, ore tiers ×2→×5, generators, jetpack, fission/fusion, MekaSuit (late).
8. Applied Energistics 2 — meteorites, inscriber, ME system, autocrafting; wireless after Nether; QNB late.
9. Industrial Foregoing, PneumaticCraft, Powah, Extreme Reactors (one chapter "More Machines", one
   column each).
10. Logistics & Wireless — Integrated Dynamics, LaserIO, Flux Networks (mid tier).
11. Oritech.
12. Resource Farming — Mystical Agriculture, Productive Bees, Mob Grinding Utils.
13. Endgame — Draconic Evolution, Extended Crafting.

**Magic**
14. Ars Nouveau — source, glyphs, rituals, familiars, Starbuncles (+ Elemental, Additions, Trinkets,
    Creo, Énergistique, Ocultas, Conflux).
15. Iron's Spells 'n Spellbooks — scrolls, inscription table, schools (+ Ars 'n Spells / Iron & Nouveau
    shared mana, Cataclysm: Spellbooks).
16. Occultism — otherworld goggles, spirits, rituals.
17. Neo Vitae — blood altar, sacrifice, runes.
18. Theurgy — alchemy.
19. Vampirism — choose vampire, hunter or neither (+ Werewolves, Bloodlines, Umbrellas).

**Exploration**
20. Explorer's Guide — compasses, YUNG's/IDAS/WDA structures, Lootr, Artifacts & Relics, archeology.
21. The Nether — Incendium, Eternal Nether, Nether fortress; difficulty step to Expert.
22. Twilight Forest — progression boss by boss.
23. The Aether (+ Deep Aether, Aether Villages).
24. Deeper and Darker — the Otherside.
25. Ad Astra — rockets and planets.
26. The End — End Remastered's eyes, Integrated Stronghold, Dragon (unlocks the Pinnacle World Tier), Nullscape.
27. Pokémon World — Bell Fragment → Johto Bell, portal frame, starter, Pokécenters, gyms, CobbleDollars.

**Bosses & Combat**
28. Combat & Gear — Better Combat, Combat Roll, Apotheosis gems/affixes/enchanting, Simply Swords.
29. L_Ender's Cataclysm — the eight bosses in order (+ Integrated Cataclysm).
30. Ice and Fire — dragons, the dragon forge; riding is late and earned.
31. Boss Hunter — Mowzie's, BoMD, Bosses'Rise, Qliphoth, Legendary Monsters, Apocalyptic Bosses.

**Life & Cozy**
32. Farming & Food — Farmer's Delight + delights, Croptopia, Vinery, Brewin', Spice of Life, seasons.
33. Pets & Critters — taming, Inventory Pets, Naturalist/Alex's Mobs, Plushies, Easy Villagers.
34. Building & Decorating — Chipped/Rechiseled, Macaw's, Handcrafted, FramedBlocks, gadgets and wands.
35. Storage — Sophisticated Storage, Functional Storage, Tom's Simple Storage.
36. Fishing — Aquaculture 2, Tide (journal).

About 35 chapters, ~10–20 quests each (~450 quests).

## Status (Oct 25, 2026)
Built: 37 chapters, 795 quests, 4 loot bags. All 1,294 distinct IDs validate against the jars
(`python -I tools/quests/build.py`), and a scratch NeoForge server with FTB Quests loaded the book
("Loaded 6 chapter groups, 37 chapters, 795 quests"). Not yet seen in a real client.

Gate anchors used across chapters: `welcome/nether` (same-dimension wireless, brass/blaze tech),
`cataclysm/netherite_monstrosity` (Mek ultimate/SPS/antimatter, AE2 256k, Extended Crafting Ultimate
Table), `cataclysm/ignis` (MekaSuit, Draconic armor, Ad Astra tier 2), `cataclysm/ender_guardian`
(AE2 Quantum Network Bridge, Draconic chaos tier, Ad Astra tier 4), `the_end/dragon` (Draconic awakened,
Ice and Fire dragon riding).

## Rule problems found while writing (need config/KubeJS; quests don't feature or reward these)
Free or cheap flight:
- Oritech Flight augment ("creative-style free flight"), Mystical Agriculture flight_augment.
- Create Stuff 'N Additions jetpacks: andesite tier on coal, copper on water; "Above the Clouds" enchant.
- Cataclysm: Spellbooks Excelsius chestplate ("infinite flight"); BoMD Table of Elevation (creative flight 7x7).
- Ice and Fire: hippogryphs (early) and dragons ridable from stage 3; `dragon.flightStamina` and
  `hippogryphs.flightStamina` are false in config (turning them on is an easy fix).
- Aether: Valkyrie armor (free temporary flight, reforgeable), Phygs; Deeper and Darker Soul Elytra (cooldown boost).
- Draconic Wyvern flight module is a cheap pre-Dragon craft (power-costed).
- Apotheosis loot can hold Potions of Flying; Inventory Pets Flying Saddle pet.
Free teleport:
- Oritech Portal augment (return portal = /home), Draconic Dislocators, Occultism Entity Wormhole,
  Bloodlines Gravebound phylactery teleport, Inventory Pets House/Enderman pets, BoMD Charged Ender Pearl,
  Legendary Monsters annihilator helmet/chorus blade, Artifacts/Relics/Forsaken Relics teleport accessories.
- Explorer's Compass `allowTeleport = true` (probably op-only; set false).
Wireless outside the tiers:
- Flux Networks and Mekanism entangloporters/teleporters work across dimensions by default.
- Mighty Mail mailboxes work in any dimension from day one (`allowedDimensions`).
- Powah Ender Cells/Gates and Player Transmitter; ExtendedAE wireless connector/hub/terminal;
  Occultism Storage Accessor/Stable Wormhole (cross-dim); Deeper and Darker Sculk Transmitter;
  Draconic wireless crystals; Oritech energy poles (competes with IE as long-distance grid);
  Gadgets & Gizmos Industrial Alternator + andesite cable (bypasses the C&A alternator nerf).
Other:
- Apotheosis world tiers (Ctrl+T, per player) are a second mob scaler next to the staged-difficulty script.
- Apocalyptic Bosses: boss chests hold elytra/nether stars/netherite; several bosses spawn in plains/forests.
- Extended Crafting Ultimate Ingot has no recipe (endgame KubeJS still to do); Numismatics coins have no
  recipe (decide how money enters the server).
- Keybind clashes in the client: B (backpack/Xaero waypoint/Occultism), R (Combat Roll/Iron's wheel),
  M (Xaero/FTB Chunks map), V (voice/Deep Aether), Z (Bosses'Rise roll/Xaero).
