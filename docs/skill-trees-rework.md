# Skill trees rework

Status: **built** by `tools/build_skill_trees.py` (shipped in 1.0; re-run after a skill-tree add-on
update).

**Redesign after 1.1 (queued):** the 1.0 trees ran out far too fast. Combat needed only 1,262 XP in total,
and without a `level_limit` Pufferfish's Skills kept giving points past the list (a player had 32 of 25 levels
after one day). Now every node can be unlocked at max level, the level cap equals the tree's total point
cost, and the climb is long:

| Tree | Nodes | Levels (cap) | Total XP (1.0) |
|---|---|---|---|
| Combat | 4 branches of 10, two keystones each (Warrior: Bloodthirst, Sunder; Ranger: Deadeye, Sharpshooter; Guardian: Bulwark, Unbreakable; Duelist: Precision, Executioner) | 57 | 20,000 (1,262) |
| Mining | 3 branches of 10, two keystones each (Speed: Tunneler, Excavator; Prospector: two Lucky Strikes; Delver: Deep Delver, Spelunker) | 43 | 45,000 (7,500) |
| Fishing | unchanged layout | 21 | 6,000 (3,300) |
| Magic | unchanged; now capped at its own level count | as before | as before |

Small nodes are smaller than 1.0's (+4% damage instead of +6%), so a full tree ends about 1.5x the 1.0
maximum. XP is kept; `server_scripts/strata_skills_refund.js` resets each player's Combat, Mining and
Fishing nodes once at their first login after the update, so every point can be re-spent. The tables
below are the 1.0 design. Mod: Pufferfish's Skills (Ctrl+K), with Default Skill
Trees (Combat, Mining), Iron's Spells Dynamic Skill Trees (magic) and our own Fishing tree.

## Problems with the default trees

| Tree | Levels (points) | What a node gives | Problem |
|---|---|---|---|
| Combat | 40 (capped by us) | +3% damage, +1% resistance, +2 health, +5% speed | Nobody notices +3%; Apotheosis gear affixes are far bigger |
| Mining | 21 | +3% mining speed or +0.1 Fortune | XP only from stone and *vanilla* ore blocks, so the pack's modded ores probably give none (from the config; not tested in game); +0.1 Fortune may do nothing at all if it rounds down (to check in game) |
| Magic (Iron's) | 50, then two school trees | +1% spell power, +5 mana, +1% cooldown | 44,700 XP for the first tree; the school trees need another 80,500 |
| Fishing (ours) | 14 | +0.25 luck, breath, swim speed | Small, but it's the one tree with a theme |

Every node is a stat bump; none changes **how** you fight, mine or cast.

## Design

- **Fewer, bigger nodes:** about 20 to 25 per tree. A small node is +5% to +8%, so a single
  point shows up.
- **Keystones:** every tree has 3 or 4 milestone nodes that change play, built on attributes the
  pack already has: Apothic Attributes (crit chance, crit damage, life steal, dodge, armor pierce,
  overheal, experience gained) and Pufferfish's Attributes (fortune, natural regeneration,
  fall reduction, sprint speed).
- **Branches = playstyles:** you can't max everything with the points you get, so two players
  end up with different builds.
- **XP from what Strata players actually do:** all ores (the `c:ores` tag, so modded ores
  count), faster magic XP, kills as in the default trees (the anti-farm limit stays).
- **Same power at the top:** a maxed tree ends near the default trees' total, just concentrated where you
  chose. Bosses and the Hollow's 40% damage cap stay balanced.

## Trees

### Combat (25 levels, 4 branches)

| Branch | Small nodes | Keystone |
|---|---|---|
| Warrior | +6% melee damage ×4, +5% attack speed | **Bloodthirst:** 5% life steal |
| Ranger | +6% ranged damage ×4, +10% draw speed | **Deadeye:** +20% arrow speed, ignore 3 armor |
| Guardian | +2 health ×3, +2% resistance ×2 | **Bulwark:** 5% dodge chance |
| Duelist | +5% crit damage ×3, +4% move speed ×2 | **Executioner:** +10% crit chance, +25% crit damage |

### Mining (20 levels)

| Branch | Small nodes | Keystone |
|---|---|---|
| Speed | +8% mining speed ×5 | **Tunneler:** +20% shovel and axe speed |
| Prospector | +8% mining speed ×2 | **Lucky Strike:** +1 Fortune (whole level), twice in the branch |
| Delver | +10% experience gained ×2 | **Deep Delver:** less fall damage, +10% sprint speed |

XP: every block in `c:ores` (modded ores too), more for deepslate and Nether ores, a little for
stone. Same 20-level curve.

### Magic (Iron's trees)

Keep the add-on's layout (a general tree, then pick a school, then a second school), but:
- **XP:** about a third of the default (first tree around 15,000 XP; the default is 44,700).
- **Node values:** doubled, so a spell-power node is +2% to +6%. The general tree has half the
  points, 25, with nodes twice as strong, which keeps "same power at the top". The school trees
  keep their points, so a maxed school is about twice as strong as the add-on's default.
- **Keystones:** −10% cooldowns on the node that opens the school trees, and +10% spell power
  (all schools; the node is shared by every school path) on the node that ends each school tree.

### Fishing (ours)

Keep the theme; double the values, and add a keystone: **Sea Legs** (+20% swim speed, longer
breath underwater). That fits the Abyssal Plain.

## Notes

- Existing players: to check on the test server how Pufferfish's Skills handles points already
  spent when a tree's layout changes (if needed, an op command resets everyone's trees once).
- Built as datapack overrides in `kubejs/data/` (and our own `strata:` category), generated by
  `tools/build_skill_trees.py`, so mod updates don't wipe them.
- To check in game before release: fractional Fortune, the keystone attributes showing in the
  attribute screen, and modded ores giving Mining XP.
