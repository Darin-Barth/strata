from dsl import *

C = chapter("ae2", "Applied Energistics 2", group="tech", icon="ae2:controller",
            subtitle="Digital storage, autocrafting and quantum links")
q = C.quest

q("intro", "What is Applied Energistics 2?", icon="ae2:terminal", deps="welcome/iron_age",
  size=1.5, shape="gear", desc="""
    AE2 turns your items into &edata&r. Thousands of items live inside small
    &estorage cells&r, and one &eterminal&r lets you search and grab any of them.

    Later it &eautocrafts&r: ask for 64 machines and it makes every part itself.

    AE2 has its own built-in guide. Item tooltips tell you which key opens it.""")

# --- getting started --------------------------------------------------------------------
q("compass", "Meteorite Compass", deps="intro", icon="ae2:meteorite_compass",
  tasks=[item("ae2:charger"), item("ae2:meteorite_compass")], desc="""
    AE2 starts with a crater. &eMeteorites&r have crashed all over the world.

    Craft a &eCharger&r and a &eCrank&r (attach the crank to the charger and right-click
    it to power the charger by hand). Charge a normal compass to get a &eMeteorite Compass&r:
    it points to the nearest meteorite.""",
  rewards=[give("minecraft:iron_ingot", 8), give("minecraft:copper_ingot", 8)])

q("meteorite", "Find a Meteorite", deps="compass", icon="ae2:sky_stone_block", tier=2,
  tasks=item("ae2:sky_stone_block", 16), desc="""
    A meteorite is a ball of dark &eSky Stone&r. Dig into it:

    The middle holds a &emysterious cube&r with the four &einscriber presses&r.
    Around it you'll find &eBudding Certus Quartz&r, which grows certus crystals.
    Grab the sky stone too, it's used in recipes.""",
  rewards=[give("minecraft:torch", 16)])

q("certus", "Certus Quartz", deps="meteorite", icon="ae2:certus_quartz_crystal",
  tasks=item("ae2:certus_quartz_crystal", 16), desc="""
    Budding certus grows &ecertus buds&r on its sides. Mine fully grown clusters for crystals.

    Budding blocks wear down as they grow. Bring some home and build a little farm;
    a &eGrowth Accelerator&r next to them speeds it up a lot.""",
  rewards=[give("minecraft:quartz", 16)])

q("charged", "Charged Certus", deps="certus", icon="ae2:charged_certus_quartz_crystal",
  tasks=item("ae2:charged_certus_quartz_crystal", 4), desc="""
    Put certus crystals in the &eCharger&r to make &eCharged Certus Quartz&r.
    You can crank it by hand, but it's much nicer once it has power.""",
  rewards=[give("ae2:certus_quartz_crystal", 8)])

q("fluix", "Fluix Crystals", deps="charged", icon="ae2:fluix_crystal",
  tasks=item("ae2:fluix_crystal", 16), desc="""
    Throw a &eCharged Certus Quartz&r, a &eRedstone&r and a &eNether Quartz&r into a pool
    of water together. After a moment they turn into &etwo Fluix Crystals&r.

    Fluix is in nearly everything AE2 makes, especially cables.""",
  rewards=[give("minecraft:redstone", 32), give("minecraft:quartz", 16)])

q("growth", "Growth Accelerator", deps="fluix", icon="ae2:growth_accelerator", optional=True,
  tasks=item("ae2:growth_accelerator"), desc="""
    Place a &eGrowth Accelerator&r next to budding certus and give it power.
    Your quartz farm grows several times faster.""",
  rewards=[give("ae2:certus_quartz_crystal", 16)])

# --- inscriber and processors -----------------------------------------------------------
q("inscriber", "The Inscriber", deps="fluix", icon="ae2:inscriber", tier=2,
  tasks=item("ae2:inscriber"), desc="""
    The &eInscriber&r presses things with the presses you found in meteorites.
    Press goes in the top slot, material in the middle.

    It can also copy a press: put an iron block in with it. Make spares
    for your friends!""",
  rewards=[give("minecraft:iron_block", 2)])

q("silicon", "Silicon", deps="inscriber", icon="ae2:printed_silicon",
  tasks=item("ae2:printed_silicon", 4), desc="""
    Grind certus into dust (the Inscriber does it with no press) and smelt the dust into
    &eSilicon&r. Press silicon with the &eSilicon Press&r for &ePrinted Silicon&r.""",
  rewards=[give("ae2:certus_quartz_crystal", 8)])

