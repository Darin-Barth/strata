# Queued for the next update

Changes committed on master since the last release (**v0.4.3**, Oct 26, 2026; notes in the GitHub release) that haven't been released yet. This release will be **v0.5.0** (Darin, Oct 27; version already set in `pack.toml` and the title screen). Policy: changes ship together in one update (merge to `master` + new `.mrpack` release + server restart); only a critical hotfix goes out on its own. Queued work can be backed up to the GitHub branch `next-update` (`git push origin master:refs/heads/next-update`); the server only follows `master`.

## Changes
- **Less memory:** Every Compat no longer makes Chipped, Rechiseled, Macaw's Furniture and Handcrafted copies in modded woods (23,002 fewer blocks; 872 MB less on the server, likely 1-1.5 GB less in your game). It also drops its Quark (posts, ladders, chests...) and Another Furniture copies in modded woods: 760k fewer block states, so a lighter, faster-loading game. Quark's and Another Furniture's own blocks stay. Those blocks disappear if anyone placed them. Distant Horizons default view distance 64 chunks for new installs.
- **Rhino** 2101.2.7-build.85 → 2101.2.8-build.91 (the build CurseForge also hosts; KubeJS needs ≥ build.81; test server: 7/7 startup and 14/14 server scripts, 0 errors).
- **CurseForge export (for the pack's maintainers):** every Modrinth mod now also carries its CurseForge file ID (`tools/curseforge_ids.py`), so `packwiz cf export` builds a CurseForge zip next to the `.mrpack`. A GitHub Action builds that zip for every GitHub release, attaches it, and can upload it to CurseForge. Nothing changes for players or the server.
- **CobbleStructures and Sunken Spires are server-only** (data only: structures and loot, no client files). Nothing changes on the server; players' downloads drop two files. Single-player worlds from the client pack won't get those structures.
- **Serene Seasons 10.1.0.9 → 10.1.0.3** (Darin, Oct 27): the newest 1.21.1 build on CurseForge, so both versions of the pack match. Test server: boots clean, seasons change normally. **Watch for:** a crash with `StackOverflowError` mentioning `sereneseasons` / `MixinBiomeClient` / `hasPrecipitation` (fixed in 10.1.0.9, #613). If it shows up, go back to 10.1.0.9 on Modrinth.
- **Inventory Pets are found, not crafted** (Darin, Oct 27): pet recipes and the Petrifier are gone. Pets now turn up in structure chests: cozy pets in dungeons, mineshafts and temples; handy ones (Anvil, Furnace, Pingot, Juggernaut...) in strongholds, mansions and fortresses; the legendary six (Black Hole, Slime, Wither, Sun, Cloud, Pufferfish) only in End cities, ancient cities, bastion treasure and ominous trial vaults. Strong pets are weaker: Juggernaut and Illuminati cooldowns are 10 minutes, Pac-Man's damage boost builds slower, the Pingot finds ore but doesn't dig it out, and several strong pets eat costlier food (diamond, emerald, ender or netherite nuggets, golden carrots, iron ingots). Pets you already have keep working.
- **MineColonies** (Darin, Oct 27): build and run a colony of NPC workers. Adds Structurize, Domum Ornamentum, BlockUI, Multi-Piston and TownTalk (colonist voices), all pinned to the tested versions. Cost measured on the test server and a test client: +94 MB server memory, +7-9 s server start, about +2 s game load, +133 MB download. Teleporting to allied Town Halls is off (limited-teleport rule); MineColonies' `/mc rtp`, colony and home teleports are off by default. Colonies get raided every 10-14 nights once founded. Not measured: server load from a busy colony. No quest chapter yet.
- **Skill trees reworked** (Ctrl+K; Darin, Oct 27; `docs/skill-trees-rework.md`): fewer, bigger nodes and keystones that change how you play. Combat has four branches (Warrior: life steal; Ranger: arrow speed and armor pierce; Guardian: dodge; Duelist: crits) and 25 levels for a 33-point tree, so you choose. Mining XP now comes from every ore in the pack, not only vanilla ones, with whole Fortune levels, a shovel/axe keystone and an experience branch. Fishing values doubled, new Sea Legs keystone. Iron's magic trees need a third of the XP, nodes are twice as strong (the first tree has 25 levels instead of 50) and the gateway nodes give -10% cooldowns or +10% spell power. Points you already spent may be reset by the change.

## Release checklist
1. Check `version` in `pack.toml` and the version line in `config/fancymenu/customization/strata_title_screen.txt` (both 0.5.0).
2. `python -I tools/curseforge_ids.py` (re-adds CurseForge IDs after mod updates; fix any "no longer used" line in
   `tools/curseforge-manual.json`), `packwiz refresh`, commit, `git push` (master, and sync `next-update`). Check no stray files sit under the server's `kubejs/data`: KubeJS refuses to start on an uppercase file name there (Oct 26 outage).
3. `packwiz mr export -o build/Strata-<version>.mrpack`; `gh release create v<version>` with the notes below.
   The CurseForge Action (`.github/workflows/curseforge.yml`) then builds `Strata-<version>-curseforge.zip`, attaches
   it to the release and, when the repo variable `CURSEFORGE_UPLOAD` is `true`, uploads it to CurseForge with the
   release notes as the changelog (CurseForge reviews it before it goes public). One-time setup by Darin: secret
   `CURSEFORGE_TOKEN`, variables `CURSEFORGE_PROJECT_ID` and `CURSEFORGE_UPLOAD`; leave the upload off until
   Drive-By-Wire is on CurseForge's approved list (requested Oct 27), or CurseForge rejects the file. To upload a
   release that's already out: Actions → CurseForge → Run workflow with its tag.
4. Wait about 5 minutes for GitHub's raw-file cache, then restart the server (Quarry restart, or `docker compose restart`
   in `/opt/minecraft/strata`). Check the log for `Loaded N/N KubeJS server scripts ... 0 errors`.
5. Tell the group to import the new `.mrpack`.

Note: `config/DistantHorizons.toml` and `config/cameraoverhaul.toml` are `preserve = true`, so players who already have
them keep their own copy. Changes there only reach new installs.
