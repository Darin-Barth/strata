from dsl import *

C = chapter("boss_hunter", "Boss Hunter", group="bosses", icon="minecraft:wither_skeleton_skull",
            subtitle="Bosses from every corner of the world")
q = C.quest

q("intro", "What is Boss Hunter?", icon="minecraft:netherite_sword", size=1.5, shape="gear", desc="""
    Strata has bosses from many mods, scattered all over the world. This chapter is a
    hunting list: one branch per mod, with where to look.

    Every boss keeps its designed strength (World Tiers don't change them).
    Most are built for a group: bring friends, food, and a way home.

    &eTip:&r an &eExplorer's Compass&r finds structures by name, and many mods add an
    "Eye" that you throw to point the way.""",
  rewards=[give("minecraft:golden_apple", 2)])

# --- Mowzie's Mobs -----------------------------------------------------------------------
q("mowzie", "Mowzie's Mobs", deps="intro", icon="mowziesmobs:wrought_helmet", desc="""
    Hand-animated bosses with lots of personality. Each one lives in its own spot in the
    Overworld and fights with clear, readable attacks: learn the pattern, then strike.""")

q("wroughtnaut", "Ferrous Wroughtnaut", deps="mowzie", icon="mowziesmobs:wrought_axe", tier=3,
  shape="hexagon", tasks=kill("mowziesmobs:ferrous_wroughtnaut"), desc="""
    A living suit of armor in a &eWrought Chamber&r underground (around Y 20 to 50).
    Its armor shrugs off hits from the front: dodge its axe swing, then get behind it.

    &6Drops:&r the &eAxe of a Thousand Metals&r and the &eWrought Helm&r.""",
  rewards=[give("minecraft:iron_block", 2)])

q("frostmaw", "Frostmaw", deps="mowzie", icon="mowziesmobs:ice_crystal", tier=4, shape="hexagon",
  tasks=kill("mowziesmobs:frostmaw"), desc="""
    A huge ice beast asleep in open snowy biomes. Don't wake it unprepared.

    &6Drops:&r the &eIce Crystal&r (frost breath of your own), if it still has it when it dies.""",
  rewards=[give("minecraft:diamond", 4)])

q("umvuthi", "Umvuthi, the Sunbird", deps="mowzie", icon="mowziesmobs:sol_visage", tier=4, shape="hexagon",
  tasks=kill("mowziesmobs:umvuthi"), desc="""
    Leader of the masked Umvuthana, in a grove in the &esavanna&r. Its masked followers
    fight at its side.

    &6Drops:&r the &eSol Visage&r mask.""",
  rewards=[give("minecraft:gold_block", 2)])

q("sculptor", "Tongbi, the Sculptor", deps="mowzie", icon="mowziesmobs:sculptor_staff", tier=4,
  shape="hexagon", tasks=kill("mowziesmobs:sculptor"), desc="""
    Lives in a monastery on &emountain peaks&r. First its challenge: climb its stone course
    to the top without placing or breaking blocks, flying or teleporting.

    &6Drops:&r the &eGeomancer Staff&r and the Geomancer armor set.""",
  rewards=[give("minecraft:emerald", 16)])

q("naga", "Naga", deps="mowzie", icon="mowziesmobs:naga_fang", tier=3, optional=True, shape="hexagon",
  tasks=kill("mowziesmobs:naga"), desc="""
    Flying serpents of &erocky shores&r and beach cliffs. Bring a bow.

    &6Drops:&r &eNaga Fangs&r for a poison dagger.""",
  rewards=[give("minecraft:arrow", 64)])

# --- Bosses of Mass Destruction ----------------------------------------------------------
q("bomd", "Bosses of Mass Destruction", deps="intro", icon="bosses_of_mass_destruction:ancient_anima", desc="""
    Four bosses, each with its own arena: one in cold lands, one deep in the Overworld,
    one in the Nether and one in the End. Their drops craft some powerful blocks.""")

q("lich", "The Night Lich", deps="bomd", icon="bosses_of_mass_destruction:ancient_anima", tier=4,
  shape="hexagon", tasks=kill("bosses_of_mass_destruction:lich"), desc="""
    Haunts a tall tower in &ecold biomes&r. Fight it at night at your own risk.

    &6Drops:&r &eAncient Anima&r.""",
  rewards=[give("minecraft:diamond", 4)])

