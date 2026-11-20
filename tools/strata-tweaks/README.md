# Strata Tweaks

Strata's own small NeoForge mod (`mods/strata-tweaks-<version>.jar`, shipped as a plain file in the pack, so it lands in
both the `.mrpack` and the CurseForge zip's overrides). Config: `config/strata_tweaks-common.toml`.

## What it does
- **Whispering Spirits' look check is cheap (1.1.0).** `WhisperingSpiritsMixin` cancels the mod's per-player tick handler
  outside `strata:hollow` and on nine ticks out of ten, and shortens its ray-trace from 100 to 32 blocks. Test server,
  one player: 1.5% of the server thread at every 5th tick and 100 blocks, 0.13% now.
- **Soul Elytra boost in the elytra slot (1.1.0).** `ElytraSlotBoostMixin` / `ElytraSlotTickMixin` redirect Elytra Slot's
  read of `DeeperDarkerConfig.soulElytraCooldown` (a static int until Deeper and Darker 1.4) to `ElytraCompat`, which
  reads the config value. Verified by setting the cooldown to 123 on a test server.
- **The Hollow's fog reaches the screen (1.1.0, Nov 15; clients only).** `kubejs/startup_scripts/hollow_fog.js` hands
  `ClientFog` a fog distance and colour from the game's fog events; `FogRendererMixin` applies them at the very end of
  `FogRenderer.setupFog` / `setupColor` (mixin priority 2000). Distant Horizons, Sodium Extra and Atmospherics all
  rewrite the fog after those events, so the script alone drew nothing. `RenderSystem` is called through method handles
  because the mod is compiled against the server jar. Re-check after an update of one of those three mods.
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

    python -I tools/strata-tweaks/build.py <JDK 21 home> <server>/libraries <server>/mods/create-1.21.1-<version>.jar <launcher>/libraries

Bump `version` in `resources/META-INF/neoforge.mods.toml` for every change (the build replaces the old jar), then
`packwiz refresh`. Re-check after a Steam 'n' Rails or Brewin' and Chewin' update: a renamed method makes the mixin
fail at startup (`defaultRequire: 1`), which is deliberate.

