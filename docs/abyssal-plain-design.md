# The Abyssal Plain: design proposal (Oct 26, 2026)

A fully underwater dimension, `strata:abyssal_plain`, in the spirit of Subnautica and of Huge Deer's "Surviving Minecraft's Abyss Mod" (Darin, Oct 26): water everywhere, no surface, a deep seafloor to explore, and bases you have to engineer before you can breathe in them. Mod research: `docs/abyssal-plain-mod-research.md`.

## 1. Decisions so far
- **No surface** (Darin, Oct 26). A rock ceiling sits above the water; there is nowhere to swim up to.
- **Core mod: Create: Deep Seas** (beta, added for the next update, test server Oct 26: boots clean with our Create Aeronautics 1.3.2 and Sable 2.0.6). It provides the gameplay systems: physics submarines, water pressure on divers and hulls, the copper diving suit, airlocks (Decompression Chamber), Electrolyzer + Oxygen Diffuser, the Seaglide. Its own Abyss creatures, vents and lianas are **switched off in released builds** ("content disabled in production"), so the dimension's life comes from other mods (section 5).
- "Deeper Oceans" (Deep Seas' Overworld ocean reshaping) stays off; `config/create_submarine-common.toml` ships with it off.

## 2. Getting there
- **Arrival: the Lifepod.** With no surface, a player stepping through the portal would drown at once. The return portal sits inside a small fixed **Lifepod**: a sealed, protected chamber with air, a porthole, a chest with a few starter supplies (nothing that skips progression) and an airlock door to the sea. The flood rule never touches it, and its blocks can't be broken. One Lifepod per portal link (BBL Portals links 1:1 by X/Z, so the pod is generated where the portal lands).
- **Portal (proposal, to pick):** a frame of **dark prismarine** lit with a **Tidecaller** (Heart of the Sea + nautilus shells + a Deep Seas pressure part), so the trip needs an ocean monument raid and some Deep Seas progress first. Same BBL Portals setup as the Pokémon world and the Hollow.

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

**Your call: Alex's Caves Continued.** Its Abyssal Chasm is the best ready-made abyss content (the Hullbreaker, lanternfish, tripodfish, Deep Ones, black vents) but it's 75 MB, its five other cave biomes would need switching off, and its submarine and diving suit duplicate Deep Seas.

## 6. Rewards
- Unique materials from vents, trenches and the Leviathan (e.g. an "Abyssal Pearl" gate item, like the Hollow's Ember).
- Per-player Lootr chests in all ruins and wrecks.
- A Field Guide / scanning quest chapter ("Abyssal Survey").

## 7. Build steps
1. Add the chosen mods; set Hybrid Aquatic's Overworld biomes off and retarget its tags.
2. `tools/build_abyssal_plain.py`: dimension, ceilinged noise settings, biomes, tags, down-scanning placed features, structure copies.
3. KubeJS: portal and Tidecaller, Lifepod generation and protection, the flood rule, damage cap/grace, breathing-gear gates.
4. Test server: leak check (nothing aquatic-only escapes, no Overworld ocean content inside), spawn counts per biome, structures land on the floor.
5. **Playtest with clients:** Lifepod arrival, a pumped-dry hull base on the seafloor, pressure bands, submarine dive to the Trench, the Leviathan.
6. Pregenerate on the server (taller dimension, so roughly 1.7× the Hollow's generation time).

## 8. Open questions
- Portal frame and igniter: the dark prismarine + Tidecaller idea, or something else.
- Alex's Caves Continued: in or out.
- Breathing gear: allow (pressure is the gate) or cap inside the dimension.
- Whether hull bases work as fixed bases (playtest), and what to do if they don't (e.g. a Lifepod-style "habitat module" block that seals a room).
