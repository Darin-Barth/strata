# Queued for the next update

Changes committed on master since the last release (**v1.0.0**; notes in the GitHub release) that haven't been released yet. Policy: changes ship together in one update (merge to `master` + new `.mrpack` release + server restart); only a critical hotfix goes out on its own. Queued work can be backed up to the GitHub branch `next-update` (`git push origin master:refs/heads/next-update`); the server only follows `master`.

## Changes
- **No mob griefing of terrain:** creeper explosions (vanilla and modded creepers) still hurt, but break no blocks; endermen can't pick up blocks. TNT and other explosions are unchanged. (Server side: takes effect with a server restart.)
- **Voice chat keys have defaults: push-to-talk on Caps Lock, whisper on Right Alt** (new installs and players who never set them): left unbound, the game logged an error every tick and stuttered. Players with an older install: bind both in Options > Controls.
- **No more "replace failed" warnings:** Inventory Profiles Next's big on-screen and sound alerts when a tool is about to break, or can't be swapped for a spare, are off. Its auto-refill still works. (Client side: comes with the next `.mrpack`.)
- **New way to collect the End portal eyes:** no more random eyes in chests. Every eye has one guaranteed source: 5 bosses (Elder Guardian, Wither, Ignis, Netherite Monstrosity, Harbinger), 5 treasure rooms (Pharaoh's tomb, jungle temple, Foundry, pirate ships, Frostbitten Temple), one eye forged on a Create assembly line and quenched and one bound and awakened with Ars Nouveau, plus 3 spare eyes to craft. Craftable **Seeker's Compasses** point to the places. The End quest chapter is rewritten as a step-by-step guide, and each eye's tooltip tells its legend. Details: `docs/end-eyes.md`. (Server and client: comes with the next `.mrpack`.)
- **Pet food explained:** pets only eat from a Feed Bag in your inventory (with the pet in your hotbar), never loose food. The pets quest now says so, and the Feed Bag quest is no longer optional.

## Check before this release
- **In a game client** (server boots don't run client code): the Rogue Eye family's textures (Incomplete, Red-Hot, the new Rogue Eye, the eye in a portal frame), the Dormant Magical Eye, the eyes' lore tooltips, and a **Seeker's Compass** right-click on a server: the message appears, the needle turns, and the server doesn't stall (searches run a few ms per tick; tested on a server only).

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
