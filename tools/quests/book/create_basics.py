from dsl import *

C = chapter("create_basics", "Create: Getting Moving", group="tech", icon="create:cogwheel",
            subtitle="Rotation, belts, presses and your first machines")
q = C.quest

q("intro", "What is Create?", deps="welcome/path_tech", icon="create:cogwheel", size=1.5,
  shape="gear", desc="""
    &eCreate&r machines run on &brotation&r: spinning shafts and cogs, like a real workshop.
    A water wheel or windmill spins a shaft, the shaft runs a press, a belt carries the
    results away. No magic boxes: you can see every part move.

    Everything in Strata's tech path starts here: trains, airships, power and big factories.
    Take it one machine at a time. This chapter walks you through the basics.""",
  rewards=[give("create:andesite_alloy", 16), give("minecraft:iron_ingot", 8)])

q("ponder", "Ponder Everything", deps="intro", icon="minecraft:spyglass", desc="""
    Create has a built-in picture book called &ePonder&r.

    Hover over almost any Create item (in your inventory or the item list) and
    &ehold W&r. A little animated scene shows how the block works, step by step.
    Use it whenever a quest says "place this next to that".

    Press &eR&r on an item for its recipe and &eU&r for its uses, as always.""",
  rewards=[give("minecraft:bread", 8)])

q("wrench", "Grab a Wrench", deps="intro", icon="create:wrench",
  tasks=item("create:wrench"), desc="""
    The &eWrench&r is your best friend:
    - &eRight-click&r a Create block to rotate it.
    - &eSneak + right-click&r to pick it up instantly (no breaking, no lost items).

    Most mistakes are fixed with one click of the wrench.""",
  rewards=[give("create:andesite_alloy", 8)])

# --- rotation -------------------------------------------------------------------------------
q("alloy", "Andesite Alloy", deps="intro", icon="create:andesite_alloy",
  tasks=item("create:andesite_alloy", 32), desc="""
    &eAndesite Alloy&r is the backbone of early Create. Almost every early machine uses it.
    Mix andesite with iron (or zinc) nuggets: look it up with &eR&r.

    Tip: a &eMechanical Mixer&r makes it in bulk later.""",
  rewards=[give("minecraft:iron_nugget", 32), give("minecraft:andesite", 32)])

q("shafts", "Shafts and Cogs", deps="alloy", icon="create:shaft",
  tasks=[item("create:shaft", 8), item("create:cogwheel", 4), item("create:large_cogwheel", 2)],
  desc="""
    &eShafts&r carry rotation in a straight line. &eCogwheels&r pass it sideways to the
    next cog.

    A &eLarge Cogwheel&r next to a small one changes the speed: big to small spins
    &afaster&r, small to big spins &cslower&r. Speed is measured in &bRPM&r.""",
  rewards=[give("create:andesite_alloy", 16), give("minecraft:oak_planks", 32)])

q("water_wheel", "Water Power", deps="shafts", icon="create:water_wheel",
  tasks=item("create:water_wheel"), desc="""
    Your first real power source. Place a &eWater Wheel&r where flowing water hits its
    blades (Ponder it with &eW&r) and it spins forever, for free.

    Several wheels on one shaft add their strength together.
    The &eLarge Water Wheel&r is slower but much stronger.""",
  rewards=[give("minecraft:water_bucket"), give("create:shaft", 8)], tier=2)

q("windmill", "Windmills", deps="shafts", icon="create:windmill_bearing",
  tasks=[item("create:windmill_bearing"), item("create:white_sail", 8)], desc="""
    Not near water? Build a &eWindmill&r.

    Place a &eWindmill Bearing&r, build a cross of &eSails&r on the block in front of it,
    then right-click the bearing to start it. More sails make more power.
    Sails can be dyed for fun.""",
  rewards=[give("minecraft:white_wool", 16), give("minecraft:stick", 32)], tier=2)

q("stress", "Stress and Goggles", deps=["water_wheel", "windmill"], any_dep=True,
  icon="create:goggles", tasks=item("create:goggles"), desc="""
    Every power source gives a fixed amount of &bStress Units (SU)&r. Every machine uses
    some. If your machines need more SU than you make, the whole network stops
    (it's "overstressed").

    Wear &eEngineer's Goggles&r and look at a block: they show how much SU a source makes,
    how much a machine uses, and what's left. Faster spinning machines cost more SU.""",
  rewards=[give("create:speedometer"), give("create:andesite_alloy", 16)], tier=2)

