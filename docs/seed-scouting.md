# Seed scouting

## Chosen seed

**Seed `-1678324137078475659`, spawn at -358, 77, -3260**, on the grass beside the tavern of an **Integrated Villages Tavern village** (structure start -352, -3248).

**Brief:** a big *ground* Integrated Village (no airship/pirate/sunken), relatively flat, near a substantial mountain, close-ish to an ocean or big water; a river is nice to have.

**How it was found:** `scout_iv.py` (scratchpad tool) boots each seed with the final pack minus Async Locator, locates `#integrated_villages:villages` from 9 points, and scores village size, distance to peaks 120–600, river ≤ 250 and ocean 200–1500. This seed was the first one tried, score 9/10: peaks 566 m, river 316 m, ocean 489 m.

**Checked** on a 900×900 render (`docs/images/spawn-tavern-village.png`): flat forest valley (median Y 77, almost no relief within 128 blocks), rivers all around, big lakes east and south-west, mountain up to **Y 287** about 450 m east. Pregenerated from here (design doc, Pregeneration).

Spawn finding is the last worldgen step, after all mods are final, since any later biome-affecting mod would undo it.

## Rules for the chosen seed
- Same seed + same terrain/biome mods = same landscape. **Don't add or remove terrain or biome mods** (Tectonic, Regions Unexplored, Streams Reflowing, Biolith/TerraBlender-based biome mods, or later Undergarden-style additions that change Overworld biomes). Doing so can reshape the map around spawn.
- Changes to structures, ores or features (moving Cobblemon worldgen to the Pokémon world, chest fixes, Inventory Pets rarity) don't move mountains, rivers or biomes. They're safe after picking the seed, but must be done **before pregenerating**.
- On the server, use the seed in `server.properties` (itzg: `SEED=`) and set the exact spawn with `/setworldspawn X Y Z` before pregenerating around it.

## Manual scouting with Genesis

**Goal (original criteria):** a fairly flat plains next to a big mountain, a river running down the mountain valley, and a village close by. Reference: terraced Tectonic peaks with snow, a river cutting the valley, and grassy flat banks at the bottom.

**Tool:** Genesis (world previewer), installed **only in the Modrinth test instance** for scouting. It is not part of the pack.

1. Create New World → **GENESIS**. Use **RANDOM** (or type a seed) and wait for the map to fill in. It uses the real generator with all of Strata's mods.
2. Look near the middle (0, 0) for:
   - a **plains/meadow** patch (flat build area),
   - right beside **mountain / peak** biomes (Tectonic's mountains; snowy peaks are their own color),
   - a **river** line running between them,
   - a **village** marker within ~500 blocks (structure markers; hover for names).
3. When one looks promising, **right-click** the plains spot to set spawn there, then **EXPORT MAP**. The PNG goes to the instance's `screenshots` folder.
4. **CREATE WORLD** (Creative) and fly around the spawn. The biome map doesn't show height, so check the mountain is actually big and the river sits in the valley.
5. Write down the **seed** and **spawn X/Z** (F3). Keep a few finalists.

Scripted tools (scratchpad): `scout.py` (boots a seed, scores villages by flat ground / mountain 60–400 / river / Pale Garden 0.8–3 km / no ocean / modded-village bonus) and `render_map.py` (top-down maps).

## Earlier candidates (not used)

**Retired seed `1121906793898615393`:** spawn X 24031, Y 111, Z −26565 (meadow village, mountains behind; world spawn in the save: X 24936, Y 64, Z −26280). Server: `SEED=1121906793898615393`, then `/setworldspawn 24031 111 -26565`; Chunky centered on the spawn (`/chunky center 24031 -26565`), radius 5000. Retired because Pale Gardens moved into the Overworld (Vanilla Backport biomes on), which reshapes the map. The follow-up criteria added a Pale Garden 1–3 km away.

**First-round finalists** (pack before Integrated Villages; not re-checked against the final mod list):
| Seed | Spot |
| --- | --- |
| A `-8410900080260329900` | Iberian village @ 304, 880 |
| B `6914056179472109047` | Plains village @ 1296, -896 |
| C `5987820650580666899` | Iberian village @ 2032, -1312 (snowy range behind, rivers down the valleys; strongest of the four) |
| D `-3032592841047253506` | Plains village @ -2144, 1168 |
