# Strata Tweaks

Strata's own small NeoForge mod (`mods/strata-tweaks-<version>.jar`, shipped as a plain file in the pack, so it lands in
both the `.mrpack` and the CurseForge zip's overrides). Config: `config/strata_tweaks-common.toml`.

## What it does
- **Structure templates read faster (Nov 14).** Steam 'n' Rails (`DataFixesInternalsImpl.updateWithAllFixers`) and
  Brewin' and Chewin' (`BnCDataFixer.updateWithFixers`) each run their own full data-fixer pass over everything vanilla
  upgrades. For structure templates (saved building pieces, `DataFixTypes.STRUCTURE`) that pass is skipped
  (`skipModStructureFixers`). Templates are read on the main thread when mob spawning looks up a structure in a chunk
  that isn't loaded yet; the live server froze for 2-30 s at a time while players explored (spark, Nov 14).
  Tested on a test server with 300 Dungeons and Taverns / When Dungeons Arise / CTOV templates: 8.2-8.9 s with the
  passes, 3.9-5.4 s without, and the resulting templates were identical. Only an old template that contains one of
  those two mods' renamed blocks would lose the rename.
- **Hostile mob cap x0.8 (Nov 14).** `monsterCapScale` scales the natural monster cap (vanilla 70, now 56): fewer spawn
  attempts and fewer mobs to tick. Animals and other categories are unchanged.

Each mod-specific mixin only applies when that mod is installed (`mixin/Plugin.java`).

## Building
No Gradle. With a JDK 21 and an installed NeoForge 21.1 server's `libraries/` folder:

    python -I tools/strata-tweaks/build.py <JDK 21 home> <server>/libraries

Bump `version` in `resources/META-INF/neoforge.mods.toml` for every change (the build replaces the old jar), then
`packwiz refresh`. Re-check after a Steam 'n' Rails or Brewin' and Chewin' update: a renamed method makes the mixin
fail at startup (`defaultRequire: 1`), which is deliberate.
