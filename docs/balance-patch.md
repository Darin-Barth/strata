# Balance patch

Status: **partly built** (queued for 0.5.0, boot-tested).

## Decisions

- **Built:** A1 (Mob Swab and MGU spawner can't take bosses: tag `strata:unfarmable`), C3 (Oritech
  fission controller needs ignitium, gate T1), D2 (Theurgy metal ores 3x, desh/ostrum reformation
  removed), D3 (Ender Quarry perimeter 1,024 and 50 FE a block, Quantum Quarry 50,000 FE a block),
  E1 (Refined Obsidian at netherite level), E2 (dragonsteel damage 14, armor 4/9/7/4, toughness 4),
  E4 (omega stack upgrades off), E5 (Simply Swords unique weight 0.02, hard pity 250), F1 (Charm of
  Sinking comes off in the Abyssal Plain, `strata_balance.js`), F2 (Ghostly Mantle >= 300 s, Chorus
  Totem >= 180 s, Seven Sins "sloth" never unlocks, Cross Necklace +0.3 s / 10%, Leafy Mantle out of
  loot; Relics extended configs on), G1 (Bountiful's top rewards kept, worth 1.5x and a quarter as
  common), G3 (Carry On can't pick up spawners, trial spawners or vaults; the Mekanism cardboard box
  still can), G4 (10 starter cogs), G5 (epic quest bag 1 netherite ingot instead of 2).
