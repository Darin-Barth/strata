# Queued for the next update

Changes committed on master since the last release (**v0.4.3**, Oct 26, 2026; notes in the GitHub release) that haven't been released yet. Policy: changes ship together in one update (merge to `master` + new `.mrpack` release + server restart); only a critical hotfix goes out on its own. Queued work can be backed up to the GitHub branch `next-update` (`git push origin master:refs/heads/next-update`); the server only follows `master`.

## Changes
- **Less memory:** Every Compat no longer makes Chipped, Rechiseled, Macaw's Furniture and Handcrafted copies in modded woods (23,002 fewer blocks; 872 MB less on the server, likely 1-1.5 GB less in your game). It also drops its Quark (posts, ladders, chests...) and Another Furniture copies in modded woods: 760k fewer block states, so a lighter, faster-loading game. Quark's and Another Furniture's own blocks stay. Those blocks disappear if anyone placed them. Distant Horizons default view distance 64 chunks for new installs.

## Release checklist
1. Bump `version` in `pack.toml` and the version line in `config/fancymenu/customization/strata_title_screen.txt`.
2. `packwiz refresh`, commit, `git push` (master, and sync `next-update`). Check no stray files sit under the server's `kubejs/data`: KubeJS refuses to start on an uppercase file name there (Oct 26 outage).
3. `packwiz mr export -o build/Strata-<version>.mrpack`; `gh release create v<version>` with the notes below.
4. Wait about 5 minutes for GitHub's raw-file cache, then restart the server (Quarry restart, or `docker compose restart`
   in `/opt/minecraft/strata`). Check the log for `Loaded N/N KubeJS server scripts ... 0 errors`.
5. Tell the group to import the new `.mrpack`.

Note: `config/DistantHorizons.toml` and `config/cameraoverhaul.toml` are `preserve = true`, so players who already have
them keep their own copy. Changes there only reach new installs.
