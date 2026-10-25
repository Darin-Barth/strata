from dsl import *

C = chapter("oritech", "Oritech", group="tech", icon="oritech:pulverizer_block",
            subtitle="Sleek machines, addons, augments and atomic forging")
q = C.quest

q("intro", "What is Oritech?", icon="oritech:machine_core_1", deps="welcome/iron_age",
  size=1.5, shape="gear", desc="""
    &bOritech&r is a modern tech mod with good-looking, animated machines.
    Each machine can be boosted with &eaddons&r (speed, efficiency, yield...) that you
    place right next to it.

    It goes from simple pulverizers all the way to nuclear power, particle accelerators
    and cybernetic &eaugments&r for yourself.""")

q("nickel", "Nickel and Dime", deps="intro", icon="oritech:nickel_ingot",
  tasks=item("oritech:nickel_ingot", 8), desc="""
    Oritech's own metals are &eNickel&r and &ePlatinum&r. Nickel ore is the common one;
    smelt the raw ore into ingots.""",
  rewards=[give("minecraft:copper_ingot", 16)])

q("generator", "Power Up!", deps="nickel", icon="oritech:basic_generator_block",
  tasks=item("oritech:basic_generator_block"), desc="""
    The &eBasic Generator&r burns fuel like coal for power.
    Later you'll get steam engines, bio, lava and fuel generators, and a reactor.

    Oritech machines use normal FE, so any power source in the pack works.""",
  rewards=[give("minecraft:coal", 32)])

q("pipes", "Pipes", deps="generator", icon="oritech:energy_pipe",
  tasks=[item("oritech:energy_pipe", 8), item("oritech:item_pipe", 8)], desc="""
    &eEnergy&r, &eFluid&r and &eItem Pipes&r connect your machines. The &ePipe Wrench&r
    changes which sides connect.

    Framed pipes hide inside walls for a tidy base.""",
  rewards=[give("minecraft:copper_ingot", 16)])

q("pulverizer", "Crushing It", deps="generator", icon="oritech:pulverizer_block", tier=2,
  tasks=[item("oritech:pulverizer_block"), item("oritech:powered_furnace_block")], desc="""
    The &ePulverizer&r turns ore into dust (more ingots per ore) and the
    &ePowered Furnace&r smelts it quickly.

    Small dusts get combined into full ones by themselves.""",
  rewards=[give("minecraft:raw_iron", 16)])

q("addons", "Machine Addons", deps="pulverizer", icon="oritech:machine_speed_addon",
  tasks=item("oritech:machine_speed_addon"), desc="""
    &eAddons&r sit next to a machine and change how it works: &eSpeed&r, &eEfficiency&r,
    &eYield&r, &eCapacitor&r and more. Each machine has a limited number of addon slots.

    Better &eMachine Cores&r let you connect more addon extenders.""",
  tier=2)

q("foundry", "Melt Down", deps="pulverizer", icon="oritech:foundry_block", tier=2,
  tasks=item("oritech:foundry_block"), desc="""
    The &eFoundry&r melts metals together into alloys like &eSteel&r, &eElectrum&r and
    &eAdamant&r.

    Bigger Oritech machines are multiblocks: press &eR&r on one to see what it needs.""")

q("assembler", "Assembly Line", deps="foundry", icon="oritech:assembler_block", tier=3,
  tasks=item("oritech:assembler_block"), desc="""
    The &eAssembler&r builds Oritech's fancier parts: motors, processing units,
    batteries and plating. Most of the mid-game goes through it.""",
  rewards=[give("oritech:nickel_ingot", 16)])

q("centrifuge", "Spin Doctor", deps="assembler", icon="oritech:centrifuge_block", tier=3,
  tasks=[item("oritech:centrifuge_block"), item("oritech:plastic_sheet", 4)], desc="""
    The &eCentrifuge&r separates fluids and materials. It makes &ePolymer Resin&r,
    which you smelt into &ePlastic Sheets&r for later parts.""")

q("frame", "Machine Frames and Lasers", deps="assembler", icon="oritech:laser_arm_block", tier=3,
  tasks=[item("oritech:machine_frame_block", 8), item("oritech:laser_arm_block")], desc="""
    Some machines move on a &eMachine Frame&r: a rectangle of frame blocks on the ground.
    A Block Destroyer, Placer or Fertilizer head runs along it like a gantry.

    The &eEnderic Laser&r mines blocks from a distance and is how you collect
    &eFluxite&r from amethyst.""")

q("drill", "Hand Drill and Chainsaw", deps="pulverizer", icon="oritech:hand_drill", optional=True,
  tasks=item("oritech:hand_drill"), desc="""
    The &eHand Drill&r and &eChainsaw&r are powered tools: fast, but they need
    charging. An &eEquipment Charger&r keeps them topped up.""")

q("resource_node", "Glittering Prizes", deps="frame", icon="oritech:resource_node_iron", tier=4,
  tasks=item("oritech:deep_drill_block"), desc="""
    Deep underground there are &eResource Nodes&r: ore spots that never run out.
    Build a &eBedrock Extractor&r on one and it mines ore forever, as long as it has
    power.""")

q("augments", "Cybernetics!", deps="centrifuge", icon="oritech:augment_application_block", tier=4,
  tasks=[item("oritech:simple_augment_station"), item("oritech:augment_application_block")], desc="""
    &eAugments&r upgrade &eyou&r: research them at a &eCybernetic Research Station&r and
    install them at the &eCybernetic Augmentation Center&r. Think extra health, speed
    or night vision.""")

q("exo", "Exosuit", deps="augments", icon="oritech:exo_chestplate", tier=4,
  tasks=[item("oritech:exo_helmet"), item("oritech:exo_chestplate"), item("oritech:exo_leggings"),
         item("oritech:exo_boots")], desc="""
    The &eExo&r armour runs on power. The helmet gives night vision, the leggings speed,
    the boots stop fall damage, and the chestplate charges your other powered items.

    Keep it charged at an Equipment Charger.""")

q("jetpack", "Exo Jetpack", deps=["exo", "welcome/nether"], icon="oritech:exo_jetpack", tier=4,
  tasks=item("oritech:exo_jetpack"), desc="""
    The &eExo Jetpack&r lets you fly, but it isn't free: it needs &eelectricity&r or
    &eTurbofuel&r (faster on turbofuel). When it's empty, you're walking.

    The Boosted Elytra versions work the same way.""")

q("reactor", "Nuclear Power", deps="centrifuge", icon="oritech:reactor_controller", tier=5,
  tasks=[item("oritech:reactor_controller"), item("oritech:reactor_rod", 4)], desc="""
    Oritech's &eNuclear Reactor&r is a multiblock of rods, heat pipes, vents and
    absorbers. It makes huge amounts of power, and a lot of heat.

    &cKeep it cool&r, or the light show will be bigger than you wanted.""")

q("atomic_forge", "Atomic Smith", deps="reactor", icon="oritech:atomic_forge_block", tier=5,
  tasks=item("oritech:atomic_forge_block"), desc="""
    The &eAtomic Forge&r makes Oritech's best materials, such as &eDuratium&r and
    &ePrometheum&r. It needs a big burst of power for every recipe.""")

q("where_next", "Where next?", deps=["assembler", "addons"], any_dep=True, icon="minecraft:oak_sign",
  desc="""
    &bMekanism&r: a different take on ore processing and power.
    &bImmersive Engineering&r: wire your generators into a long-distance grid.
    &bEndgame&r: Draconic Evolution needs everything you can generate.""")