q("void_blossom", "The Void Blossom", deps="bomd", icon="bosses_of_mass_destruction:void_thorn", tier=4,
  shape="hexagon", tasks=kill("bosses_of_mass_destruction:void_blossom"), desc="""
    A giant plant boss hidden in the Overworld. Craft a &eVoid Lily&r (lily of the valley +
    amethyst shard) and watch where its pollen leads.

    &6Drops:&r &eVoid Thorns&r and &eCrystal Fruit&r (brief regeneration and resistance).""",
  rewards=[give("minecraft:emerald", 12)])

q("gauntlet", "The Nether Gauntlet", deps=["bomd", "welcome/nether"],
  icon="bosses_of_mass_destruction:blazing_eye", tier=4, shape="hexagon",
  tasks=kill("bosses_of_mass_destruction:gauntlet"), desc="""
    A giant living gauntlet in an arena deep in the &cNether&r. Its treasure holds the
    &eBlazing Eye&r.""",
  rewards=[give("minecraft:netherite_scrap", 2)])

q("obsidilith", "The Obsidilith", deps=["gauntlet", "the_end/dragon"],
  icon="bosses_of_mass_destruction:obsidian_heart", tier=5, shape="hexagon",
  tasks=kill("bosses_of_mass_destruction:obsidilith"), desc="""
    An obsidian pillar that comes alive in an arena on the &5End&r islands. Its treasure
    holds the &eObsidian Heart&r.""",
  rewards=[give("minecraft:diamond_block", 2)])

# --- Bosses'Rise -------------------------------------------------------------------------
q("rise", "Bosses'Rise", deps="intro", icon="block_factorys_bosses:ancient_trial_key", desc="""
    Souls-like boss fights: big telegraphed attacks, dodge (Combat Roll!) and punish.
    Five bosses, each in its own lair.""")

q("sandworm", "Sirok, the Sandworm", deps="rise", icon="block_factorys_bosses:sandworm_gauntlet", tier=3,
  shape="hexagon", tasks=kill("block_factorys_bosses:sandworm"), desc="""
    Lurks in a nest in the &edesert&r.

    &6Drops:&r the Sandworm Gauntlet.""",
  rewards=[give("minecraft:gold_ingot", 12)])

q("yeti", "Skor, the Yeti", deps="rise", icon="block_factorys_bosses:ice_gauntlet", tier=3, shape="hexagon",
  tasks=kill("block_factorys_bosses:yeti"), desc="""
    Hides out in the &esnowy plains&r and throws ice.

    &6Drops:&r the Skor Gauntlet.""",
  rewards=[give("minecraft:diamond", 3)])

q("kraken", "Nerakyss, the Kraken", deps="rise", icon="block_factorys_bosses:kraken_tooth", tier=4,
  shape="hexagon", tasks=kill("block_factorys_bosses:kraken"), desc="""
    Its lair is a ship in the &edeep ocean&r.

    &6Drops:&r Kraken Teeth.""",
  rewards=[give("minecraft:heart_of_the_sea")])

q("ashlord", "Ashlord, the Infernal Dragon", deps="rise", icon="block_factorys_bosses:dragon_skull",
  tier=4, shape="hexagon", tasks=kill("block_factorys_bosses:infernal_dragon"), desc="""
    Rules a tower in plains, jungles, swamps and savannas. Its guards drop
    &eAncient Trial Keys&r: keep them.

    &6Drops:&r Ashlord's bones and skull.""",
  rewards=[give("minecraft:diamond", 6)])

q("helvar", "Helvar, the Underworld Knight", deps=["rise", "welcome/nether"],
  icon="block_factorys_bosses:knight_sword", tier=4, shape="hexagon",
  tasks=kill("block_factorys_bosses:underworld_knight"), desc="""
    Waits in an arena in the &cNether&r (nether wastes and soul sand valleys). Soul skeletons
    and wither knights drop the &eUnderworld Arena Key&r.

    &6Drops:&r &eHelvar's Sword&r.""",
  rewards=[give("minecraft:netherite_scrap", 2)])

# --- Qliphoth Awakening ------------------------------------------------------------------
q("qliphoth", "Qliphoth Awakening", deps="intro", icon="fdbosses:qliphothic_codex",
  tasks=item("fdbosses:qliphothic_codex"), desc="""
    Three hard, mechanic-heavy bosses. Craft the &eQliphothic Codex&r (a book, logs and
    glowstone): it's the boss guide, with each boss and its attacks.

    Each has a craftable &eEye&r that points to its arena.""",
  rewards=[give("minecraft:ender_eye", 3)])

