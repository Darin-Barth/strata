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
8. **When Things Go Wrong** — GraveStone, PlayerRevive, Redomesticate (pets come back).
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
26. The End — End Remastered's eyes, Integrated Stronghold, Dragon (→ Master difficulty), Nullscape.
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
