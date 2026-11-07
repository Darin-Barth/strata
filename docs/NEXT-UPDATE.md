# Queued for the next update

Changes committed on master since the last release (**v1.3.0**; notes in the GitHub release) that haven't been released yet. Policy: changes ship together in one update (merge to `master` + new `.mrpack` release + server restart); only a critical hotfix goes out on its own. Queued work can be backed up to the GitHub branch `next-update` (`git push origin master:refs/heads/next-update`); the server only follows `master`.

## Changes
- **JEI back: machine recipes show in EMI again** (tested Nov 4). Create (pressing, mixing, compacting, deploying...), Immersive Engineering, Diesel Generators (plant oil, fermenting, distillation), Apprentice Codex's Essence Smoker and many others only register their recipes with JEI; EMI shows them when JEI is installed (EMI hides JEI's own screen). Test join: 261 JEI categories read, 355,783 recipes in EMI (247,848 before), no kick. JEI 19.69.0.457 is pinned (19.70 crashes against All The Leaks' JEI mixin) with MezzConfig. Cost: joining takes longer and the first minute or so is choppy (JEI froze the client 32 s on a fast PC; EMI's reload went from about 57 s to 108 s).
  **Server start option needed at release:** JEI's freeze is why players timed out on Oct 25: the server drops a client that sends nothing for 30 s. Add `-Dneoforge.readTimeout=120` to the server's Java options (`JVM_OPTS` in the Docker setup) *before* restarting on this version, or slower PCs get kicked while joining. The same limit dropped a far-away player (Europe) on Nov 5: when she joins an empty server, the step after sign-in takes about 45 s instead of 8 s, and one try timed out at 58 s.
- **Server freezes fixed (already live, Nov 1):** the server crashed three times in 15 minutes (12:44, 12:52, 12:56): its main thread spent over 60 s loading saved chunks and the watchdog shut it down. Distant Horizons on the server (`generatorPlan = "SURFACE_THEN_CHUNKS"`) loaded real chunks for every player's distant view, and Eric exploring far north flooded it. Now `SURFACE_ONLY`: distant land is drawn from a quick terrain pass on DH's own threads, no chunk loads. Changed on the live server directly (backup `config/DistantHorizons.toml.bak-20261101-1257`) and in the pack's copy for new installs. Distant views lose trees and buildings past the normal view distance.
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
