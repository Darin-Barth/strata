# Strata quest book (FTB Quests 2101.1.37)

The quest book is generated: edit the Python files in `book/`, then run

```
python -I tools/quests/build.py   # writes config/ftbquests/quests/, checks every ID, runs packwiz refresh
```

- `book/_order.py` — chapter groups and chapter order. `book/_tables.py` — loot bags.
- `book/<chapter>.py` — one file per chapter (see `welcome.py` for the reference style).
- `dsl.py` — the helpers (`chapter`, `quest`, tasks, rewards). `snbt.py` — SNBT writer.
- `check_ids.py` — validates every item, entity, dimension, structure, biome and advancement ID in
  the SNBT files against the mod jars (Darin's Modrinth profile + `server/mods`, read-only). Also
  catches edits made with the in-game editor. `find_ids.py` searches the index:
  `python -I tools/quests/find_ids.py "^mekanism:.*infuser"` (`-entities`, `-structures`, ... for other kinds).
- `build.py --out <scratch dir> --only a,b` builds a subset somewhere else (for parallel work).

The generator owns `config/ftbquests/quests/`: it is wiped on every build. If someone edits quests
in game, port the change back into `book/` (IDs are stable hashes of `chapter/quest_key`, so
regenerating keeps players' progress as long as keys don't change; never rename a key after
release).

## Writing a chapter

```python
from dsl import *
C = chapter("mekanism", "Mekanism", group="tech", icon="mekanism:metallurgic_infuser",
            subtitle="Ore processing, gas, power and the MekaSuit")
q = C.quest
q("intro", "What is Mekanism?", icon="mekanism:steel_casing", desc="""
    Two or three short lines.""")
q("infuser", "Metallurgic Infuser", deps="intro", tasks=item("mekanism:metallurgic_infuser"), tier=2)
```

- `tasks=`: `item(id, count)`, `check()`, `dim(id)`, `kill(entity, n)`, `structure(id)`, `biome(id)`,
  `adv(id)`; a list for several. No tasks = a checkmark.
- `rewards=`: `give(id, count)`, `xp(n)`, `levels(n)`, `bag("common"|"uncommon"|"rare"|"epic")`,
  added on top of the tier defaults: tier 1 = 100 XP, 2 = 250 XP + common bag,
  3 = 500 XP + uncommon bag, 4 = 10 levels + rare bag, 5 = 20 levels + epic bag, 0 = nothing.
- `deps=` a key or list; `"other_chapter/key"` for cross-chapter. The first same-chapter dependency
  is the "parent" for the automatic left-to-right tree layout; `at=(x, y)` overrides.
- Also: `icon=`, `subtitle=`, `shape=` ("circle" default, "square", "hexagon", "gear", "diamond",
  "pentagon", "octagon", "heart", "rsquare"), `size=1.5` for milestones, `optional=True`,
  `any_dep=True` (one dependency is enough).
- Text: `&e` highlight, `&6` gold, `&a` green, `&c` red, `&d` pink, `&b` aqua, `&r` reset.

## Style and rules

- Audience: six friends, two of them new to modded Minecraft. Short, friendly, concrete:
  what the thing does, how to use it, what to do next. 2–6 lines per quest.
- First quest of a chapter: "What is X?" (checkmark) explaining the mod's idea in plain words.
  Last: a "Where next?" pointer to related chapters.
- Teach by doing: the item task is the thing the player should make or find next.
- Rewards are generous (Darin's call) but never: flight items, teleport items (warp scrolls/stones,
  portstones), wireless items, or the item the next quest asks for.
- Gates (design doc). Quests only order things; KubeJS does the real recipe gates later.
  - Same-dimension wireless (Flux Networks, AE2 wireless terminals, Mekanism quantum
    entangloporters, LaserIO across distance) depends on `welcome/nether`.
  - Cross-dimension wireless (AE2 Quantum Network Bridge) depends on `cataclysm/ender_guardian`.
  - Late Mekanism (SPS/antimatter, ultimate tier, MekaSuit) and late AE2 depend on
    `cataclysm/netherite_monstrosity` or `cataclysm/ignis`.
  - Draconic Evolution's top tiers and Extended Crafting's final crafts depend on `the_end/dragon`
    and a Cataclysm boss.
  - Flight (jetpacks, MekaSuit, Oritech exosuit, elytra) is presented as a costed, later reward,
    and its text says what it costs (fuel, power, mana, durability).
- Keybinds: only name keys verified in Darin's client options. Known: R/U = recipe/uses in EMI,
  M = Xaero world map, U = Xaero waypoints, ` = FTB Ultimine, V = voice chat, mouse 5 = ping,
  B = backpack. Several keys clash (B, R, M, V), so for others say "its key in Options > Controls".

## Registry dump (authoritative ID check)

Some mods ship a model and lang entry for items they don't register (disabled or conditional), so
the jar scan alone can pass a missing item. `registry.json` is a dump of the real item, entity,
structure, biome and dimension registries, and `check_ids.py` uses it whenever it exists. Refresh it
after adding, removing or updating mods: copy `registry_dump.js` into a scratch server copy's
`kubejs/server_scripts/` (never into the shipped `kubejs/`), start it once, then run
`python -I tools/quests/import_registry.py <that server>/logs/kubejs/server.log`.
