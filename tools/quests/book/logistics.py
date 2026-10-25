from dsl import *

C = chapter("logistics", "Logistics & Wireless", group="tech", icon="laserio:laser_node",
            subtitle="Logic networks, laser item transport and (later) wireless power")
q = C.quest

q("intro", "Moving Things Around", icon="laserio:laser_wrench", deps="welcome/iron_age",
  size=1.5, shape="gear", desc="""
    Once you have a few machines, you'll want them to talk to each other.

    &bIntegrated Dynamics&r: read anything (a chest, a tank, the time of day) and make
    your base react to it.
    &bLaserIO&r: move items, fluids and power between nearby blocks with lasers.
    &bMore Red&r: compact redstone logic gates and wires.
    &bFlux Networks&r: wireless power, &cafter the Nether&r.""")

# --- Integrated Dynamics ----------------------------------------------------------------
q("id_menril", "ID: Menril", deps="intro", icon="integrateddynamics:menril_sapling",
  tasks=item("integrateddynamics:crystalized_menril_chunk", 16), desc="""
    Integrated Dynamics runs on &eMenril&r, from pale blue Menril trees.
    Squeeze Menril logs in a &eSqueezer&r for resin, then dry the resin in a
    &eDrying Basin&r to get &eCrystallized Menril&r.

    The book &eOn the Dynamics of Integration&r explains the whole mod.""",
  rewards=[give("integrateddynamics:menril_sapling", 4)])

q("id_cable", "ID: Logic Cables", deps="id_menril", icon="integrateddynamics:cable",
  tasks=[item("integrateddynamics:cable", 16), item("integrateddynamics:variable", 8)], desc="""
    &eLogic Cables&r join everything into one network. Information travels on
    &eVariable Cards&r: little cards that hold a value, like "how many iron ingots
    are in this chest".""",
  rewards=[give("integrateddynamics:crystalized_menril_chunk", 16)])

q("id_reader", "ID: Readers and Displays", deps="id_cable", icon="integrateddynamics:part_display_panel",
  tier=2, tasks=[item("integrateddynamics:part_inventory_reader"), item("integrateddynamics:part_display_panel")],
  desc="""
    Put an &eInventory Reader&r on a cable facing a chest, pick a value in its GUI and
    write it to a variable card. Put the card in a &eDisplay Panel&r and it shows
    the number live.

    There are readers for blocks, fluids, energy, entities, redstone and more.""")

q("id_programmer", "ID: Logic Programmer", deps="id_reader", icon="integrateddynamics:logic_programmer",
  tier=2, tasks=item("integrateddynamics:logic_programmer"), desc="""
    The &eLogic Programmer&r combines values with operators:
    "if iron is under 64, then turn on the redstone signal".

    Feed the result into a &eRedstone Writer&r to switch machines on and off by
    themselves.""")

q("id_writer", "ID: Make It Happen", deps="id_programmer", icon="integrateddynamics:part_redstone_writer",
  tier=3, tasks=item("integrateddynamics:part_redstone_writer"), desc="""
    Writers turn logic into action. A &eRedstone Writer&r gives off a signal based on
    a variable, so your smelter only runs when coal is in stock, or a lamp lights up
    when the reactor gets hot.

    Small logic, big results.""")

# --- LaserIO ----------------------------------------------------------------------------
q("lio_node", "LaserIO: Laser Nodes", deps="intro", icon="laserio:laser_node",
  tasks=[item("laserio:laser_node", 2), item("laserio:laser_wrench")], desc="""
    A &eLaser Node&r sits next to your machines and chests. Link two nodes with the
    &eLaser Wrench&r and a laser beam connects them.

    Links have a &emaximum range&r, so nodes are for moving things around a base,
    not across the map.""",
  rewards=[give("minecraft:redstone", 16)])

q("lio_cards", "LaserIO: Cards", deps="lio_node", icon="laserio:card_item", tier=2,
  tasks=[item("laserio:card_item", 2), item("laserio:logic_chip", 4)], desc="""
    &eCards&r go into a node's sides and say what to do: an &eItem Card&r set to
    &eExtract&r on one node and &eInsert&r on another moves items between them.

    There are cards for fluids, energy, Mekanism chemicals and redstone too.
    Add &efilters&r to choose what goes where.""",
  rewards=[give("minecraft:gold_ingot", 4)])

q("lio_filters", "LaserIO: Filters and Speed", deps="lio_cards", icon="laserio:filter_basic",
  tasks=[item("laserio:filter_basic"), item("laserio:overclocker_card")], desc="""
    A &eBasic Filter&r on a card picks which items move. Tag, mod and count filters
    do clever sorting.

    &eCard Overclockers&r make a card move more at once. Great for ore lines.""")

# --- More Red ---------------------------------------------------------------------------
q("mr_alloy", "More Red: Red Alloy", deps="intro", icon="morered:red_alloy_ingot",
  tasks=[item("morered:red_alloy_ingot", 4), item("morered:red_alloy_wire", 16)], desc="""
    &bMore Red&r adds thin &eRed Alloy Wire&r that you can stick on walls and ceilings,
    plus logic gates that fit in one block.

    Red alloy is a metal ingot plus redstone (press &eR&r to see it).""",
  rewards=[give("minecraft:redstone", 32)])

q("mr_gates", "More Red: Logic Gates", deps="mr_alloy", icon="morered:and_gate",
  tasks=[item("morered:soldering_table"), item("morered:and_gate")], desc="""
    The &eSoldering Table&r makes logic gates: AND, OR, NOT, XOR, latches, pulse gates
    and more. Each gate is one small plate, so tricky redstone fits in tight spaces.

    &eBundled cables&r carry 16 colour signals in one line.""")

# --- Flux Networks (gated) --------------------------------------------------------------
q("flux_dust", "Flux Dust", deps=["intro", "welcome/nether"], icon="fluxnetworks:flux_dust",
  tasks=item("fluxnetworks:flux_dust", 16), desc="""
    &bFlux Networks&r sends power without wires. It's part of Strata's wireless tier
    that opens &eafter the Nether&r.

    &eFlux Dust&r is made in the world by crushing redstone between &ebedrock&r and
    &eobsidian&r. Press &eR&r on Flux Dust to see the setup.""",
  rewards=[give("minecraft:redstone", 32), give("minecraft:obsidian", 4)])

q("flux_net", "A Flux Network", deps="flux_dust", icon="fluxnetworks:flux_point", tier=3,
  tasks=[item("fluxnetworks:flux_plug"), item("fluxnetworks:flux_point"), item("fluxnetworks:basic_flux_storage")],
  desc="""
    &eFlux Plug&r: put it next to a generator; it pulls power into the network.
    &eFlux Point&r: put it next to a machine; it hands power out.
    &eFlux Storage&r: a battery for the network.

    Open any of them to create a network and pick it on every device.
    Set a password if you don't want others plugging in.""")

q("where_next", "Where next?", deps=["id_reader", "lio_cards"], any_dep=True, icon="minecraft:oak_sign",
  desc="""
    &bApplied Energistics 2&r: a full digital storage network.
    &bImmersive Engineering&r: real power lines for long distances.
    &bMekanism&r: ore lines that LaserIO can feed.""")
