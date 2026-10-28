from dsl import *

C = chapter("mekanism", "Mekanism", group="tech", icon="mekanism:metallurgic_infuser",
            subtitle="Ore processing, gases, power and the MekaSuit")
q = C.quest

q("intro", "What is Mekanism?", icon="mekanism:steel_casing", deps="welcome/iron_age",
  size=1.5, shape="gear", desc="""
    Mekanism is a big tech mod about &eprocessing&r: its machines turn one ore into two,
    three, four or even five ingots, using gases like oxygen and hydrogen along the way.

    It also has strong generators, energy storage, a jetpack, teleporters and, at the
    very end, the &5MekaSuit&r.

    Machines run on power (FE). Any generator from another mod works too.""")

# --- basics -----------------------------------------------------------------------------
q("osmium", "Osmium", deps="intro", icon="mekanism:ingot_osmium",
  tasks=item("mekanism:ingot_osmium", 8), desc="""
    &eOsmium&r is Mekanism's main metal. Its blue-grey ore is common underground.
    Smelt the raw ore into ingots.

    Keep an eye out for &eTin&r, &eLead&r, &eUranium&r and &eFluorite&r ores too:
    Mekanism uses all of them later.""",
  rewards=[give("mekanism:raw_osmium", 8)])

q("infuser", "Metallurgic Infuser", deps="osmium", icon="mekanism:metallurgic_infuser", tier=2,
  tasks=item("mekanism:metallurgic_infuser"), desc="""
    The &eMetallurgic Infuser&r mixes a metal with an infusion material.
    Put coal or charcoal in the left slot for &8carbon&r, redstone for &credstone&r,
    diamonds for &bdiamond&r, and so on. Then put the metal in the middle.

    Osmium + redstone makes a &eBasic Control Circuit&r. Iron + carbon makes Enriched Iron.""",
  rewards=[give("minecraft:redstone", 32), give("minecraft:coal", 16)])

q("steel", "Mekanism Steel", deps="infuser", icon="mekanism:ingot_steel",
  tasks=item("mekanism:ingot_steel", 8), desc="""
    Steel takes two trips through the infuser:
    iron + carbon = &eEnriched Iron&r, then Enriched Iron + carbon = &eSteel Dust&r.
    Smelt the dust into a &eSteel Ingot&r.

    (IE steel works for most recipes too.)""",
  rewards=[give("minecraft:iron_ingot", 16)])

q("casing", "Steel Casing", deps="steel", icon="mekanism:steel_casing",
  tasks=item("mekanism:steel_casing", 2), desc="""
    The &eSteel Casing&r is the frame inside almost every Mekanism machine.
    Make a few: you'll go through them fast.""",
  rewards=[give("mekanism:ingot_osmium", 8)])

q("circuits", "Control Circuits", deps="infuser", icon="mekanism:basic_control_circuit",
  tasks=item("mekanism:basic_control_circuit", 4), desc="""
    Circuits are the brains of every machine. The &eBasic Control Circuit&r comes from
    osmium + redstone in the infuser.

    Each higher tier needs the alloy of the same tier, so circuits and alloys go up
    together.""",
  rewards=[give("minecraft:redstone", 16)])

q("alloys", "Alloys", deps="circuits", icon="mekanism:alloy_infused", tier=2,
  tasks=[item("mekanism:alloy_infused", 4), item("mekanism:alloy_reinforced", 2)], desc="""
    &eInfused Alloy&r: copper + redstone in the infuser.
    &eReinforced Alloy&r: Infused Alloy + diamond.
    &eAtomic Alloy&r (later): Reinforced Alloy + refined obsidian.

    Alloys upgrade circuits, machines, cables and energy cubes to the next tier.""",
  rewards=[give("minecraft:copper_ingot", 16), give("minecraft:diamond", 2)])

q("circuits_up", "Better Circuits", deps="alloys", icon="mekanism:elite_control_circuit", tier=3,
  tasks=[item("mekanism:advanced_control_circuit", 2), item("mekanism:elite_control_circuit")], desc="""
    Circuit + two matching alloys = the next circuit:
    Basic, &eAdvanced&r, &eElite&r and finally &5Ultimate&r.

    Elite parts open up the bigger factories and faster cables.""")

