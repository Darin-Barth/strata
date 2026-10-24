# Seed scouting

**Goal:** a fairly flat plains next to a big mountain, a river running down the mountain valley, and a village close by. Reference: terraced Tectonic peaks with snow, a river cutting the valley, and grassy flat banks at the bottom.

**Tool:** Genesis (world previewer), installed **only in the Modrinth test instance** for scouting. It is not part of the pack.

## Steps
1. Create New World → **GENESIS**. Use **RANDOM** (or type a seed) and wait for the map to fill in. It uses the real generator with all of Strata's mods.
2. Look near the middle (0, 0) for:
   - a **plains/meadow** patch (flat build area),
   - right beside **mountain / peak** biomes (Tectonic's mountains; snowy peaks are their own color),
   - a **river** line running between them,
   - a **village** marker within ~500 blocks (structure markers; hover for names).
3. When one looks promising, **right-click** the plains spot to set spawn there, then **EXPORT MAP**. The PNG goes to the instance's `screenshots` folder; tell me and I can look at it too.
4. **CREATE WORLD** (Creative) and fly around the spawn. The biome map doesn't show height, so check the mountain is actually big and the river sits in the valley.
5. Write down the **seed** and **spawn X/Z** (F3). Keep a few finalists.

## Rules for the chosen seed
- Same seed + same terrain/biome mods = same landscape. **After choosing, don't add or remove terrain or biome mods** (Tectonic, Regions Unexplored, Streams Reflowing, Biolith/TerraBlender-based biome mods, or later Undergarden-style additions that change Overworld biomes). Doing so can reshape the map around spawn.
- Changes to structures, ores or features (moving Cobblemon worldgen to the Pokémon world, chest fixes, Inventory Pets rarity) don't move mountains, rivers or biomes. They're safe to finish after picking the seed, but they must be done **before pregenerating**.
- On the server, use the seed in `server.properties` (itzg: `SEED=`) and set the exact spawn with `/setworldspawn X Y Z` before pregenerating around it.
