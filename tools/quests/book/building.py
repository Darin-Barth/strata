from dsl import *

C = chapter("building", "Building & Decorating", group="life", icon="mcwfurnitures:oak_chair",
            subtitle="Thousands of blocks, comfy furniture and tools that build for you")
q = C.quest

q("intro", "What Can I Build?", icon="handcrafted:oak_couch", size=1.5, shape="gear", desc="""
    Pretty much anything! Strata has thousands of extra blocks: furniture, roofs, windows,
    lamps, paths, bridges and fancy stone and wood patterns.

    Tip: search the item list by mod. &e@mcw&r shows Macaw's blocks,
    &e@handcrafted&r furniture, &e@supplementaries&r all the little decorations.

    These quests show you the best tools. Then build your dream house!""",
  rewards=[give("minecraft:oak_log", 32), give("minecraft:cobblestone", 64)])

q("colony", "Found a Colony", deps="intro", icon="minecolonies:blockhuttownhall", optional=True,
  tasks=item("minecolonies:supplycampdeployer"), desc="""
    &eMineColonies&r lets you build a whole town of NPC workers: builders, farmers, miners,
    guards and dozens more. Craft a &eSupply Camp&r (press &eR&r on it), place it, and it gives you
    a &eTown Hall&r to start your colony. Your builder then builds every other hut for you.

    &cWarning:&r once your colony is founded, raiders attack it every couple of weeks
    (in-game nights). Build guard towers before then.""")

# --- new looks for old blocks -----------------------------------------------------------
q("chipped", "One Block, Many Looks", deps="intro", icon="chipped:carpenters_table",
  tasks=item("chipped:carpenters_table"), desc="""
    &eChipped&r workbenches turn a plain block into dozens of new versions.
    Put planks in the &eCarpenter's Table&r and pick the look you like.

    Other benches handle other blocks: the &eMason Table&r (stone), &eGlassblower&r (glass),
    &eLoom Table&r (wool and carpet), &eBotanist's Workbench&r (plants) and more.""",
  rewards=[give("minecraft:oak_planks", 64)])

q("mason", "Stonework", deps="chipped", icon="chipped:mason_table", optional=True,
  tasks=item("chipped:mason_table"), desc="""
    The &eMason Table&r gives stone, bricks and more a whole new set of looks.""",
  rewards=[give("minecraft:stone_bricks", 64)])

q("chisel", "Rechiseled", deps="chipped", icon="rechiseled:chisel",
  tasks=item("rechiseled:chisel"), desc="""
    The &eChisel&r turns blocks into patterns: tiles, bricks, beams, mosaics and more.
    Right-click with it to open it, put your blocks in, then choose a pattern.

    Many patterns &aconnect&r to each other when placed side by side.""",
  rewards=[give("minecraft:stone", 64)])

q("framed", "Framed Blocks", deps="chisel", icon="framedblocks:framed_cube", optional=True,
  tasks=item("framedblocks:framed_cube", 4), desc="""
    A &eFramed Block&r copies the look of any block you right-click it with.
    Want stairs, slabs or doors that look like diamond blocks, glass or leaves? Easy!

    There are framed versions of almost every shape. The &eFramed Hammer&r takes the
    block back out.""",
  rewards=[give("framedblocks:framed_stairs", 8), give("framedblocks:framed_slab", 8)])

# --- furniture ----------------------------------------------------------------------------
q("handcrafted", "Handcrafted Furniture", deps="intro", icon="handcrafted:hammer",
  tasks=item("handcrafted:hammer"), desc="""
    &eHandcrafted&r adds chairs, tables, couches, beds, shelves, cupboards, plates, cups and
    mob trophies, in every kind of wood. You can &esit&r on the chairs and couches.

    The &eHammer&r changes a furniture block's look or shape: right-click (or sneak +
    right-click) to cycle through the options.""",
  rewards=[give("handcrafted:oak_chair", 2), give("handcrafted:oak_table")])

q("cushions", "Comfy Cushions", deps="handcrafted", icon="handcrafted:pink_cushion", optional=True,
  tasks=item("handcrafted:oak_couch"), desc="""
    Make a &eCouch&r for your living room. Add a cushion or a sheet to change its colour.""",
  rewards=[give("handcrafted:pink_cushion", 2), give("handcrafted:light_blue_cushion", 2)])

