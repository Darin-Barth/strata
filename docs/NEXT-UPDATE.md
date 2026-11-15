# Queued for the next update

Changes committed on master since the last release (**v1.4.2**; notes in the GitHub release) that haven't been released yet. Policy: changes ship together in one update (merge to `master` + new `.mrpack` release + server restart); only a critical hotfix goes out on its own. Queued work can be backed up to the GitHub branch `next-update` (`git push origin master:refs/heads/next-update`); the server only follows `master`.

## Changes
- **Fewer and shorter freezes while exploring (Darin, Nov 14; tested Nov 14 on a test server):** spark on the live server showed 2-30 s freezes whenever players explored. Mob spawning looks up which structure a spot belongs to, which loads that structure's saved pieces on the main thread, and Steam 'n' Rails and Brewin' and Chewin' each run an extra full data-fixer pass over every piece. The pack now ships its own small mod, **Strata Tweaks** (`mods/strata-tweaks-1.0.0.jar`, source in `tools/strata-tweaks/`), which skips those two passes for structure pieces. Tested: 300 real pieces read in 3.9-5.4 s instead of 8.2-8.9 s, with identical results. Not yet checked: a client launch with the mod (it loads on both sides).
- **Hostile mob cap 56 instead of 70 (Darin, Nov 14; tested Nov 14 on a test server):** Strata Tweaks scales the natural monster cap by 0.8 (`config/strata_tweaks-common.toml`): fewer spawn attempts and fewer mobs to tick, which were the biggest steady costs. Animals are unchanged. Tested: the cap reads 56, animals 10.
- **Incendium only scans Nether mobs (Darin, Nov 14; tested Nov 14 on a test server):** Incendium's every-tick function walked every mob in every dimension three times (about 5% of tick time on the live server). Those scans now run in the Nether only (`tools/build_incendium_clock.py`); its mobs and structures only exist there. Tested: a pig in the Nether still gets Incendium's tags, one in the Overworld doesn't.

## Still to check in play (released untested)
- Tested and working in play (Darin, Nov 8): /spawn and YouTube links on WATERFrAMES. /spawn from the Nether and its 10 s cooldown tested Nov 12 on a test server (a second use within 10 s is refused).
- **Fairy Lights:** loads without errors, and right-clicking a fence with hanging lights attaches a string (test server, Nov 12). Still to check in game: finishing the string on a second fence, then one on an assembled airship in flight.
- **1.4.2 (Nov 14):** single-player world creation on an install updated from before 1.4.1 (create a flat world); Excelsius leggings fall immunity worn by a player (tested on mobs only).

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
4. On the server, add `JVM_OPTS: "-Dneoforge.readTimeout=120"` under `environment:` in `/opt/minecraft/strata/compose.yml` (back it up first); a compose change needs `docker compose up -d`, not just a restart. After any `up -d`, check `docker exec strata cat /proc/sys/net/ipv4/tcp_congestion_control` prints `bbr` (the compose `sysctls`, Nov 8). Wait about 5 minutes for GitHub's raw-file cache, then restart the server (Quarry restart, or `docker compose restart`
   in `/opt/minecraft/strata`). Check the log for `Loaded N/N KubeJS server scripts ... 0 errors`.
5. Tell the group to import the new `.mrpack`.

Note: `config/DistantHorizons.toml` and `config/cameraoverhaul.toml` are `preserve = true`, so players who already have
them keep their own copy. Changes there only reach new installs.
