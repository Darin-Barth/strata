from dsl import *

C = chapter("create_extras", "Create: Extras", group="tech", icon="createbigcannons:cannon_mount",
            subtitle="Enchanting, cannons, kitchens and building blocks")
q = C.quest

q("intro", "More Create", deps="welcome/path_tech", icon="create:brass_casing", size=1.5,
  shape="gear", desc="""
    Create has a huge family of add-ons. This chapter is a sampler: pick whatever looks fun.

    &dEnchanting&r with liquid experience, &cBig Cannons&r, &aautomated cooking&r, and a
    pile of &6building blocks&r and tools for making your factories look great.""")

# --- Enchantment Industry -------------------------------------------------------------------
q("xp_hatch", "Liquid Experience", deps="intro", icon="create_enchantment_industry:experience_hatch",
  tasks=item("create_enchantment_industry:experience_hatch"), desc="""
    &eCreate: Enchantment Industry&r turns XP into a fluid: &eLiquid Experience&r.
    The &eExperience Hatch&r on a tank lets you pour your own levels in (and take them
    back out). Store it in tanks and pipe it like any fluid.

    Spilled liquid experience turns back into XP orbs.""",
  rewards=[give("minecraft:experience_bottle", 8)], tier=2)

q("grindstone", "Mechanical Grindstone", deps="xp_hatch",
  icon="create_enchantment_industry:mechanical_grindstone",
  tasks=item("create_enchantment_industry:mechanical_grindstone"), desc="""
    Right-click an &eItem Drain&r with a &eMechanical Grindstone&r to make a &eGrindstone
    Drain&r, then put another grindstone on top. It grinds XP nuggets and other
    experience items into Liquid Experience.

    Mob farms with crushing wheels or deployers drop &eNuggets of Experience&r for it.""",
  rewards=[give("create:experience_nugget", 16)], tier=2)

q("blaze_enchanter", "Blaze Enchanter", deps="xp_hatch",
  icon="create_enchantment_industry:blaze_enchanter",
  tasks=item("create_enchantment_industry:blaze_enchanter"), size=1.5, shape="hexagon", desc="""
    An automatic enchanting table. Feed it Liquid Experience, set the enchanting level on
    its panel and give it items: it enchants them.

    Put an item in its filter slot to pick which kind of enchantments you get, onto
    &eEnchanting Templates&r. Some enchantments only show up at lower levels.""",
  rewards=[give("minecraft:lapis_lazuli", 32), give("minecraft:book", 8)], tier=3)

q("blaze_forger", "Blaze Forger", deps="blaze_enchanter", icon="create_enchantment_industry:blaze_forger",
  tasks=item("create_enchantment_industry:blaze_forger"), desc="""
    An automatic anvil that runs on Liquid Experience, with &ano repair cost&r. It merges
    enchantments, applies templates to items, or pulls an enchantment off onto a blank
    template.""",
  rewards=[give("minecraft:iron_block", 2)], tier=2)

q("printer", "Printer", deps="xp_hatch", icon="create_enchantment_industry:printer",
  tasks=item("create_enchantment_industry:printer"), desc="""
    The &ePrinter&r copies things: written books, enchanted books, train schedules,
    clipboards, package addresses and names. Set the item in its filter, feed it the
    right fluid and blank items. Press &eU&r on the printer to see every recipe.""",
  rewards=[give("minecraft:book", 8)], optional=True)

# --- Big Cannons ----------------------------------------------------------------------------
q("cannons", "Create Big Cannons", deps="intro", icon="createbigcannons:cannon_mount",
  tasks=[item("createbigcannons:cannon_mount"), item("createbigcannons:log_cannon_chamber"),
         item("createbigcannons:log_cannon_end")], desc="""
    Build real artillery out of blocks. A cannon is a line of parts: a &eCannon End&r
    at the back, &eChambers&r for powder, then &eBarrels&r. Put it on a &eCannon Mount&r
    (with rotation to aim) and assemble it.

    Start with a wooden &eLog Cannon&r. Later cannons are cast from molten metal in
    moulds and bored out with a &eCannon Drill&r.

    Explosions are real, but &aclaimed land is protected&r: blocks in claims don't
    break.""",
  rewards=[give("minecraft:gunpowder", 16), give("minecraft:oak_log", 16)], tier=2)

q("ammo", "Load and Fire", deps="cannons", icon="createbigcannons:solid_shot",
  tasks=[item("createbigcannons:powder_charge", 4), item("createbigcannons:solid_shot", 4)], desc="""
    Load &ePowder Charges&r first, then a shot. A &eSolid Shot&r is a big iron ball;
    &eHE Shells&r explode (they need a &efuze&r). More powder means more range, but too
    much for the cannon's material can burst it!

    Give the mount a redstone signal to fire.""",
  rewards=[give("minecraft:gunpowder", 16), give("minecraft:iron_ingot", 8)], tier=2)

q("cast_iron", "Cast Iron Cannons", deps="ammo", icon="createbigcannons:cast_iron_cannon_barrel",
  tasks=[item("createbigcannons:cast_iron_cannon_barrel", 2),
         item("createbigcannons:cast_iron_sliding_breech")], desc="""
    &eCast Iron&r cannons are stronger and take bigger charges. A &eSliding Breech&r at the
    back lets you reload without taking the cannon apart.

    Later: bronze, steel and nethersteel, autocannons and quick-firing breeches. Mount one
    on an airship for sky battles!""",
  rewards=[give("minecraft:iron_block", 4)], tier=3)