q("macaw", "Macaw's Furniture", deps="handcrafted", icon="mcwfurnitures:oak_desk",
  tasks=item("mcwfurnitures:oak_wardrobe"), desc="""
    &eMacaw's&r is a whole family of mods. &eFurniture&r has desks, drawers, wardrobes,
    kitchen cabinets and bookshelves. Many open up and store items!

    Make a &eWardrobe&r for your clothes. Fancy!""",
  rewards=[give("mcwfurnitures:oak_chair", 2), give("mcwfurnitures:oak_table")])

q("roofs", "A Roof Over Your Head", deps="macaw", icon="mcwroofs:oak_roof",
  tasks=item("mcwroofs:oak_roof", 16), desc="""
    &eMacaw's Roofs&r has proper sloped roof pieces: plain, attic, steep, lower and more.
    No more stair-block roofs (unless you like them)!""",
  rewards=[give("minecraft:oak_planks", 32)])

q("windows_doors", "Windows and Doors", deps="roofs", icon="mcwwindows:oak_window",
  tasks=[item("mcwwindows:oak_window", 4), item("mcwdoors:oak_cottage_door")], desc="""
    &eMacaw's Windows&r: windows that open, shutters, curtains and blinds.
    Big windows connect into one when placed together.
    &eMacaw's Doors&r: cottage doors, barn doors, Japanese doors, stable doors.

    There are Macaw's &etrapdoors, fences, stairs, bridges, paths, lights&r and
    &epaintings&r too. Search &e@mcw&r!""",
  rewards=[give("mcwfences:oak_picket_fence", 8), give("mcwtrpdoors:oak_cottage_trapdoor", 4)])

q("lights", "Let There Be Lamps", deps="windows_doors", icon="mcwlights:chain_lantern", optional=True,
  tasks=item("mcwlights:chain_lantern", 2), desc="""
    &eMacaw's Lights & Lamps&r: hanging lanterns, paper lamps, street lamps,
    tiki torches and lava lamps. A cozy house needs warm lights!""",
  rewards=[give("mcwlights:pink_paper_lamp", 2), give("mcwlights:oak_tiki_torch", 4)])

q("paths", "Garden Paths", deps="windows_doors", icon="mcwpaths:cobblestone_square_paving", optional=True,
  tasks=item("mcwpaths:cobblestone_square_paving", 16), desc="""
    &eMacaw's Paths & Pavings&r turns stone into pretty garden paths.
    &eMacaw's Bridges&r has rope bridges and stone bridges for crossing rivers.""",
  rewards=[give("mcwbridges:rope_oak_bridge", 8)])

q("another_furniture", "Another Furniture", deps="handcrafted", icon="another_furniture:red_sofa",
  tasks=item("another_furniture:oak_shelf"), desc="""
    &eAnother Furniture&r has sofas, curtains, shutters, stools, benches, shelves,
    planter boxes and a &eService Bell&r for your shop counter. Ding!

    Shelves hold items on display: right-click to place things on them.""",
  rewards=[give("another_furniture:service_bell"), give("another_furniture:pink_curtain", 2)])

q("every_wood", "Every Wood, Every Style", deps="another_furniture", icon="minecraft:cherry_planks", desc="""
    Found a pretty new wood in another biome or dimension? Good news: &eEvery Compat&r
    makes Macaw's roofs, doors, windows, fences and bridges in &aevery wood type&r from every mod.
    Search for the wood's name to see them all. Furniture (Macaw's Furniture, Handcrafted,
    Another Furniture) and Chipped or Rechiseled patterns come in the vanilla woods.""",
  rewards=[give("minecraft:cherry_log", 16), give("minecraft:birch_log", 16)])

# --- little details -----------------------------------------------------------------------
q("supplementaries", "Little Things", deps="intro", icon="supplementaries:jar",
  tasks=item("supplementaries:jar"), desc="""
    &eSupplementaries&r is full of charming details: &ejars&r (for cookies, fireflies or fish),
    sacks, globes, flags, wind vanes, notice boards, signposts, clocks, pedestals,
    hourglasses and a &eblackboard&r you can draw on.

    Put a cookie or a fish in a jar and place it on a shelf. Adorable.""",
  rewards=[give("supplementaries:flower_box", 2), give("supplementaries:doormat")])

