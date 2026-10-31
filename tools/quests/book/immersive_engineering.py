from dsl import *

C = chapter("immersive_engineering", "Immersive Engineering", group="tech",
            icon="immersiveengineering:hammer",
            subtitle="Big chunky machines, steel and real power lines")
q = C.quest

q("intro", "What is Immersive Engineering?", icon="immersiveengineering:manual",
  deps="welcome/iron_age", size=1.5, shape="gear", desc="""
    Immersive Engineering (IE) is old-school industry: you build machines as
    &ebig multiblock structures&r out of special blocks, then whack them with a hammer
    to bring them to life.

    It's also Strata's &epower grid&r: copper, electrum and steel wires strung between
    poles carry power between your buildings.""")

# --- getting started --------------------------------------------------------------------
q("hammer", "Engineer's Hammer", deps="intro", icon="immersiveengineering:hammer",
  tasks=item("immersiveengineering:hammer"), desc="""
    The hammer is IE's main tool.

    &eRight-click&r a finished pile of blocks with it to &eform a multiblock&r.
    In a crafting grid, hammer + ingot makes a &eplate&r, and hammer + ore makes grit.
    It also rotates and configures IE blocks.""",
  rewards=[give("minecraft:iron_ingot", 8), give("minecraft:copper_ingot", 8)])

q("manual", "Engineer's Manual", deps="hammer", icon="immersiveengineering:manual",
  tasks=item("immersiveengineering:manual"), desc="""
    Every IE multiblock has an exact shape. The &eEngineer's Manual&r shows each one
    layer by layer, with a list of the blocks you need.

    Keep it in your hotbar while you build.""",
  rewards=[give("minecraft:book", 2)])

q("coke_oven", "Coke Oven", deps="manual", icon="immersiveengineering:cokebrick", tier=2,
  tasks=item("immersiveengineering:cokebrick", 27, title="27 Coke Bricks"), desc="""
    Your first multiblock: a &e3x3x3 cube of Coke Bricks&r.
    Hit the middle block of one side with the hammer to form it.

    Put in coal and it slowly bakes it into &eCoal Coke&r, plus &eCreosote Oil&r
    (fill buckets from it). Charcoal works too.""",
  rewards=[give("minecraft:coal", 32), give("minecraft:clay_ball", 16)])

q("treated_wood", "Treated Wood", deps="coke_oven", icon="immersiveengineering:treated_wood_horizontal",
  tasks=item("immersiveengineering:treated_wood_horizontal", 16), desc="""
    Planks soaked in Creosote Oil become &eTreated Wood&r. It's the frame for lots of
    IE machines, posts and the Engineer's Workbench.

    Treated wood posts make nice poles for your power lines later.""",
  rewards=[give("minecraft:oak_planks", 32)])

q("blast_furnace", "Blast Furnace and Steel", deps="coke_oven", icon="immersiveengineering:ingot_steel",
  tier=2, tasks=[item("immersiveengineering:blastbrick", 27, title="27 Blast Bricks"),
                 item("immersiveengineering:ingot_steel", 4)], desc="""
    Another 3x3x3 cube, this time of &eBlast Bricks&r. Form it with the hammer.

    Feed it &eiron&r and &eCoal Coke&r and it slowly makes &eSteel Ingots&r.
    Steel is used all over IE (and other mods too).

    Later, Reinforced Blast Bricks build the Improved Blast Furnace, which
    Blast Furnace Preheaters can speed up.""",
  rewards=[give("immersiveengineering:coal_coke", 16)])

q("workbench", "Engineer's Workbench", deps="treated_wood", icon="immersiveengineering:workbench",
  tasks=item("immersiveengineering:workbench"), desc="""
    The Workbench crafts from &eBlueprints&r. Put a blueprint in the slot and it shows
    what it can make.

    The &eComponents&r blueprint makes Mechanical Components (iron and steel) and parts
    for electronics. Machines need lots of them.""",
  rewards=[give("immersiveengineering:plate_steel", 4)])

q("components", "Mechanical Components", deps="workbench", icon="immersiveengineering:component_iron",
  tasks=[item("immersiveengineering:component_iron", 4), item("immersiveengineering:component_steel", 2)],
  tier=2, desc="""
    Iron Mechanical Components are iron plates plus copper; steel ones use steel plates.
    You'll need a stack of each sooner or later.

    Tip: the &eMetal Press&r multiblock makes plates for you once you have power.""",
  rewards=[give("minecraft:copper_ingot", 16)])

# --- power ------------------------------------------------------------------------------
q("generators", "Making Power", deps="components", icon="immersiveengineering:dynamo", desc="""
    IE makes power from moving things. A &eWater Wheel&r or &eWindmill&r turns a
    &eKinetic Dynamo&r, which outputs power (FE).

    Want more? Later the &eDiesel Generator&r burns biodiesel for lots of it.
    Create rotation, Crafts & Additions and Mekanism power all plug into the same grid.""",
  tasks=item("immersiveengineering:dynamo"),
  rewards=[give("immersiveengineering:windmill_blade", 4)])