q("processors", "Processors", deps="silicon", icon="ae2:logic_processor", tier=3,
  tasks=[item("ae2:logic_processor", 4), item("ae2:calculation_processor", 4),
         item("ae2:engineering_processor", 4)], desc="""
    Processors are made in two steps:
    1. Press &egold&r (Logic), &ecertus&r (Calculation) or &ediamond&r (Engineering)
    with its press to get a printed circuit.
    2. Put the printed circuit on top, printed silicon on the bottom and
    &eredstone&r in the middle.

    Automate this early. You'll need hundreds.""",
  rewards=[give("minecraft:gold_ingot", 8), give("minecraft:diamond", 2)])

# --- the network ------------------------------------------------------------------------
q("controller", "ME Controller", deps="processors", icon="ae2:controller", tier=3,
  tasks=[item("ae2:controller"), item("ae2:energy_acceptor")], desc="""
    The &eME Controller&r is the heart of the network. Feed it power through an
    &eEnergy Acceptor&r (it takes FE from any mod).

    Everything else connects to it with &eFluix cables&r.""",
  rewards=[give("ae2:fluix_glass_cable", 16)])

q("channels", "Cables and Channels", deps="controller", icon="ae2:fluix_smart_cable",
  tasks=item("ae2:fluix_smart_dense_cable", 4), desc="""
    Each device on the network uses a &echannel&r. A normal cable carries &e8&r channels;
    a &edense&r cable carries &e32&r. Smart cables light up to show how many are in use.

    Tip: run dense cable as the backbone from the controller and branch off with
    normal cable.""",
  rewards=[give("ae2:fluix_crystal", 8)])

q("drive", "ME Drive and Storage Cells", deps="controller", icon="ae2:drive", tier=2,
  tasks=[item("ae2:drive"), item("ae2:item_storage_cell_1k", 2)], desc="""
    An &eME Drive&r holds up to 10 &estorage cells&r. A cell holds a set amount of
    data and a limited number of &edifferent&r item types.

    Bigger cells (4k, 16k, 64k, 256k) hold more. Keep similar things on one cell.""",
  rewards=[give("ae2:logic_processor", 4)])

q("terminal", "Terminals", deps="drive", icon="ae2:crafting_terminal",
  tasks=[item("ae2:terminal"), item("ae2:crafting_terminal")], desc="""
    The &eME Terminal&r shows everything stored. Search, sort and grab.
    The &eCrafting Terminal&r adds a crafting grid that pulls ingredients straight
    from the network.

    Put one in your base and say goodbye to chest-diving.""",
  rewards=[give("ae2:calculation_processor", 4)])

q("buses", "Import, Export and Storage Buses", deps="terminal", icon="ae2:import_bus",
  tasks=[item("ae2:import_bus"), item("ae2:export_bus"), item("ae2:storage_bus")], desc="""
    &eImport Bus&r: pulls items out of a machine into the network.
    &eExport Bus&r: pushes chosen items into a machine.
    &eStorage Bus&r: lets the network see into a chest, a drawer wall or a
    Sophisticated Storage chest as if it were a cell.

    Connect your Mekanism ore line and let AE2 feed it.""",
  tier=2)

q("cells_up", "Bigger Cells", deps="drive", icon="ae2:item_storage_cell_16k", tier=3,
  tasks=item("ae2:item_storage_cell_16k"), desc="""
    Cell components stack up: four 1k components make a 4k, four 4k make a 16k,
    and so on. Put the component in a cell housing.

    There are &efluid cells&r too, for lava, water and everything Mekanism pumps out.""")

# --- autocrafting -----------------------------------------------------------------------
q("cpu", "Crafting CPU", deps="channels", icon="ae2:crafting_unit", tier=3,
  tasks=[item("ae2:crafting_unit", 2), item("ae2:1k_crafting_storage")], desc="""
    Autocrafting needs a &eCrafting CPU&r: a solid box of &eCrafting Units&r with at
    least one &eCrafting Storage&r block, attached to the network.

    More storage handles bigger jobs; &eCo-Processing Units&r make it faster.""")

q("patterns", "Patterns", deps="cpu", icon="ae2:blank_pattern",
  tasks=[item("ae2:pattern_encoding_terminal"), item("ae2:blank_pattern", 8)], desc="""
    A &ePattern&r is a recipe saved on a card. Write them in the
    &ePattern Encoding Terminal&r: put in the recipe, press encode.

    Crafting-table recipes and machine recipes (smelting, crushing...) both work.""",
  rewards=[give("ae2:certus_quartz_crystal", 16)])