q("malkuth", "Malkuth", deps="qliphoth", icon="fdbosses:eye_of_malkuth", tier=4, shape="hexagon",
  tasks=kill("fdbosses:malkuth"), desc="""
    A fallen fire-and-ice king in an arena by the &edeep ocean&r (Eye of Malkuth: ice,
    magma and an Eye of Ender). You'll be weak to fire or ice in turns: the crosshair shows
    which. Use the cannons on your side. Leaving mid-fight is deadly.
    The developer says: fight him at night.""",
  rewards=[give("minecraft:diamond", 6)])

q("chesed", "Chesed", deps="qliphoth", icon="fdbosses:eye_of_chesed", tier=4, shape="hexagon",
  tasks=kill("fdbosses:chesed"), desc="""
    A sculk-corroded rock giant with huge lightning powers, in an arena deep underground
    (Y -30 to -50; Eye of Chesed: sculk around an Eye of Ender). It can't be hurt directly:
    read the Codex for how to turn its power against it. Diamond axes are recommended.""",
  rewards=[give("minecraft:diamond", 6)])

q("geburah", "Geburah", deps=["qliphoth", "the_end/dragon"], icon="fdbosses:eye_of_geburah", tier=5,
  shape="hexagon", tasks=kill("fdbosses:geburah"), desc="""
    A divine judge construct in an arena in the &5End&r, near End Cities
    (Eye of Geburah: gold and blackstone bricks).""",
  rewards=[give("minecraft:diamond_block", 2)])

# --- Legendary Monsters ------------------------------------------------------------------
q("legendary", "Legendary Monsters", deps="intro", icon="legendary_monsters:nature_crystal", desc="""
    Lots of bosses, each guarding a temple, ruin or nest. Their drops are rare crafting
    parts and weapons. Here are the main ones.""")

q("colossus", "Overgrown Colossus", deps="legendary", icon="legendary_monsters:nature_crystal", tier=3,
  shape="hexagon", tasks=kill("legendary_monsters:overgrown_colossus"), desc="""
    Lurks in a mossy temple in the &ejungle&r. &6Drops:&r a Nature Crystal.""",
  rewards=[give("minecraft:emerald", 8)])

q("dune_sentinel", "Dune Sentinel", deps="legendary", icon="legendary_monsters:crystal_of_sandstorm", tier=3,
  shape="hexagon", tasks=kill("legendary_monsters:dune_sentinel"), desc="""
    Guards a ruined pyramid in the &edesert&r, with bombers for company.
    &6Drops:&r the Crystal of Sandstorm.""",
  rewards=[give("minecraft:gold_ingot", 12)])

q("frostbitten_golem", "Frostbitten Golem", deps="legendary", icon="legendary_monsters:frozen_rune", tier=3,
  shape="hexagon", tasks=kill("legendary_monsters:frostbitten_golem"), desc="""
    In a frozen temple in &esnowy&r plains, taiga and ice spikes. &6Drops:&r a Frozen Rune.""",
  rewards=[give("minecraft:diamond", 3)])

q("cumulonimbus", "Cumulonimbus", deps="legendary", icon="legendary_monsters:air_rune", tier=4,
  shape="hexagon", tasks=kill("legendary_monsters:cloud_golem"), desc="""
    A storm-cloud golem at the top of the Cloudy Temple on &emountain peaks&r, with
    Hovering Hurricanes on the way up. &6Drops:&r an Air Rune.""",
  rewards=[give("minecraft:diamond", 4)])

q("ancient_guardian", "Ancient Guardian", deps="legendary", icon="legendary_monsters:anchor_handle", tier=4,
  shape="hexagon", tasks=kill("legendary_monsters:ancient_guardian"), desc="""
    Deep in an Ancient Stronghold under &edark forests&r and taigas, past the Ambushers.""",
  rewards=[give("minecraft:diamond", 4)])

