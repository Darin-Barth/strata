# The Abyssal Plain (approved and built Oct 26, 2026)

A fully underwater dimension, `strata:abyssal_plain`, in the spirit of Subnautica and of Huge Deer's "Surviving Minecraft's Abyss Mod" (Darin, Oct 26): water everywhere, no surface, a deep seafloor to explore, and bases you have to engineer before you can breathe in them. Mod research: `docs/abyssal-plain-mod-research.md`.

## 1. Decisions so far
- **No surface** (Darin, Oct 26). A rock ceiling sits above the water; there is nowhere to swim up to.
- **Core mod: Create: Deep Seas** (beta, added for the next update, test server Oct 26: boots clean with our Create Aeronautics 1.3.2 and Sable 2.0.6). It provides the gameplay systems: physics submarines, water pressure on divers and hulls, the copper diving suit, airlocks (Decompression Chamber), Electrolyzer + Oxygen Diffuser, the Seaglide. Its own Abyss creatures, vents and lianas are **switched off in released builds** ("content disabled in production"), so the dimension's life comes from other mods (section 5).
- "Deeper Oceans" (Deep Seas' Overworld ocean reshaping) stays off; `config/create_submarine-common.toml` ships with it off.

## 2. Getting there
- **Arrival: the Lifepod.** With no surface, a player stepping through the portal would drown at once. The return portal sits inside a small fixed **Lifepod**: a sealed, protected chamber with air, a porthole, a chest with a few starter supplies (nothing that skips progression) and an airlock door to the sea. The flood rule never touches it, and its blocks can't be broken. One Lifepod per portal link (BBL Portals links 1:1 by X/Z, so the pod is generated where the portal lands).
- **Portal (Darin, Oct 26):** a frame of **dark prismarine** lit with the **Tidecaller**: a Conduit in the middle, a Deep Seas Ballast Tank above and below it, prismarine crystals down both sides (`P B P / P C P / P B P`). The Conduit needs a Heart of the Sea (buried treasure) and nautilus shells; the ballast tanks mean Deep Seas progress first. The Conduit is an ingredient, not the lighter, because a Conduit is a placeable block. Same BBL Portals setup as the Pokémon world and the Hollow. **Look and sound (Darin, Oct 26):** its own animated "marine snow" texture (near-black water, flecks drifting down, now and then a blinking light) in BBL Portals' "molten" texture slot, pale dust flecks, water drips and glow sparkles; the Nether whoosh is swapped for deep-sea sounds (`startup_scripts/portal_ambience.js`). The Tidecaller is a drowned compass whose needle strains upward and snaps back to the deep.

## 3. The world
- **Height and depth bands.** Ceiling underside around Y 100, seafloor between about Y −150 (shelves) and Y −480 (trench bottoms). Deep Seas measures pressure from the top of the water column, here the ceiling (to confirm in game), so depth tiers map onto its limits:
  - **Shelves and ridges (0–120 m):** reachable in plain gear. Kelp, coral, lighter water.
  - **The Plain (120–280 m):** needs the full copper diving suit. Sediment flats, glass sponges, whale falls, ruins.
  - **The Trenches (280 m and down):** submarines only (hull ratings). The biggest creatures, the boss, the best loot.
- **Biomes** (our own, under `strata:`, never in `#minecraft:is_ocean`, `#c:is_ocean` or `is_overworld`, so Overworld ocean content stays out; each mod is opted in through its own tags): Abyssal Shelf, Abyssal Plain, Hydrothermal Field (vents, brine pools, magma), Bioluminescent Garden (glowing flora, the "wonder" biome), The Trench.
- **Dimension type:** no skylight, fixed time (permanent dark, which many aquatic mobs read as night), `sea_level` at the ceiling underside (mobs check spawn height against it), beds don't work, compasses spin.
- **Terrain generator:** our own noise settings: a wide, gently rolling plain cut by deep trench lines and ridges, with the ceiling as a solid cap. Built with a generator script like `tools/build_hollow.py`.
- **The ceiling problem:** most mod flora and many structures place themselves using the topmost block, which here is the ceiling. Fix: our own placed features that reuse the mods' configured features but scan down to the floor (like the Nether), and fixed-height copies of structures that need it.
- **Atmosphere:** deep blue-black water fog, underwater ambience, AmbientSounds whale calls and creaks, light only from glowing life, vents and what players bring.

## 4. Rules
- **The sea always wins:** in this dimension, any block broken that would leave air becomes water (KubeJS). There is no "dig a dry tunnel" trick. The Lifepod is exempt.
- **Bases are pressure hulls:** you build a sealed structure, pump it dry through a Decompression Chamber airlock, and keep the air with an Electrolyzer + Oxygen Diffuser. Hull blocks have depth ratings, so deeper bases need better hulls. **To test in game:** whether a hull parked on the seafloor works as a permanent base (the oxygen system is written for submarines; it may need the base to be an assembled "ship" that rests on the floor).
- **Breathing gear:** several existing items give long or free breathing (Create backtank, Aquamirae oxygen tank, Aquaculture Neptunium, water-breathing spells and potions). Pressure still limits depth for all of them, so the proposal is to allow them: they make the shelves comfortable, they don't unlock the trenches. Option: cap them inside the dimension if they trivialise it.
- **No Conduit power in the Abyssal Plain** (Darin, Oct 26): a placed Conduit would give water breathing, night vision and fast mining around a base and make the pumps, airlocks and oxygen pointless. Conduits keep working everywhere else (KubeJS: remove the effect inside the dimension).
- **Scary but fair:** the Hollow's damage cap and grace period apply here too, bosses excepted.

## 5. Life and content
**New mods (recommended):**
- **Hybrid Aquatic** (+ Hybrid API): the main kit, about 140 creatures (trench anglerfish, barreleye, dragonfish, fangtooth, colossal and vampire squid, firefly squid, yeti crab, the Karkinos miniboss) plus thermal vents, brine pools, glass sponges and whale-fall structures. Spawns follow its own biome tags, so we point the trench and vent creatures at our biomes; its Overworld biomes can be switched off in config. Its diving suits likely give free breathing: gate or remove (KubeJS).
- **Scannable**: an FE-powered scanner, the Subnautica scanner feel.
- **Field Guide** (+ Immersive Overlays, Item Descriptions, client): scan creatures and plants with a spyglass to fill an in-game encyclopedia. Natural FTB Quests goals.
- **Sunken Spires**: 11 ruins of an ancient civilisation with minibosses and a prismarine trial chamber.
- **MOS – Moog's Ocean Structures**: Atlantis ruins, wrecks, a sea-dragon skeleton (server-only; needs fixed-height copies because of the ceiling).

**Already in the pack, moved or shared here:**
- Naturalist anglerfish and giant isopod (its `#naturalist:has_*` tags), Alex's Mobs frilled shark, giant squid and cachalot (spawn configs), Upgrade Aquatic thrasher and great thrasher plus its prismarine coral and jelly torches, Critters and Companions dumbo octopus, Regions Unexplored deep flora.
- **The boss: Cataclysm's Leviathan.** Move the Sunken City into the Trench (`#cataclysm:has_structure/sunken_city_biomes`), so the Abyssal Plain has a real final goal. Its drops can gate late tiers.
- Ice and Fire sea serpents: possible in the Trench, but they're very dangerous; decide after the playtest.

**Alex's Caves Continued: abyss content only (Darin, Oct 26, option B).** Its Abyssal Chasm creatures (Deep Ones, Deep One knights and mages, the Hullbreaker, lanternfish, tripodfish) spawn only through ordinary biome spawn lists, with nothing in their code tied to its own chasm biome (checked in the 1.1.3 jar), so they and its abyssal blocks go into the Trench and Hydrothermal Field. **All six of its Overworld cave biomes are switched off** in its config (the Overworld is pregenerated, so they would only appear past 5 km with seams; Forlorn Hollows overlaps the Hollow; its submarine and diving suit overlap Deep Seas and stay unused). Cost: about 85 MB more content (RAM, startup, join time).

## 6a. Something to work toward (proposal, Oct 26)
**The big goal: a Deep Station on the Trench floor.** Establishing a working pressure-hull base about 400+ m down, where only the best hulls hold, is the dimension's endgame. Three tracks lead there:
1. **Depth (gear):** shelves in plain gear → the Plain with the copper diving suit (120 m) → the trenches in a first submarine (280 m+) → the Trench floor with reinforced hulls. Each milestone is a quest with rewards.
2. **Boss ladder:** Karkinos (Hybrid Aquatic miniboss; it doesn't spawn naturally: you summon it by fishing with an Ominous Hook in your off hand, crafted from nine crab species' claws, anywhere with fishable water, including the Lifepod's moon pool; its claw drops wherever it dies) → the Hullbreaker (Alex's Caves, the trenches; it hunts submarines) → the **Leviathan** (Cataclysm, final boss, Sunken City at the Trench bottom). Each drops what the next step needs.
3. **The Abyssal Survey (discovery):** scan creatures and plants with the Field Guide and Scannable; completed survey sections give rewards and the story of the drowned civilisation (Sunken Spires, the Deep Ones).

**Payoff outside the dimension:** the pack rule that late Mekanism and AE2 tiers need boss drops gets one of its gates here: the Leviathan's drop plus rare **Abyssal Pearls** from the trenches. Deep-only crafting also unlocks the best hull tier and deep-dive upgrades. All of it becomes an "Abyssal Plain" FTB Quests chapter.

## 6. Rewards
- Unique materials from vents, trenches and the Leviathan (e.g. an "Abyssal Pearl" gate item, like the Hollow's Ember).
- Per-player Lootr chests in all ruins and wrecks.
- A Field Guide / scanning quest chapter ("Abyssal Survey").

## 7a. What was built (Oct 26)
- **Generator:** `tools/build_abyssal_plain.py --out kubejs/data --mods <server mods folder>` writes the dimension, noise settings, biomes, features, tags, spawn wiring, structure copies and loot modifiers. Re-run after an update to Hybrid Aquatic, Alex's Caves, Sunken Spires or MOS.
- **Heights:** the column runs Y −48 to 591 because the standard noise generator hard-codes **lava below Y −54** in every dimension. Ceiling underside ~Y 560 (sea level 568), shelves ~Y 479, the plain ~Y 314, trench floors ~Y 14. Depths below the ceiling are as designed.
- **What the ceiling breaks, and the workarounds:** surface rules count depth from the topmost air and water doesn't reset that count, so seafloor sediment is laid down as disk features (clay/mud, sand/gravel, blackstone/magma, mud/moss, abyssmarine). Vanilla kelp, seagrass, sea pickles and coral find their own height from the OCEAN_FLOOR heightmap, so they're rebuilt as our own block-column/simple-block features. All decorations use down-scanning placement (`environment_scan`, max 32 blocks). `initial_density_without_jaggedness` is 0, like the Nether. Alex's Caves' boulders, tube worms and anemones don't place outside its chasm biome and are left out; its mussels, black vents, whale falls and Deep One ruins work.
- **Structures:** 26 copies under `strata:abyssal/` at fixed heights with `beard_box` (Sunken Spires: spires, temple, conduit ruins, spikes, fossils, forge, shrine, trial chamber buried under the plain, Colosseum and Sunken City in the trench; Moog's: Atlantis ruins and tribune, castle, church, archway, temple, wrecks, garden, magma ravine, conduit arch, dog statue, dragon skeletons in the trench). Sunken Spires now exists only here (its biome tag is emptied); Moog's keeps its Overworld oceans too. Test: the Colosseum generated on the trench floor (Y 0–40).
- **The Leviathan:** Cataclysm's Sunken City picks its height in code from the ocean-floor heightmap, so it can't be moved here. Instead the **Leviathan Lure** (6 Abyssal Pearls + Karkinos Claw + Heart of the Sea + Immortal Embryo, both boss drops guaranteed) summons the Leviathan when used in the Trench below Y 120 (one at a time).
- **Creatures:** Hybrid Aquatic's trench and vent species via its trench tags (its own Overworld biomes off), Alex's Caves' deep-sea creatures and Deep Ones and the Hullbreaker in the biome spawn lists (its six cave biomes off), Naturalist anglerfish/isopod and Upgrade Aquatic thrashers via their tags, Alex's Mobs frilled shark/giant squid/cachalot via their spawn configs.
- **Quests:** `config/ftbquests/quests/chapters/abyssal_plain.snbt`, 23 quests in the Exploration group after the Pokémon World: intro and rules, depth (shelves, diving suit, plain, first submarine, trench), base (airlock and pump, electrolyzer and oxygen diffuser), survey (Field Guide, creature observations, Scannable), ruins (Atlantis, trial chamber, Colosseum, Sunken City), bosses (Karkinos, Hullbreaker, 6 pearls, Lure, Leviathan), ending in the Deep Station. Loads clean on the test server; the observation tasks are the first in the pack, so check them in the quest editor.
- **Scripts:** `server_scripts/abyssal_rules.js` (Tidecaller and Lure recipes, Lifepod, flood rule, no Conduit power, no sponges, Pearl drops, Lure use); the Hollow's damage cap also covers `hybrid_aquatic` and `alexscaves`; `client_scripts/strata_lang.js` names every custom dimension and biome (the Pokémon world's and the Hollow's had no names before).
- **Test server (Oct 26):** clean boot; 6,561-chunk sample: no air pockets, no lava (a few vent blocks), floors at design heights, sediment coverage 50–88% by biome, kelp/seagrass/coral/sea pickles/sponges/vents/brine pools present; all five biomes found only in the Abyssal Plain.
- **Not yet tested with a client:** the portal (look, sounds, particles) and Lifepod, the flood rule, creature spawns, Deep Seas pressure under a ceiling, a pumped-dry or parked-hull base, the Lure.

## 7. Build steps
1. Add the chosen mods; set Hybrid Aquatic's Overworld biomes off and retarget its tags.
2. `tools/build_abyssal_plain.py`: dimension, ceilinged noise settings, biomes, tags, down-scanning placed features, structure copies.
3. KubeJS: portal and Tidecaller, Lifepod generation and protection, the flood rule, damage cap/grace, breathing-gear gates.
4. Test server: leak check (nothing aquatic-only escapes, no Overworld ocean content inside), spawn counts per biome, structures land on the floor.
5. **Playtest with clients:** Lifepod arrival, a pumped-dry hull base on the seafloor, pressure bands, submarine dive to the Trench, the Leviathan.
6. Pregenerate on the server (taller dimension, so roughly 1.7× the Hollow's generation time).

## 8. Open questions
- Breathing gear: allowed (pressure is the gate), revisit after the playtest.
- Whether hull bases work as fixed bases (playtest), and what to do if they don't (e.g. a Lifepod-style "habitat module" block that seals a room).