q("autocraft", "Autocrafting", deps="patterns", icon="ae2:molecular_assembler", tier=4,
  tasks=[item("ae2:pattern_provider"), item("ae2:molecular_assembler")], desc="""
    A &ePattern Provider&r holds patterns and sends ingredients out.
    Put a &eMolecular Assembler&r next to it for crafting-table recipes,
    or point it at any machine (a furnace, a Mekanism chamber) for processing.

    Now ask the terminal for something you don't have and it'll make it.""",
  rewards=[give("ae2:engineering_processor", 8)])

# --- add-ons ----------------------------------------------------------------------------
q("extendedae", "ExtendedAE", deps="autocraft", icon="extendedae:ex_pattern_provider",
  tasks=item("extendedae:ex_pattern_provider"), desc="""
    &bExtendedAE&r adds bigger versions of AE2 blocks: the &eExtended Pattern Provider&r
    holds many more patterns, plus extended interfaces, drives, buses and inscribers.

    The &eAssembler Matrix&r multiblock is a giant crafting factory.""",
  tier=3)

q("infinity_cell", "Infinite Water and Cobble", deps="extendedae", icon="extendedae:infinity_cell",
  optional=True, tasks=item("extendedae:infinity_cell"), desc="""
    ExtendedAE's &eME Infinity Cell&r holds an endless supply of one basic thing,
    like water or cobblestone. Perfect for machines that eat them.""")

q("appflux", "Applied Flux: Power in the Network", deps="cells_up", icon="appflux:fe_1k_cell",
  tasks=item("appflux:fe_1k_cell"), desc="""
    &bApplied Flux&r adds &eFE Storage Cells&r: they store power inside your ME network,
    like a battery in a drive. Its parts can push that power into machines on the
    network.

    Press &eR&r on the cell to see its parts.""",
  tier=3)

q("appmek", "Applied Mekanistics: Chemical Cells", deps=["cells_up", "mekanism/separator"],
  icon="appmek:chemical_storage_cell_1k", tasks=item("appmek:chemical_storage_cell_1k"), desc="""
    &bApplied Mekanistics&r lets AE2 store &eMekanism gases and chemicals&r
    (hydrogen, oxygen, acids, slurries) in &eChemical Storage Cells&r.

    Hook your ore line's tanks to the network and pull exactly what each machine needs.""",
  tier=3)

# --- wireless (gated) -------------------------------------------------------------------
q("wireless", "Wireless Terminal", deps=["terminal", "welcome/nether"], icon="ae2:wireless_terminal",
  tier=3, tasks=[item("ae2:wireless_access_point"), item("ae2:wireless_terminal")], desc="""
    Mid-game wireless: a &eWireless Access Point&r on your network lets a
    &eWireless Terminal&r reach it from nearby. It runs on stored power, so charge it
    in a Charger.

    Range is limited; &eWireless Boosters&r in the access point stretch it.
    It's part of Strata's wireless tier that opens after the Nether.""")

q("cells_late", "256k Cells", deps=["cells_up", "cataclysm/netherite_monstrosity"],
  icon="ae2:item_storage_cell_256k", tier=4, tasks=item("ae2:item_storage_cell_256k"), desc="""
    The biggest standard cell. Strata places the top cells after the
    &cNetherite Monstrosity&r: boss drops will be part of the recipe.""")

q("quantum", "Quantum Network Bridge", deps=["autocraft", "cataclysm/ender_guardian"],
  icon="ae2:quantum_link", tier=5, size=1.5, shape="diamond",
  tasks=[item("ae2:quantum_ring", 8), item("ae2:quantum_link"),
         item("ae2:quantum_entangled_singularity", 2)], desc="""
    The &5Quantum Network Bridge&r links two ME networks anywhere, &eeven in other
    dimensions&r. It's Strata's only cross-dimension wireless, so it's late.

    Build a ring of 8 &eQuantum Rings&r around a &eQuantum Link Chamber&r at each end.
    &eEntangled Singularities&r (made in pairs, in an explosion) go in the chambers.
    Both ends must stay loaded. Gated behind the &cEnder Guardian&r.""")

q("where_next", "Where next?", deps=["autocraft", "buses"], icon="minecraft:oak_sign", desc="""
    &bMekanism&r: feed your ore line straight from the network.
    &bLogistics & Wireless&r: Integrated Dynamics can read your storage and react to it.
    &bResource Farming&r: Mystical Agriculture crops are great for autocrafting.""")