# --- cooking --------------------------------------------------------------------------------
q("slicer", "Slice & Dice", deps="intro", icon="sliceanddice:slicer",
  tasks=item("sliceanddice:slicer"), desc="""
    &eCreate: Slice & Dice&r adds the &eSlicer&r: a powered cutting board. Right-click it
    with a knife (or another tool) and it cuts items below it automatically, using
    Farmer's Delight cutting recipes.

    It also adds the &eSprinkler&r: put it under a pipe to water crops (or splash mobs).""",
  rewards=[give("farmersdelight:iron_knife"), give("minecraft:potato", 16)], tier=2)

q("kitchen", "Central Kitchen", deps="slicer", icon="farmersdelight:cooking_pot", desc="""
    &eCreate: Central Kitchen&r teaches Create to cook Farmer's Delight food (and its
    add-ons):

    - Funnels fill and empty &eCooking Pots&r; Blaze Burners heat them faster.
    - Deployers with a knife, or Mechanical Saws, use the &eCutting Board&r.
    - Mechanical Arms put ingredients on boards and take food off.

    Ponder a cooking pot or cutting board with &eW&r to see the setups.""",
  rewards=[give("minecraft:beef", 8), give("minecraft:carrot", 16)])

# --- building and decoration ----------------------------------------------------------------
q("deco", "Create Deco", deps="intro", icon="createdeco:andesite_catwalk",
  tasks=[item("createdeco:andesite_catwalk", 8), item("createdeco:yellow_brass_lamp", 2)], desc="""
    &eCreate Deco&r adds industrial building blocks: catwalks, metal bars, sheet metal,
    train hulls, cage lamps, windows, doors and supports in every Create metal.

    Most are made in a stonecutter or from metal sheets.""",
  rewards=[give("create:andesite_alloy", 16), give("create:brass_ingot", 4)])

q("copycats", "Copycats+", deps="deco", icon="copycats:copycat_slope",
  tasks=item("copycats:copycat_slope", 4), desc="""
    &eCopycat&r blocks take the look of any block you right-click them with. &eCopycats+&r
    adds dozens of shapes: slopes, slices, layers, beams, stairs, doors and even
    copycat cogwheels and shafts.

    Great for ship hulls and curved roofs.""",
  rewards=[give("create:zinc_ingot", 8)])

q("interiors", "Interiors", deps="deco", icon="interiors:white_chair",
  tasks=item("interiors:white_chair", 2), desc="""
    &eCreate: Interiors&r adds &echairs&r, floor chairs and cushions. Sit on a chair on a
    moving contraption and you stay put: perfect for trains and airship cabins.""",
  rewards=[give("minecraft:white_wool", 8)])

q("chisel", "Mechanical Chisel", deps="deco", icon="rechiseledcreate:mechanical_chisel",
  tasks=item("rechiseledcreate:mechanical_chisel"), desc="""
    &eRechiseled: Create&r adds Create-themed &eRechiseled&r block variants and the
    &eMechanical Chisel&r, a Create-powered chisel for turning blocks into their
    variants in bulk (Ponder it with &eW&r).""",
  rewards=[give("minecraft:stone_bricks", 32)], optional=True)

q("trowel", "Mech Trowel", deps="deco", icon="mechtrowel:mech_trowel",
  tasks=item("mechtrowel:mech_trowel"), desc="""
    The &eMech Trowel&r places blocks picked from a palette you set up, so walls and
    floors get a natural mixed look. Upgrade it in a smithing table with templates:
    a wand mode, longer reach, or taking blocks from your AE2 storage.""",
  rewards=[give("minecraft:cobblestone", 64)], optional=True)

# --- mechanics ------------------------------------------------------------------------------
q("transmission", "Transmission Chains", deps="intro", icon="createtransmission:transmission_chain",
  tasks=item("createtransmission:transmission_chain", 4), desc="""
    &eCreate: Transmission&r adds &eTransmission Chains&r: chain drives that pass rotation
    between belts. They can be encased like other Create parts. Ponder them with &eW&r.""",
  rewards=[give("minecraft:chain", 8)], optional=True)

q("dragons_plus", "Dragons Plus", deps="intro", icon="create_dragons_plus:fluid_hatch",
  tasks=item("create_dragons_plus:fluid_hatch"), desc="""
    &eCreate: Dragons Plus&r adds new fan processing: air through &epowder snow&r
    &bfreezes&r, through &eliquid dye&r it &ecolors&r items, through &esand-like
    catalysts&r it &esands&r them, and through &5Dragon's Breath&r it does "ending".

    The &eFluid Hatch&r makes a tank easy to fill and empty with buckets.""",
  rewards=[give("minecraft:powder_snow_bucket")])

# --- where next -----------------------------------------------------------------------------
q("next", "Where Next?", deps=["cannons", "blaze_enchanter"], icon="minecraft:oak_sign",
  shape="square", desc="""
    &bCreate: Airships&r: put a cannon on a ship.
    &bFarming & Food&r: more recipes for your automatic kitchen.
    &bBuilding & Decorating&r: more blocks for your bases.""")