# --- first machines -------------------------------------------------------------------------
q("casing", "Andesite Casing", deps="alloy", icon="create:andesite_casing",
  tasks=item("create:andesite_casing", 8), desc="""
    Right-click a stripped log or stripped wood with &eAndesite Alloy&r to make
    &eAndesite Casing&r. Casings are the bodies of most machines.

    You can also encase shafts and cogs in casing to tidy up your builds.""",
  rewards=[give("minecraft:stripped_oak_log", 16), give("create:andesite_alloy", 8)])

q("press", "Mechanical Press", deps="casing", icon="create:mechanical_press",
  tasks=[item("create:mechanical_press"), item("create:iron_sheet", 8)], desc="""
    The &eMechanical Press&r stamps things flat. Put a &eDepot&r (or a belt) under it,
    drop iron ingots on, and out come &eIron Sheets&r.

    Sheets of iron, copper, gold and brass are used everywhere.""",
  rewards=[give("minecraft:iron_ingot", 16), give("minecraft:copper_ingot", 16)], tier=2)

q("mixer", "Mixer and Basin", deps="press", icon="create:mechanical_mixer",
  tasks=[item("create:mechanical_mixer"), item("create:basin")], desc="""
    A &eMechanical Mixer&r over a &eBasin&r mixes items and fluids, like a giant
    crafting bowl. A Press over a Basin &ecompacts&r things instead.

    Throw ingredients into the basin and let it spin. Recipes that need heat want a
    burner under the basin (more on that with brass).""",
  rewards=[give("minecraft:andesite", 32), give("minecraft:iron_nugget", 32)], tier=2)

q("fan", "Wash, Smelt, Haunt", deps="casing", icon="create:encased_fan",
  tasks=item("create:encased_fan"), desc="""
    An &eEncased Fan&r blows air. Air passing through a block processes items on the
    ground or on a belt in front of it:

    &bWater&r: &eBulk Washing&r (sand, gravel, crushed ores).
    &6Lava or fire&r: &eBulk Smelting&r (like a furnace with no fuel).
    &dSoul fire&r: &eBulk Haunting&r (spooky transformations).
    &7Campfire&r: &eBulk Smoking&r (cooks food).

    Press &eU&r on an item to see what each fan type does with it.""",
  rewards=[give("minecraft:lava_bucket"), give("minecraft:soul_sand", 4)], tier=2)

q("crushing", "Crushing Ores", deps=["casing", "stress"], icon="create:crushing_wheel",
  tasks=[item("create:millstone"), item("create:crushing_wheel", 2)], desc="""
    A &eMillstone&r grinds things slowly. Two &eCrushing Wheels&r side by side, spinning
    toward each other, crush fast.

    Crushed ores give extra nuggets when washed and smelted: much more metal per ore.
    Crushing wheels are hungry for stress, so check your goggles.""",
  rewards=[give("minecraft:raw_iron", 16), give("minecraft:raw_copper", 16)], tier=3)

# --- moving items ---------------------------------------------------------------------------
q("belts", "Belts and Depots", deps="shafts", icon="create:belt_connector",
  tasks=[item("create:belt_connector", 8), item("create:depot", 2),
         item("create:andesite_funnel", 4)], desc="""
    &eMechanical Belts&r connect two shafts and carry items along. Right-click one shaft,
    then the other, with the belt in hand.

    A &eDepot&r holds one stack for a machine to work on.
    &eFunnels&r put items onto belts and pull them off into chests.""",
  rewards=[give("minecraft:dried_kelp", 32), give("create:shaft", 8)], tier=2)

# --- contraptions ---------------------------------------------------------------------------
q("contraptions", "Moving Machines", deps="casing", icon="create:mechanical_piston",
  tasks=[item("create:mechanical_piston"), item("create:super_glue")], desc="""
    Create can move whole groups of blocks: these are &eContraptions&r.
    A &eMechanical Piston&r, &eBearing&r or &eCart Assembler&r moves everything stuck
    to it. Use &eSuper Glue&r (drag a box) to stick blocks together.

    Contraptions are how you build drills, farms, elevators, trains and airships.""",
  rewards=[give("minecraft:slime_ball", 8), give("create:andesite_alloy", 16)], tier=2)

