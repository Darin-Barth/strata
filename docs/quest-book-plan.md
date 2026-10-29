# Strata quest book: plan

FTB Quests 2101.1.37. Generated from Python sources in `tools/quests/` → `config/ftbquests/quests/`
(chapter SNBT + text in `lang/en_us.snbt`, the format the in-game editor writes). Every item ID is checked
against the mod jars by `tools/quests/check_ids.py`.

## Style
- Each chapter opens with a short "What is this mod?" quest (checkmark), then quests that teach by doing:
  craft the key block, use it, make the next tier. Descriptions: 2–4 short lines, approachable, with the
  key controls/tips ("Press U on an item in EMI to see what it's used for").
- Chapters end with a "Where next?" quest pointing to related chapters.
- Rewards: XP, a few useful items, and quest loot bags by tier (Small, Loot, Large, Grand; `tools/build_quest_bags.py`). A bag rolls a rarity, then an item from that rarity's pool.
  No flight items, no teleport items, no wireless items as rewards.
- Quest order follows the gate map (`docs/gate-map.md`): late Mekanism/AE2, nuclear power, Draconic and
  Extended Crafting finals come after the boss quests that supply their materials (Cataclysm, the Hollow,
  the Abyssal Plain). Wireless is not gated. Quests only order things; the recipes do the real gating.

## Starter flow (chapter "Welcome to Strata")
1. **Welcome to Strata** — Build. Fly. Explore. How the quest book works.
2. **A Tavern Town** — you spawn by a tavern; villagers, Bountiful board, Guard Villagers.
3. **What's That Recipe?** — EMI (R = recipe, U = uses), plus ore heights, drops and breeding in EMI.
4. **Find Your Way** — Xaero's minimap/world map, waypoints, Ping Wheel.
5. **Timber!** — logs (FallingTree, FTB Ultimine with the ` key).
6. **A Bag for Everything** — Sophisticated Backpack.
7. **Home Sweet Claim** — FTB Teams (make a team) + FTB Chunks claims from the map.
8. **When Things Go Wrong** — Corail Tombstone, PlayerRevive, Redomesticate (pets come back).
9. **Rules of the Road** — one /home (10-second cooldown), no /back, /rtp or /tpa; flight costs fuel/power/mana/stamina.
10. **Waystones** — find or craft one; XP cost grows with distance, more across dimensions.
11. **Iron Age** — iron tools and armor, Apotheosis gear and Better Combat basics.
12. **Choose Your Challenge** — Apotheosis World Tiers (Alt+L), picked by each player; other dimensions
    are tougher than home; bosses keep their own stats.
13. **Pick a Path** — branches to: Tech (Create), Magic (Ars Nouveau), Exploration, Life & Cozy,
    Pokémon (the Kakuto Region). Nothing is locked; all chapters stay visible.

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
8. Applied Energistics 2 — meteorites, inscriber, ME system, autocrafting, wireless; QNB late.
9. Industrial Foregoing, PneumaticCraft, Powah, Extreme Reactors (one chapter "More Machines", one
   column each).
10. Logistics & Wireless — Integrated Dynamics, LaserIO, Flux Networks.
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
21. The Nether — Incendium, Eternal Nether, Nether fortress.
22. Twilight Forest — progression boss by boss.
23. The Aether (+ Deep Aether, Aether Villages).
24. Deeper and Darker — the Otherside.
25. Ad Astra — rockets and planets.
26. The End — End Remastered's eyes, Integrated Stronghold, Dragon (unlocks the Pinnacle World Tier), Nullscape.
27. The Kakuto Region (Pokémon) — Bell Fragment → Johto Bell, portal frame, starter, Pokécenters, gyms, CobbleDollars.
28. The Abyssal Plain — depth, base, survey, ruins and bosses, ending in the Deep Station.
29. The Hollow (planned; `docs/hollow-progression.md`).

**Bosses & Combat**
30. Combat & Gear — Better Combat, Combat Roll, Apotheosis gems/affixes/enchanting, Simply Swords.
31. L_Ender's Cataclysm — the eight bosses in order (+ Integrated Cataclysm).
32. Ice and Fire — dragons, the dragon forge; riding is late and earned.
33. Boss Hunter — Mowzie's, BoMD, Bosses'Rise, Qliphoth, Legendary Monsters, Apocalyptic Bosses.

**Life & Cozy**
34. Farming & Food — Farmer's Delight + delights, Croptopia, Vinery, Brewin', Spice of Life, seasons.
35. Pets & Critters — taming, Inventory Pets, Naturalist/Alex's Mobs, Plushies, Easy Villagers.
36. Building & Decorating — Chipped/Rechiseled, Macaw's, Handcrafted, FramedBlocks, gadgets and wands.
37. Storage — Sophisticated Storage, Functional Storage, Tom's Simple Storage.
38. Fishing — Aquaculture 2, Tide (journal).

## Status
Built: 38 chapters, 820 quests. Every distinct ID validates against a registry dump of the
pack (`python -I tools/quests/build.py`), and the book loads on the server and in the client.

Gate anchors used across chapters: `cataclysm/ignis` (nuclear power), `cataclysm/netherite_monstrosity`
(Mekanism ultimate tier), `cataclysm/ender_guardian` (AE2 256k cells, AppliedFlux, QIO),
`the_end/dragon` (Draconic awakened tier, Pinnacle World Tier, Ice and Fire dragon riding).

## Open items (config/KubeJS; quests don't feature or reward these)
- Flight, teleport and wireless items follow the rules in `docs/design-doc.md` and `docs/gate-map.md`
  section 5.
- Explorer's Compass `allowTeleport = true` (probably op-only; set false).
- Apocalyptic Bosses: boss chests hold elytra/nether stars/netherite; several bosses spawn in plains/forests.
- Extended Crafting Ultimate Ingot has no recipe (endgame KubeJS still to do).
- Numismatics coins have no recipe; players start with 10 starter cogs (`docs/balance-patch.md` G4).
- Keybind clashes in the client: `docs/keybinds.md`.