# --- ore processing ---------------------------------------------------------------------
q("x2", "Ore x2: Enrichment", deps="casing", icon="mekanism:enrichment_chamber", tier=2,
  tasks=item("mekanism:enrichment_chamber"), desc="""
    The &eEnrichment Chamber&r turns one ore into &etwo dusts&r. Smelt them for two ingots.
    Every later step builds on this one, so don't throw it out.

    It also makes Enriched Carbon and Enriched Redstone, a denser feed for the infuser.""",
  rewards=[give("minecraft:iron_ingot", 16)])

q("separator", "Splitting Water", deps="x2", icon="mekanism:electrolytic_separator",
  tasks=item("mekanism:electrolytic_separator"), desc="""
    The &eElectrolytic Separator&r splits water into &eHydrogen&r and &eOxygen&r gas.
    Pipe water in and power it. Store the gases in chemical tanks or send them
    straight to machines.

    Oxygen powers the next ore step. Hydrogen fuels the jetpack.""",
  rewards=[give("mekanism:basic_chemical_tank")])

q("x3", "Ore x3: Purification", deps="separator", icon="mekanism:purification_chamber", tier=3,
  tasks=item("mekanism:purification_chamber"), desc="""
    The &ePurification Chamber&r uses &eoxygen&r to turn one ore into &ethree clumps&r.
    Then: clumps go into a &eCrusher&r for dirty dust, dirty dust into the
    &eEnrichment Chamber&r for dust, and dust into a furnace.

    That's a production line: connect the machines with pipes and let it run.""",
  rewards=[give("minecraft:raw_iron", 16)])

q("x4", "Ore x4: Injection", deps="x3", icon="mekanism:chemical_injection_chamber", tier=3,
  tasks=item("mekanism:chemical_injection_chamber"), desc="""
    The &eChemical Injection Chamber&r uses &eHydrogen Chloride&r to turn one ore into
    &efour shards&r, which feed into the Purification Chamber line.

    Hydrogen Chloride is hydrogen + chlorine in a &eChemical Infuser&r. Chlorine comes
    from brine. Press &eR&r on any gas in EMI to see where it comes from.""",
  rewards=[give("minecraft:raw_gold", 16)])

q("x5", "Ore x5: Dissolution", deps="x4", icon="mekanism:chemical_dissolution_chamber", tier=4,
  tasks=[item("mekanism:chemical_dissolution_chamber"), item("mekanism:chemical_washer"),
         item("mekanism:chemical_crystallizer")], desc="""
    The top step. The &eChemical Dissolution Chamber&r dissolves ore in &eSulfuric Acid&r
    into a dirty slurry, the &eChemical Washer&r cleans it with water, and the
    &eChemical Crystallizer&r turns it into &efive crystals&r per ore.

    Crystals go into the Injection Chamber and down the rest of the line.
    It's a big build. Do it with friends!""",
  rewards=[give("minecraft:raw_copper", 32), give("mekanism:raw_osmium", 16)])

q("factories", "Factories", deps="x2", icon="mekanism:basic_smelting_factory",
  tasks=item("mekanism:basic_smelting_factory"), desc="""
    A &eFactory&r is several machines in one block: it works on 3, 5, 7 or 9 items at once
    depending on tier. Upgrade a machine into a factory with a &eTier Installer&r,
    or craft one directly.

    &eSpeed&r and &eEnergy Upgrades&r (in the machine's side tab) help too.""",
  tier=2)

q("digital_miner", "Digital Miner", deps="circuits_up", icon="mekanism:digital_miner", tier=4,
  tasks=item("mekanism:digital_miner"), desc="""
    The &eDigital Miner&r mines a huge area underground without you being there,
    only taking the blocks you filter for (say, all ores).

    It uses a lot of power and needs Atomic Alloy. Set its filters, give it a chest
    and power, and press start.""")

