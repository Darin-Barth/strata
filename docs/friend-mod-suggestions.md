# Friend's mod suggestions: review (Oct 24, 2026)

Source: the shared list (37 mods; focus on post-Dragon bosses, magic power to beat them, QoL and group fun). Each was checked for a **Minecraft 1.21.1 NeoForge** build on CurseForge (the list's own links) and opened to see what worldgen it adds. **Update (Oct 24):** the Recommended list was added, except T.O Magic 'n Extras (its only 1.21.1 file is a deprecated alpha that crashes the game) and Frieren Flight (blocked from automatic downloads on CurseForge, not on Modrinth). Ars Trinkets also needed Caelus (added; it has no flight items).

**Important context:** the Overworld seed and spawn are already chosen. Mods that add Overworld **biomes** would reshape the land around spawn. None on this list do. Mods that add **structures** are fine, but must be decided **before the world is pregenerated**.

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
| **T.O Magic 'n Extras** | Combat/magic | Big Iron's Spells add-on with endgame spells and gear ("get stronger to beat the bosses") |
| **Cataclysm: Spellbooks** | Combat/magic | Iron's spells themed on Cataclysm bosses; ties the boss and magic pillars together |
| **Apprentice's Codex** | Magic | Guide/progression book for Iron's Spells |
| **StarbuncleMania** | Magic/utility | Ars Nouveau starbuncle automation upgrades |
| **Ars Trinkets** | Magic | Ars accessories. Check each trinket against the flight rule |
| **Frieren Flight (Iron's Spells)** | Magic | Flight spell that costs mana, which the flight rule allows |
| **PlayerRevive** | Utility | Downed players can be revived. Revive window can be shortened in config, as suggested |
| **Locked In Slots** | Utility | Lock inventory slots (QoL) |
| **Mighty Mail** | Friendly fun | Mailboxes between players |
| **What Are They Up To** | Friendly fun | Shows what other players are doing (crafting, chatting, AFK) |
| **Meccha Crafteleon** | Friendly fun | Hide-and-seek minigame with its own arena dimension |
| **Hyperbox** | Utility/fun | Pocket-dimension boxes (walk into a box to enter a bigger room); not a teleport |

## Maybe (concerns to settle first)
| Mod | Concern |
| --- | --- |
| **Legendary Monsters** | Good endgame bosses; 13 structures and **mob spawns added to Overworld biomes**. Tune spawns so new players near spawn aren't flattened |
| **Apocalyptic Bosses** | 25+ bosses, but the author describes **"OP items"**, and it adds 11 structures plus Overworld spawns (mutant zombies and more). Balance risk with Apotheosis/boss gating |
| **Hyper 'N Hiei's Shenanigans** | Small Iron's add-on with 2 structures; fine but low priority |
| **Crystal Chronicles (Iron's)** | Alpha build. Adds its own dimension plus one End sub-biome (doesn't touch the Overworld) |
| **Wings of Fire** | Phoenix mounts summoned from a lantern. That's **free flight**, which breaks the flight rule unless we cost-gate it (e.g. KubeJS: fuel or durability per summon) |
| **WaterFrames: Multimedia** | Picture/video frames from URLs. Pulls in WATERMeDIA + native media binaries (large download) and an alpha video player |

## If any are added
- Add every new boss to the difficulty script's "never scale" list, and to boss gating/quests.
- New structures need Lootr compatibility checks (vanilla chests) and a rarity pass, like Inventory Pets got.
- Decide before pregeneration.