- **Built, part 2:** A2-A4 (the `strata:unfarmable` tag also blocks Ars jars and Drygmys, Occultism soul
  gems, Industrial Foregoing's duplicator and imprisonment tool, and Oritech's spawner; normal mobs
  stay farmable), C1 (Rainbow Generator 250,000 FE/t), C2 (Powah reactors: starter 60, basic 240,
  hardened 600, blazing 1,500, niotic 4,000, spirited 6,000, nitro 15,000 FE/t; no boss gate:
  Powah stays below the gated nuclear options instead), E3 (Affix Augmentor needs a Hollow Ember; the Gem Cutter's flawless and perfect cuts
  are out of reach, so they stay on Apotheosis' table with its Pearl; affix templates capped at 2),
  F6 (explosions and Big Cannons shots do at most 10 per hit to Bosses of Mass Destruction and
  Bosses'Rise bosses; `startup_scripts/strata_boss_blast_cap.js`).
- **Keep as is:** A5, B1-B3 (these magic teleports stay), C4, D1, D4, D5, E6, F3 (extremely expensive), F4,
  F5 (resets on death), F7, G2, H1, H2, I4.
- **Correction to I1:** the Qliphoth Awakening cores *do* have a use: combined with a weapon or armor
  in a crafting table they add Chesed's lightning, Malkuth's fireballs or Geburah's damage cap (done
  in code, so the recipe scan missed it). Their trophies have no use. Powah got no gate (capped below nuclear instead).

## Audit

The rows below come from four read-only audits (tech, magic,
gear/bosses, everyday/QoL) that read the mods' own recipes, loot and configs on the 0.5.0 test
server. The key numbers were re-checked by hand. "Inference" means read from code or text but not
tried in game. Skill trees and Inventory Pets were handled separately (already queued).

Legend: **Rec** = the audit's recommended fix. The decision for each row is in Decisions above.

## A. Boss drops can be farmed (undercuts the whole gate map)

Every gate ingredient (ignitium, lava power cell, void core, naga scale, lich trophy, Embers,
Pearls...) becomes renewable from a base farm through several routes:

| # | Route | Evidence | Rec |
|---|---|---|---|
| A1 | Mob Grinding Utils **Mob Swab** turns any mob, bosses included, into spawn eggs (Cataclysm and Twilight bosses have eggs) for its Entity Spawner + Saw | `no_swab` tag = only Wither and Ender Dragon | add `#c:bosses`, `#twilightforest:bosses` and the mini-bosses below to `no_swab` and `no_spawn` |
| A2 | Ars Nouveau **Containment Jar** + **Drygmy** "produce items from nearby monsters as if slain", jars count | `capturing_not_supported` lists only Aether, Mowzie's, the mimic | add the same list to `c:capturing_not_supported` (covers Ars jars and Occultism soul gems) and `ars_nouveau:drygmy_blacklist` |
| A3 | Occultism soul gem + Dimensional Battlefield on mini-bosses outside `#c:bosses`: Ender Golem (void core, T6), Baby Leviathan (abyssal egg, T10), Void Worm (M7) | soul gems deny only `#c:bosses` | covered by A2's list |
| A4 | Industrial Foregoing Mob Duplicator, Oritech spawner | blacklists empty / dragon only | add `#c:bosses` + list |
| A5 | Ember/Pearl drops in `hollow_rules.js` / `abyssal_rules.js` check only "killed by a player"; the Saw kills with a fake player (inference) | code read | skip fake players in both scripts |

## B. Teleports that break the travel rule (one /home, XP-costed waystones)

| # | What | Evidence | Rec |
|---|---|---|---|
| B1 | Occultism **Entity Wormhole**: free, permanent teleport to spawn, home, random spot (4096 blocks), last death or any lodestone | ritual = otherstone, ender pearl, crying obsidian, iesnium; no per-use cost | remove both wormhole rituals |
| B2 | Ars **Stable Warp Scroll**: never consumed, crosses dimensions; on a portal frame makes a permanent portal | recipe: warp scroll + 4 blaze powder + 2 pearls, source cost 0; `enableWarpPortals = true` | remove the recipe (single-use warp scrolls stay); `enableWarpPortals = false` |
| B3 | Ars Additions **Nexus Towers** (worldgen): 9-destination free warp nexus | `nexus_tower_enabled = true` | turn off |

## C. Power ladder (C&A 240 FE < New Age < nuclear/fission/fusion)

| # | What | Evidence | Rec |
|---|---|---|---|
| C1 | Excessive Utilities **Rainbow Generator** | `rainbowGeneratorFePerTick = 25000000` (25 M FE/t) | 50,000 |
| C2 | **Powah** reactors: basic 1,000 FE/t from Overworld uraninite, no boss item; blazing 10k, niotic 25k, spirited 100k. Makes C&A and New Age pointless (*too weak* by comparison) | `powah.json5` | ignitium ingot in the blazing and higher reactor recipes (like T1); rates of blazing+ to 25% |
| C3 | **Oritech fission reactor** controller has no boss item; 25,000 FE/t | `crafting/controller.json` | ignitium ingot, like T1 |
| C4 | IE **diesel generator** 4096 FE/t, ungated, above New Age | `dieselGen_output` | Keep |

## D. Ore and resource multiplication (Mekanism 5× is the intended top)

| # | What | Evidence | Rec |
|---|---|---|---|
| D1 | **Oritech** chain: about 12 ingots per ore block, no gate | grinder → clumps → acid centrifuge (3 gems) → foundry (2 gems → 3 ingots) | centrifuge 2 gems, foundry 2 → 2 (≈5 per ore, like Mekanism) |
| D2 | **Theurgy** liquefaction: 5× from copper/iron/stone-age machines, uranium and osmium too; reformation turns iron/gold into Ad Astra **desh/ostrum** | ore → 5 sulfur, 1 sulfur → 1 ingot | ores 3, raw 2; remove the 4 desh/ostrum reformation recipes |
| D3 | Excessive Utilities **Quantum Quarry** (ores from nothing for 1 nether star) and **Ender Quarry** (100,000-block perimeter, 10 FE a block; a server-load and grief risk) | server config | Ender Quarry perimeter 256, 100 FE a block; Quantum Quarry 100,000 FE a block |
| D4 | Excessive Utilities **Creative Builder's/Destruction Wands** from one unstable ingot | recipes | remove if they don't use up blocks (check in game) |
| D5 | Mystical Agriculture **netherite essence** (8 → 1 ingot) skips the Ember on Theurgy's netherite route | recipes | minor: gate or leave |

## E. Gear and gear progression

| # | What | Evidence | Rec |
|---|---|---|---|
| E1 | **Mekanism Tools Refined Obsidian**: 31 armor, toughness 5, sword 12, costs a diamond + osmium, no boss. Beats netherite (20/3) and Cataclysm weapons (11–16) | `tools-materials-startup.toml` | netherite level (armor 3/8/6/3, toughness 3, damage 4) |
| E2 | **Ice and Fire dragonsteel**: damage 25, armor 34, toughness 6; obsoletes every endgame weapon | `iaf-common.json` | damage 14, armor 4/9/7/4, toughness 4 |
| E3 | **Create Enchantment Industry** skips gear gates G3/G4: Affix Augmentor with no Ember, Gem Cutter to Perfect with no Pearl, affixes up to level 4 | recipes, `apotheoticAffixTemplateMaxLevel = 4.0` | Ember in the Augmentor, Pearl in the Gem Cutter, template max 2 |
| E4 | **Sophisticated omega stack upgrade**: unlimited per slot, skips the void-core gate (T6) on big storage | enabled in `sophisticatedcore-common.toml` | disable (both mods) |
| E5 | **Simply Swords** uniques: hard pity at 75 chests, and Lootr rolls per player, so everyone gets one early | `loot.toml` | hard pity 250, weight 0.02 |
| E6 | Relics **Glitchy Mantle** walks on air, End loot, free to run | constants | Keep |

## F. Survivability (makes bosses and the Hollow's 40% cap moot)

| # | What | Evidence | Rec |
|---|---|---|---|
| F1 | Reliquified **Charm of Sinking**: 1–5% damage reduction per block of water overhead, immortality standing still on the bottom, air refills; early ocean loot. The Abyssal Plain has 80–500 blocks of water | `charm_of_sinking.yaml` | 0.2–0.5% a block, no immortality, no air refill |
| F2 | Cheat-death stacking in separate Curios slots: **Ghostly Mantle** (cooldown down to 25 s), **Chorus Totem** (to 33 s), **Ring of the Seven Sins** "sloth" (immortal after standing still 10 s), **Leafy Mantle** (leaves absorb fatal hits), **Cross Necklace** (25% to cancel fatal damage, 3× i-frames) | relics yaml constants | Ghostly Mantle ≥ 300 s, Chorus Totem ≥ 180 s, sloth off, Cross Necklace +0.3 s / 10%; Leafy Mantle out of loot |
| F3 | Ars Trinkets **Omnipotence Crown**: damage capped at 10% of max health and 9 extra lives; soul levels give ×15 damage | lang, `ars_trinkets-common.toml` | remove the crown recipe; flatten soul damage bonus to ×2 at most |
| F4 | Ars 'n Spells resonance ×5 spell damage near full mana (inference: may stack with F3) | config | 1.5 |
| F5 | **Spice of Life: Onion** gives permanent Strength II, Regeneration and Speed for eating varied food; with Croptopia + Farmer's Delight that's trivial | generated `solonion.json` (the pack ships none) | ship it with health and toughness steps only, no effects |
| F6 | **Boss damage caps**: Cataclysm and Legendary Monsters cap each hit at 20–25; BoMD and Bosses'Rise have none, so a nuke, a cannon or dragonsteel deletes them | configs | KubeJS cap of 25 per hit (10 for explosions) on `#c:bosses` outside Cataclysm |
| F7 | **Death is nearly free**: PlayerRevive revives forever with no item, downed players can't be hit by mobs; Tombstone's `soulbound_enchanting_table = true` (default false) | repo configs | Keep: cheap deaths are intended in this pack |

## G. Economy and everyday

| # | What | Evidence | Rec |
|---|---|---|---|
| G1 | **Bountiful** turns iron into netherite armor (chestplate = 48 iron), diamond tools, Mending, totems; boards refresh every 45 s | reward pool worths | remove netherite pieces, totem, ominous key; diamond items and Mending ×3 worth |
| G2 | **Easy Villagers**: iron farm block every 4 min, stacks without limit; `universal_reputation` + converter makes every trade cost ~1 emerald | `easy_villagers-server.toml` | iron farm 24,000 ticks; universal reputation off; `trade_price_multiplier_scale = 0` |
| G3 | **Carry On** picks up spawners, trial spawners and vaults | `forbiddenTiles` | forbid those three |
| G4 | **Create Numismatics** has almost no coins (only ~128 spurs a player from quests): *too weak* | `starter_*` = 0 | 10 starter cogs, coins in Bountiful rewards |
| G5 | Quest bags: roughly 25–30 netherite and 450 diamonds per player across the book (random bags) | quest book | minor: halve netherite in the epic bag |

## H. The Pokémon world (Kakuto Region)

| # | What | Evidence | Rec |
|---|---|---|---|
| H1 | Risk-free resource world: full vanilla ores incl. diamonds, and copies of ancient cities, trial chambers, mansions, monuments, with In Control denying hostile spawns | `kubejs/data/pokeworld/...` | drop those four structure copies; cut diamond/gold/redstone ore features (`build_pokeworld.py`) |
| H2 | **Flying Pokémon** everywhere within about an hour (Pidgeotto at level 18, 2× XP, rare candies for emeralds) | 53 species with AIR riding | Keep: riding everywhere includes flying |

## I. Too weak to bother with

| # | What | Rec |
|---|---|---|
| I1 | Boss drops with no use: Qliphoth Awakening's Lightning/Justice/Fire-and-Ice Cores have no recipe anywhere; Bosses'Rise, Mowzie's and Legendary Monsters drops aren't in any gate | give them roles: swap them into some Hollow Ember gate slots (e.g. M3/M8) or quests |
| I2 | C&A alternators and New Age generators vs Powah | fixed by C2 |
| I3 | Create Numismatics money | G4 |
| I4 | Ars Creo starbuncle wheel: 256–384 SU | stress capacity 32–48 |

## Checked and fine

Waystones (XP by distance), backpack smelting/magnet, Functional Storage, FTB Ultimine (64 blocks,
exhaustion), Hyperbox, Mighty Mail, Scannable, Productive Bees endgame bees (spawn-egg only),
Occultism tier gates and miners, Iron's Angel Wings, vampire bat form, flight rituals (cost source
or EV), Apothic × Iron's affixes, Twilight charms, Apotheosis top tiers, Apocalyptic gear (G6).

## Not checked yet

MineColonies' worker economy (e.g. the Enchanter), Supplementaries in depth, Ice and Fire dragon,
Twilight and Mowzie's boss damage caps, whether librarians sell Apotheosis' raised enchant levels.
