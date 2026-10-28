# Mod requests: review

Requested mods: 37, focused on post-Dragon bosses, magic power to beat them, QoL and multiplayer fun. Each was checked for a **Minecraft 1.21.1 NeoForge** build on CurseForge and opened to see what worldgen it adds.

**Status:** the Recommended list is added, except:
- T.O Magic 'n Extras: its only 1.21.1 file is a deprecated alpha that crashes the game.
- Frieren Flight: blocked from automatic downloads on CurseForge, and not on Modrinth.

Ars Trinkets also needed Caelus (added; it has no flight items). Boot test with the chosen seed: loads cleanly. PlayerRevive's revive window is 30 s (`config/playerrevive.json`, `bleedTime` 600; default 60 s).

**Known gap:** Cataclysm: Spellbooks' mechanical items (gauntlets, mechanical scrap and their upgrades) don't register in this pack, so 11 of its recipes don't load. The rest of the mod works.

**Worldgen context:** the Overworld seed and spawn are already chosen. Mods that add Overworld **biomes** would reshape the land around spawn. None on this list do. Mods that add **structures** are fine, but must be decided **before the world is pregenerated**.

## Already in Strata
Ars 'n Spells, Vampires Need Umbrellas, Occultism, Vampirism, Inventory Pets.

## No 1.21.1 NeoForge build (can't add)
Ars Instrumentum, Ars Nouveau – Extended Glyphs, Fantasy Ending, Ice and Fire: Spellbooks, Terramity, Catzilla, Souls Like Bosses, Automobility (Fabric only), Table Top Craft, Mino.

## Recommended
| Mod | Category | Notes |
| --- | --- | --- |
| **Bosses'Rise** | Bosses | Souls-like boss fights; 5 structures. Directly serves the endgame goal |
| **Qliphoth Awakening** | Bosses | Endgame bosses; 3 structures (needs FDLib) |
| **Cinematic Cataclysm** | Bosses | Cinematic intros for Cataclysm bosses (already in) |
| **GTBC's Cataclysmic Boss UI** | Bosses | Proper boss bars for Cataclysm |
| **T.O Magic 'n Extras** | Combat/magic | Big Iron's Spells add-on with endgame spells and gear. **Not added** (see Status) |
| **Cataclysm: Spellbooks** | Combat/magic | Iron's spells themed on Cataclysm bosses; ties the boss and magic pillars together |
| **Apprentice's Codex** | Magic | Guide/progression book for Iron's Spells |
| **StarbuncleMania** | Magic/utility | Ars Nouveau starbuncle automation upgrades |
| **Ars Trinkets** | Magic | Ars accessories. Check each trinket against the flight rule |
| **Frieren Flight (Iron's Spells)** | Magic | Flight spell that costs mana, which the flight rule allows. **Not added** (see Status) |
| **PlayerRevive** | Utility | Downed players can be revived. Revive window shortened to 30 s in config |
| **Locked In Slots** | Utility | Lock inventory slots (QoL) |
| **Mighty Mail** | Social | Mailboxes between players |
| **What Are They Up To** | Social | Shows what other players are doing (crafting, chatting, AFK) |
| **Meccha Crafteleon** | Social | Hide-and-seek minigame with its own arena dimension. **Removed:** in-game it took over the T (chat) key, popped a controls guide and posted an advert for an outside server and Discord in chat |
| **Hyperbox** | Utility/fun | Pocket-dimension boxes (walk into a box to enter a bigger room); not a teleport |

## Maybe (concerns reviewed)
**Outcome:** added Legendary Monsters, Apocalyptic Bosses, Crystal Chronicles and WaterFrames. Hyper 'N Hiei's Shenanigans was approved but blocks automatic CurseForge downloads, so it can't be packed. Wings of Fire not adopted: Ice and Fire dragons cover flying mounts.

| Mod | Concern |
| --- | --- |
| **Legendary Monsters** | Good endgame bosses; 13 structures and **mob spawns added to Overworld biomes**. Tune spawns so new players near spawn aren't flattened |
| **Apocalyptic Bosses** | 25+ bosses, but the author describes **"OP items"**, and it adds 11 structures plus Overworld spawns (mutant zombies and more). Balance risk with Apotheosis/boss gating |
| **Hyper 'N Hiei's Shenanigans** | Small Iron's add-on with 2 structures; fine but low priority |
| **Crystal Chronicles (Iron's)** | Alpha build. Adds its own dimension plus one End sub-biome (doesn't touch the Overworld) |
| **Wings of Fire** | Phoenix mounts summoned from a lantern. That's **free flight**, which breaks the flight rule unless cost-gated (e.g. KubeJS: fuel or durability per summon) |
| **WaterFrames: Multimedia** | Picture/video frames from URLs. Pulls in WATERMeDIA + native media binaries (large download) and an alpha video player |

## Checklist for added mods
- Add every new boss to boss gating and the quest book (bosses keep their designed stats).
- New structures need Lootr compatibility checks (vanilla chests) and a rarity pass, like Inventory Pets got.
- Decide before pregeneration.
