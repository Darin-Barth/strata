from dsl import *

C = chapter("more_machines", "More Machines", group="tech", icon="pneumaticcraft:air_compressor",
            subtitle="Industrial Foregoing, PneumaticCraft, Powah and Extreme Reactors")
q = C.quest

q("intro", "More Ways to Build", icon="industrialforegoing:machine_frame_simple",
  deps="welcome/iron_age", size=1.5, shape="gear", desc="""
    Four smaller tech mods, each with its own style. Pick the ones that sound fun:

    &bIndustrial Foregoing&r: farms and factories that run by themselves.
    &bPneumaticCraft&r: machines that run on &ecompressed air&r, plus drones.
    &bPowah&r: simple, strong generators and power storage.
    &bExtreme Reactors&r: build your own reactor, any size you like.""")

# --- Industrial Foregoing ---------------------------------------------------------------
q("if_latex", "IF: Tapping Trees", deps="intro", icon="industrialforegoing:fluid_extractor",
  tasks=item("industrialforegoing:fluid_extractor"), desc="""
    Industrial Foregoing starts with &elatex&r. Place a &eFluid Extractor&r facing a log
    and power it: it slowly drains latex out of the tree.

    It's the first step to rubber and plastic.""",
  rewards=[give("minecraft:oak_log", 32)])

q("if_plastic", "IF: Plastic", deps="if_latex", icon="industrialforegoing:plastic",
  tasks=[item("industrialforegoing:latex_processing_unit"), item("industrialforegoing:plastic", 16)],
  tier=2, desc="""
    The &eLatex Processing Unit&r turns latex and water into &eDry Rubber&r.
    Smelt dry rubber into &ePlastic&r.

    Plastic goes into every IF machine frame.""",
  rewards=[give("industrialforegoing:dryrubber", 8)])

q("if_frames", "IF: Machine Frames", deps="if_plastic", icon="industrialforegoing:machine_frame_simple",
  tier=2, tasks=[item("industrialforegoing:machine_frame_pity"), item("industrialforegoing:machine_frame_simple")],
  desc="""
    IF machines are built on &eMachine Frames&r: Pity, Simple, Advanced and Supreme.
    The Pity frame is crafted; the better ones are made in the &eDissolution Chamber&r
    with latex or other fluids.

    The frame tier decides which machines you can build.""",
  rewards=[give("minecraft:iron_ingot", 16)])

q("if_farms", "IF: Automatic Farms", deps="if_frames", icon="industrialforegoing:plant_gatherer",
  tasks=[item("industrialforegoing:plant_sower"), item("industrialforegoing:plant_gatherer")], desc="""
    The &ePlant Sower&r plants seeds in an area, and the &ePlant Gatherer&r harvests it.
    Add a &ePlant Fertilizer&r and you have a farm that never needs you.

    IF also has animal ranchers, mob crushers and more. Have a look with &eU&r on a frame.""",
  rewards=[give("minecraft:wheat_seeds", 32), give("minecraft:bone_meal", 32)])

q("if_laser", "IF: Laser Drill", deps="if_frames", icon="industrialforegoing:ore_laser_base", tier=4,
  tasks=[item("industrialforegoing:ore_laser_base"), item("industrialforegoing:laser_drill", 4)], desc="""
    The &eOre Laser Base&r pulls ores out of thin air. Surround it with &eLaser Drills&r
    feeding it power.

    Coloured &elenses&r bias it toward certain ores. Expensive, but a source of ore
    that never runs out.""")

# --- PneumaticCraft ---------------------------------------------------------------------
q("pnc_iron", "PNC: Compressed Iron", deps="intro", icon="pneumaticcraft:ingot_iron_compressed",
  tasks=item("pneumaticcraft:ingot_iron_compressed", 8), desc="""
    PneumaticCraft starts with a bang. Drop iron ingots on the ground and blow them up
    with TNT (or a creeper): some of them become &eCompressed Iron&r.

    Some iron gets lost, so throw in a stack. Later the Pressure Chamber does this
    without losses.""",
  rewards=[give("minecraft:tnt", 4), give("minecraft:iron_ingot", 16)])

q("pnc_compressor", "PNC: Air Compressor", deps="pnc_iron", icon="pneumaticcraft:air_compressor",
  tier=2, tasks=[item("pneumaticcraft:air_compressor"), item("pneumaticcraft:pressure_tube", 8)], desc="""
    The &eAir Compressor&r burns fuel to pump out &ecompressed air&r.
    &ePressure Tubes&r carry air to your machines.

    &cWatch the pressure!&r Every machine and tube has a limit. Go over it and it
    explodes. Check with a &ePressure Gauge&r or the &eManometer&r.""",
  rewards=[give("minecraft:coal", 32)])

q("pnc_chamber", "PNC: Pressure Chamber", deps="pnc_compressor", icon="pneumaticcraft:pressure_chamber_wall",
  tier=3, tasks=[item("pneumaticcraft:pressure_chamber_wall", 20), item("pneumaticcraft:pressure_chamber_valve"),
                 item("pneumaticcraft:pressure_chamber_interface", 2)], desc="""
    The &ePressure Chamber&r is a hollow box (3x3x3 or bigger) of walls and glass with a
    valve to let air in. Items put in through an &einterface&r get squeezed into new things:
    compressed iron without losses, circuit boards, even coal into diamonds.

    Bigger chambers and higher pressure unlock more recipes.""")

