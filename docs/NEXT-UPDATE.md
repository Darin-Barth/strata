# Queued for the next update

Changes committed on master since the last release (**v1.3.0**; notes in the GitHub release) that haven't been released yet. Policy: changes ship together in one update (merge to `master` + new `.mrpack` release + server restart); only a critical hotfix goes out on its own. Queued work can be backed up to the GitHub branch `next-update` (`git push origin master:refs/heads/next-update`); the server only follows `master`.

## Changes
- **Crimson Blade crash workaround (NOT TESTED, not shipped; Darin: hold):** Forsaken Relics 1.0.1 crashed the server five times (Oct 30 22:40; Nov 1 01:31, 01:42, 01:43, 01:48): a mob killed by the blade's Bleed curse changes the mod's list of cursed mobs while the mod is walking through it (`ConcurrentModificationException` in `CrimsonBladeItem.tickCurses`). `kubejs/server_scripts/strata_crimson_blade.js` cancels the bleed damage (indirect magic, player as attacker and direct source, on ticks divisible by 20) and deals it one tick later, outside that loop. **Test before shipping:** reproduce the crash without the script (fake player with a Crimson Blade in Bleed mode, several zombies hit until cursed, then their health set to 1), then confirm with the script: no crash, the mobs still bleed and die, Hemorrhage still spreads, KubeJS 0 errors, and other magic damage (Iron's spells, potions) is unchanged. Ship as a server-only hotfix (1.3.1).

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
