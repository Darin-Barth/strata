# Strata — "Build. Fly. Explore."

Kitchen-sink Minecraft modpack (500–600 mods) for 5–6 friends. Managed with **packwiz** in this repo.
Source of truth: `docs/design-doc.md` (rules) and `docs/strata-mod-tracker.xlsx` (mod list, sheet `Mods`).

## Hard constraints
- **Minecraft 1.21.1, NeoForge only.** Create Aeronautics forces this. Never add a Forge/Fabric-only or other-version file.
- Only add mods whose tracker Status is **Keep**. Maybe = undecided (ask), Cut = never add.
- Verify builds via the Modrinth/CurseForge APIs (or packwiz), never from memory.
- Prefer Modrinth; fall back to CurseForge. Set `side` (client/server/both) to match the tracker.
- Hosting: treehouse server, itzg/minecraft-server Docker image. Server-side choices must work headless.

## Pillars
1. Tech/automation (Create + add-ons, Mekanism, AE2, IE, etc.) 2. Magic (Ars Nouveau hub + bridges) 3. Exploration/bosses/dungeons.
Test for any mod: keep if it adds a different way to play; question it if it duplicates something already in.

## Rules to enforce while building
- **No free teleport**: no `/home`, `/back`, `/rtp`, `/tpa` for non-ops (no FTB Essentials). Waystones only with distance-scaled XP cost + extra cross-dimension cost; remove warp scrolls/stones from loot. Earned teleporting (Mek teleporters, Ars, blink spells, Vampirism skill) is fine.
- **Flight must cost something** (fuel, power, mana, stamina, durability). No free "wear it and fly" items: Inventory Pets Cloud pet and Excessive Utilities angel-ring style items get removed or cost-gated. MekaSuit flight = late-game.
- **Wireless tiers**: early none (cables/belts/trains/IE wires) → mid (after Nether or first boss) same-dimension wireless (Flux Networks, AE2 wireless, Mek entangloporters) → late cross-dimension (AE2 Quantum Network Bridge, boss-drop gated).
- **Power**: Crafts & Additions alternator (FE output lowered) < New Age generators < New Age nuclear / Mek fission+fusion. Remove New Age wire recipes; grid = C&A wires (local) + IE LV/MV/HV (long distance).
- **Difficulty**: our KubeJS staged-difficulty script (phase 2; Majrusz's was dropped) is the ONLY regular-mob scaler. Normal → Expert (Nether, modest step) → Master (Dragon). Bosses keep designed stats. Apotheosis elites rare near spawn. Vampirism scales its own mobs — include in tests.
- **Boss gating**: late Mek/AE2 tiers and cross-dim wireless need boss drops (e.g. Cataclysm).
- **Combat**: Better Combat + Apothic Combat + Combat Roll. Not Epic Fight.
- **Magic bridges**: Ars 'n Spells + Iron & Nouveau (never also Ars↔Iron Mana Bridge), Ars Ocultas, Ars Énergistique, Ars Creo, Apotheosis×Iron's, Vampirism×Iron's.
- **Worldgen**: Tectonic + Regions Unexplored + Streams Reflowing. No Terralith, no Dynamic Trees, no C2ME. Incendium (not with Amplified Nether), Nullscape. Pregenerate with Chunky.
- **Client/visual**: every heavy visual is client-only and optional. Sodium (not Embeddium) + Iris. EMI is the only recipe viewer (EMI Ores, Advanced Loot Info and Just Enough Breeding cover what JER did). JEI and JER were removed Oct 25: JEI builds its recipe index on the client's main thread when joining (about 60 s with this pack), which timed players out. Botania and Ars Botania are out (no 1.21.1 build). Curios is the accessory standard (Accessories only if a mod needs it).
- **Pokémon**: Cobblemon in its own dimension (datapack, own namespace); wild spawns disabled elsewhere; riding allowed everywhere. Built after the base pack is stable.

## Phase plan
1. packwiz setup + add Keep mods with confirmed builds (**done in phase 1; stop for review**).
2. Configs + KubeJS to-do list (see design doc). 3. Test server on treehouse + backups + Discord bridge + Chunky. 4. Test plan, then FTB Quests. 5. Pokémon world.

## Working notes
- packwiz: `packwiz refresh` after manual edits; `packwiz mr add <slug>` / `packwiz cf add <slug>`.
- Lookup script and results: `tools/` (results in `tools/lookup-results.json`).
- Configs in `config/` ship with the pack. Pack-balance configs (Quark, ModernFix) are enforced. Per-player comfort/performance configs (Distant Horizons, Camera Overhaul) get `preserve = true` in `index.toml` so updates don't overwrite players' own settings (`packwiz refresh` keeps the flag).
