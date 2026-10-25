from dsl import *

C = chapter("create_power", "Create: Power & Wires", group="tech",
            icon="createaddition:alternator",
            subtitle="Steam, electricity and the Strata power ladder")
q = C.quest

q("intro", "Two Kinds of Power", deps="welcome/path_tech", icon="create:steam_engine", size=1.5,
  shape="gear", desc="""
    Create runs on &brotation&r (stress, SU). Most other tech mods (Mekanism, AE2, IE) run on
    &eelectricity&r (FE). This chapter shows how to make both, and how to turn one into
    the other.

    Strata has a &6power ladder&r. Each step is better than the last:
    1. Rotation into a &eCrafts & Additions Alternator&r (easy, but weak).
    2. &eCreate: New Age&r generators with coils and magnets (much better).
    3. &eNew Age nuclear&r heat into steam engines (huge), next to Mekanism fission and fusion.""")

# --- steam ----------------------------------------------------------------------------------
q("steam", "Steam Engines", deps=["intro", "welcome/nether"], icon="create:steam_engine",
  tasks=[item("create:steam_engine", 2), item("create:fluid_tank", 4)], desc="""
    The strongest early rotation in Create. Build a &eboiler&r: Fluid Tanks with a
    &eBlaze Burner&r under them, pump in water, and put &eSteam Engines&r on the tank's
    sides with a shaft in front.

    Bigger boilers with more heat run more engines. Look at the tank with Engineer's
    Goggles: it tells you what's missing (heat, water or size). Ponder it with &eW&r.
    A &eBlaze Cake&r makes a burner &csuperheated&r for even more steam.""",
  rewards=[give("minecraft:coal_block", 8), give("create:fluid_pipe", 16)], tier=3)

# --- Crafts & Additions ---------------------------------------------------------------------
q("alternator", "The Alternator", deps="intro", icon="createaddition:alternator",
  tasks=item("createaddition:alternator"), desc="""
    &eCrafts & Additions&r turns rotation into electricity. The &eAlternator&r needs at
    least &e32 RPM&r; faster spinning gives more FE.

    In Strata the alternator is kept &cweak on purpose&r: it's your starter generator,
    not your power plant. It's still great for charging tools and running a few machines.""",
  rewards=[give("minecraft:copper_ingot", 16), give("minecraft:redstone", 16)], tier=2)

q("motor", "Electric Motor", deps="alternator", icon="createaddition:electric_motor",
  tasks=item("createaddition:electric_motor"), desc="""
    The other direction: the &eElectric Motor&r eats FE and spins a shaft. Scroll on its
    back panel to set the RPM; higher RPM uses more power.

    Handy where water wheels can't go, like deep underground.""",
  rewards=[give("create:shaft", 8)])

q("rolling_mill", "Rolling Mill", deps="alternator", icon="createaddition:rolling_mill",
  tasks=[item("createaddition:rolling_mill"), item("createaddition:copper_wire", 8)], desc="""
    The &eRolling Mill&r presses ingots and plates into &erods&r and &ewires&r with
    rotation. Drop ingots on top, or feed it from a belt with funnels.

    Wires go onto &eSpools&r, and spools make the power lines in the next quest.""",
  rewards=[give("minecraft:copper_ingot", 16)])

q("connectors", "Local Wiring", deps="rolling_mill", icon="createaddition:connector",
  tasks=[item("createaddition:connector", 4), item("createaddition:copper_spool")], desc="""
    &eConnectors&r go on generators and machines. Right-click two connectors with a
    &eCopper Spool&r to string a wire between them.

    Wrench a connector to set its mode: &ePull&r on a generator, &ePush&r on a machine.
    These wires are for &elocal&r use, inside and around your base.
    (Large Connectors reach farther.)""",
  rewards=[give("createaddition:copper_wire", 8), give("minecraft:copper_ingot", 8)], tier=2)

