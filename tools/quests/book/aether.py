from dsl import *

C = chapter("aether", "The Aether", group="explore", icon="aether:aether_portal_frame",
            subtitle="Islands in the sky")
q = C.quest

q("intro", "What is the Aether?", deps="welcome/iron_age", icon="minecraft:glowstone", size=1.5,
  shape="gear", desc="""
    The Aether is a world of &bfloating islands&r high above the clouds: blue grass,
    golden trees, fluffy sheep and flying pigs. It's the opposite of the Nether.

    Strata is about flying, and the Aether is the sky dimension: islands, clouds and
    dungeons in the air. Don't fall off the edge!

    It has its own wood, stone, ores and three dungeons with bosses.""",
  rewards=[give("minecraft:glowstone", 4)])

q("portal", "The Glowstone Portal", deps="intro", icon="aether:aether_portal_frame", tier=2,
  tasks=dim("aether:the_aether", title="Enter the Aether"), desc="""
    Build a portal frame like a Nether portal, but out of &eGlowstone&r blocks.
    Then pour a &ebucket of water&r into it to light it.

    Glowstone comes from the Nether ceiling (or from witches).
    Bring a water bucket and some blocks: you'll arrive high in the sky.""",
  rewards=[give("minecraft:feather", 8), give("minecraft:cooked_beef", 12)])

# --- materials --------------------------------------------------------------------------
q("skyroot", "Skyroot and Holystone", deps="portal", icon="aether:skyroot_log",
  tasks=[item("aether:skyroot_planks", 16), item("aether:holystone", 32)], desc="""
    Aether wood is &eSkyroot&r and its stone is &eHolystone&r.
    Build tools from them: &eSkyroot tools&r double the drops of Holystone and Ambrosium.

    &eAmbrosium Shards&r are the Aether's coal. Eat one in a pinch for a little health.""",
  rewards=[give("minecraft:bread", 8)])

q("zanite", "Zanite", deps="skyroot", icon="aether:zanite_gemstone", tier=2,
  tasks=item("aether:zanite_gemstone", 8), desc="""
    Mine &eZanite Ore&r with a Holystone pickaxe or better.
    Zanite tools are like iron, with a twist: they get &efaster&r as they wear down.""",
  rewards=[give("minecraft:iron_ingot", 8)])

q("altar", "The Altar", deps="zanite", icon="aether:altar", tier=2,
  tasks=item("aether:altar"), desc="""
    The &eAltar&r enchants and repairs things using Ambrosium as fuel.
    The &eFreezer&r (powered by Icestone) freezes items, like water buckets into ice.
    The &eIncubator&r hatches Moa eggs (powered by Ambrosium Torches).""",
  rewards=[give("aether:ambrosium_shard", 16)])

q("gravitite", "Enchanted Gravitite", deps="altar", icon="aether:enchanted_gravitite", tier=3,
  tasks=item("aether:enchanted_gravitite", 4), desc="""
    &eGravitite Ore&r is the rarest Aether ore, and it floats up when nothing is above it.
    Put it in the Altar to make &eEnchanted Gravitite&r for the Aether's best tools and armor.

    A Gravitite pickaxe can lift stone blocks into the air with a right-click.""",
  rewards=[give("minecraft:diamond", 2)])

q("moa", "Raise a Moa", deps="altar", icon="aether:blue_moa_egg", tier=2,
  tasks=item("aether:incubator"), desc="""
    &eMoas&r are big friendly birds. Find a &eMoa Egg&r (Silver Dungeon chests have them),
    put it in an &eIncubator&r with Ambrosium Torches and wait for it to hatch.

    Ride your moa: it can jump in mid-air a few times. Blue moas get 3 jumps,
    rare black moas get 8. Great for hopping between islands!""",
  rewards=[give("aether:ambrosium_torch", 8)])

q("food", "Aether's Delight", deps="skyroot", icon="aethersdelight:blue_berry_muffin", optional=True,
  desc="""
    &eAether's Delight&r adds Aether cooking: blue berry muffins, ginger soup, moa stew,
    gingerbread cookies and a Holystone stove.""",
  rewards=[give("aethersdelight:gingerbread", 4)])

q("deep_aether", "The Deep Aether", deps="portal", icon="deep_aether:roseroot_planks", desc="""
    &eDeep Aether&r adds new biomes to the sky: glowing aerglow forests, golden heights,
    lavender fields and the yagroot swamp, with new animals like the &equail&r.

    It also adds &eSkyjade&r, a gem even sharper than diamond (but fragile),
    and a fourth dungeon, made of brass.""",
  rewards=[give("minecraft:wheat_seeds", 8)])

