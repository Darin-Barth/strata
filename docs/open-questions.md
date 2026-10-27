# Strata — open questions after phase 1

> **Answered Oct 23, 2026.** What was applied is in REPORT.md ("Round 1 decisions applied"). Still open: the Discord bridge pick (#5), MI vs Oritech (#10, decide in the creative test), and the portal and Kanto license (#22–23, when we build the Pokémon world).

Context for whoever answers: Strata is a 1.21.1 NeoForge kitchen-sink pack (Create Aeronautics, Mekanism, Ars Nouveau hub, Cobblemon in its own dimension) for 5–6 friends. Phase 1 added every "Keep" mod with a 1.21.1 NeoForge build, checked against the Modrinth and CurseForge APIs on Oct 23, 2026. These are the choices still open. A short answer per question is enough; "don't know" is fine too.

## A. Mods with no exact match (Keep rows)

1. **"Create Thrusters"**: no mod has this exact name. Which one was meant?
   - (a) Create Aeronautics: Gadgets & Gizmos (formerly "Thrusters'n'Things", 1M+ downloads, 2.0 pre-release)
   - (b) Create: Simulated Thrusters (26k downloads)
   - (c) Create: Linked Thrusters (redstone-linked thrusters)
   - (d) None. Create Propulsion: Simulated (already in) covers it.
2. **Drive By Wire**: the original is Forge-only with no 1.21.1 build. Use the fork **"Drive-By-Wire with Sable"** (395k downloads, made for Sable/Aeronautics vehicles)? Yes / no.
3. **Domestication Innovation**: abandoned since 2023. Use the fork **Redomesticate** (1.21.1 NeoForge, updated Oct 2026)? Yes / no. (The design doc uses it as the pet safety net.)
4. **Botania**: no 1.21.1 build exists, so **Ars Botania** (which requires Botania) is out too. OK to leave both out for now? Is there a replacement Ars ↔ mana bridge you want instead?
5. **Discord bridge mod**: not named in the tracker, and Discord Integration (dcintegration) has no 1.21.1 NeoForge build. Was a specific mod chosen? If not, should I list the ones that do have builds?
6. **Farmer's Delight add-ons**: Farmer's Delight, Vampire's Delight and Create Slice & Dice / Central Kitchen are in. Were any other add-ons decided (e.g. Ender's Delight, Ocean's Delight, Expanded Delight)?

## B. Conflicts found

7. **Just Enough Resources (JER)** is a JEI plugin, and JEI isn't in the pack (EMI was chosen). Pick one:
   - (a) Add JEI alongside EMI (EMI can run JEI plugins).
   - (b) Drop JER.
8. **Continuity** was removed, because on NeoForge it only runs through Sinytra Connector (a layer for running Fabric mods), a crash risk in a pack this size. Fusion already covers connected textures. OK to keep it out?
9. **Quark (+ Zeta)** was pulled in as a required dependency of Integrated Cataclysm. The tracker doesn't list Quark. Keep it (and maybe disable its features that overlap other mods), or drop Integrated Cataclysm?

## C. "Maybe" rows (all have 1.21.1 NeoForge builds unless noted)

10. **Modern Industrialization or Oritech**: which one? (Both have builds.)
11. **Spice of Life or Diet**: Diet has no 1.21.1 build, so this is **Spice of Life: Onion** or nothing. Add it?
12. **Neo Vitae** (Blood Magic continuation): in or out?
13. **The Aether**: in or out?
14. **The Undergarden** (beta build): in or out?
15. **Blue Skies**: no 1.21.1 build. Confirm it's out.
16. **Alex's Mobs**: the original has no 1.21.1 build. Use **Alex's Mobs Continued** (fork, 1.21.1 NeoForge)?
17. **Bosses of Mass Destruction**: the original has no NeoForge build. Use the **"Bosses of Mass Destruction Forge"** port (has 1.21.1 NeoForge)?
18. **Create: Better Motors**: still skipped unless alternators feel weak?
19. **Plushie mod**: "Plushie Mod" has a 1.21.1 NeoForge build. Add it, or was a different one meant?
20. **Accessories + Accessories Compatibility Layer**: no mod needs it so far. Keep it out unless one does?
21. **Dimension Gated Difficulty** (fallback): no 1.21.1 build. Not needed, since Majrusz's Progressive Difficulty Continued has a build. OK?

## D. Older open questions (from the design doc)

22. **Pokémon world portal**: a NeoForge portal mod or a KubeJS-scripted portal? Any specific mod in mind?
23. **Cobblemon Kanto map** (second portal, later): still planned? Any license info already checked?

## Already decided (no answer needed)
- Gravestone: Corail Tombstone (replaced GraveStone Mod, Oct 27). Dynamic lighting: LambDynamicLights.
- Create: Steam 'n' Rails: using the unofficial 1.21.1 port (beta); snow-track crash is test 10.
- No Mons In My World: Fabric-only; we recreate it when we build the Pokémon world (options are in the design doc).
