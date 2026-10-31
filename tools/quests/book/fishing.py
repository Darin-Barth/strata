from dsl import *

C = chapter("fishing", "Fishing", group="life", icon="minecraft:fishing_rod",
            subtitle="Hundreds of fish, a fishing journal and a quiet afternoon by the water")
q = C.quest

q("intro", "Gone Fishing", icon="minecraft:fishing_rod", size=1.5, shape="gear", desc="""
    Fishing in Strata is a whole hobby! &eTide&r adds a &efishing journal&r with
    over a hundred fish to discover, and &eAquaculture&r adds more fish, hooks and tools.

    Different fish live in different places: rivers, oceans, caves, lava, even the End.
    Time of day, weather and the moon matter too.

    Grab a rod and find a quiet pond. It's a great way to relax!""",
  rewards=[give("minecraft:fishing_rod"), give("minecraft:cooked_cod", 8), give("tide:fishing_journal")])

# --- tide basics --------------------------------------------------------------------------
q("first_catch", "First Catch", deps="intro", icon="minecraft:cod",
  tasks=adv("minecraft:husbandry/fishy_business", title="Catch a fish"), desc="""
    Cast your rod into water and wait for a bite.

    When a fish bites, a little &eminigame&r appears: keep up with the fish to reel it in.
    Bigger, rarer fish fight harder. Don't worry if one gets away, there are plenty more!""",
  rewards=[give("tide:bait", 8)])

q("journal", "The Fishing Journal", deps="first_catch", icon="tide:fishing_journal",
  tasks=check("Open the Fishing Journal"), desc="""
    Open the &eFishing Journal&r you got for starting this chapter. Every new fish you catch
    gets its own page with a picture and a fun fact. (Lost it? Craft one from a book and any fish.)

    Can you fill it? Some fish only bite at night, in the rain, or in special places.""",
  rewards=[give("tide:duck_bobber"), give("minecraft:book", 2)])

q("bait", "Bait", deps="first_catch", icon="tide:bait",
  tasks=item("tide:bait", 4), desc="""
    Fish bite faster with &eBait&r. Craft it from a plant, rotten flesh, seeds and bone meal.

    Tide rods have &ebait slots&r: in your inventory, pick up the bait and
    right-click it onto your rod. Special baits add luck or a better chance of crates
    (the tooltip says what each one does).""",
  rewards=[give("minecraft:rotten_flesh", 8), give("minecraft:bone_meal", 8)])

q("angling_table", "The Angling Table", deps="journal", icon="tide:angling_table",
  tasks=item("tide:angling_table"), desc="""
    At the &eAngling Table&r you customise your rod with a &ebobber&r, a &ehook&r and a
    &eline&r. Lines make fish easier to catch, special hooks let you fish in new places,
    and bobbers just look cute. Try the duck!""",
  rewards=[give("tide:heart_bobber"), give("minecraft:string", 8)])

q("line", "A Stronger Line", deps="angling_table", icon="tide:iron_line",
  tasks=item("tide:iron_line"), desc="""
    An &eIron Line&r makes fish easier to catch. Diamond lines are even better,
    and golden lines add some luck. Put it on your rod at the Angling Table.""",
  rewards=[give("minecraft:iron_ingot", 8)])

q("better_rod", "A Better Rod", deps="angling_table", icon="tide:iron_fishing_rod", tier=2,
  tasks=item("tide:iron_fishing_rod"), desc="""
    Upgrade your rod at a &eSmithing Table&r: a fishing rod, an iron ingot and string
    make an &eIron Fishing Rod&r. Gold, diamond and netherite rods come after.

    Better rods reel in faster and handle tougher fish.""",
  rewards=[give("minecraft:gold_ingot", 4)])

q("crate", "That's No Fish!", deps="better_rod", icon="tide:wooden_crate",
  tasks=adv("tide:pull_crate", title="Reel in a crate"), desc="""
    Sometimes you'll hook a &ecrate&r instead of a fish. Open it for treasure:
    supplies, fishing gear and sometimes rare loot.""",
  rewards=[give("minecraft:experience_bottle", 8)])

q("display", "Show It Off", deps="journal", icon="tide:fish_display", optional=True,
  tasks=item("tide:fish_display"), desc="""
    Caught a whopper? Put it on a &eFish Display&r and hang it on your wall.""",
  rewards=[give("handcrafted:salmon_trophy")])

q("satchel", "Fish Satchel", deps="journal", icon="tide:fish_satchel", optional=True,
  tasks=item("tide:fish_satchel"), desc="""
    Right-click a &eFish Satchel&r to open it. While it's open,
    fish you catch go straight inside. Tidy!""",
  rewards=[give("tide:bait", 8)])

q("lava_fishing", "Fishing in Lava", deps="crate", icon="tide:lavaproof_hook", optional=True, tier=3,
  tasks=adv("tide:fish_in_lava", title="Fish in lava"), desc="""
    With a &eLavaproof Hook&r on your rod you can fish in &clava&r! The Nether has its own
    fiery fish. Bring fire resistance, and maybe a friend.""",
  rewards=[give("minecraft:magma_cream", 4), give("minecraft:blaze_powder", 4)])