# --- moving stuff -----------------------------------------------------------------------
q("cables", "Cables, Pipes and Tubes", deps="casing", icon="mekanism:basic_universal_cable",
  tasks=[item("mekanism:basic_universal_cable", 8), item("mekanism:basic_mechanical_pipe", 8),
         item("mekanism:basic_pressurized_tube", 8), item("mekanism:basic_logistical_transporter", 8)],
  desc="""
    &eUniversal Cables&r carry power. &eMechanical Pipes&r carry fluids.
    &ePressurized Tubes&r carry gases. &eLogistical Transporters&r carry items.

    Use the &eConfigurator&r (or the machine's side config tab) to pick which sides
    push and pull. Inside a base these are all you need; for long distances, IE power
    lines and trains do the job.""",
  rewards=[give("mekanism:ingot_osmium", 8)])

q("energy_cube", "Energy Cubes", deps="cables", icon="mekanism:basic_energy_cube",
  tasks=item("mekanism:basic_energy_cube"), desc="""
    An &eEnergy Cube&r stores power. Set its sides to input or output in its GUI.
    Upgrade it with alloys and circuits for much more storage.

    Really big storage comes later: the &eInduction Matrix&r multiblock.""",
  rewards=[give("minecraft:redstone_block", 4)])

# --- generators -------------------------------------------------------------------------
q("gen_basic", "First Generators", deps="casing", icon="mekanismgenerators:heat_generator",
  tasks=[item("mekanismgenerators:heat_generator"), item("mekanismgenerators:solar_generator")], desc="""
    &bMekanism Generators&r adds its own power.

    &eHeat Generator&r: burns fuel, and gets a bonus from lava next to it.
    &eSolar Generator&r: free power while the sun is up.
    Neither is huge, but they get you started.""",
  rewards=[give("minecraft:coal", 32)])

q("gen_mid", "Wind and Gas", deps="gen_basic", icon="mekanismgenerators:wind_generator", tier=2,
  tasks=[item("mekanismgenerators:wind_generator"), item("mekanismgenerators:gas_burning_generator")],
  desc="""
    &eWind Generator&r: the higher you build it, the more it makes.
    &eGas-Burning Generator&r: burns gas fuel like &eEthylene&r for a lot of power.

    For truly big power you need a reactor.""")

q("fission", "Fission Reactor", deps=["gen_mid", "x2"], icon="mekanismgenerators:fission_reactor_casing",
  tier=4, tasks=item("mekanismgenerators:fission_reactor_casing", 16), desc="""
    The &eFission Reactor&r is a multiblock that burns fuel made from uranium.
    It makes heat; pair it with an &eIndustrial Turbine&r to turn that into power.

    &cCareful:&r a reactor without enough cooling can melt down and spread radiation.
    Wear a Hazmat suit, add redstone safety controls and read up on reactor design
    before turning it on.

    Its waste is useful: it leads to polonium and plutonium.""")

q("fusion", "Fusion Reactor", deps="fission", icon="mekanismgenerators:fusion_reactor_controller",
  tier=5, tasks=item("mekanismgenerators:fusion_reactor_controller"), desc="""
    The &eFusion Reactor&r is Mekanism's biggest generator. It burns deuterium and
    tritium and needs a powerful laser blast to start.

    Once it runs it makes enormous amounts of power. A true late-game project.""")

# --- tools, gear and travel ------------------------------------------------------------
q("tools", "Mekanism Tools", deps="osmium", icon="mekanismtools:osmium_pickaxe",
  tasks=item("mekanismtools:osmium_pickaxe"), desc="""
    &bMekanism Tools&r adds tools and armour from Mekanism's metals: osmium, bronze,
    steel, lapis, glowstone and &erefined obsidian&r (as tough as netherite).

    Each also has a &ePaxel&r: pickaxe, axe and shovel in one.""",
  rewards=[give("mekanism:ingot_osmium", 8)])

q("tools_up", "Refined Obsidian Armour", deps="tools", icon="mekanismtools:refined_obsidian_chestplate",
  tier=3, tasks=item("mekanismtools:refined_obsidian_chestplate"), desc="""
    &eRefined Obsidian&r is as tough as netherite, without the trip to the Nether.
    Obsidian is crushed, infused with diamond and compressed with osmium into ingots
    (press &eR&r on the ingot to follow the chain).

    A full set is great armour for the dangerous dimensions.""")