q("skyjade", "Skyjade", deps="deep_aether", icon="deep_aether:skyjade", tier=2,
  tasks=item("deep_aether:skyjade", 4), desc="""
    Find and mine &eSkyjade&r in the Deep Aether.
    Skyjade tools are very strong but get slower as they wear out. Repair them often.""")

q("villages", "Olympic Citadel", deps="portal", icon="minecraft:quartz_pillar", tier=2,
  tasks=structure("aether_villages:olympic_citadel", title="Find an Olympic Citadel"), desc="""
    &eAether Villages&r builds grand white citadels on the Skyroot islands.
    A nice place to visit, trade and catch your breath.""",
  rewards=[give("minecraft:emerald", 8)])

q("sky_dungeon", "Inventory Pets' Sky Dungeon", deps="portal", icon="minecraft:mossy_stone_bricks",
  tier=2, optional=True, tasks=structure("inventorypets:sky_dungeon", title="Find a Sky Dungeon"),
  desc="""
    Rare &eSky Dungeons&r from Inventory Pets float in the Aether too.
    Their chests have special loot that only exists in one place: no copies for friends here,
    so share what you find!""")

# --- dungeons ---------------------------------------------------------------------------
q("bronze", "Bronze Dungeon: The Slider", deps="zanite", icon="aether:bronze_dungeon_key", tier=3,
  tasks=kill("aether:slider"), desc="""
    Bronze dungeons hide inside islands. The boss is the &eSlider&r, a huge stone block
    that slides at you. Only a &epickaxe&r can hurt it.

    It drops a &eBronze Key&r to open the treasure chest. The treasure can include the
    &eValkyrie Lance&r and the Hammer of Kingbdogz.""",
  rewards=[give("minecraft:golden_apple", 2)])

q("silver", "Silver Dungeon: The Valkyrie Queen", deps="bronze", icon="aether:silver_dungeon_key",
  tier=4, tasks=[item("aether:victory_medal", 10, title="Collect 10 Victory Medals"),
                 kill("aether:valkyrie_queen")], desc="""
    Silver dungeons sit in the clouds, guarded by &eValkyries&r.
    Each defeated Valkyrie drops a &eVictory Medal&r. Bring &e10&r to prove to the
    &bValkyrie Queen&r that you're worthy, then fight her.

    Her &eSilver Key&r opens the treasure: Valkyrie gear, golden feathers and
    regeneration stones.""")

q("gold", "Gold Dungeon: The Sun Spirit", deps="silver", icon="aether:gold_dungeon_key", tier=5,
  tasks=kill("aether:sun_spirit"), desc="""
    The final Aether dungeon lies in a big island of hellfire stone.
    The &6Sun Spirit&r burns everything near it. Watch for its &bice crystals&r:
    when the Spirit is frozen, that's your moment to hit it.

    It drops a &eGold Key&r and a &eSun Altar&r (it controls the time of day).
    The treasure room has &cPhoenix armor&r and &dLife Shards&r (an extra heart each).""")

q("brass", "Brass Dungeon: Eye of the Storm", deps=["deep_aether", "bronze"],
  icon="deep_aether:skyjade_block", tier=4,
  tasks=structure("deep_aether:brass_dungeon", title="Find the Brass Dungeon"), desc="""
    Deep Aether's &eBrass Dungeon&r holds the &bEye of the Storm&r, a boss made of wind.
    "What a wind. Maybe I should try to hit that?"

    Deep Aether's storm weapons and heavy Stormforged armor come from this part of the sky.""")

q("reforging", "Treasure Reforging", deps="silver", icon="aether_treasure_reforging:valkyrum_ingot",
  tier=3, optional=True, desc="""
    &eAether Treasure Reforging&r lets you make more dungeon gear.
    The bronze, silver and gold treasure chests can hold &eupgrade smithing templates&r:
    Neptune (on Zanite armor), Valkyrie (on Gravitite gear) and Phoenix (on Gravitite armor).

    Smelt old dungeon gear down for its metal (Neptune Mesh, Valkyrum, Pyral) and reforge it.""")

q("where_next", "Where Next?", deps=["gold", "moa"], icon="minecraft:compass", shape="hexagon",
  tier=2, desc="""
    You've conquered the sky dimension. More to see:

    &aThe Twilight Forest&r: a magic forest with eight bosses.
    &5The End&r: the stronghold portal and the Ender Dragon.
    &bAd Astra&r: if the sky isn't high enough, go to space.""")
