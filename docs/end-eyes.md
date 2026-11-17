# End portal eyes

The stronghold portal (End Remastered) needs 12 **different** eyes. Strata has 15 obtainable eyes, and every
one has a single **guaranteed** source: no eye is a random chest or mob drop. Built by `tools/build_end_eyes.py`
(re-run after an End Remastered, Create, Ars Nouveau or structure-mod update); compasses in
`kubejs/server_scripts/strata_end_eyes.js`; the quest chapter **The End** walks players through all of it.

| Eye | Source | How to find it |
|---|---|---|
| Guardian | Elder Guardian (100%, killer only; 3 per monument) | Seeker's Compass: Ocean Monument |
| Wither | the Wither (100%) | summoned |
| Cursed | Ignis (100%) | Cataclysm's Eye of Flame |
| Nether | Netherite Monstrosity (100%) | Cataclysm's Eye of Monstrous |
| Corrupted | the Harbinger (100%) | Cataclysm's Eye of Mech |
| Old | YUNG's desert temple, Pharaoh's tomb chests (`betterdeserttemples:chests/tomb_pharaoh`) | Seeker's Compass: Pharaoh's Tomb |
| Evil | YUNG's jungle temple treasure room (`betterjungletemples:chests/treasure`) | Seeker's Compass: Jungle Temple |
| Lost | Dungeons Arise Foundry treasure chests | Seeker's Compass: Foundry |
| Black | pirate ship treasure chests (Corsair Corvette, Pirate Junk, Undead Pirate Ship) | Seeker's Compass: Pirate Ship |
| Cold | `minecraft:chests/igloo_chest`: the Frostbitten Temple (always) and igloo cellars (about half of igloos) | Seeker's Compass: Frostbitten Temple |
| Rogue | Create sequenced assembly from an Eye of Ender (2 loops: deploy brass sheet, deploy precision mechanism, deploy electron tube, spout 250 mB lava, press) → Red-Hot Rogue Eye → quenched by washing (Encased Fan through water); redrawn as a machine eye (brass gear housing, green lens) in `kubejs/assets/endrem/textures` | crafted |
| Magical | Ars Enchanting Apparatus (Eye of Ender, 7 essences, Source Gem Block, 5,000 source) → Dormant Magical Eye → Imbuement Chamber (amethyst cluster, ghast tear, Source Gem Block, 5,000 source) | crafted |
| Undead, Witch, Exotic | End Remastered's own recipes (Undead Soul from skeleton horses, Witch Pupil from witches, conduits and corals): the **spares** | crafted |

- **Spares:** with 15 eyes for 12 frames, a player can skip up to three eyes. Ten eyes need no boss, so the
  minimum is two boss eyes, and the Elder Guardian is the easy one.
- **Everyone gets their own:** boss loot bags roll the boss's table (with the eye) for every player in the fight,
  and Lootr gives each player their own chest loot. One filled portal works for everyone.
- **Off:** End Remastered's eyes in vanilla chest tables and from Evokers (`kubejs/data/endrem/loot_table`),
  the Cryptic Eye (random on enchanting) and the Evil Eye's Cleric trade
  (`config/EndRemastered-NeoForge/endrem.json`). The Cryptic Eye is unobtainable: the "sixteenth eye" of the lore.
- **Seeker's Compass:** a vanilla compass with custom data, crafted from the compass, an Eye of Ender and four
  corner plus three side items that fit the place. Right-click: it finds the nearest matching structure within
  6,400 blocks (`#strata:seeker/<key>`), points its needle there and gives a rough distance (no coordinates).
  Overworld only. The Explorer's Compass can't search for these structures
  (`config/explorerscompass-common.toml` blacklist), so exploring is free and the compass is the paid way.
- **Lore:** each eye's tooltip (`kubejs/assets/endrem/lang/en_us.json`) names its keeper.

## The End is sealed until the portal is opened (Nov 17)
The eyes are the gate, but a portal is not the only way into a dimension in a pack this size. An audit on Nov 17
(every jar's loot, recipes, structures and teleport code) found the eye sources sound and four ways around them,
none of them tried in play:

| Way in | Closed by |
|---|---|
| A Weeping Angels catacomb room ("psycho") holds a working 3x3 End portal; catacombs generate in the Hollow | the room is taken out of the catacomb's pool (`tools/build_mod_fixes.py <mods dir>`) |
| Oritech's particle accelerator makes an End portal when two ender pearls collide fast enough | `endPortalRequiredSpeed = 2147483647` in `config/oritech-common.toml` |
| AE2 Spatial IO could move portal blocks and the pre-filled vanilla frames of a Neo Vitae dungeon room; End Remastered counts a filled vanilla frame | portal blocks and frames are in `c:relocation_not_supported` (also read by Mekanism's Cardboard Box, Ars and Create) |
| Integrated Dynamics' teleport packet moves the sender anywhere with no permission check (needs a modified client) | Strata Tweaks 1.2.1 ignores it from non-ops |

**The rule behind them** (`kubejs/startup_scripts/strata_end_gate.js`): until the End has been opened, no player can
travel to `minecraft:the_end` by any means, except through an End portal ringed by twelve End Remastered frames
that each hold an eye. The first such crossing opens the End for good (server flag `strata_end_open`) and is
announced; after that every way in works as the mods ship it (/tpa to a friend, teleporters, waystones). Ops pass
without opening it; `/endgate`, `/endgate open`, `/endgate close` (ops) show and set the flag. Tested Nov 17 on a
test server with a non-op player: a command teleport, a bare portal, a ring of twelve filled vanilla frames and a
ring with eleven eyes were all refused; twelve eyes let the player through and opened it; `/endgate close` sealed
it again.

Noted, not changed: the Guardian Eye's loot entry has no "killed by a player" condition (the table above says
killer only), and the Elder Guardian is not in the tags that keep bosses out of mob farms and soul gems. Duplicate
eyes don't help against the twelve-different rule.
