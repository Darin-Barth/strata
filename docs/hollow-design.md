# The Hollow: design proposal (Oct 25, 2026)

A separate, opt-in horror dimension, `strata:hollow`. It leans mostly on dread and atmosphere, with some combat, and has unique loot that makes the trip worth it (Darin, Oct 25). Horror mobs exist only here. Mod research and build checks are in `docs/hollow-mod-research.md`.

## 1. Getting there
- **Frame:** a nether-portal-shaped frame of **resin bricks** (Vanilla Backport). Resin only comes from Overworld Pale Gardens (`resin_loot` and `pale_trades` are already off).
- **Lighter: the Pale Lantern** = Creaking Heart + soul lantern + resin clumps.
  - The Creaking Heart needs **Silk Touch** (Vanilla Backport's loot table matches vanilla). Without it the heart breaks into 1–3 resin clumps. Taking the heart also ends that garden's resin supply, which is a deliberate choice for the player.
  - The soul lantern means a Nether trip (soul sand/soil), so the Hollow is mid-game.
  - Reusable, like the Johto Bell. Lighting the portal plays a heartbeat or creak sound.
- Same portal setup as the Pokémon world (BBL Portals, one more entry in `kubejs/startup_scripts/pokeworld_portal.js`). It links 1:1 and returns to the Overworld.

## 2. The world
- **Dimension type:** permanent night (`fixed_time` 18000), `ambient_light` 0, monsters spawn at light 0–7. Beds don't let you sleep ("Something is watching you." via KubeJS), and respawn anchors don't work.
- **Terrain:** our own noise settings, built like the Pokémon world (a copy of vanilla, so Tectonic doesn't touch it). Mostly dense forest, swamp and cave country.
- **Biomes**, all copied under `strata:` and tagged only `#strata:hollow_biomes`, never `is_overworld` (otherwise Overworld mobs like Vampirism leak in and Hollow mobs leak out):
  - Hollow Pale Garden (copy of Vanilla Backport's; keeps Creaking Hearts and Creakings)
  - Hollow dark forest, Hollow swamp/mangrove, Hollow taiga (vanilla copies)
  - Dark palettes copied from Regions Unexplored (ashen woodland, blackwood taiga, fungal fen)
  - Grim & Bleak's 8 biomes (eerie forest, grim taiga, bleak plains, grimstone mountains, ...): they only exist in its own dimension, so we use them directly
  - Caves: deep dark style plus dripstone
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
  - Sanity: hallucinations scare you but don't hurt you; resting outside the Hollow recovers sanity.
- **No one-shots:** a KubeJS damage cap so a single hit from any Hollow horror mob can take at most ~40% of a player's max health (bosses excluded, since they keep designed stats). This also covers mod updates that buff damage.
- **Tuned in testing:** Cave Dweller and Ravenous damage, speed and spawn timers; Weeping Angel teleport range (short, same dimension only) and theft/light-breaking off if they feel cheap; Sanity's drain rate.
- **Breathing room:** a short grace period after arriving, safe-ish zones around the portal (light-based spawn rules), and GraveStone keeps items safe on death.
- Spawn rates start low; we raise them after playtests rather than the other way round.

## 4. Loot and reward
- Hollow structures: Grim & Bleak chapels/ruins, Graveyard crypts and lich prison (Corrupted Champion boss), all Lootr per-player.
- Unique materials from the mods: darksteel and red amber (Grim & Bleak), Graveyard boss drops, mutant drops (Mutant skulls/armor, Endersoul Hand = earned short teleport).
- **Our own:** "Hollow Ember", dropped by Hollow mobs and found in Hollow chests, used as a gate ingredient for a few strong late-game items (to pick: e.g. a late Mekanism/AE2 tier, a top Apotheosis item, or Draconic Evolution tiers).

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
- What Hollow Ember gates.
- Staged difficulty: the Hollow's mobs keep their designed stats (like bosses) when that script is built.
