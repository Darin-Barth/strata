# Pre-upgraded structure templates (`strata_templates` datapack)

Server-only. Not part of the player pack and not in this repo (216 MB, 11,500 templates on Nov 14): it lives in the
server's `world/datapacks/strata_templates/`. A local copy of the last build is kept in `build/strata_templates.zip`
(git-ignored).

## Why
Most structure mods ship their templates (saved building pieces, `data/<mod>/structure/**.nbt`) in an older Minecraft
data format. Every time the server first needs one after a restart, it upgrades it through the data fixer on the main
thread: 10-30 ms for a small piece, tens of seconds and gigabytes of memory for the biggest (IDAS' Collectors Museum,
Legendary Monsters' space station). While players explore, that showed up as 2-30 s freezes (spark, Nov 14). This
datapack holds the same templates already saved in the current format, so the server reads them without upgrading.
Strata Tweaks (`tools/strata-tweaks`) removes two mods' extra passes; this removes vanilla's.

Tested Nov 14 on a test server: 300 Dungeons and Taverns / When Dungeons Arise / CTOV templates read in 0.13-0.19 s
from the datapack against 3.5 s from the mod jars (8.2-8.9 s without Strata Tweaks), with identical results; the
datapack is enabled automatically and wins over the mod jars. IDAS' Collectors Museum reads in under 1 s plus 4 s
of NBT decoding (the original ran a 10 GB server out of memory); Legendary Monsters' space station (6 million
blocks) still takes about 6 s, which is its size. `/place` of upgraded templates and structures works. The
"Tried to load invalid item/fluid" errors when IDAS' castle is placed come from the mod's own file (same 24 with the
original).

## Regenerating (after any update that changes a mod with structures)
`python -I tools/structure-templates/datapack.py check <datapack> <mods dir>` lists templates whose original changed.
A stale copy overrides the mod's new piece, so regenerate whenever it reports anything:

1. On a local test server with the full pack (18 GB heap: `-Xmx18G`, the big pieces need it, and
   `max-tick-time=-1`), copy `zz_tplgen.js` and
   a scratch eval command into `kubejs/server_scripts/` (never into the pack). Make sure no `strata_templates`
   datapack is active in that server's world, or the generator would read its own output.
2. Run `tplRun(server, 60)` through the eval command over RCON until it reports `next=<total>/<total>` (a batch of 60
   keeps each tick under the watchdog; resumable, it skips files that already exist). Output:
   `<server>/tpl_out/strata_templates/data/...`.
3. `python -I tools/structure-templates/datapack.py finish <server>/tpl_out/strata_templates <mods dir>` writes
   `pack.mcmeta` and `manifest.json`.
4. Replace `world/datapacks/strata_templates` on the server with it and restart (new datapacks in that folder are
   enabled automatically).

Only templates older than the current data version are included; current ones are left to the mods.
