# Queued for the next update

Changes committed on master since the last release (**v0.3.0**, Oct 26, 2026) that haven't been released yet. Policy: changes ship together in one update (merge to `master` + new `.mrpack` release + server restart); only a critical hotfix goes out on its own. Queued work can be backed up to the GitHub branch `next-update` (`git push origin master:refs/heads/next-update`); the server only follows `master`.

## Changes
- **New: skill trees** (Pufferfish's Skills 0.19.2 beta + Attributes + Unofficial Additions; Lopez's request, Darin approved Oct 26). Press the skills key (default K) to open them. Trees: **Combat** and **Mining** (Default Skill Trees; Combat capped at 40 levels in `kubejs/data/puffish_skills/.../combat/experience.json`, otherwise it never ends: a full tree is +18 hearts, +75% damage, +50% speed), **Fishing** (our own, `kubejs/data/strata/puffish_skills`: luck, breath, swim speed, a couple of hearts), and Iron's **Magic I/II + Primary/Secondary School** (spell casting gives XP; you pick one school per tier). Test server Oct 26: all three tree packs load (`Data pack ... loaded successfully`); not yet checked in-game (open the screen, earn XP from kills/mining/fishing/casting, unlock a node).

## Release checklist
1. Bump `version` in `pack.toml` and the version line in `config/fancymenu/customization/strata_title_screen.txt`.
2. `packwiz refresh`, commit, `git push` (master, and sync `next-update`). Check no stray files sit under the server's `kubejs/data`: KubeJS refuses to start on an uppercase file name there (Oct 26 outage).
3. `packwiz mr export -o build/Strata-<version>.mrpack`; `gh release create v<version>` with the notes below.
4. Wait about 5 minutes for GitHub's raw-file cache, then restart the server (Quarry restart, or `docker compose restart`
   in `/opt/minecraft/strata`). Check the log for `Loaded N/N KubeJS server scripts ... 0 errors`.
5. Tell the group to import the new `.mrpack`.

Note: `config/DistantHorizons.toml` and `config/cameraoverhaul.toml` are `preserve = true`, so players who already have
them keep their own copy. Changes there only reach new installs.
