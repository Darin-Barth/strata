# Queued for the next update

Changes committed on master since the last release (**v1.2.1**; notes in the GitHub release) that haven't been released yet. Policy: changes ship together in one update (merge to `master` + new `.mrpack` release + server restart); only a critical hotfix goes out on its own. Queued work can be backed up to the GitHub branch `next-update` (`git push origin master:refs/heads/next-update`); the server only follows `master`.

## Changes
- **Mob spawn overlay:** More Overlays Updated (client). F7 marks blocks where monsters can spawn (yellow X at night, red X any time); F9 shows chunk borders.
- **Longer days:** a day takes 30 minutes instead of 20: 20 minutes of daylight, 10 of night, with sunrise and sunset split between them (`kubejs/server_scripts/strata_daylight.js`; `doDaylightCycle` stays on, the script holds the clock back on some ticks and syncs clients).
- **Slower seasons:** Serene Seasons no longer moves on while nobody is online (`progress_season_while_offline = false`; it ran 24/7 on the server, a new season about every 8 hours of real time), and its day length matches the 30-minute day (`day_duration = 36000`). A season is 24 days, about 12 hours of play. Changing the day length can move the live world back a season or two (Serene Seasons saves a tick count, which now reads as fewer, longer days): mention it in the notes, or set it with `/season set` after the restart.
- **Less rain:** Serene Seasons' dry spells between rains are back to vanilla's in spring, summer and autumn (10 minutes to 2.5 hours; they were cut to at most 1 h 20 in spring and summer) and longer in winter (20 minutes to 1.5 hours, was 10 to 30 minutes).
- **Crafting on a Stick:** crafting table, anvil, smithing table, stonecutter, loom, grindstone and cartography table on a stick (stick + the workbench). Use it in hand, or put it in its own Curios slot (Alt+G) and press **Shift+C** to open it (moved off the mod's V on Nov 1: V also fires item-only keys like MekaSuit, Ad Astra suit and wands; Shift+C only shares with Draconic tool modules while holding a Draconic tool).
- **Simple Voice Chat removed:** the group uses Discord. Its key script (`strata_voice_keys.js`, the unbound-key stutter fix) and default keys are gone with it. Players who already have the old keys keep them in `options.txt`; existing players get the new Shift+C only with Reset All (or rebind it).
- **Umbrella slot (Lopez):** Vampires Need Umbrellas umbrellas go in their own Curios slot (Alt+G) and shade a vampire from the sun from there, so both hands stay free. The mod ships the slot but never gives it to players; `kubejs/data/strata/curios/entities/umbrella.json` does. Tested on the test server: the slot is on players, takes all 65 umbrellas, and the mod finds an umbrella in it. **Test:** a vampire in daylight with the umbrella in the slot gets no sun damage, and the umbrella wears down.
- **Sleeping bag slot:** a Comforts sleeping bag goes in its own Curios slot (Alt+G); **Alt+S** lays it out one block in front of you and you go to sleep, and it packs itself back into the slot when you wake (`kubejs/*/strata_sleeping_bag.js`, slot in `kubejs/data/strata/curios`). Night only, like placing it by hand. **Test:** placement on flat and uneven ground, daytime refusal (bag must come back), monsters nearby, breaking the bag while asleep, logging out asleep, the key in Options > Controls, and the slot icon.
- **Legendary ink back to default:** Iron's Spells' legendary ink is brewed with amethyst again (Epic Ink + amethyst shard in the Alchemist Cauldron). Boss gate M5 (dragon blood) is dropped: removed from `tools/gates/build_magic.py`, its override and the `strata:dragon_bloods` tag deleted, `docs/gate-map.md` updated.
- **EMI info pages for Iron's Spells' cauldron:** inks, elixirs, Ice Venom, Timeless Slurry and Bloody Vellum get an info page in EMI with their Alchemist Cauldron recipe (`kubejs/client_scripts/strata_emi_info.js`). The cauldron brews liquids, so looking up the bottle found no recipe. **Test:** the pages show (EMI, press R on Legendary Ink).
- **Less lag: The Ravenous removed.** Its code searched 70 blocks around every mob, item and item frame, every tick, in every dimension (a broken check meant it never skipped anything that wasn't a Ravenous), on the server and on players' computers. It was the largest single cost left in the server's tick after 1.2.1 (8 of 50 busy samples; no other mod over 2). The Hollow loses the Ravenous and its Screechers: the quests *Something Is Listening*, *Sound Walls* and *The Ravenous* are gone, Sanctuary follows the Pale Beacon directly, and the beacon's upgrade now takes an **Echo Shard** instead of the echolocation organ (a beacon already upgraded stays upgraded). Nothing in the Hollow eats blocks any more. (Needs the new `.mrpack` and the server restart.) **Test:** KubeJS loads with 0 errors, the Hollow quest chapter opens, the beacon takes an Echo Shard.
- **What Are They Up To shows other players' screens again:** the little screen in front of a player who has their inventory, a chest, a crafting table and so on open never appeared, only the raised hands. WATUT copies the player's real screen and shrinks it with its own blur shader, and in this pack that step draws nothing (tested Nov 1: the copy of the inventory is right, the shrunk image is empty, with or without Iris shaders; WATUT's shaders load, so some other rendering mod gets in the way). `config/watut-server.toml` now sets `dynamicGuiUseOldSimpleGUIVisual = true`: WATUT's own pictures of an inventory, chest, crafting table, furnace etc. instead of a live copy of the screen. The typing bubble in front of a player was already working (tested with and without shaders).
- **/tpa for everyone:** `/tpa <player>` asks to go to a player, `/tpahere <player>` asks them to come to you; they answer with `/tpaccept` or `/tpdeny` (or the chat buttons). Works across dimensions; requests last 60 seconds; a teleported player waits 10 seconds before the next one (`kubejs/server_scripts/strata_tpa.js`). Welcome quest, README and joining guide updated. **Test:** both directions, across dimensions, deny, expiry, the target logging off, the chat buttons, tab-completion of names.

## Client tests (Nov 1, morning)
Test client on the rehearsal server, with Complementary Unbound shaders on and off.

**Passed**
- Join: about 35 s from Connect to in-game (the client needs more than 6 GB of memory: it ran out loading resource packs at 6 GB, fine at 10 GB).
- EMI: Legendary Ink has its info page (Alchemist Cauldron recipe) next to its loot tabs.
- F7 turns the spawn overlay on, F9 cycles chunk borders (corners, grid, off).
- Sleeping bag key (real key press on the test client, bound to Scroll Lock for the test): lays the bag out, you fall asleep, the night fast-forwards (Seamless Sleep) and you wake at dawn with the bag back in its slot.
- Sun: the clock moves 0.55 ticks per tick by day and steps back by one tick now and then when the server corrects it (1/24000 of a day, invisible).
- /tpa: the request shows **[Accept]** and **[Deny]** buttons that run /tpaccept and /tpdeny; /tpaccept from the real client answers.
- The Hollow quest chapter opens with its 24 quests.
- Umbrella slot: the umbrella sits in its own slot and gives Sunscreen from there.
- WATUT: typing bubble shows in front of another player (shaders on and off); with the setting above, the inventory picture shows too.

**Bugs found and fixed**
- After a night in the sleeping bag, the bag landed in the main inventory, not the slot (Comforts packs an auto-used bag into the inventory itself), so the next Alt+S found the slot empty: `strata_sleeping_bag.js` moves it back into the slot.
- WATUT's live screen copy is blank (above).

**Found, not fixed (Darin's call)**
- Draconic Evolution's tool keys sit on **C** (tool config) and **Shift+C** (tool modules), and they fire with no Draconic tool: every C press (Iron's spell wheel) also prints "You don't have any configurable items in your inventory!", and Shift+C, the new Crafting on a Stick key, will too.

**Not tested** (needs a real keyboard: Shift, Ctrl and Alt can't be faked into the game window)
- Shift+C opening the Crafting on a Stick workbench; Alt+S itself (the key behind it works).
- /tpa between two real players across dimensions (only a stand-in player here).

## Rehearsal (Nov 1, overnight)
Fresh server and fresh client installed from this build, plus a copy of the 1.2.0 rehearsal server upgraded to it.

**Passed**
- Server boots, KubeJS 0 errors (startup 13, server 28 incl. the test script); upgrade from 1.2.0 deletes The Ravenous, Simple Voice Chat, Whispering Spirits and the legendary-ink override, adds Crafting on a Stick; no new errors in the log (the rest were already there in 1.2.0).
- Client starts with no crash; KubeJS client scripts 0 errors; default keys applied: F7/F9 More Overlays, V Crafting on a Stick (since moved to Shift+C, not yet re-tested), Alt+S sleeping bag.
- Day length measured: 0.542 clock ticks per tick by day, 0.916 by night (20 + 10 minutes).
- Seasons: `day_duration` 36000, not moving while empty; rain intervals as planned (winter 20 min–1.5 h, rest vanilla).
- All 17 gated recipes carry their gate items (M1–M4, M7–M21 incl. Theurgy); legendary ink is amethyst again.
- Sleeping bag slot: registered (size 1, icon), takes all 16 Comforts bags. Key logic (fake player): lays the bag one block ahead, empties the slot, keeps the held item; packs both halves back into the slot; blocked ground leaves it in the slot; a bag broken while out just drops.
- Pale Beacon: Ember lights it, Echo Shard upgrades it, a second shard is refused and kept.
- /tpa: commands registered; accept, deny, expired and offline-requester paths run cleanly.
- Crafting on a Stick: 9 items and recipes; its Curios slot exists.

**Bugs found and fixed**
- TooManyRecipeViewers made every client fail to load (it declares JEI 19.27; Polymorph, Sophisticated Core and FramedBlocks need newer): removed again.
- 30-minute day did nothing (`level.dayTime` is a function in KubeJS): fixed.
- Sleeping bag key threw for everyone (`getDirection()` is hidden in KubeJS): fixed.
- /tpaccept and /tpdeny threw for everyone (`server.getPlayer(name)` throws): fixed.

**Still to test with real players** (the overnight client couldn't render with the PC's display off)
- Join time; EMI info page on Legendary Ink; gate items visible in EMI.
- Alt+S at night: you actually fall asleep, and wake with the bag back in the slot; in daytime the bag comes straight back.
- Shift+C opens the Crafting on a Stick workbench, and plain C still opens the Iron's spell wheel.
- F7 / F9 overlays; the sun moving smoothly (no jumps); sleeping through the night still skips to morning.
- /tpa and /tpahere between two players, across dimensions, with the chat buttons.
- Hollow quest chapter opens.

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