## Added Nov 16
- `LevelSeaLevelMixin`: `Level.getSeaLevel()` returns 568 in `strata:abyssal_plain` (hard-coded 63 in 1.21.1; mob spawn rules compare against it).
- `NightVisionMixin` (client): `GameRenderer.getNightVisionScale` returns 0 in `strata:hollow`, after every other mod's patch (priority 2000).
- `AbyssalAir` (server): in `strata:abyssal_plain`, the dry space a player stands in must hold a Create: Deep Seas Oxygen Diffuser with oxygen, or it floods after a ten-second warning (docs/abyssal-plain-design.md, Rules). Config: `abyssalRoomsNeedOxygen`.
- `AbyssalAir` also pushes the water out of a closed room that holds a Diffuser with oxygen (top layer first, 1 mB per 20 cells; nothing in a space open to the sea), and checks a big room that was fine less often. `-Dstrata.tweaks.airTiming=true` logs how long each check took.
- `ShoulderSurfingPickMixin` (client): caps the entity search distance of Shoulder Surfing's crosshair pick when it is absurd (a Sable ship block's hit position is in storage coordinates), which stopped an error with a stack trace every frame.
- **Diving suit tiers (1.2.0, Nov 17).** `DivingSuit` registers the Carapace and Abyssal chestplates, leggings and platings (and, through `SuitGear`, helmets and boots that are subclasses of Create's `DivingHelmetItem` and `DivingBootsItem`, which is why the build needs Create's jar and the mod requires Create) and answers Deep Seas' questions: `DiverPressureMixin` replaces its suit test and its 280 m with the tier's depth (`divingSuitDepthCarapace`, `divingSuitDepthAbyssal`, 0 = no limit), `DeepSeasBacktanksMixin` its list of backtanks carried in the inventory (any suit chestplate, copper and netherite tanks). `TierTanks` registers the Carapace and Abyssal backtanks, copper and netherite: instances of Create's `BacktankBlock` and `BacktankItem` (with the hidden placeable block item Create uses), added to Create's backtank block entity type and given Create's stress cost. `BacktankUtilMixin` and `BacktankBlockEntityMixin` multiply their capacity by the tier (2 or 3), as an item and placed; `BacktankRendererMixin` (client) gives the ones made from a netherite tank Create's netherite cogs and shaft. Their models use Create's backtank models as parents and swap the one texture, which `art/make_art.py --create <Create jar>` paints onto the faces of Create's model (it reads only the model's layout). Recipes (`resources/data`), names and textures (`resources/assets`) ship in the jar. The textures are drawn by `art/make_art.py` (three looks per tier; `python tools/strata-tweaks/art/make_art.py carapace=c abyssal=c`, `--preview <dir>` for a contact sheet), from scratch, because Create's and Deep Seas' assets are All Rights Reserved. Tested on a test server with a player at each tier's limit.
- **Leviathan laser (1.2.0).** `DivingSuit.onIncomingDamage` scales `cataclysm:deathlaser` damage by `abyssalSuitLaserScale` (0.25) for a player in the full Abyssal suit. Test server: 10 a hit became 2.5.
- **Loot Pet chat line (1.2.0).** Inventory Pets keeps the Loot Pet's mining bonus off while FTB Ultimine is installed and said so in chat on every ore broken. `LootPetMessageMixin` drops that one line (`item.loot.ftbultimine`) in `HarvestHandler.notifyHarvest`; the bonus stays off. Re-check after an Inventory Pets update.
- **No pressure right after arriving (1.2.0).** `DivingSuit.onChangedDimension` stamps the time and `DiverPressureMixin` cancels Deep Seas' pressure tick for five seconds after it: the Abyssal Plain's portal spot is far below the crush depth and the pressure could act before the Lifepod arrival moved the player.
- **Start-up crash "Duplicate client extensions registration" (1.2.0, clients).** `ClientExtensionsMixin` makes NeoForge's `ClientExtensionsManager.register` ignore (and log) a second registration of the same extension class for the same target, which killed about one launch in ten at `create:belt`; a different class for a taken target is still an error. The mixin applying was checked by launching; the rare duplicate itself can't be forced.
- **Integrated Dynamics teleport packet (1.2.1, Nov 17).** `IntegratedDynamicsTeleportMixin` makes the server ignore `PlayerTeleportPacket` from anyone who is not an op: its handler moved the sender to any dimension and position the client named, with no check. Server-side; clients on 1.2.0 can still join.
- **Waystone waypoints only for players who activated the waystone (1.2.2, Nov 17).** Xaero's Minimap & World Map - Waystones Compatibility 2.1.0 sends its "add a waypoint" packet to the player who activates a waystone, and also to every player online whenever any waystone is renamed or edited, without looking at the dimension. `WaystoneWaypointMixin` stops `W2w2Mod.sendWaypointPacket` unless the receiver has activated that waystone and is in its dimension (Waystones is reached by reflection). Server-side; clients on an older build can still join. Waypoints already on a player's map stay until that player deletes them. The mixin applying was checked by a test server boot; not yet tried with two players.
- **Repair Talisman leaves Inventory Pets alone (1.2.2, Nov 17).** Forsaken Relics' Repair Talisman mends anything with a durability bar, and an Inventory Pet's bar is its hunger, so it fed every pet for free. `RepairTalismanMixin` makes `RepairTalismanItem.repairable` (the one test all five of its repair paths use) answer no for `inventorypets:*` items and for the item tag `strata_tweaks:repair_talisman_skips` (empty; add items there from `kubejs/data` if another case turns up). Server-side. Tested on a test server: after 90 s with the talisman in the inventory a damaged pickaxe and chestplate were repaired and two damaged pets were not.
- **The Omnistrata (1.3.0, Nov 19, Darin's idea).** One hotbar slot for six tools (`Omnistrata`, `client/OmnistrataClient`, `mixin/ToolBreakMixin`). The slot always holds a real item: put away it is the Omnistrata item with the tools in its `strata_tweaks:omnistrata_kit` component; with a tool out it is that tool itself, carrying the other five in the same component, so enchantments, durability and every mod's own test for its wrench or wand work untouched. Hold the Omnistrata key (V) for a wheel around the crosshair and let go over a tool; a quick tap goes back to the last tool; the scroll wheel steps through; letting go in the middle puts the tool away. Tools go in and out like a bundle (right-click in the inventory while it is put away). What may go in is the item tag `strata_tweaks:omnistrata_tools` (pickaxes, axes, shovels, hoes, shears, brush, flint and steel, wrenches, building wands and gadgets; no weapons), one-per-stack items only; add to it from `kubejs/data`. A tool that breaks while out hands the rest back as the Omnistrata (the mixin sits in NeoForge's `ItemStack.hurtAndBreak(int, ServerLevel, LivingEntity, Consumer)`). The wheel is the mod's first compiled client code, so the build now also needs a launcher's `libraries/` folder (the game's client classes). The icon is drawn by `art/make_omnistrata.py`. Tested on a test server without a client: the swap logic, the accept list, a tool breaking, the recipe. Not yet tested: the key, the wheel and the inventory clicks (no test client was free). Known limit: a tool that is out IS the kit, so anything that destroys or consumes that tool (a recipe that uses it up, salvaging) takes the stowed tools with it.