q("drill", "Drills and Saws", deps="contraptions", icon="create:mechanical_drill",
  tasks=[item("create:mechanical_drill"), item("create:mechanical_saw")], desc="""
    A &eMechanical Drill&r breaks the block in front of it. On a moving piston or bearing,
    it digs tunnels or quarries. Glue a chest to the contraption and it collects the loot.

    A &eMechanical Saw&r fells trees in front of it, or (facing up, under a belt) cuts
    logs into planks and stone into stonecutter shapes. Great for a tree farm.""",
  rewards=[give("minecraft:iron_ingot", 8), give("minecraft:oak_sapling", 16)])

q("harvester", "Farming Machines", deps="contraptions", icon="create:mechanical_harvester",
  tasks=[item("create:mechanical_harvester", 2), item("create:mechanical_plough")], desc="""
    &eMechanical Harvesters&r on a moving contraption cut ripe crops and leave the
    plant to regrow. A &eMechanical Plough&r tills soil as it passes.

    Put them on a piston or a cart that sweeps over your fields.""",
  rewards=[give("minecraft:wheat_seeds", 32), give("minecraft:carrot", 16)])

# --- brass ----------------------------------------------------------------------------------
q("zinc", "Zinc", deps="alloy", icon="create:raw_zinc",
  tasks=item("create:raw_zinc", 16), desc="""
    &eZinc&r is Create's own ore. Look for it underground (EMI Ores shows the
    best heights: press &eR&r on zinc ore).

    Smelt it into ingots. Crushing it first gives more.""",
  rewards=[give("minecraft:raw_copper", 16), give("minecraft:coal", 16)])

q("blaze_burner", "Catch a Blaze", deps=["zinc", "welcome/nether"], icon="create:blaze_burner",
  tasks=item("create:blaze_burner"), desc="""
    Some recipes need heat. Make an &eEmpty Blaze Burner&r, take it to the Nether and
    right-click a &cBlaze&r with it to catch it.

    Put the &eBlaze Burner&r under a basin and feed it fuel (coal, logs, etc.).
    A &eBlaze Cake&r makes it &csuperheated&r for the hottest recipes.""",
  rewards=[give("minecraft:coal_block", 4), give("minecraft:blaze_rod", 4)], tier=3)

q("brass", "Brass", deps=["blaze_burner", "mixer"], icon="create:brass_ingot",
  tasks=item("create:brass_ingot", 16), desc="""
    Mix &ecopper&r and &ezinc&r in a heated basin (Mixer over Basin over Blaze Burner)
    to get &6Brass&r.

    Brass opens Create's smart parts: filters, arms, deployers, trains and airship parts.""",
  rewards=[give("minecraft:copper_ingot", 16), give("create:zinc_ingot", 16)], tier=3)

q("brass_casing", "Brass Casing and Tubes", deps="brass", icon="create:brass_casing",
  tasks=[item("create:brass_casing", 8), item("create:electron_tube", 4)], desc="""
    Right-click stripped logs with a &eBrass Ingot&r to make &eBrass Casing&r,
    just like andesite casing.

    &eElectron Tubes&r: polish &eRose Quartz&r (quartz + redstone) with &eSand Paper&r,
    then craft it with an iron sheet. Tubes go into smart blocks like brass funnels,
    tunnels and display links.""",
  rewards=[give("minecraft:stripped_oak_log", 16), give("create:brass_ingot", 8)])

q("precision", "Precision Mechanism", deps="brass_casing",
  icon="create:precision_mechanism", tasks=item("create:precision_mechanism", 2),
  size=1.5, shape="hexagon", desc="""
    Your first &eSequenced Assembly&r: an item built step by step on a belt.
    A golden sheet goes past &eDeployers&r (adding cogwheels and nuggets) and a
    &ePress&r, around and around several times. Sometimes it fails and gives scrap.

    Ponder it with &eW&r and check the steps with &eR&r. Many airship and train parts
    need these.""",
  rewards=[give("create:golden_sheet", 8), give("create:cogwheel", 16)], tier=4)

q("deployer", "Deployers", deps="brass_casing", icon="create:deployer",
  tasks=item("create:deployer", 2), desc="""
    A &eDeployer&r is a robot hand: it uses, places or applies whatever it holds,
    like a player clicking.

    Deployers are key for sequenced assembly, auto-casing, farms and even fights.""",
  rewards=[give("create:brass_hand"), give("create:andesite_alloy", 16)])

