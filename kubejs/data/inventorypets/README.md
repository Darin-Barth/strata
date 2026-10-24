Datapack overrides for Inventory Pets worldgen (loaded by KubeJS from `kubejs/data/`).

- `worldgen/structure_set/*.json`: much rarer placement. The mod's defaults were 3–16 chunk spacing (24 tree tops near spawn in one test world); now 40–48, and 24 for the sky dungeon. Salts are the mod's own.
- `tags/worldgen/biome/has_structure/sky_dungeon_biomes.json`: sky dungeons only generate in the Aether (`#aether:is_aether`, replacing the mod's Overworld biome list).

These structures' chests have their items baked in (no loot table), so Lootr can't make them per-player. Rarity keeps them special.