q("amendments", "Little Tweaks", deps="supplementaries", icon="minecraft:flower_pot", desc="""
    &eAmendments&r makes vanilla blocks nicer: lanterns can hang on &ewalls&r,
    flower pots can &ehang&r from the ceiling, carpets come as stairs and slabs,
    banners can hang from ceilings, and you can dye things in a cauldron.""",
  rewards=[give("minecraft:lantern", 4), give("minecraft:flower_pot", 4)])

q("frame", "Pictures from the Internet", deps="supplementaries", icon="waterframes:frame", optional=True,
  tasks=item("waterframes:frame"), desc="""
    A &eWaterFrames Frame&r shows a picture or video from a web link. Put a photo of your
    group on the wall, or a TV in your living room! Some websites may not be allowed.""",
  rewards=[give("minecraft:item_frame", 4)])

q("comforts", "Sleep Anywhere", deps="supplementaries", icon="comforts:sleeping_bag_red",
  tasks=item("comforts:sleeping_bag_red"), desc="""
    A &eSleeping Bag&r is a bed you can carry. Use it while crouching to put it down,
    then rest through the night on your adventures.

    &eHammocks&r are for naps during the &eday&r. Hang one between two
    &eRope and Nail&r blocks.""",
  rewards=[give("comforts:rope_and_nail", 2), give("comforts:hammock_blue")])

# --- building tools -----------------------------------------------------------------------
q("wand", "A Building Wand", deps="intro", icon="wands:stone_wand",
  tasks=item("wands:stone_wand"), desc="""
    A &eBuilding Wand&r places a whole row or wall of blocks at once, copying the blocks
    you're looking at. Great for floors and walls.

    Better wands (iron, diamond, netherite) place more at a time and have more modes.""",
  rewards=[give("minecraft:cobblestone", 64), give("minecraft:oak_planks", 64)])

q("effortless", "Effortless Building", deps="wand", icon="effortlessbuilding:randomizer_tool", desc="""
    &eEffortless Building&r lets you build &elines, walls, floors, circles, spheres&r
    and more with a few clicks, using blocks from your inventory. It also has undo and redo!

    Open its build-mode menu with its key (set it in &eOptions > Controls&r).
    The &eRandomizer Tool&r places random blocks from a mix, great for natural-looking walls.""",
  rewards=[give("minecraft:stone_bricks", 64)])

q("gadgets", "Building Gadgets", deps="effortless", icon="buildinggadgets2:gadget_building", tier=3,
  tasks=item("buildinggadgets2:gadget_building"), desc="""
    The &eBuilding Gadget&r places big shapes of blocks from a distance, and later gadgets
    can copy and paste whole buildings or swap one block for another.

    Gadgets run on &cpower&r (FE): charge them in a charger from the tech chapters.""",
  rewards=[give("minecraft:redstone", 32)])

q("megatorch", "No More Monsters at Home", deps="supplementaries", icon="torchmaster:megatorch", tier=3,
  tasks=item("torchmaster:megatorch"), desc="""
    Tired of creepers in your garden? The &eMega Torch&r stops hostile monsters from
    naturally spawning in a huge area: &e64 blocks in every direction&r around it.

    It doesn't stop mob spawners or monsters walking in from outside. The &eDread Lamp&r does
    the same for passive animals like bats and squid.""",
  rewards=[give("minecraft:torch", 64)])

# --- milestone ---------------------------------------------------------------------------
q("house", "Decorate a House", deps=["roofs", "another_furniture", "amendments", "comforts"],
  icon="minecraft:oak_door", size=1.5, shape="heart", tier=3,
  tasks=check("Build and decorate a house you love"), desc="""
    Time to put it all together! Build a house and make it feel like home:

    a roof and windows, comfy chairs and a table, lamps, a bed (or a pet bed!),
    a kitchen, plants in pots, and maybe a plushie or two.

    Show it off to your friends, then click the checkmark. There's no wrong way to do it.""",
  rewards=[give("plushies:cat_plushie"), give("plushies:wolf_plushie"), give("minecraft:flower_pot", 8),
           give("minecraft:painting", 4)])

q("where_next", "Where Next?", deps="house", icon="minecraft:oak_sign", shape="hexagon", desc="""
    Your house looks great! Next:

    &aStorage&r: chests, drawers and a storage system to keep it tidy.
    &aFarming & Food&r: a kitchen and a garden to go with it.
    &aPets & Critters&r: someone to share it with.
    &bCreate&r chapters: Create Deco adds industrial blocks (and a Create house is fun too).""",
  rewards=[give("minecraft:cake")])
