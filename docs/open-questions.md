# Strata — open design questions

Strata is a 1.21.1 NeoForge kitchen-sink pack (Create Aeronautics, Mekanism, Ars Nouveau hub, Cobblemon in its own dimension). Phase 1 added every "Keep" mod with a 1.21.1 NeoForge build, checked against the Modrinth and CurseForge APIs. These are the design questions that came out of it. Details of what was applied are in REPORT.md ("Round 1 decisions applied"). Numbers are kept so other docs can refer to them.

## Open

- **#22 Pokémon world portal**: a NeoForge portal mod or a KubeJS-scripted portal? To decide when the Pokémon world is built.
- **#23 Cobblemon Kanto map** (second portal, later): still planned? License not yet checked. To decide when the Pokémon world is built.

## Resolved

### A. Mods with no exact match (Keep rows)

1. **"Create Thrusters"**: no mod has this exact name. Candidates were Create Aeronautics: Gadgets & Gizmos (formerly "Thrusters'n'Things", 1M+ downloads, 2.0 pre-release), Create: Simulated Thrusters (26k downloads), Create: Linked Thrusters (redstone-linked thrusters), or none (Create Propulsion: Simulated covers it). **Resolved:** Create Aeronautics: Gadgets & Gizmos, pinned to 1.2.10. Create Propulsion: Simulated stays in too.
2. **Drive By Wire**: the original is Forge-only with no 1.21.1 build. **Resolved:** the fork **Drive-By-Wire with Sable** (395k downloads, made for Sable/Aeronautics vehicles).
3. **Domestication Innovation**: abandoned since 2023. **Resolved:** the fork **Redomesticate** (1.21.1 NeoForge, updated Oct 2026). The design doc uses it as the pet safety net.
4. **Botania**: no 1.21.1 build, so **Ars Botania** (which requires Botania) is out too. **Resolved:** both cut, no replacement bridge. Ars, Iron's, Occultism, Vampirism and Neo Vitae cover magic.
5. **Discord bridge mod**: not named in the tracker, and Discord Integration (dcintegration) has no 1.21.1 NeoForge build. **Resolved:** Simple Discord Link (`sdlink`, server-only, + CraterLib). Options compared in REPORT.md.
6. **Farmer's Delight add-ons**: Farmer's Delight, Vampire's Delight and Create Slice & Dice / Central Kitchen were already in. **Resolved:** added Ender's Delight, Twilight's Flavor & Delight, Ars Nouveau's Flavors & Delight, L_Ender's Cataclysm Delight and Aether's Delight (list in REPORT.md). Ocean's Delight and My Nether's Delight came in later (`docs/mod-gap-analysis.md`).

### B. Conflicts found

7. **Just Enough Resources (JER)** is a JEI plugin, and the pack uses EMI. **Resolved:** JEI and JER are both out. EMI is the only recipe viewer; EMI Ores, Advanced Loot Info and Just Enough Breeding cover what JER did. JEI builds its recipe index on the client's main thread when joining (about 60 s with this pack), which timed players out.
8. **Continuity**: on NeoForge it only runs through Sinytra Connector (a layer for running Fabric mods), a crash risk in a pack this size. **Resolved:** kept out. Fusion covers connected textures.
9. **Quark (+ Zeta)**: pulled in as a required dependency of Integrated Cataclysm; not in the tracker. **Resolved:** kept, with overlapping modules disabled (`config/quark-common.toml`, see REPORT.md).

### C. "Maybe" rows

10. **Modern Industrialization or Oritech**: **Resolved:** Oritech.
11. **Spice of Life or Diet**: Diet has no 1.21.1 build. **Resolved:** Spice of Life: Onion added.
12. **Neo Vitae** (Blood Magic continuation): in.
13. **The Aether**: in.
14. **The Undergarden** (beta build): not added.
15. **Blue Skies**: no 1.21.1 build; cut.
16. **Alex's Mobs**: the original has no 1.21.1 build. **Resolved:** Alex's Mobs Continued (fork, 1.21.1 NeoForge).
17. **Bosses of Mass Destruction**: the original has no NeoForge build. **Resolved:** the "Bosses of Mass Destruction Forge" port (1.21.1 NeoForge).
18. **Create: Better Motors**: not added.
19. **Plushie mod**: **Resolved:** "Plushie Mod" (1.21.1 NeoForge).
20. **Accessories + Accessories Compatibility Layer**: not added. Curios is the accessory standard; Accessories only if a mod needs it.
21. **Dimension Gated Difficulty** (fallback): no 1.21.1 build; cut. Majrusz's Progressive Difficulty Continued was dropped too (excluded from third-party downloads). Difficulty is per player; there are no server-wide stages.

### Other settled choices
- Gravestone: Corail Tombstone (replaced GraveStone Mod). Dynamic lighting: LambDynamicLights.
- Create: Steam 'n' Rails: the unofficial 1.21.1 port (beta); the snow-track crash is test 10.
- No Mons In My World: Fabric-only; recreated when the Pokémon world is built (options are in the design doc).
