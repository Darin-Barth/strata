# Queued for the next update

Changes committed on master since the last release (**v1.4.1**; notes in the GitHub release) that haven't been released yet. Policy: changes ship together in one update (merge to `master` + new `.mrpack` release + server restart); only a critical hotfix goes out on its own. Queued work can be backed up to the GitHub branch `next-update` (`git push origin master:refs/heads/next-update`); the server only follows `master`.

## Changes
- **Mod crops compost again (Darin, Nov 10; NOT TESTED yet):** Critters and Companions' acorn showed a 30% composting chance in EMI but the composter refused it. NeoForge's composter only reads the `neoforge:compostables` data map; a few mods still add their items to vanilla's old `ComposterBlock.COMPOSTABLES` map, which only EMI reads now. A scan of every mod jar found 174 such items: all of Croptopia's crops, seeds, fruits and saplings (167), Alex's Mobs' banana, banana peel, acacia blossom and gongylidia, Friends & Foes' buttercup, the acorn, and Naturalist's snail shell (its data map file sits at a path NeoForge never reads). `tools/build_compostables.py <mods dir>` writes them into `kubejs/data/neoforge/data_maps/item/compostables.json` with each mod's own chances (merges with the other entries; re-run after one of those mods updates). Fine already: Ars Nouveau, Immersive Engineering, Integrated Dynamics and Regions Unexplored ship the data map too, and Let's Do Vinery patches the composter. Not covered: Every Compat's generated Quark/Regions Unexplored wood variants (created at runtime, can't be listed from the jars). **Test:** acorns, a Croptopia crop and seed, and a banana go into a composter.
- **Less lag while exploring (Darin, Nov 11; NOT TESTED yet):** boating through existing land rubberbanded, with the server stalling 2-15 s every 15-20 s. A spark profile of the slow ticks showed about 12% of them spent loading chunks, nearly all of it re-reading structure templates and running them through the data fixer on the main thread. ModernFix's `dynamic_structure_manager` (on by default) keeps templates as soft references that Java drops under memory pressure, so each one is read and converted again and again. Now off in `config/modernfix-mixins.properties`: templates stay loaded after the first read (a little more memory). Needs a server restart. **Test:** after the update, boat through explored land and check the log for "Can't keep up" and "moved too quickly".

## Untested in 1.4.1 (released untested, Darin Nov 8)
- Tested and working in play (Darin, Nov 8): /spawn and YouTube links on WATERFrAMES. (Not checked yet: /spawn from the Nether and its 10 s cooldown.)
- **Fairy Lights:** a string between two fences, then one on an assembled airship in flight.

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
