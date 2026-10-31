# Queued for the next update

Changes committed on master since the last release (**v1.1.0**; notes in the GitHub release) that haven't been released yet. Policy: changes ship together in one update (merge to `master` + new `.mrpack` release + server restart); only a critical hotfix goes out on its own. Queued work can be backed up to the GitHub branch `next-update` (`git push origin master:refs/heads/next-update`); the server only follows `master`.

## Changes
- **Inventory buttons no longer overlap:** Inventory Profiles Next shows only its Sort and Move All buttons (its sort-in-columns and sort-in-rows buttons covered the quest book button in your inventory and Sophisticated Backpacks' buttons in a backpack), and the Accessories button moved off the player preview. (Client side: comes with the next `.mrpack`; older installs can hide the two buttons in Inventory Profiles Next's settings, Gui tab.)
- **Welcome quest "A Tavern Town" is now "Find a Village":** it assumed every world starts next to a tavern village; now any village counts. Progress already made on it is kept. (Server side: the quest book updates with the server restart.)
- **Carry On picks up with Left Alt, not Shift:** hold **Left Alt** and right-click with an empty hand to pick up a block, chest or animal. Shift + right-click goes back to every other mod's own action (it opened Carry On instead of, for example, magic blocks). New installs get it automatically; older installs: Options > Controls > Carry On > Carry, set to Left Alt (or **Reset All**).
- **Skill trees redesigned:** Combat, Mining and Fishing are bigger (Combat 41 nodes, Mining 31, with two keystones per branch) and take much longer (Combat about 20,000 XP to max instead of 1,262). Every node can be unlocked at max level, and levels now stop there (1.0 kept giving points forever). XP you already earned is kept, and your points in those trees are refunded once when you log in after the update so you can re-pick. (Server side: takes effect with the restart.)
- **Players finally show on the map:** 1.1 turned on "everyone sees everyone" for Xaero's minimap and world map, but Xaero only ran on players' computers, so the server never sent anyone's position. Xaero now also runs on the server. (Server side: takes effect with the restart.)
- **No more sudden sky and fog switch at biome edges:** Atmospherics recoloured only vanilla biomes, so walking between a vanilla and a modded biome (most of Strata's) snapped the sky and fog in one frame. Its per-biome colours are now off by default; its haze, clouds, stars, comets and weather effects stay. Every biome uses Minecraft's own colours, which blend as you walk. (Client side: comes with the next `.mrpack`; on an existing install, turn off each biome's colours in Atmospherics' menu, F6, or copy `config/ambientfog/biome_fog.json` from the new pack.)

## Release checklist
1. Check `version` in `pack.toml` and the version line in `config/fancymenu/customization/strata_title_screen.txt` (both the new version).
2. `python -I tools/curseforge_ids.py` (re-adds CurseForge IDs after mod updates; fix any "no longer used" line in
   `tools/curseforge-manual.json`), `packwiz refresh`, commit, `git push` (master, and sync `next-update`). Check no stray files sit under the server's `kubejs/data`: KubeJS refuses to start on an uppercase file name there.
3. `packwiz mr export -o build/Strata-<version>.mrpack`; `gh release create v<version>` with the notes below.
   The CurseForge Action (`.github/workflows/curseforge.yml`) then builds `Strata-<version>-curseforge.zip`, attaches
   it to the release and, when the repo variable `CURSEFORGE_UPLOAD` is `true`, uploads it to CurseForge with the
   release notes as the changelog (CurseForge reviews it before it goes public). One-time setup by the repo owner: secret
   `CURSEFORGE_TOKEN`, variables `CURSEFORGE_PROJECT_ID` and `CURSEFORGE_UPLOAD`; leave the upload off until
   Drive-By-Wire is on CurseForge's approved list (requested), or CurseForge rejects the file. To upload a
   release that's already out: Actions → CurseForge → Run workflow with its tag.
4. Wait about 5 minutes for GitHub's raw-file cache, then restart the server (Quarry restart, or `docker compose restart`
   in `/opt/minecraft/strata`). Check the log for `Loaded N/N KubeJS server scripts ... 0 errors`.
5. Tell the group to import the new `.mrpack`.

Note: `config/DistantHorizons.toml` and `config/cameraoverhaul.toml` are `preserve = true`, so players who already have
them keep their own copy. Changes there only reach new installs.