q("logistics", "Smart Logistics", deps="brass_casing", icon="create:brass_funnel",
  tasks=[item("create:brass_funnel", 2), item("create:brass_tunnel", 2), item("create:filter")],
  desc="""
    &eBrass Funnels&r and &eBrass Tunnels&r can be filtered: put an item (or a
    &eList Filter&r) in their slot and only that item passes.

    Tunnels on a belt split items evenly between several belts or machines.""",
  rewards=[give("create:brass_ingot", 8), give("minecraft:paper", 16)], tier=2)

q("arm", "Mechanical Arm", deps="precision", icon="create:mechanical_arm",
  tasks=item("create:mechanical_arm"), desc="""
    The &eMechanical Arm&r picks items up and puts them down anywhere in its reach.
    Hold the arm and right-click the blocks it should take from and deliver to,
    then place it.

    It feeds machines from chests, depots and belts with no belts at all.""",
  rewards=[give("create:brass_ingot", 8)], tier=2)

q("crafter", "Mechanical Crafters", deps="precision", icon="create:mechanical_crafter",
  tasks=item("create:mechanical_crafter", 9), desc="""
    Some big recipes (up to 9x9!) only work in &eMechanical Crafters&r. Place them in a
    grid, point their arrows toward one output corner (wrench), fill the slots and
    give them a redstone pulse.

    Jetpacks, drilling machines and some airship parts need them.""",
  rewards=[give("create:electron_tube", 4), give("create:brass_ingot", 8)], tier=3,
  optional=True)

# --- fluids ---------------------------------------------------------------------------------
q("fluids", "Pipes and Pumps", deps="casing", icon="create:mechanical_pump",
  tasks=[item("create:fluid_pipe", 16), item("create:mechanical_pump"), item("create:fluid_tank", 2)],
  desc="""
    &eFluid Pipes&r carry water, lava and other fluids. A &eMechanical Pump&r on the pipe
    (powered by rotation) pushes the fluid along. &eFluid Tanks&r stack into big tanks.

    Fluids feed mixers, steam engines and fuel lines. A &eSpout&r pours fluid into items
    under it (filling buckets and bottles); an &eItem Drain&r empties them again.""",
  rewards=[give("minecraft:copper_ingot", 16), give("minecraft:bucket", 2)], tier=2)

# --- Create Ore Excavation ------------------------------------------------------------------
q("vein_finder", "Hidden Ore Veins", deps="precision", icon="createoreexcavation:vein_finder",
  tasks=item("createoreexcavation:vein_finder"), desc="""
    &eCreate Ore Excavation&r adds huge ore veins deep under some chunks. You can't see them;
    you drill them with a machine.

    Right-click with the &eOre Vein Finder&r to learn which vein is in your chunk or
    nearby. A &eSample Drill&r (with a copper backtank on top) records a vein's details in
    an &eOre Vein Atlas&r.""",
  rewards=[give("minecraft:ender_pearl", 2), give("minecraft:amethyst_shard", 4)], tier=2)

q("drilling", "Drilling Machine", deps="vein_finder", icon="createoreexcavation:drilling_machine",
  tasks=[item("createoreexcavation:drilling_machine"), item("createoreexcavation:drill")],
  size=1.5, shape="hexagon", desc="""
    The &eDrilling Machine&r sits on top of a vein and mines it with rotation, forever or
    until the vein runs out. Put a &eDrill&r head in it and give it lots of stress.

    Some veins need drilling fluid, and the richest need a better drill head.
    The &eFluid Well Extractor&r works the same way for fluid veins.""",
  rewards=[give("create:brass_ingot", 16), give("minecraft:iron_block", 4)], tier=4)

# --- where next -----------------------------------------------------------------------------
q("next", "Where Next?", deps=["precision", "stress"], icon="minecraft:oak_sign", shape="square",
  desc="""
    You know the basics of Create. Pick what's next:

    &bCreate: Power & Wires&r: steam engines, electricity and the power ladder.
    &bCreate: Trains & Trade&r: railways, stations and shops.
    &bCreate: Airships&r: build a ship and fly it!
    &bCreate: Extras&r: enchanting, cannons, kitchens and decoration.""")
