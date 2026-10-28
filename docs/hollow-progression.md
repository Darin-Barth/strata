# The Hollow: progression with bite

**Status: approved (decisions D1–D5 in section 6). Not built yet.**

Goal: the Hollow should have real bite, not be a shallow jumpscare world. This builds on `docs/hollow-design.md` (the world, mobs, dread events, the 40% damage cap). That doc stays the reference for what's built. This one adds what to work toward.

What gates elsewhere in the pack is in `docs/gate-map.md`. Research notes (from the mod jars) are summarised in section 7.

## 1. What "bite" means here
Scary but fair still holds: no one-shots, and every threat has a warning and a counter. Bite comes from **consequences and pressure, not cheap deaths**:
- **Sanity is a resource you manage.** Below 25% sanity, hallucinations become real mobs that attack (Sanity: Renewed's Rotting Stalker and Sneaking Terror). The meter is the clock on every trip.
- **Nothing you build is safe by default.** The Ravenous hears building and opening chests within 70 blocks and eats blocks to reach you (decision D1). Camps need planning: obsidian walls or the Sanctuary.
- **The bosses are hard and must be earned.** Each one is summoned or unlocked with materials from the one before it.
- **The rewards are worth it.** Hollow Embers and the boss trophies gate strong items across the whole pack, magic included.
- **There's a story to piece together.** A lost expedition left pages behind, and they point toward the Sanctuary.

## 2. Fixes to the current build (items 1–6 done)
1. **The Ravenous and its Screechers never spawn.** Their spawn code requires open sky and a biome tagged `#minecraft:is_overworld`, and Hollow biomes deliberately aren't. Fix: a KubeJS spawner in the Hollow (rare, at night-level light, open sky, away from the portal and the Sanctuary). Don't tag the biomes: that would let Overworld mobs in.
2. **The Corrupted Champion (Graveyard lich) can't be summoned.** Its blood vial only fills from villagers, and the Hollow has none. Fix: in `config/graveyard`, set `bloodEntities` to the Hollow's own mobs (for example tormented villagers, ghouls and other Graveyard undead; to be confirmed against the entity list).
3. **The damage cap misses hits without an attacker.** That covers the Weeping Angel neck snap and Grim & Bleak's 500-damage smite around a dying Gate Guardian. Fix: also cap by damage type in the Hollow, for Weeping Angels and Grim & Bleak (`godly_power`).
4. **One Hollow Ember loot modifier never fires.** It targets `grim_and_bleak:chests/abandonned_tower_loot`, which no structure uses. Move it to `small_tent_loot` and `cabinloot`.
5. **Sanity hallucinations can hurt.** Below 25% sanity they become real mobs. Keep it, because it's good bite: they're under the damage cap and you get warned well before. `docs/hollow-design.md` section 3a and the quest text reflect this.
6. **Check Chemical X.** Mutant Monsters' potion turns vanilla mobs into mutants in any dimension. Confirm that In Control! stops those mutants outside the Hollow.

## 3. The quest chapter "The Hollow" (about 26 quests, 5 tracks)
It follows the same shape as the Abyssal Plain chapter. Rewards follow the tier defaults, and gate materials are never quest rewards.

**Arrival**
1. *What is the Hollow?* What the dimension is, and that it's optional and dangerous.
2. *The Pale Lantern*: craft it (Creaking Heart via Silk Touch, soul lantern, resin).
3. *Through the Static*: enter `strata:hollow`.
4. *The Rules*: no sleeping, compasses spin, sanity drains, everything has a warning (checkmark).
5. *First Light*: build a lit camp; campfires, lanterns and a Garland (Sanity: Renewed) restore sanity.

**Survival track** (the counters)
6. *Timey-Wimey Detector*: warns when Weeping Angels are near. You fight them with pickaxes.
7. *Something Is Listening*: survive a Ravenous hunt, or craft the Anti-Ravenous (a Screecher's echolocation organ; stuns everything within 25 blocks).
8. *Darksteel*: mine darksteel and make Grim & Bleak gear. Its weapons have useful extras.
9. *Sound Walls*: build from obsidian (Ravenous-proof), or learn which blocks it can't eat.

**Exploration track**
10. *Chapels*: find a Grim & Bleak chapel and take its Holy Cross. You need one for the Sanctuary.
11. *The Dead Rest Here*: Graveyard crypts and graveyards; the great crypt has the best chest.
12. *The Catacombs*: Weeping Angel catacombs.
13. *The Haunted House*.
14. *Bone Staff Fragments*: collect the upper, middle and lower fragments from three Graveyard ruins.
15. *Lost Signal* (story, 6 pages): **The Pale Survey** expedition came through a portal of static and stopped answering. Its log pages turn up in Hollow chests (loot modifiers, one page per chest, Lootr per player). Read in order, they tell what happened and describe the Sanctuary they never finished. Each page is a quest task; all six complete the track.

**Boss ladder** (each one unlocks the next)
16. *The Damned Templar*: summoned with a Cursed Amulet (darksteel, banshee collar, Holy Cross), or met in the grimstone mountains. Drops the **Templar Artifact** and unbreakable templar armor.
17. *Mutants*: kill two of the four mutants. Drops: hulk hammer, skeleton armor parts, creeper shard, Endersoul fragments.
18. *The Corrupted Champion*: the Graveyard ritual. Fill the blood vial, lay the three staff fragments, pour it on the altar in the lich prison at night. 600 HP across two phases, summons undead. Drops a **bone staff**.
19. *The Gate Guardian*: forge the Gate Key (darksteel, suffering flesh) and wake it at the Dimensional Gate. 300 HP, armor 20, summons clones. Grim & Bleak means you to finish it with the **Thunder Sword**, which needs the Templar Artifact. This is the Hollow's final boss.
20. *The Ravenous* (apex, optional): hunt it down to its last phase for the **echolocation organ**. Bragging rights and a Sanctuary upgrade (section 4).

**The big goal**
21. *The Pale Beacon* (craft), 22. *Sanctuary* (build it and light it in the Hollow), 23. *The Survey Complete* (finish the story and the beacon).

## 4. The Sanctuary: the Pale Beacon
The Hollow's version of the Deep Station: an earned safe haven in the dark.

**Recipe** (KubeJS block `strata:pale_beacon`, shaped):
- the Holy Cross (unique: one per chapel)
- the Champion's bone staff
- the Templar Artifact
- the Pale Lantern
- 8 Hollow Embers

**Effects within 24 blocks**, while lit:
- Sanity is restored. It's added to Sanity: Renewed's per-dimension comfort list in `dimension/hollow.toml`, plus a KubeJS top-up so it beats the drain.
- No dread events (`hollow_dread.js` skips players near a beacon).
- No natural horror spawns (KubeJS cancels them inside the radius).
- The Ravenous can't eat it or the blocks around it. Add `strata:pale_beacon` to `#minecraft:screech_blocks`; walls still need obsidian or similar.
- **Beds work.** A respawn point in the Hollow, the only one.

**Bite: it needs feeding (decision D3).** One Hollow Ember per in-game day, put in the beacon. Unfed, it goes dark and everything above stops. It's the "ongoing cost" idea from the flight rule, used for safety.

**Upgrade:** the Ravenous' echolocation organ extends the radius to 48 and warns everyone inside when a horror mob comes within 64 blocks.

## 5. Hollow Ember and trophies: what they gate
Hollow Embers are the main gate material. Boss trophies gate a few top items. The full list is in `docs/gate-map.md`. Embers gate these (about 40 for a player who wants everything):

| Pillar | Item | Embers |
|---|---|---|
| Hollow | Pale Beacon (and its upkeep) | 8 (+1/day) |
| Tech | Mekanism fusion reactor controller | 4 (+ Harbinger's witherite) |
| Tech | MekaSuit pieces and Meka-Tool | 2 each |
| Tech | Draconic Evolution awakened core | 2 |
| Magic | Ars Nouveau tier-3 mage armor upgrade | 1 per piece |
| Magic | Iron's Spells legendary ink (replaces the amethyst) | 1 |
| Magic | Iron & Nouveau legendary-spell glyphs | 1 |
| Magic | Occultism afrit summoning (red chalk tier) and the miner djinni | 1 each |
| Magic | Theurgy netherite route | 1 |
| Magic | Neo Vitae crystal cluster (transcendent orb) and teleposition reagent | 1 each |
| Magic | Vampirism lord level 3 (vampire and hunter) | 2 |
| Gear | Apotheosis Summit world tier (advancement) | 1 owned |

Supply today: horror mobs drop one 15% of the time, mutants 1–2 half the time, bosses 3–5, and chest loot. That's enough for players who visit regularly, and none for players who never go. That pull toward the Hollow is intended, but everything gated is optional (decision D4).

## 6. Design decisions
- **D1. The Ravenous eats blocks** (the mod's default). Keep it on: camps need obsidian walls or the Sanctuary. That's the biggest piece of bite. Or turn it off, so it only hunts and builds are safe. **Decided: on.**
- **D2. Low sanity spawns real hallucination mobs** below 25%. **Decided: keep them** (capped, with warning).
- **D3. The Pale Beacon needs 1 Hollow Ember per in-game day**, rather than being free once built. **Decided: feed it.**
- **D4. How hard Hollow Ember gates:** only the items in section 5, or also the Apotheosis Pinnacle tier (killing the Corrupted Champion or Gate Guardian)? **Decided: section 5 only;** Pinnacle stays the Dragon.
- **D5. The Lost Signal story pages:** worth it (6 written pages, quest text)? **Decided: yes.**

## 7. Research notes (from the mod jars)
- **Corrupted Champion** (`graveyard:lich`):
  - Stats: 400 + 200 HP, armor 14, toughness 12, damage 30 (+40 hunting).
  - Abilities: summons up to 30 mobs, teleport-heals, levitation.
  - Lives in `graveyard:lich_prison` (sky, Y 210). Drops one of five bone staffs, which bind a Ghouling companion.
- **Gate Guardian** (`grim_and_bleak:gate_guardian`):
  - Stats: 300 HP, armor 20, damage 10; immune to fire, fall, explosions, potions and wither.
  - Sits dormant in `grim_and_bleak:dimensional_gate`; the Gate Key wakes it.
  - Its only drop needs the Thunder Sword killing blow. Whether other weapons can damage it needs an in-game test.
- **Damned Templar:** 40 HP, armor 10. Summoned with `grim_and_bleak:cursed_amulet`. Drops templar armor or a claymore, the `templar_artifact` and a Zap book.
- **Mutants:** zombie 150 HP, skeleton 150, creeper 120, enderman 200.
  - The Endersoul Hand isn't a drop: toss an Ender Eye near Endersoul Fragments.
- **The Ravenous:** phases at 250–550 HP. It eats kills, mutates and lays eggs that hatch Screechers.
  - Block-breaking is on by default (op command `/RavenousBreak_false`). `#minecraft:screech_blocks` lists what it can't eat.
- **Sanity: Renewed:**
  - Commands `/sanity set|add` (op level 2).
  - Per-dimension `[sanity.passive] blocks` comfort list, with radius and line of sight.
  - Advancements give +20 sanity, so Hollow quest advancements double as relief.
  - Below 25% sanity, hostile hallucination mobs spawn.
- **Holy Cross:**
  - Not craftable: one in each Grim & Bleak chapel, and it drops itself when mined.
  - When placed, it gives "in church" comfort and plays a bell.
- **Strong items to watch:**
  - Grim & Bleak's Totem of Resurrection: reusable, costs "worthiness".
  - Grim & Bleak's offering ritual pays out netherite and enchanted golden apples.
  - Carbon Blood's Blood Dash: a short dash to a target, which counts as earned movement.
  - The Nameless Hanged trade (corruption for 2 emeralds) is an emerald engine. Consider lowering it.