q("pnc_drone", "PNC: Drones", deps="pnc_chamber", icon="pneumaticcraft:drone", tier=3,
  tasks=[item("pneumaticcraft:programmer"), item("pneumaticcraft:drone")], desc="""
    &eDrones&r are little flying robots you program yourself with puzzle pieces in the
    &eProgrammer&r: dig an area, move items, harvest crops, fight mobs.

    They run on compressed air, so give them a &eCharging Station&r to come home to.""")

q("pnc_armor", "PNC: Pneumatic Armour", deps="pnc_chamber", icon="pneumaticcraft:pneumatic_helmet",
  tier=3, tasks=[item("pneumaticcraft:charging_station"), item("pneumaticcraft:pneumatic_helmet")], desc="""
    &ePneumatic Armour&r runs on compressed air. Fill it in a &eCharging Station&r.

    Upgrades add all sorts of tricks: the helmet can scan for ores and mobs, the
    boots can stop fall damage. Each trick uses air.""",
  rewards=[give("pneumaticcraft:ingot_iron_compressed", 16)])

q("pnc_jet", "PNC: Jet Boots", deps="pnc_armor", icon="pneumaticcraft:jet_boots_upgrade_1", tier=4,
  tasks=[item("pneumaticcraft:pneumatic_boots"), item("pneumaticcraft:jet_boots_upgrade_1")], desc="""
    Put &eJet Boots Upgrades&r in your Pneumatic Boots and you can fly.

    &6The cost:&r jet boots burn through &ecompressed air&r fast. When the boots run dry,
    you fall. Higher tiers fly faster. Plan long trips around a Charging Station.""")

# --- Powah ------------------------------------------------------------------------------
q("powah_orb", "Powah: Energizing Orb", deps="intro", icon="powah:energizing_orb",
  tasks=[item("powah:energizing_orb"), item("powah:energizing_rod_starter", 2)], desc="""
    &bPowah&r is all about the &eEnergizing Orb&r. Place &eEnergizing Rods&r around it,
    feed them power, and drop items into the orb: it charges them into new materials.

    Iron + gold makes &eEnergized Steel&r. Blaze rods, diamonds and emeralds become
    crystals for higher tiers. The &eManual&r (Powah's book) explains everything.""",
  rewards=[give("minecraft:gold_ingot", 8)])

q("powah_gen", "Powah: Generators", deps="powah_orb", icon="powah:furnator_starter",
  tasks=[item("powah:furnator_starter"), item("powah:energy_cell_starter")], desc="""
    &eFurnators&r burn fuel, &eMagmators&r burn lava, &eThermo Generators&r use heat
    under them, and &eSolar Panels&r use the sun.

    &eEnergy Cells&r store the power. Everything comes in tiers: Starter, Basic,
    Hardened, Blazing, Niotic, Spirited and Nitro.""",
  rewards=[give("minecraft:coal", 32)])

q("powah_reactor", "Powah: Reactor", deps="powah_gen", icon="powah:reactor_starter", tier=3,
  tasks=item("powah:reactor_starter", 36, title="36 Reactor blocks"), desc="""
    The Powah &eReactor&r is a multiblock that burns &eUraninite&r (from Powah's own ore)
    for power. Add coolant and a carbon source to make it run better. Each tier makes more:
    a Basic reactor about matches a Create alternator, a Nitro one makes 15,000 FE/t.
    The boss-gated nuclear reactors stay the top power.

    Place 36 reactor blocks of the same tier together and it builds itself.""")

# --- Extreme Reactors -------------------------------------------------------------------
q("er_yellorium", "ER: Yellorium", deps="intro", icon="bigreactors:yellorium_ingot",
  tasks=item("bigreactors:yellorium_ingot", 16), desc="""
    &bExtreme Reactors&r burns &eYellorium&r. Its bright yellow ore hides deep
    underground. Smelt it into ingots.""",
  rewards=[give("minecraft:iron_ingot", 16)])

q("er_reactor", "ER: Your First Reactor", deps="er_yellorium", icon="bigreactors:basic_reactorcontroller",
  tier=3, tasks=[item("bigreactors:basic_reactorcontroller"), item("bigreactors:basic_reactorfuelrod", 4),
                 item("bigreactors:basic_reactorcontrolrod")], desc="""
    An Extreme Reactor is a box of &eReactor Casing&r (glass is fine on the sides) with a
    &eController&r, a &ePower Tap&r and an &eAccess Port&r on the outside.

    Inside: columns of &eFuel Rods&r, each topped with a &eControl Rod&r. Fill the gaps
    with water or other moderators. Any size you like, bigger is more efficient.""",
  rewards=[give("bigreactors:yellorium_ingot", 8)])

q("er_turbine", "ER: Turbines", deps="er_reactor", icon="bigreactors:basic_turbinecontroller", tier=4,
  tasks=[item("bigreactors:basic_turbinecontroller"), item("bigreactors:basic_turbinerotorblade", 8)],
  desc="""
    For more power, build a &eReinforced&r reactor that makes &esteam&r (it needs fluid
    ports and water) and pipe it into a &eTurbine&r: a rotor of shafts and blades inside
    a housing.

    A good turbine setup makes far more power from the same fuel.""")

q("where_next", "Where next?", deps=["if_frames", "pnc_compressor", "powah_gen", "er_reactor"], any_dep=True, icon="minecraft:oak_sign", desc="""
    &bMekanism&r and &bOritech&r: more machines, more processing.
    &bImmersive Engineering&r: wire all these generators into one grid.
    &bLogistics & Wireless&r: move things between them automatically.""")
