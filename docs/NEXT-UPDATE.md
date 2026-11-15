# Queued for the next update

Changes committed on master since the last release (**v1.4.3**; notes in the GitHub release) that haven't been released yet. Policy: changes ship together in one update (merge to `master` + new `.mrpack` release + server restart); only a critical hotfix goes out on its own. Queued work can be backed up to the GitHub branch `next-update` (`git push origin master:refs/heads/next-update`); the server only follows `master`.

## Changes
- **C2ME on the server (Darin, Nov 15; live trial, not tested beforehand):** generating new land stalled the server while players explored past the pregenerated area (the chunk scheduler runs on the main thread). C2ME 0.4.0-alpha.0.124 is now a server-only mod (players install nothing). Build .123 was verified clean for the Overworld pregen in October (.124 only adds a chunk ticket event for other mods); with players it is untested, and newly generated Nether, End and Kakuto Region land can get clipped Integrated Cobblemon gyms. Watch for cut-off structures and crashes; to undo, remove `mods/c2me-neoforge.pw.toml` and restart.

## Still to check in play (released untested)
- Tested and working in play (Darin, Nov 8): /spawn and YouTube links on WATERFrAMES. /spawn from the Nether and its 10 s cooldown tested Nov 12 on a test server (a second use within 10 s is refused).
- **Fairy Lights:** loads without errors, and right-clicking a fence with hanging lights attaches a string (test server, Nov 12). Still to check in game: finishing the string on a second fence, then one on an assembled airship in flight.
- **1.4.2 (Nov 14):** single-player world creation on an install updated from before 1.4.1 (create a flat world). Excelsius leggings worn by a player: tested Nov 15 on a test server (15 blocks without them cost 8.7 health, 40 blocks with them cost none).
- **1.4.3 (Nov 15):** with someone exploring, take a spark profile and compare with Nov 14 (freezes of 2-30 s, Overworld 69 ms/tick); compare a backup's "Backup completed in" time with the 1:48 before. Place a Steam 'n' Rails track and brew in a Brewin' and Chewin' keg (Strata Tweaks only skips their data fixers for structure pieces). CurseForge: `mods/strata-tweaks-*.jar` is a plain jar in the zip's overrides, which CurseForge rejects unless approved (like Drive-By-Wire); keep the upload off or publish the mod.

## Watch
- **Server crash at 21:43 on Nov 6** (entity tracking map changed mid-tick, `ChunkMap.tick`): not explained by the Cloudy Temple fix in 1.4.0. If it happens again, keep the crash report.

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
4. If `python -I tools/structure-templates/datapack.py check <datapack> <mods dir>` reports anything (or the datapack isn't on the server yet), regenerate it and copy it to the server's `world/datapacks/strata_templates` before restarting. On the server, add `JVM_OPTS: "-Dneoforge.readTimeout=120"` under `environment:` in `/opt/minecraft/strata/compose.yml` (back it up first); a compose change needs `docker compose up -d`, not just a restart. After any `up -d`, check `docker exec strata cat /proc/sys/net/ipv4/tcp_congestion_control` prints `bbr` (the compose `sysctls`, Nov 8). Wait about 5 minutes for GitHub's raw-file cache, then restart the server (Quarry restart, or `docker compose restart`
   in `/opt/minecraft/strata`). Check the log for `Loaded N/N KubeJS server scripts ... 0 errors`.
5. Tell the group to import the new `.mrpack`.

Note: `config/DistantHorizons.toml` and `config/cameraoverhaul.toml` are `preserve = true`, so players who already have
them keep their own copy. Changes there only reach new installs.
