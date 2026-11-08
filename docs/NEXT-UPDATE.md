# Queued for the next update

Changes committed on master since the last release (**v1.4.0**; notes in the GitHub release) that haven't been released yet. Policy: changes ship together in one update (merge to `master` + new `.mrpack` release + server restart); only a critical hotfix goes out on its own. Queued work can be backed up to the GitHub branch `next-update` (`git push origin master:refs/heads/next-update`); the server only follows `master`.

## Changes
- **Far players stuck on "Loading terrain" (already live, Nov 8):** a player in Scotland (150 ms, about 2% packet loss on the route) got 20-40 KB/s from the server: standard TCP congestion control (CUBIC) cut its sending window to 2-3 packets on every loss, so terrain never finished loading and the player rubber-banded and dropped. The server's Docker container now uses BBR (`sysctls: net.ipv4.tcp_congestion_control: bbr`, host module `tcp_bbr` loaded at boot): the same player got 110-380 KB/s, loaded in and played. Server-side only.
- **/spawn for everyone (Darin, Nov 8; NOT TESTED yet):** `/spawn` takes a player back to the world spawn (the Tavern village) from any dimension, with a 10-second cooldown like `/home` (its own timer; `kubejs/server_scripts/strata_spawn.js`, server-only). Welcome quest, README, joining guide and design doc mention it. **Test:** from the Nether, /spawn lands at the world spawn on its block; a second /spawn within 10 s is refused; KubeJS 0 errors.
- **YouTube on WATERFrAMES screens (Darin, Nov 7; NOT TESTED yet):** a YouTube link on a frame or TV failed with `NoImageException`: WaterMedia 2.1.37 has no YouTube support of its own (Twitch, Kick, Drive, Dropbox and the like only). Added WATERMeDIA: Youtube Extension 2.1.2, client only, pinned (it requires WaterMedia 2.1.37 to below 2.2; WaterMedia stays pinned, and moving to WaterMedia 3 means the 3.0 extension and a WATERFrAMES check). It is 10 months old and YouTube changes can break it. **Test:** client boot, a youtu.be link and a youtube.com/watch link on a frame play with sound.
- **Fairy Lights (Darin, Nov 7; NOT TESTED yet: boot and join test before release):** Rafacasari's fork of Fairy Lights 1.3.1 (hanging string lights, buntings and garlands; MC Eternal 2 had the original). Picked over the lucalabs-de port for its Sable support (lights on Create Aeronautics ships) and Flywheel rendering. Needs only NeoForge; both sides, so everyone imports the new pack. On CurseForge too (same file). **Test:** server boot (KubeJS 0 errors), client join, hang a string between two fences, then hang one on an assembled airship and fly it.

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
4. On the server, add `JVM_OPTS: "-Dneoforge.readTimeout=120"` under `environment:` in `/opt/minecraft/strata/compose.yml` (back it up first); a compose change needs `docker compose up -d`, not just a restart. Wait about 5 minutes for GitHub's raw-file cache, then restart the server (Quarry restart, or `docker compose restart`
   in `/opt/minecraft/strata`). Check the log for `Loaded N/N KubeJS server scripts ... 0 errors`.
5. Tell the group to import the new `.mrpack`.

Note: `config/DistantHorizons.toml` and `config/cameraoverhaul.toml` are `preserve = true`, so players who already have
them keep their own copy. Changes there only reach new installs.
