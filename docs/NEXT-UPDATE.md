# Queued for the next update

Changes committed on master since the last release (**v1.2.1**; notes in the GitHub release) that haven't been released yet. Policy: changes ship together in one update (merge to `master` + new `.mrpack` release + server restart); only a critical hotfix goes out on its own. Queued work can be backed up to the GitHub branch `next-update` (`git push origin master:refs/heads/next-update`); the server only follows `master`.

## Changes
- **Mob spawn overlay:** More Overlays Updated (client). F7 marks blocks where monsters can spawn (yellow X at night, red X any time); F9 shows chunk borders.
- **Longer days:** a day takes 30 minutes instead of 20: 20 minutes of daylight, 10 of night, with sunrise and sunset split between them (`kubejs/server_scripts/strata_daylight.js`; `doDaylightCycle` stays on, the script holds the clock back on some ticks and syncs clients).
- **Slower seasons:** Serene Seasons no longer moves on while nobody is online (`progress_season_while_offline = false`; it ran 24/7 on the server, a new season about every 8 hours of real time), and its day length matches the 30-minute day (`day_duration = 36000`). A season is 24 days, about 12 hours of play. Changing the day length can move the live world back a season or two (Serene Seasons saves a tick count, which now reads as fewer, longer days): mention it in the notes, or set it with `/season set` after the restart.

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