q("lv_wire", "LV Power Lines", deps="generators", icon="immersiveengineering:wirecoil_copper",
  tasks=[item("immersiveengineering:wirecoil_copper", 4), item("immersiveengineering:connector_lv", 4)],
  tier=2, desc="""
    &eLow Voltage&r is copper wire. Place &eLV Wire Connectors&r on machines, posts or
    accumulators, then right-click one connector with an &eLV Wire Coil&r and right-click
    the other to string a wire between them.

    Each wire has a maximum length, so put poles in between for long runs.
    LV is fine around a base.""",
  rewards=[give("minecraft:copper_ingot", 16)])

q("accumulator", "Storing Power", deps="lv_wire", icon="immersiveengineering:capacitor_lv",
  tasks=item("immersiveengineering:capacitor_lv"), desc="""
    An &eLV Accumulator&r stores power. Use one as a battery between your generators
    and machines.

    It's also a good meeting point: wire IE lines into it on one side and run
    Crafts & Additions or Mekanism cables out of it on the other.""",
  rewards=[give("minecraft:redstone", 16)])

q("mv_wire", "MV Power Lines", deps="lv_wire", icon="immersiveengineering:wirecoil_electrum",
  tasks=[item("immersiveengineering:wirecoil_electrum", 4), item("immersiveengineering:connector_mv", 4)],
  tier=2, desc="""
    &eMedium Voltage&r uses &eElectrum&r wire (gold + silver). It carries more power
    than copper. Connectors and wire must match: MV wire only goes on MV connectors.""",
  rewards=[give("immersiveengineering:ingot_electrum", 8)])

q("transformer", "Transformers", deps="mv_wire", icon="immersiveengineering:transformer",
  tasks=item("immersiveengineering:transformer"), desc="""
    A &eTransformer&r links two voltages: LV on one side, MV on the other.
    That's how you step power up for a long run and back down at the other end.

    The &eHV Transformer&r does the same between MV and HV.""",
  rewards=[give("immersiveengineering:connector_lv", 4)])

q("hv_wire", "HV: The Long-Distance Grid", deps="transformer", icon="immersiveengineering:wirecoil_steel",
  tasks=[item("immersiveengineering:wirecoil_steel", 4), item("immersiveengineering:connector_hv", 4),
         item("immersiveengineering:transformer_hv")], tier=3, desc="""
    &eHigh Voltage&r steel lines are Strata's long-distance power. They carry the most
    power and reach the farthest between poles.

    &6Plan a grid:&r HV between buildings and outposts, a substation (HV Transformer, then
    a Transformer) at each end, and LV or Mekanism cables inside.
    Wireless power (Flux Networks) costs a lot, so a real power line is the cheap way to move energy.""",
  rewards=[give("immersiveengineering:ingot_steel", 16)])

# --- machines ---------------------------------------------------------------------------
q("crusher", "Crusher", deps="components", icon="immersiveengineering:crusher", tier=3,
  tasks=[item("immersiveengineering:steel_scaffolding_standard", 10),
         item("immersiveengineering:light_engineering", 10)], desc="""
    The &eCrusher&r is a big multiblock that grinds ore into grit: about two dusts per
    ore, which you smelt into ingots. It also crushes cobble, bones and more.

    Build it from Steel Scaffolding, Light Engineering Blocks and a few other parts
    (check the manual), then form it with the hammer and power it.""",
  rewards=[give("immersiveengineering:component_iron", 8)])

q("metal_press", "Metal Press", deps="crusher", icon="immersiveengineering:metal_press",
  tasks=item("immersiveengineering:mold_plate"), desc="""
    The &eMetal Press&r stamps ingots with &emolds&r: plates, gears, rods and wire.
    Way faster than hammering plates by hand.

    Make the &ePlate Mold&r on the Workbench (Molds blueprint) to get started.""",
  rewards=[give("minecraft:iron_ingot", 16)])

q("core_sample", "Finding Mineral Veins", deps="crusher", icon="immersiveengineering:coresample",
  tasks=item("immersiveengineering:coresample"), desc="""
    Huge &emineral veins&r hide deep under the ground in each chunk area.

    Place a &eCore Sample Drill&r and give it power: it drills down and hands you a
    &eCore Sample&r that tells you what's under that spot. The Mineral Survey Tools
    give a rough hint while you're out exploring.""",
  rewards=[give("immersiveengineering:component_steel", 4)])

q("excavator", "The Excavator", deps="core_sample", icon="immersiveengineering:excavator", tier=4,
  tasks=[item("immersiveengineering:heavy_engineering", 4), item("immersiveengineering:sheetmetal_steel", 16)], desc="""
    The &eExcavator&r is IE's biggest machine: a giant bucket wheel that digs ore
    straight out of a mineral vein for a very long time.

    Build it (plus its bucket wheel) on a good vein you found with core samples. It needs a lot of
    power, so it's a great reason to run an HV line out to it.""",
  rewards=[give("immersiveengineering:ingot_steel", 32)])

q("where_next", "Where next?", deps=["hv_wire", "metal_press"], icon="minecraft:oak_sign", desc="""
    You've got steel, machines and a power grid. Some ideas:

    &bMekanism&r: turn one ore into up to five ingots.
    &bApplied Energistics 2&r: a digital storage system for all that loot.
    &bCreate&r: the Crusher pairs nicely with Create's own ore processing.""")
