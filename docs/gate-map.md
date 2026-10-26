# Gate map: what late tiers cost (proposal, Oct 26, 2026)

**Status: proposal for Darin's review; section 5 decided (Oct 26). Nothing built yet.**

The design doc's rule says late tiers need boss drops ("Boss gating"), but nothing enforces it yet. This map is the plan for that, across all three pillars plus gear.

Darin, Oct 26: gate "other mods as well instead of just tech mods. Magic tends to lean easier and also more overpowered... I would want some road blocks for magic along the way."

Principles:
- **Add an ingredient; don't rewrite recipes.** One KubeJS file per pillar (`server_scripts/gates_tech.js`, `gates_magic.js`, `gates_gear.js`), so a mod update can't silently undo a gate.
- **Spread the bosses.** No single boss gates more than a couple of rows, and every pillar has gates at mid, late and endgame, not just at the top.
- **Magic gets more road blocks than tech**, and earlier ones.
- **Close bypasses first.** A gate that can be crafted around isn't a gate (section 1).
- **Don't gate what CLAUDE.md protects:** wireless (Flux Networks, entangloporters, AE2 wireless and the Quantum Bridge as shipped), earned teleporting, and flight that has an ongoing cost.
- **Gate materials:** `strata:hollow_ember` (E, the Hollow), `strata:abyssal_pearl` (P, the Abyssal Plain), and boss drops.

Item and recipe IDs below were read from the mod jars on Oct 26. Rows marked *(check)* need a recipe-slot check before building.

## 1. Bypasses to close first
**Approved by Darin (Oct 26):** all four as recommended: Theurgy nether star and calorite routes removed and its netherite route +1 E; `possess_warden` +1 E; renewable nether stars accepted (no nether-star boss gates); Cataclysm's Overworld Sunken City removed (empty `#cataclysm:has_structure/sunken_city_biomes`).
| Bypass | What it breaks | Fix |
|---|---|---|
| Theurgy: diamonds → precious niter → netherite / nether stars / calorite | Every nether-star gate (Ars archmage book, Occultism marid miner, Neo Vitae crystal cluster, Apotheosis augmenting table), plus Ad Astra's calorite tier | Remove the nether-star and calorite reformation recipes; netherite route +E (section 3) |
| Oritech particle collider makes nether stars | Nether star as a Wither-only gate | Accept it: nether stars aren't a boss gate. Use boss-specific drops below |
| Mekanism antiprotonic nucleosynthesizer makes nether stars, dragon eggs, hearts of the sea | Same | Gate the SPS (row T5); accept the rest |
| Occultism `possess_warden` (6 sculk) | Free warden drops → Apotheosis sculkshelves | +E |
| Cataclysm Sunken City still generates in Overworld deep oceans | Leviathan drops aren't Abyssal-only | Pair Leviathan drops with pearls in recipes (done below), or empty `#cataclysm:has_structure/sunken_city_biomes` *(decision G1)* |

