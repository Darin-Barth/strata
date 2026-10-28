# Progressive difficulty: options

> **Superseded, kept for reference.** Option E (a KubeJS script) was chosen over Majrusz's, which is not in the pack. The script was then not built: the pack has no server-wide difficulty stages, and difficulty stays per player (see the design doc's Progression and difficulty). The planned script spec is in the design doc's KubeJS to-do list.

**Problem:** Majrusz's Progressive Difficulty Continued (CurseForge only, by DraupnirDev) is excluded from the CurseForge API, so packwiz, the itzg server image and launcher installs can't download it automatically. It is not on Modrinth.

**What the design asks for:** staged difficulty (Normal → Expert after the first Nether visit → Master after the Ender Dragon); it is the only thing scaling regular mobs; bosses keep their designed stats; a modest Nether step with bigger jumps in dangerous dimensions.

## Majrusz's Continued: facts
- **MIT license.** Redistributing the jar with its license notice is allowed. The CurseForge opt-out is the author's distribution preference, not a license term.
- Actively maintained (updated Oct 14, 2026; 46.9k downloads). No dependencies in this port. Every setting can be edited in-game.
- Extras beyond mob scaling: mob groups with leaders, the Undead Army raid, Treasure Bags, Bleeding plus Bandages, and an Enderium ore/armor tier above Netherite (affects gear progression; check it against Apotheosis and the boss gating).
- **Watch out:** its page says Expert starts on entering the Nether "or any dimension from other mods". In Strata that includes Twilight Forest, the Aether and the Pokémon world. The trigger would need to be limited to the Nether.

## Options
| Option | Auto-download | Matches the stage design | Bosses keep stats | Trust / upkeep | Notes |
| --- | --- | --- | --- | --- | --- |
| **A. Majrusz's, self-hosted** (jar committed to the repo, MIT notice) | Yes, from the pack URL | Yes (watch the "any dimension" trigger) | Unverified | Maintained upstream; the jar is re-uploaded the jar on each update | Legal under MIT, but works around the author's opt-out. Asking the author first is the courteous move |
| **B. Majrusz's, manual download** | No | Same as A | Same as A | Every player and the server download each update by hand; breaks packwiz auto-updates | Not practical for 6 players |
| **C. Better Difficulty** (Modrinth, MIT) | Yes | Yes: the same Normal → Expert (Nether) → Master (Dragon) stages, global or per player | Unknown | 1.2k downloads, closed source, last update Apr 2026 | 21 toggleable features (charged creepers, homing pillager rockets, etc.). Closest drop-in replacement, but little adoption |
| **D. Further Difficulty Config** (Modrinth, MIT) | Yes | Yes: JSON stages triggered by entering a dimension or killing a mob, with health/armor/damage modifiers | Unclear (has a per-stage spawn blacklist) | ~500 downloads, v1.0.0 (Feb 2026), closed source | Does only the stat scaling, nothing extra |
| **E. KubeJS script** (no new mod) | Yes (a pack script) | Exactly: global stage set on the first Nether entry or Dragon kill, multipliers per stage and per dimension | Yes (skip `c:bosses` / an exclude list) | About 60 lines to write and maintain in the pack | Tailored to the design, but none of Majrusz's extras |
| **F. Location-based**: Dungeon Difficulty (790k, ARR), Configurable Difficulty, Silent's Power Scale (Scaling Health successor) | Yes | No: these scale by dimension, biome, distance or time, not milestones | Configurable | Well maintained (Dungeon Difficulty, Power Scale) | Dungeon Difficulty also scales loot, which overlaps Apotheosis. Better as an add-on than a replacement |

Others seen but not shortlisted: Improved Mobs (time-based, all rights reserved), Scaling Difficulty (time/distance), Remnants RPG Mobs (levels plus elite ranks, which overlap Apotheosis elites), Buff Mobs, NoreStages (95 downloads, beta), HyperStorm's / Dynamic Difficulty (CurseForge only, not checked for the API opt-out).

## Recommendation
**A (self-host Majrusz's under its MIT license)** keeps the mod the design was built around, with no manual downloads. As a courtesy, the author would be told it is bundled in a private 6-player pack. If bundling someone else's jar is not wanted, **E (KubeJS)** is the cleanest fit for the stage rules and boss exemption. **C (Better Difficulty)** is the closest one-mod swap, but it has little adoption and no public source.

Either way, the Nether-only trigger and boss exemption go into test 6 (the Nether difficulty jump).