q("accumulator", "Storing Power", deps="connectors", icon="createaddition:modular_accumulator",
  tasks=item("createaddition:modular_accumulator", 2), desc="""
    The &eAccumulator&r is a battery that grows when you place several together.
    Give it an input connector and an output connector.

    Store power from a windmill at night or from a slow generator over time.""",
  rewards=[give("minecraft:redstone", 16)])

q("long_wires", "Long-Distance Lines", deps="connectors", icon="immersiveengineering:wirecoil_copper",
  desc="""
    For power lines between bases or across the map, Strata uses &eImmersive
    Engineering&r wires: &eLV&r (copper), &eMV&r (electrum) and &eHV&r (steel) on poles
    with connectors and transformers.

    Rule of thumb: Crafts & Additions wires inside the base, IE lines between places.
    See the &bImmersive Engineering&r chapter to build them.""",
  rewards=[give("minecraft:copper_ingot", 16)])

# --- Create: New Age ------------------------------------------------------------------------
q("magnets", "Magnets", deps="alternator", icon="create_new_age:redstone_magnet",
  tasks=item("create_new_age:redstone_magnet", 8), desc="""
    &eCreate: New Age&r is the next step up. Its generators need &emagnets&r.
    &eRedstone Magnets&r are the first kind; stronger magnets come later.""",
  rewards=[give("minecraft:redstone", 32), give("minecraft:iron_ingot", 8)], tier=2)

q("generator", "Coil Generator", deps="magnets", icon="create_new_age:generator_coil",
  tasks=[item("create_new_age:generator_coil", 4), item("create_new_age:carbon_brushes")],
  size=1.5, shape="hexagon", desc="""
    Stack &eGenerator Coils&r on a spinning shaft and surround them with magnets.
    &eCarbon Brushes&r collect the electricity and push it into the block next to them.

    Stronger magnets turn more of your stress into power, but the coils also use more SU.
    Ponder it with &eW&r. This beats the alternator by a lot.
    (New Age's own wires aren't used in Strata: hook the brushes to Crafts & Additions
    or IE connectors.)""",
  rewards=[give("create_new_age:redstone_magnet", 8), give("minecraft:copper_ingot", 16)], tier=3)

q("better_magnets", "Stronger Magnets", deps="generator", icon="create_new_age:layered_magnet",
  tasks=item("create_new_age:layered_magnet", 8), desc="""
    &eLayered Magnets&r make your coils far more efficient, and &eNetherite Magnets&r are
    the best of all. Swap them in around your coils and watch the output climb.""",
  rewards=[give("minecraft:iron_block", 2)], tier=3)

q("energiser", "Energiser", deps="generator", icon="create_new_age:basic_energiser",
  tasks=[item("create_new_age:basic_energiser"), item("create_new_age:overcharged_iron", 4)],
  desc="""
    The &eEnergiser&r uses electricity and rotation to charge items on a depot or belt
    below it. Iron becomes &eOvercharged Iron&r, a key New Age material.""",
  rewards=[give("minecraft:iron_ingot", 16)], tier=2)

# --- nuclear --------------------------------------------------------------------------------
q("thorium", "Thorium", deps="better_magnets", icon="create_new_age:thorium",
  tasks=item("create_new_age:thorium", 8), desc="""
    &eThorium Ore&r is the fuel source for New Age nuclear power. Find it underground
    (press &eR&r on thorium ore to see where).""",
  rewards=[give("minecraft:leather", 16), give("minecraft:coal", 16)], tier=2)

q("reactor", "Nuclear Reactor", deps=["thorium", "steam"], icon="create_new_age:reactor_rod",
  tasks=[item("create_new_age:reactor_rod", 4), item("create_new_age:reactor_fuel_acceptor"),
         item("create_new_age:reactor_heat_vent"), item("create_new_age:reactor_casing", 16)],
  size=1.5, shape="hexagon", desc="""
    A reactor makes &cenormous&r heat. It needs &eReactor Rods&r, a &eFuel Acceptor&r
    (feed it &eNuclear Fuel&r) and a &eHeat Vent&r that sends the heat into pipes.

    &cWarning:&r a running reactor gives off deadly radiation. Wear leather armor or fully
    enclose it in Reactor Casing and Reactor Glass. And always use its heat, or it melts
    down. Ponder every part with &eW&r before you start.""",
  rewards=[give("create_new_age:reactor_glass", 8)], tier=4)

