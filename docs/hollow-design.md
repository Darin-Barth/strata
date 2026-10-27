# The Hollow (approved Oct 25, 2026; built Oct 26)

> Progression proposal (quest chapter, boss ladder, the Pale Beacon, fixes): `docs/hollow-progression.md`. What Hollow Ember gates across the pack: `docs/gate-map.md`.

A separate, opt-in horror dimension, `strata:hollow`. It leans mostly on dread and atmosphere, with some combat, and has unique loot that makes the trip worth it (Darin, Oct 25). Horror mobs exist only here. Mod research and build checks are in `docs/hollow-mod-research.md`.

## 1. Getting there
- **Frame:** a nether-portal-shaped frame of **resin bricks** (Vanilla Backport). Resin only comes from Overworld Pale Gardens (`resin_loot` and `pale_trades` are already off).
- **Lighter: the Pale Lantern** = Creaking Heart + soul lantern + resin clumps.
  - The Creaking Heart needs **Silk Touch** (Vanilla Backport's loot table matches vanilla). Without it the heart breaks into 1–3 resin clumps. Taking the heart also ends that garden's resin supply, which is a deliberate choice for the player.
  - The soul lantern means a Nether trip (soul sand/soil), so the Hollow is mid-game.
  - Reusable, like the Johto Bell. Lighting the portal plays a heartbeat or creak sound.
- Same portal setup as the Pokémon world (BBL Portals, one more entry in `kubejs/startup_scripts/pokeworld_portal.js`). It links 1:1 and returns to the Overworld.
- **Look and sound (Darin, Oct 26):** "Dead Signal", grey TV static that freezes now and then and once drops to black, in BBL Portals' "nether" texture slot; ash-grey dust. Near it the Nether whoosh becomes whispers, creaking, a slow heartbeat and cave noises, with long stretches of silence; ash, pale petals and smoke drift off it (`startup_scripts/portal_ambience.js`). Hollow portals lit before this change may show the Pokémon portal's texture until they are broken and relit (the texture is stored in each portal block when it is lit).

## 2. The world
- **Dimension type:** permanent night (`fixed_time` 18000), `ambient_light` 0, monsters spawn at light 0–7. Beds don't let you sleep ("Something is watching you." via KubeJS), and respawn anchors don't work.
- **Terrain:** our own noise settings, built like the Pokémon world (a copy of vanilla, so Tectonic doesn't touch it). Mostly dense forest, swamp and cave country.
- **Biomes**, all copied under `strata:` and tagged only `#strata:hollow_biomes`, never `is_overworld` (otherwise Overworld mobs like Vampirism leak in and Hollow mobs leak out):
  - Hollow Pale Garden (copy of Vanilla Backport's; keeps Creaking Hearts and Creakings)
  - Hollow dark forest, Hollow swamp/mangrove, Hollow taiga (vanilla copies)
  - Dark palettes copied from Regions Unexplored (ashen woodland, blackwood taiga, fungal fen)
  - Grim & Bleak's 8 biomes (eerie forest, grim taiga, bleak plains, grimstone mountains, ...): they only exist in its own dimension, so we use them directly
  - Caves: deep dark style plus dripstone
- **Fog (Darin, Oct 26):** heavy fog that makes the Hollow hard to navigate: about 10 blocks of sight, about 28 while holding a light (any lantern or torch, the Pale Lantern, glowstone, froglights, sea lanterns, glow sticks) in either hand, easing between the two. Client-side `startup_scripts/hollow_fog.js`.
- **Atmosphere** (biome effects, no extra mods): dark fog and black sky, ash/spore particles, cave mood sounds, quiet ambient loops, Deep Dark style music. AmbientSounds (in the pack) adds Hollow-only soundscapes such as whispers and distant knocks. A KubeJS script adds short Darkness pulses now and then while in the Hollow.

## 3. Mobs (8 new mods)
| Role | Mod | How it's kept in the Hollow |
|---|---|---|
| Dread | Cave Dweller ReEvolved (beta) | `dimension_whitelist = [strata:hollow]` |
| Dread | Weeping Angels | spawn tag → Hollow biomes; no interdimensional teleport, no snow angels |
| Dread | Whispering Spirits | one spawn file → Hollow biomes |
| Dread | Sanity: Renewed | sanity meter and hallucinations in the Hollow only (per-dimension config); recovers outside |
| Chase | The Ravenous | two spawn files → Hollow biomes |
| Combat + loot | Grim & Bleak | its biomes, mobs, structures and darksteel/red amber gear live in the Hollow; its own portal and Overworld ruins removed |
| Combat + loot | The Graveyard 4.0 | spawn/structure tags → Hollow biomes; hordes off (needs new dependency villagertradingplus) |
| Mini-bosses | Mutant Monsters | config spawns 0; our own Hollow spawn file |

Also in the Hollow: Creakings (Pale Garden copy). Not used: Born in Chaos (spawn rules hard-code the Overworld; possible later with a custom spawner), and every mod whose scares follow the player into other dimensions or grief bases (list in the research doc).

**Safety net:** an In Control! rule denies every horror mod's mobs outside `strata:hollow`, so a mod update can't leak them.

## 3a. Scary but fair (Darin, Oct 25)
"I really don't want BS mobs that just kill you without any chance of survival. Scary, but also fun."
- **Every threat has a warning and a counter.**
  - Cave Dweller: cave noises and a chase phase before an attack. You can run, block it off, or fight it.
  - Weeping Angels: they only move when unseen, so watching them and keeping lights up works.
  - The Ravenous: a screech before the chase.
  - Mutants: big, visible mini-bosses with readable attacks.
  - Sanity: hallucinations mostly just scare you, but below 25% sanity some become real mobs that attack (Rotting Stalker, Sneaking Terror; capped like every horror mob). Light, campfires, friends and resting outside the Hollow recover sanity. Kept on purpose (Darin, Oct 26).
- **No one-shots:** a KubeJS damage cap so a single hit from any Hollow horror mob can take at most ~40% of a player's max health (bosses excluded, since they keep designed stats). This also covers mod updates that buff damage.
- **Tuned in testing:** Cave Dweller and Ravenous damage, speed and spawn timers; Weeping Angel teleport range (short, same dimension only) and theft/light-breaking off if they feel cheap; Sanity's drain rate.
- **Breathing room:** a short grace period after arriving, safe-ish zones around the portal (light-based spawn rules), and Corail Tombstone keeps items safe on death.
- Spawn rates start low; we raise them after playtests rather than the other way round.

## 3b. Dread events (Darin, Oct 25)
`kubejs/server_scripts/hollow_dread.js`. Only for players in the Hollow, never harmful, sounds played to the one player they target. After a 30 s quiet start, about one event every 1.5–3 minutes:
- **Footsteps:** steps come up behind you and stop the moment you turn around.
- **Whisper:** your own name (always the player hearing it), plus a whisper sound.
- **Phantom sounds:** a creeper hiss, door, chest, heartbeat, Enderman stare... with nothing there.
- **Torch flicker:** a nearby torch goes out and relights 2–4 s later.
- **Watcher:** a dark figure (a frozen, silent, invulnerable Enderman) at the edge of your view; it vanishes in smoke when you look at it, or after 15 s.
- **Fog:** 5 s of Darkness with a heartbeat.
- **Compasses and clocks spin:** the dimension type isn't "natural" (vanilla behaviour, like the Nether).

## 4. Loot and reward
- Hollow structures: Grim & Bleak chapels/ruins, Graveyard crypts and lich prison (Corrupted Champion boss), all Lootr per-player.
- Unique materials from the mods: darksteel and red amber (Grim & Bleak), Graveyard boss drops, mutant drops (Mutant skulls/armor, Endersoul Hand = earned short teleport).
- **Our own:** "Hollow Ember", dropped by Hollow mobs and found in Hollow chests, used as a gate ingredient for a few strong late-game items (to pick: e.g. a late Mekanism/AE2 tier, a top Apotheosis item, or Draconic Evolution tiers).

## 4a. What was built (Oct 26)
- `tools/build_hollow.py` writes the dimension, biome copies, layout, tags and every mod override (re-run after a mod update). Terrain: the Pokémon world's vanilla router + Grim & Bleak's grimstone materials. Vanilla ores don't generate in grimstone: the Hollow is for loot, its ore is darksteel.
- Pale Lantern: animated texture (a dark iron cage around a pulsing Creaking Heart "eye", resin roots dripping), no enchantment shimmer. Hollow Ember: dark ember with a violet glow.
- Configs: Cave Dweller (`dimensionWhitelist = strata:hollow`, surface too, 1 at a time, 200 health, no shield disabling), Weeping Angels (spawn tag + dimension blacklist, groups ≤2, 48-block same-dimension teleports at 25%, no light breaking or theft, no snow angels), Mutant Monsters (config spawns 0; Hollow spawn file; Endersoul Hand range 64), The Graveyard (hordes off, smaller ghoul packs), Sanity: Renewed (drains ~0 outside the Hollow with slow recovery; `dimension/hollow.toml` turns them on, light/campfires/lanterns comfort, friends count more), In Control! `spawn.json` (horror mods: default in `strata:hollow`, denied everywhere else, for natural spawns and anything joining the world).
- Damage cap and grace: `startup_scripts/hollow_damage_cap.js`. Rules (recipe, no sleeping, Grim & Bleak's Compass of pain can't open Limbo, Hollow Ember drops): `server_scripts/hollow_rules.js`.
- Hollow Ember in chests: NeoForge loot modifiers on Grim & Bleak, Graveyard and catacomb chests (10–75%). Drops: horror mobs 15%, mutants 50% (1–2), bosses 3–5.
- Test server (Oct 26): boots clean (4/4 startup, 9/9 server scripts). `/locate`: Hollow biomes and Graveyard, Grim & Bleak and catacomb structures found in the Hollow, none in the Overworld; Grim & Bleak's Overworld portal ruins generate nowhere. Not yet tested with a client: portal, spawns, Sanity HUD, dread events.

## 5. Build steps
1. Add the 8 mods (Modrinth), plus villagertradingplus for The Graveyard.
2. `tools/build_hollow.py` (based on `build_pokeworld.py`): dimension, noise, biome copies with Hollow effects, biome tag, spawn and structure overrides.
3. Configs: Cave Dweller whitelist, Weeping Angels, Sanity per-dimension files, Mutant Monsters weights, Graveyard hordes off, In Control! deny rule.
4. KubeJS: portal entry, Pale Lantern recipe, bed message, Darkness pulses, Grim & Bleak portal removal, Hollow Ember.
5. Test server: `/locate` leak check (no Hollow mobs/structures elsewhere, no Overworld mobs in the Hollow), spawn counts in both, then an in-game test with a client (portal, Sanity HUD, Cave Dweller).
6. Pregenerate the Hollow on the server with Chunky.

## 6. Open choices
- Sanity meter: in or out? It's the strongest dread piece but adds a HUD and needs a client test.
- The Graveyard 4.0 is three days old and adds a dependency; fallback is the unofficial 2.6.2 port.
- What Hollow Ember gates (not wired into any recipe yet).
- Staged difficulty: the Hollow's mobs keep their designed stats (like bosses) when that script is built.
