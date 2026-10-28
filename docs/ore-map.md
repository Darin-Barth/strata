# Ore map (proposal)

**Status: proposed, not built.** Applies to a freshly generated world only: ore placement is fixed when a
chunk generates, so this has to be final before pregeneration.

Today every mod generates its ores on its defaults, mostly everywhere in the Overworld. Almost Unified
merges duplicate items in recipes and hides them in EMI, but every duplicate ore still generates and drops its
own mod's raw item. This proposal gives each dimension a reason to visit, cuts the duplicate ores, and keeps
every tech line startable at home.

## Principles

1. **Starting metals stay at home.** Anything a mod needs for its first machines spawns in the Overworld.
   No mod is locked behind a dangerous dimension just to begin.
2. **Concentrated, not exclusive, for core metals.** A thin Overworld supply is enough to start; the rich veins
   are elsewhere, so mass production means a trip.
3. **Exclusive for late materials.** Materials that belong to late game spawn only in their dimension.
4. **One generator per metal.** Where several mods add the same metal, only the Almost Unified target
   generates.
5. **Every dimension has a signature.** Each one has something worth mining that the others don't.
6. **Our dimensions get one signature ore each,** not a whole tech line (the Abyssal Plain and the Hollow
   already carry boss gates).

## The map

| Dimension | Signature ores | Story |
|---|---|---|
| **Overworld** | Coal, iron, copper, gold, redstone, lapis, diamond, emerald, tin, zinc, lead, silver, nickel, aluminum (bauxite), sal ammoniac, Mystical Agriculture's inferium and prosperity, sapphire (snowy biomes); **thin** osmium, fluorite, uranium, mithril | The everyday world: everything to get started |
| **Abyssal Plain** | **Rich osmium** across the seafloor; **rich fluorite** in the Hydrothermal Field | Osmium forms only under the crushing weight of the deep sea; fluorite crystallises around the vents |
| **Nether** | Quartz, nether gold, ancient debris, iesnium, draconium (nether), benitoite, Mystical Agriculture's soulium | Heat-forged and occult materials |
| **The End** | **Draconium** (End only, no longer in the Overworld), **rich platinum**, anglesite, enderitium | Metals touched by the dragon and the void: Draconic Evolution becomes post-Dragon by nature |
| **The Hollow** | Darksteel, red amber, thunder (as now), **rich mithril** | Mithril grows where light never reaches; magic gets its road block in the dark |
| **Aether** | Ambrosium, zanite, gravitite, skyjade, arkenium (unchanged) | Sky metals |
| **Kakuto Region** | Vanilla ores and the evolution-stone ores (unchanged) | A plain vanilla world with Pokémon stones |
| **Otherside, Twilight Forest, Ad Astra planets** | Their own ores (unchanged) | Already themed |

## Per ore

| Ore | Today | Proposed | How |
|---|---|---|---|
| Osmium (Mekanism) | Overworld: upper 65/chunk, middle 6, small 8 | Overworld about a fifth of today (enough for early Mekanism); Abyssal Plain: big deepslate veins (size ~12, ~20/chunk) on the Shelf, Plain and Trench | `config/Mekanism/world.toml` (thin) + a Strata feature in the Abyssal Plain biomes |
| Fluorite (Mekanism) | Overworld deep, 5 + 3/chunk | Overworld about half; Hydrothermal Field: rich veins near the vents | Mekanism config + Strata feature |
| Uranium (IE, Almost Unified target) | Overworld -64..-16, 9/chunk | Unchanged (deep and already fairly rare); Alex's Caves Toxic Caves keep their radrock uranium | none |
| Uranium (Mekanism, Oritech patch), yellorite (Extreme Reactors) | All generate (duplicates of IE uranium) | Off | Mekanism config; datapack overrides for Oritech and Extreme Reactors |
| Uraninite (Powah) | Overworld, 3 veins | Unchanged (its own reactor fuel; Powah reactors are already nerfed) | none |
| Lead | IE + Mekanism | IE only | Mekanism config |
| Silver | IE + Occultism + Ice and Fire + Werewolves | IE only | Werewolves config; datapack overrides for Occultism and Ice and Fire |
| Nickel | IE + Oritech | IE only | datapack override (Oritech) |
| Platinum | Oritech (deepslate + End stone) + Create Propulsion (not unified) | One platinum, unified to Oritech: thin deep Overworld, rich End | Create Propulsion ore off (datapack); add platinum to Almost Unified; tune Oritech's two features |
| Draconium | Overworld (rare), Nether, End | Nether + End only | datapack override (Overworld feature) |
| Mithril (Iron's Spells) | Overworld -63..-38, 7/chunk | Overworld about a third; Hollow: rich veins | datapack retune + Strata feature (Hollow biomes, grimstone target) |
| Zinc, thorium, magnetite (Create, Create New Age) | Overworld | Unchanged | none |
| Bauxite, tin, sal ammoniac, inferium, prosperity, sapphire | Overworld | Unchanged | none |
| Iesnium, benitoite, soulium, anglesite, enderitium | Nether / End | Unchanged | none |
| Oritech resource nodes | Surface boulders with ore, 1 in 350–500 chunks; the rarest includes uranium and platinum | Keep the boulders; drop uranium and platinum from them | datapack override |

## Other mining dimensions

- **Excessive Utilities' The Depths** is a mining dimension with very rich vanilla ores, and because it is
  tagged `c:is_overworld` it also receives Mekanism's ores. Proposed: limit Mekanism's ore tag
  (`#mekanism:spawn_ores`) to the real Overworld, so the Depths has vanilla ores only and osmium stays
  thin outside the Abyssal Plain.
- The **Quantum Quarry** dimension reuses the Overworld's biomes and gets its ores; it is already costly
  (balance patch D3) and needs no change.

## Building it

- One generator, `tools/build_ores.py`, writes everything: the Mekanism and Immersive Engineering config
  values, the datapack overrides that turn duplicates off, and the new placed features for the Abyssal Plain,
  the Hollow and the End. Re-run it after a mod update.
- Abyssal Plain features target deepslate and use count + height placement (no heightmaps, per the
  dimension's rules). Hollow features target grimstone.
- Check: generate a test world, pregenerate a small area in each dimension, and count ore blocks per
  dimension with a region scan (as done for the Kakuto Region).
- Quest text that says where to find these ores is updated with it (Mekanism's osmium, Draconic's
  draconium, Iron's mithril, Oritech's platinum).

## Open questions

1. How thin should home osmium be: a fifth of today, or less?
2. Platinum: Create Propulsion also uses it (fluid tanks and vessels). Is "thin at home, rich in the End"
   enough for airship builders, or should platinum stay common in the Overworld?
3. Mithril: thin at home plus rich in the Hollow, or Hollow only?
4. Should the Kakuto Region keep its full vanilla ore set, or be lighter so it isn't the easiest place to mine?
