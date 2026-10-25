# Queued for the next update

Changes committed on master since the last release (**v0.2.0**, Oct 25, 2026) that haven't been pushed to GitHub or the
beta server yet. Policy: changes ship together in one update (push + new `.mrpack` release + server restart); only a
critical hotfix goes out on its own. Clear this list when the release goes out.

## Changes
- **New: Seamless Sleep**: the night fast-forwards smoothly while someone sleeps. (Already live on the server: `gamerule playersSleepingPercentage 1`, so one sleeping player skips the night. It's a world setting, so it doesn't need the update.)
- **Village guards no longer turn on players over low reputation** (Guard Villagers' instant-aggro threshold -100 → -9999). They still defend villagers and guards you attack.
- **Minimap defaults to the top right** (`config/xaerohud.txt`, `preserve = true`, so players who moved it keep their spot).
- **Hotfix: JEI, Just Enough Resources and MezzConfig removed.** JEI built its recipe index on the game's main thread when
  joining a server (about 60 seconds with this pack), so slower clients froze on "Loading terrain" and were timed out
  (Lopez, Oct 25). EMI is the recipe viewer; EMI Ores, Advanced Loot Info and Just Enough Breeding cover what JER
  showed. Two quests now point to EMI instead of JER.
- **Quieter first join** (e5ac5ea):
  - Inventory Pets' update notice is off.
  - Distant Horizons' G1 garbage-collector warning is off. The joining guide now tells players to add
    `-XX:+UseZGC -XX:+ZGenerational` to their instance's Java arguments, which fixes the stutter the warning was about.
  - Iron & Nouveau's "Ars 'n Spells overlap" notice is blanked. It only applies to Ars 'n Spells 3.4.0+, and the pack
    has 3.3.5. **If Ars 'n Spells is ever updated to 3.4+**, set `enable_iron_glyphs = false` and
    `enable_glyph_press = false` in Ars 'n Spells' server config instead.
- **No guide books dumped on first join:** Ars Nouveau's Worn Notebook, Alex's Mobs' Animal Dictionary, Tide's Fishing
  Journal and Integrated Dynamics' guide are no longer given on spawn (`spawnBook`, `giveBookOnStartup`, `giveJournal`,
  `obtainOnSpawn` = false). Each one becomes a reward on the first quest of its chapter instead.
- **Hotbar HUD overlap fixed:** Combat Roll no longer draws its "R" keybind label next to the hotbar, and its roll-charge arrow only shows while a roll is recharging (`config/combat_roll/client.json5`).
- **New: Cubes Without Borders** (client): a borderless fullscreen window option in Video Settings.
- **Quest book: 6 quest items that don't exist in game swapped for real ones** (Ad Astra Astrodux, ExtendedAE Infinity Cell, Inventory Pets iron nugget, My Nether's Delight stove, Better Archeology identified artifact, Amendments hanging pot); the quest ID checker now validates against a registry dump from a running server.
- **Quest book: guide books come from quests** instead of the hotbar: the first quest of Ars Nouveau (Tattered Tome), Pets & Critters (Animal Dictionary), Fishing (Fishing Journal) and Logistics & Wireless (On the Dynamics of Integration) gives that book; the quests that used to ask players to craft them are now "read it" checkmarks.
- **Quest book: Combat Roll key named** (R by default, or rebind in Controls) in Welcome and Combat & Gear, since the HUD no longer shows it.

## Release checklist
1. Bump `version` in `pack.toml` and the version line in `config/fancymenu/customization/strata_title_screen.txt`.
2. `packwiz refresh`, commit, `git push`.
3. `packwiz mr export -o build/Strata-<version>.mrpack`; `gh release create v<version>` with the notes below.
4. Wait about 5 minutes for GitHub's raw-file cache, then restart the server (Quarry restart, or `docker compose restart`
   in `/opt/minecraft/strata`). Check the log for `Loaded N/N KubeJS server scripts ... 0 errors`.
5. Tell the group to import the new `.mrpack`.

Note: `config/DistantHorizons.toml` and `config/cameraoverhaul.toml` are `preserve = true`, so players who already have
them keep their own copy. Changes there only reach new installs.