q("half_journal", "Aquatic Archivist", deps="crate", icon="tide:fishing_journal", size=1.5, shape="heart",
  tier=4, tasks=adv("tide:journal_halfway_completed", title="Complete half the fishing journal"), desc="""
    Fill &ehalf&r of your fishing journal. That's a lot of fish!
    Check the journal for hints about where and when the missing ones bite.""",
  rewards=[give("tide:golden_bobber"), give("plushies:axolotl_plushie")])

# --- aquaculture --------------------------------------------------------------------------
q("aquaculture", "Aquaculture", deps="first_catch", icon="aquaculture:iron_fishing_rod",
  tasks=item("aquaculture:iron_fishing_rod"), desc="""
    &eAquaculture&r adds its own fish (catfish, tuna, piranhas, turtles and more)
    and its own fishing rods.

    Aquaculture rods take &ehooks&r, &ebait&r, a &eline&r and a &ebobber&r.
    Each hook does something: the gold hook adds luck, the light hook casts farther,
    the double hook can catch two things at once.""",
  rewards=[give("aquaculture:iron_hook"), give("aquaculture:fishing_line")])

q("worms", "Wiggly Worms", deps="aquaculture", icon="aquaculture:worm",
  tasks=item("aquaculture:worm", 8), desc="""
    &eWorms&r are Aquaculture's favorite bait. A &eWorm Farm&r (made with dirt) gives you
    a steady supply. Put bait on your Aquaculture rod to catch fish faster.""",
  rewards=[give("aquaculture:gold_hook")])

q("tackle_box", "Tackle Box", deps="aquaculture", icon="aquaculture:tackle_box", tier=2,
  tasks=item("aquaculture:tackle_box"), desc="""
    The &eTackle Box&r stores all your hooks, bait and bobbers, and it's where you put
    them on your Aquaculture rod. Place it by your favorite fishing spot.""",
  rewards=[give("aquaculture:light_hook"), give("aquaculture:bobber")])

q("fillet", "Fish Fillets", deps="aquaculture", icon="aquaculture:fish_fillet_cooked",
  tasks=item("aquaculture:wooden_fillet_knife"), desc="""
    Craft a fish together with a &eFillet Knife&r to cut it into &eFish Fillets&r.
    Cook them for a tasty, filling meal. Big fish give more fillets.""",
  rewards=[give("aquaculture:fish_fillet_cooked", 8)])

q("neptunium", "Neptune's Treasure", deps="tackle_box", icon="aquaculture:neptunium_ingot", tier=3,
  tasks=item("aquaculture:neptunium_ingot"), desc="""
    Very rarely you'll fish up &eNeptunium&r, or a &eNeptune's Bounty&r chest full of it.
    Neptunium gear is made for the sea: armor that lets you breathe and swim fast underwater,
    tools that work at full speed under water, and a rod that fish love.""",
  rewards=[give("aquaculture:neptunium_nugget", 4), give("minecraft:prismarine_shard", 8)])

# --- ocean life ---------------------------------------------------------------------------
q("upgrade_aquatic", "Life Under the Sea", deps="intro", icon="upgrade_aquatic:pike", desc="""
    &eUpgrade Aquatic&r makes the water more alive: pike, perch and lionfish to catch,
    glowing &ejellyfish&r, nautiluses, new coral and driftwood on the beaches.

    Jellyfish make pretty &eJelly Torches&r that work underwater.
    Beachgrass and driftwood are great for a seaside cottage!""",
  rewards=[give("upgrade_aquatic:driftwood", 16), give("upgrade_aquatic:beachgrass", 8)])

q("seafood", "Seafood Feast", deps=["upgrade_aquatic", "first_catch"], icon="oceansdelight:fugu_roll",
  tier=2, tasks=[item("oceansdelight:squid_rings"), item("farmersdelight:fish_stew")], desc="""
    Cook your catch! &eOcean's Delight&r adds seafood recipes for Farmer's Delight:
    squid rings, stuffed cod, guardian soup, fugu rolls and more.

    Cut squid on a cutting board for tentacles, then cook them up.
    Farmer's Delight's &eFish Stew&r is a cozy classic.""",
  rewards=[give("farmersdelight:cod_roll", 4), give("farmersdelight:salmon_roll", 4)])

q("where_next", "Where Next?", deps=["half_journal", "neptunium"], any_dep=True, icon="minecraft:oak_sign",
  shape="hexagon", desc="""
    You're a real angler now! Where next?

    &aFarming & Food&r: fish count toward your varied diet.
    &aPets & Critters&r: cats love fish, and otters live by rivers.
    &aExplorer's Guide&r: new dimensions mean new fish for the journal.""",
  rewards=[give("plushies:turtle_plushie"), give("tide:feather_bobber")])