q("paladin", "Possessed Paladin", deps="legendary", icon="legendary_monsters:soul_great_sword", tier=4,
  shape="hexagon", tasks=kill("legendary_monsters:posessed_paladin"), desc="""
    The last stand of a Collapsed Kingdom in &eplains and forests&r, guarded by haunted
    knights. &6Drops:&r a Corrupted Soul and the Soul Great Sword.""",
  rewards=[give("minecraft:diamond", 4)])

q("lava_eater", "Lava Eater", deps=["legendary", "welcome/nether"], icon="legendary_monsters:lava_eaters_skin",
  tier=4, shape="hexagon", tasks=kill("legendary_monsters:lava_eater"), desc="""
    Lives in the &cNether Wastes&r. &6Drops:&r Lava Eater's Skin.""",
  rewards=[give("minecraft:netherite_scrap", 2)])

q("withered_abomination", "Withered Abomination", deps=["legendary", "welcome/nether"],
  icon="legendary_monsters:withered_bone", tier=4, shape="hexagon",
  tasks=kill("legendary_monsters:withered_abomination"), desc="""
    In the remains of a soul fortress, in &cSoul Sand Valleys&r and Nether Wastes.""",
  rewards=[give("minecraft:netherite_scrap", 2)])

q("shulker_mimic", "Shulker Mimic", deps=["legendary", "the_end/dragon"],
  icon="legendary_monsters:large_shulker_shell", tier=4, shape="hexagon",
  tasks=kill("legendary_monsters:shulker_mimic"), desc="""
    Not every shulker is a shulker. Climb the Shulker Tower on the &5End&r's outer islands.""",
  rewards=[give("minecraft:shulker_shell", 4)])

q("annihilation_pursuer", "Annihilation Pursuer", deps="shulker_mimic",
  icon="legendary_monsters:enderitium_gem", tier=5, shape="hexagon",
  tasks=kill("legendary_monsters:annihilation_pursuer"), desc="""
    The boss of the &5End&r's Space Station, full of flameborn guards and wandering eyes.
    &6Drops:&r Enderitium Gems.""",
  rewards=[give("minecraft:diamond_block", 2)])

# --- Apocalyptic Bosses ------------------------------------------------------------------
q("apocalyptic", "Apocalyptic Bosses", deps="intro", icon="minecraft:skeleton_skull", desc="""
    Over 25 bosses, most of them in dungeons with rich treasure.

    &cCareful:&r a few of them, like the Gargoyle, the Golem King and mutant zombies, wander
    the forests and plains on their own. If one shows up early, run.""")

q("furacas", "Furacas", deps="apocalyptic", icon="minecraft:sand", tier=3, shape="hexagon",
  tasks=kill("panascraftrpgmod:furacas"), desc="""
    Waits in its dungeon in the &edesert&r.""",
  rewards=[give("minecraft:gold_ingot", 12)])

q("ice_lord", "Ice Lord", deps="apocalyptic", icon="minecraft:packed_ice", tier=3, shape="hexagon",
  tasks=kill("panascraftrpgmod:ice_lord"), desc="""
    Rules a dungeon in the &eIce Spikes&r.""",
  rewards=[give("minecraft:diamond", 3)])

q("t_rex", "T-Rex", deps="apocalyptic", icon="minecraft:bone_block", tier=3, optional=True, shape="hexagon",
  tasks=kill("panascraftrpgmod:t_rex"), desc="""
    Yes, really. Look for its dungeon in the &ejungle&r.""",
  rewards=[give("minecraft:bone_block", 8)])

q("silence_death", "The Silence Death", deps="apocalyptic", icon="minecraft:sculk_shrieker", tier=4,
  shape="hexagon", tasks=kill("panascraftrpgmod:the_silence_death"), desc="""
    Deep under the &emountains&r, in a sculk dungeon with the Echo King and sculk creatures.""",
  rewards=[give("minecraft:echo_shard", 4)])

q("lava_lord", "Lava Lord", deps=["apocalyptic", "welcome/nether"], icon="minecraft:magma_block", tier=4,
  shape="hexagon", tasks=kill("panascraftrpgmod:lava_lord"), desc="""
    Lives underground in the &cNether&r.""",
  rewards=[give("minecraft:netherite_scrap", 2)])

q("skeleton_god", "Skeleton God", deps=["apocalyptic", "welcome/nether"], icon="minecraft:wither_skeleton_skull",
  tier=4, shape="hexagon", tasks=kill("panascraftrpgmod:skeleton_god"), desc="""
    Holds court in a dungeon in the &cSoul Sand Valley&r.""",
  rewards=[give("minecraft:netherite_scrap", 2)])