q("heater", "Nuclear Steam", deps="reactor", icon="create_new_age:heater",
  tasks=item("create_new_age:heater", 4), desc="""
    A &eBoiler Heater&r works like a Blaze Burner under a boiler, but uses heat from pipes
    instead of fuel. Pipe your reactor's heat into heaters under a big boiler and run a
    wall of steam engines.

    That's the top of Create's power ladder. Mekanism fission and fusion sit at the same
    level.""",
  rewards=[give("create:steam_engine", 2)], tier=5)

# --- Diesel Generators ----------------------------------------------------------------------
q("plant_oil", "Plant Oil", deps="intro", icon="createdieselgenerators:plant_oil_bucket",
  tasks=item("createdieselgenerators:plant_oil_bucket"), desc="""
    &eCreate: Diesel Generators&r adds engines that burn liquid fuel for rotation.
    The easiest fuel is &ePlant Oil&r: compact seeds with a Press over a Basin.""",
  rewards=[give("minecraft:wheat_seeds", 64)])

q("diesel_engine", "Diesel Engine", deps="plant_oil", icon="createdieselgenerators:diesel_engine",
  tasks=item("createdieselgenerators:diesel_engine"), desc="""
    Pipe fuel into a &eDiesel Engine&r and it spins a shaft. A redstone signal stops it.
    Small, strong and portable: great on trains, boats and remote outposts.

    Better fuels make it stronger: plant oil is the weakest, &eethanol&r and
    &ebiodiesel&r are better, &ediesel&r and &egasoline&r from crude oil are best.
    &eModular&r engines stack, and the &eHuge Diesel Engine&r is the biggest of all.""",
  rewards=[give("createdieselgenerators:plant_oil_bucket", 2)], tier=2)

q("pumpjack", "Strike Oil", deps="diesel_engine", icon="createdieselgenerators:pumpjack_crank",
  tasks=[item("createdieselgenerators:oil_scanner"), item("createdieselgenerators:pumpjack_crank"),
         item("createdieselgenerators:pumpjack_head"), item("createdieselgenerators:pumpjack_hole")],
  desc="""
    Some chunks hide &eCrude Oil&r deep below: right-click an &eOil Scanner&r to see how
    much is under you (some biomes have more).

    A &ePumpjack&r is a glued contraption that rocks up and down over an oil chunk.
    Run a straight vertical pipe down to bedrock, cap it with a &ePumpjack Hole&r, and
    pump the oil out. Ponder it with &eW&r: it has a few parts.""",
  rewards=[give("create:fluid_pipe", 32)], tier=3)

q("distill", "Distillation", deps="pumpjack", icon="createdieselgenerators:distillation_controller",
  tasks=[item("createdieselgenerators:distillation_controller"), item("createdieselgenerators:diesel_bucket")],
  desc="""
    Put a &eDistillation Controller&r on a fluid tank at least 3 blocks tall, heat it and
    pump crude oil in at the bottom. Out come &eDiesel&r and &eGasoline&r, the best
    engine fuels.""",
  rewards=[give("create:fluid_tank", 4)], tier=3)

# --- where next -----------------------------------------------------------------------------
q("next", "Where Next?", deps=["generator", "connectors"], icon="minecraft:oak_sign", shape="square",
  desc="""
    Plenty of power? Spend it:

    &bImmersive Engineering&r: long power lines and big industrial machines.
    &bMekanism&r: ore processing, generators, fission and fusion.
    &bApplied Energistics 2&r: digital storage that runs on FE.
    &bCreate: Airships&r: engines and thrusters to fly what you build.""")