q("jetpack", "Jetpack", deps=["separator", "steel"], icon="mekanism:jetpack", tier=3,
  tasks=item("mekanism:jetpack"), desc="""
    The &eJetpack&r lets you fly, but it burns &eHydrogen&r the whole time.
    Fill it from an Electrolytic Separator or a chemical tank. When the tank's empty,
    you fall, so watch the gauge!

    Toggle its mode (normal or hover) with its key in Options > Controls.""",
  rewards=[give("mekanism:basic_chemical_tank")])

q("teleporter", "Teleporter", deps="circuits_up", icon="mekanism:teleporter", tier=4,
  tasks=[item("mekanism:teleporter"), item("mekanism:teleporter_frame", 9)], desc="""
    Earned teleporting! Build a &eTeleporter&r inside a doorway of &eTeleporter Frames&r
    at each place you want to link, and give them the same &efrequency&r.

    Every jump costs &epower&r, and longer trips cost more. There's a teleporter only
    where someone built one, so a network takes real work.""")

q("entangloporter", "Quantum Entangloporter", deps=["circuits_up", "welcome/nether"],
  icon="mekanism:quantum_entangloporter", tier=4, tasks=item("mekanism:quantum_entangloporter"),
  desc="""
    Mid-game wireless. Two &eQuantum Entangloporters&r on the same frequency act like
    one block: items, fluids, gases, power and heat put into one come out of the other.

    It needs Atomic Alloy and an Ultimate Control Circuit, so it's a real investment.
    It's part of Strata's wireless tier that opens after the Nether.""")

# --- late game (boss gated) -------------------------------------------------------------
q("ultimate", "Ultimate Tier", deps=["circuits_up", "cataclysm/netherite_monstrosity"],
  icon="mekanism:ultimate_control_circuit", tier=4,
  tasks=[item("mekanism:ultimate_control_circuit"), item("mekanism:ultimate_energy_cube")], desc="""
    The &5Ultimate&r tier: the fastest factories, biggest cubes and thickest cables.

    In Strata the top tier is meant for after you've beaten the
    &cNetherite Monstrosity&r (Cataclysm). Boss drops will be part of the recipes.""")

q("sps", "Supercritical Phase Shifter", deps=["fission", "cataclysm/netherite_monstrosity"],
  icon="mekanism:sps_casing", tier=5, tasks=item("mekanism:sps_casing", 16), desc="""
    The &eSPS&r is a huge multiblock that turns polonium into &dantimatter&r.
    It eats an enormous amount of power.

    Antimatter goes into the &eAntiprotonic Nucleosynthesizer&r and the very best
    MekaSuit parts.""")

q("antimatter", "Antimatter", deps="sps", icon="mekanism:pellet_antimatter", tier=5,
  tasks=item("mekanism:pellet_antimatter"), desc="""
    An &dAntimatter Pellet&r is one of the most expensive items in Mekanism.
    Crystallize the antimatter from your SPS into pellets.

    Congratulations: your power grid is officially huge.""")

q("mekasuit", "The MekaSuit", deps=["ultimate", "fission", "cataclysm/ignis"],
  icon="mekanism:mekasuit_bodyarmor", tier=5, size=1.5, shape="diamond",
  tasks=item("mekanism:mekasuit_bodyarmor"), desc="""
    The &5MekaSuit&r is the best armour in Mekanism. It runs on &epower&r and takes
    &emodules&r (installed at a Modification Station) for things like vision, speed
    and protection.

    &6Flight:&r its jetpack module burns hydrogen and its gravitational module drains
    a lot of power. It's a late-game reward, and it's never free.

    Made from netherite armour, polonium pellets and Ultimate circuits, after beating
    &cIgnis&r.""")

q("where_next", "Where next?", deps=["x5", "energy_cube"], icon="minecraft:oak_sign", desc="""
    &bApplied Energistics 2&r: store everything your ore line makes. Applied Mekanistics
    even lets it store gases.
    &bImmersive Engineering&r: HV lines carry your reactor's power across the map.
    &bEndgame&r: Draconic Evolution needs a lot of power.""")