## 2. Tech
**Approved by Darin (Oct 26):** all ten as proposed.
| # | Gate | Needs | Stage |
|---|---|---|---|
| T1 | Nuclear: Mekanism fission port, Create New Age reactor fuel acceptor, Extreme Reactors reinforced controllers | 1 `cataclysm:ignitium_ingot` (Ignis, Nether) | late |
| T2 | Mekanism ultimate tier: every recipe with a `mekanism:ultimate_*` output (installers, factories, cube, induction, tanks, bin) | 1 `cataclysm:lava_power_cell` (Netherite Monstrosity, 16–24 per kill) | late |
| T3 | Mekanism fusion reactor controller | 1 `cataclysm:witherite_ingot` (Harbinger) + 4 **E** | endgame |
| T4 | MekaSuit pieces and Meka-Tool | 2 **E** each | endgame |
| T5 | SPS: supercharged coil, SPS port, antiprotonic nucleosynthesizer | 2 **P** each | endgame |
| T6 | Top storage: AE2 256k cell component (covers every 256k item and Ars Énergistique's source cell), AppliedFlux 256M core, Mekanism QIO supermassive drive | 1 `cataclysm:void_core` (End citadel) | late |
| T7 | Ad Astra tier 2 and up: desh engine (each later engine needs the previous one) | 1 `twilightforest:fiery_blood` (Hydra) | mid |
| T8 | Ad Astra tier 4 and jet suit: calorite engine | 2 `cataclysm:essence_of_the_storm` (Scylla) | late |
| T9 | Draconic Evolution awakened core (already needs the dragon heart) | +2 **E** | endgame |
| T10 | Extended Crafting ultimate table | 1 `cataclysm:abyssal_egg` + 4 **P** | endgame |

Already gated (left alone): Draconic wyvern and chaotic cores, Powah nitro, Extended Crafting stars. The Mekanism ultimate circuit has two recipes and feeds everything, so it's gated through its outputs (T2), not directly.

## 3. Magic: road blocks along the way
| # | Gate | Needs | Stage |
|---|---|---|---|
| M1 | Ars Nouveau tier-3 mage armor upgrade (`ars_nouveau:second_armor_upgrade`, now 2 ender pearls + chorus + source) | +1 **E** | mid |
| M2 | Ars Elemental Mark of Mastery (elemental foci and armor; pedestals full) | swap one pedestal item for **E** | late |
| M3 | Iron & Nouveau glyphs of legendary spells (black hole, starfall, sculk tentacles, ...) | +1 **E** each | late |
| M4 | Ars archmage book (already a nether star + Wilden Chimera tribute) | swap one ender pearl for **P** | late |
| M5 | Iron's Spells legendary ink (now epic ink + 1 amethyst) | amethyst → **E** | mid–late |
| M6 | Iron's Spells strongest spells (black hole, starfall, sculk tentacles, dragon breath) | loot only: `allow_crafting=false` in the spell config | late |
| M7 | Iron's Spells netherite spellbook (already a loot-only ruined book) | +1 **P** | endgame |
| M8 | Occultism afrit tier (red chalk): summon unbound afrit ritual | +1 **E** | mid |
| M9 | Occultism marid tier (blue chalk): summon unbound marid ritual (already uses a conduit) | +1 **P** | late |
| M10 | Occultism infinite ores: miner djinni / dimensional mineshaft rituals | +1 **E** | mid |
| M11 | Theurgy netherite route (both sulfur recipes) | +1 **E** | mid–late |
| M12 | Neo Vitae transcendent orb: hellfire-forge crystal cluster (slots full) | sculk → **E** | late |
| M13 | Neo Vitae deus tier: prismatic gem (athanor) *(check slots)* | +1 **P** | endgame |
| M14 | Neo Vitae diamond meteor (1 diamond → a sphere of diamond ore) | input → **P**, or remove | late |
| M15 | Neo Vitae teleposition reagent | +1 **E** | mid–late |
| M16 | Vampirism lord level 3 (vampire and hunter tasks) | 2 **E** | late |
| M17 | Vampirism lord level 5 | 2 **P** | endgame |

**Earlier road blocks** (so magic doesn't fly through early-mid):

| # | Gate | Needs | Stage |
|---|---|---|---|
| M18 | Ars apprentice book upgrade *(check)* | 1 `twilightforest:naga_scale` (Naga) | early–mid |
| M19 | Iron's Spells diamond spellbook *(check)* | 1 Twilight Lich drop (scepter or trophy) | mid |
| M20 | Occultism djinni tier (yellow chalk) *(check)* | 1 Nether boss drop (`cataclysm:ignitium_ingot` or a Bosses of Mass Destruction item) | mid |

Already gated (left alone): Iron's ruined book, dragonskin, Necronomicon and Cataclysm spellbooks (boss loot), Occultism's marid master miner, Neo Vitae's archmage orb (its own demon dungeon).

## 4. Gear
| # | Gate | Needs | Stage |
|---|---|---|---|
| G1 | Apotheosis Summit world tier (already rare gear + a Wither kill) | own 1 **E** (advancement criterion) | late |
| G2 | Apotheosis Pinnacle world tier (already epic gear + a Dragon kill) | own 1 **P** | endgame |
| G3 | Apotheosis augmenting table | +1 **E** | late |
| G4 | Apotheosis flawless gem cutting; heart and crystal seashelves | +1 **P** | endgame |
| G5 | Oritech flight augment (needs an in-game check that it drains power) | 1 Ice and Fire dragon heart | late |
| G6 | Apocalyptic Bosses ultimate ingot (now netherite + nether star + amethyst, 2 per craft) | nether star → 2 `panascraftrpgmod:void_gem` + 1 `cataclysm:cursium_ingot` | endgame |

## 5. Teleport and flight items (Darin, Oct 26: "super easy or cheap = I don't like it")
Checked in the jars on Oct 26.
1. **Iron's Spells.**
   - **Recall** (free warp to spawn): **removed**, including the Iron & Nouveau glyph copy.
   - **Portal:** **kept**. Every cast costs 200 mana and has a 3-minute cooldown, and the portals expire.
   - **Pocket Dimension:** **kept**.
2. **Draconic Evolution dislocators:** **all four removed** (Darin, Oct 26).
   - **Dislocator:** blaze powder, draconium dust and an Ender Eye. Remembers one spot in any dimension, limited uses.
   - **Player dislocator:** the basic one plus a draconium core and a ghast tear. Teleports you to a player who sneaks to agree, so it's a /tpa.
   - **Point-to-point pair:** the same, but between two linked dislocators.
   - **Advanced dislocator:** fusion crafting with a wyvern core (needs a nether star). Unlimited saved spots in any dimension; each jump burns 1 ender pearl.
3. **Forsaken Relics linking book:** **removed from loot** (Darin, Oct 26). He wanted home-only, but its modes (home, last death, marked spot) are hard-coded and Forsaken Relics has no config.
4. **Oritech portal augment:** **kept** (Darin, Oct 26).
   - A body augment that opens a portal back to your research station.
   - Researching it is a big one-time cost: the top (Arcane) station, 250 million RF, 16 ender pearls, 64 obsidian, an Unholy Intelligence and 32 adamant ingots.
   - After that every use is free and unlimited, with no cooldown.
   - Late-game and earned, like the Mekanism portable teleporter.
5. **Borderline flight:** **removed**:
   - the Artifacts Helium Flamingo (short flight that recharges)
   - the Forsaken Relics Wind Staff (wind jet that recharges)

   The Aether's Cloud Staff isn't flight (it summons Cloud Minions that fight), so it stays.
   The Oritech flight augment is free to run but very costly to research (500 million RF, 64 ion thrusters, 32 plutonium pellets), so it passes the flight rule; row G5 adds a dragon heart.
6. **Wireless:** **no tiers** (Darin, Oct 25, confirmed Oct 26). The old design-doc to-do is dropped.

Powah, Oritech and the Draconic reactor still need a place on the power ladder.

**Built Oct 26** (`server_scripts/strata_removed_items.js`, `config/irons_spellbooks_spell_config/irons_spellbooks/recall.json`): Recall disabled; the four dislocator recipes removed; Helium Flamingo, Wind Staff and Linking Book filtered out of all loot (LootJS). Copies players already have keep working.

## 6. Building it
1. Section 1 fixes and section 5 removals (KubeJS `event.remove` + Iron's spell config datapack).
2. `gates_tech.js`, `gates_magic.js`, `gates_gear.js` (KubeJS `event.replaceInput` / recipe rebuilds; ritual and altar recipes via their KubeJS add-on or a datapack override).
3. Apotheosis and Vampirism advancement and task overrides (datapack under `kubejs/data`).
4. The quest book: say on each gated item's quest what it needs and where to get it, so nobody hits a wall blind.
5. Test server: every gated recipe shows the new ingredient in EMI; no old recipe left behind; boot with 0 errors.