q("the_chaos", "The Chaos", deps="lava_lord", icon="minecraft:crying_obsidian", tier=5, shape="hexagon",
  tasks=kill("panascraftrpgmod:the_chaos"), desc="""
    Hidden underground in the &cNether&r.""",
  rewards=[give("minecraft:diamond_block", 2)])

q("queen_abyss", "The Queen of the Abyss", deps=["the_chaos", "the_end/dragon"],
  icon="minecraft:dragon_head", tier=5, size=1.5, shape="hexagon",
  tasks=kill("panascraftrpgmod:the_queen_of_the_abyss"), desc="""
    The final boss, in a dungeon in the &5End&r, guarded by Abyssal Knights.""",
  rewards=[give("minecraft:netherite_ingot", 2), give("minecraft:enchanted_golden_apple")])

# --- Eternal Nether ----------------------------------------------------------------------
q("eternal_nether", "Eternal Nether", deps=["intro", "welcome/nether"], icon="minecraft:blackstone", tier=3,
  tasks=[structure("eternalnether:catacomb", title="A Catacomb (Soul Sand Valley)"),
         structure("eternalnether:citadel", title="A Citadel (Warped Forest)"),
         structure("eternalnether:piglin_manor", title="A Piglin Manor (Crimson Forest)")], desc="""
    &eEternal Nether&r has no single boss. Instead it adds three dangerous strongholds and
    tough new mobs: Wither Skeleton Knights, Wraithers, Corpors, Warped Endermen and
    Piglin Hunters. Visit all three. Some piglins are prisoners: rescue them.""",
  rewards=[give("minecraft:gold_block", 2)])

# --- Aquamirae ---------------------------------------------------------------------------
q("aquamirae", "The Ice Maze", deps="intro", icon="aquamirae:frozen_key", tier=2,
  tasks=adv("aquamirae:adventure/find_ice_maze", title="Enter the Ice Maze"), desc="""
    &eAquamirae&r covers &eDeep Frozen Oceans&r with the &bIce Maze&r: icebergs, frozen pirate
    ships and nasty sea creatures. Bring warm gear, a boat and torches.""",
  rewards=[give("minecraft:oak_boat"), give("minecraft:torch", 32)])

q("maze_mother", "Maze Mother", deps="aquamirae", icon="aquamirae:abyssal_amethyst", tier=3, shape="hexagon",
  tasks=kill("aquamirae:maze_mother"), desc="""
    A giant creature of the Ice Maze waters. &6Drops:&r &eAbyssal Amethyst&r for the
    Abyssal armor upgrade.""",
  rewards=[give("minecraft:prismarine_crystals", 16)])

q("shell_horn", "The Shell Horn", deps="aquamirae", icon="aquamirae:shell_horn", tier=2,
  tasks=item("aquamirae:shell_horn"), desc="""
    Frozen pirate ships in the Ice Maze hold a &eShell Horn&r. Blow it near water in the
    Ice Maze to summon a ghost.""",
  rewards=[give("minecraft:emerald", 8)])

q("cornelia", "Ghost of Captain Cornelia", deps="shell_horn", icon="aquamirae:frozen_key", tier=4,
  shape="hexagon", tasks=kill("aquamirae:captain_cornelia"), desc="""
    The restless ghost of a pirate captain. &6Drops:&r the &eFrozen Key&r and Salvager gear.""",
  rewards=[give("minecraft:diamond", 6)])

q("shipbreaker", "The Shipbreaker", deps="maze_mother", icon="aquamirae:ship_graveyard_echo", tier=4,
  optional=True, tasks=adv("aquamirae:adventure/encounter_the_shipbreaker", title="Meet the Shipbreaker"),
  desc="""
    The most fearsome thing in the Ice Maze. It finds you, not the other way round.
    Survive.""",
  rewards=[give("minecraft:golden_apple", 2)])

q("where_next", "Where Next?", deps=["mowzie", "bomd", "rise", "qliphoth", "legendary"], any_dep=True,
  icon="minecraft:compass", shape="diamond", desc="""
    &cL_Ender's Cataclysm&r: the bosses that unlock late tech.
    &cIce and Fire&r: dragons.
    &cCombat & Gear&r: salvage and reforge the loot you've collected.""")
