from dsl import *

C = chapter("endgame", "Endgame", group="tech", icon="draconicevolution:chaotic_core",
            subtitle="Draconic Evolution and Extended Crafting: the biggest projects in Strata")
q = C.quest

q("intro", "The Long Road", icon="draconicevolution:draconium_ingot", deps="welcome/iron_age",
  size=1.5, shape="gear", desc="""
    This chapter is the far horizon. Nobody finishes it in a week, and that's the point.

    &bDraconic Evolution&r: draconium, fusion crafting, a giant energy core and the
    strongest gear in the pack.
    &bExtended Crafting&r: bigger and bigger crafting tables for huge recipes.

    The top tiers need the &5Ender Dragon&r and &cCataclysm&r bosses beaten first.""")

# --- Draconic Evolution -----------------------------------------------------------------
q("draconium", "Draconium", deps="intro", icon="draconicevolution:draconium_ingot",
  tasks=item("draconicevolution:draconium_ingot", 16), desc="""
    &eDraconium Ore&r is rare and deep. It shows up in the Overworld, the Nether and
    the End (the End has the most). Smelt the dust or ore into ingots.

    The &eInformation Tablet&r is Draconic Evolution's guide.""",
  rewards=[give("minecraft:diamond", 4)])

q("draconium_core", "Draconium Core", deps="draconium", icon="draconicevolution:draconium_core", tier=2,
  tasks=item("draconicevolution:draconium_core", 4), desc="""
    The &eDraconium Core&r (draconium, gold and a diamond) is the basic building block
    of almost every Draconic machine. Make a handful.""",
  rewards=[give("minecraft:gold_ingot", 16)])

q("generator", "DE Generator", deps="draconium_core", icon="draconicevolution:generator",
  tasks=item("draconicevolution:generator"), desc="""
    Draconic machines are hungry. The &eGenerator&r burns fuel for power, but you'll
    want a real power plant (Mekanism, Oritech, Extreme Reactors) behind this chapter.""",
  rewards=[give("minecraft:coal_block", 8)])

q("fusion", "Fusion Crafting", deps="draconium_core", icon="draconicevolution:crafting_core", tier=3,
  tasks=[item("draconicevolution:crafting_core"), item("draconicevolution:basic_crafting_injector", 4)],
  desc="""
    &eFusion Crafting&r: a &eFusion Crafting Core&r in the middle with &eInjectors&r
    facing it. Put the main item in the core and the ingredients in the injectors,
    give the injectors power, and watch it fuse.

    Better injectors (Wyvern, Draconic, Chaotic) unlock bigger recipes.""")

q("wyvern_core", "Wyvern Core", deps="fusion", icon="draconicevolution:wyvern_core", tier=3,
  tasks=item("draconicevolution:wyvern_core"), desc="""
    The first big upgrade: a &eWyvern Core&r needs Draconium Cores and a
    &eNether Star&r, so you'll be fighting the Wither for this one.""")

q("energy_core", "Energy Core", deps="wyvern_core", icon="draconicevolution:energy_core", tier=4,
  tasks=[item("draconicevolution:energy_core"), item("draconicevolution:energy_core_stabilizer", 4),
         item("draconicevolution:energy_pylon")], desc="""
    The &eEnergy Core&r is a giant power bank built in tiers. It needs &eStabilizers&r
    around it and &ePylons&r to move energy in and out, plus a shell of blocks
    (Redstone, then Draconium) that grows with each tier.

    Fill it with your whole power plant's output.""")

q("wyvern_gear", "Wyvern Gear", deps="wyvern_core", icon="draconicevolution:wyvern_pickaxe", tier=4,
  tasks=item("draconicevolution:wyvern_pickaxe"), desc="""
    &eWyvern&r tools and armour run on power and take &emodules&r you slot in:
    more energy, speed, area mining, shields and more.

    Every module needs power, so charge your gear often.""")

q("awakened", "Awakened Draconium", deps=["wyvern_core", "the_end/dragon"],
  icon="draconicevolution:awakened_draconium_ingot", tier=4,
  tasks=item("draconicevolution:awakened_draconium_ingot", 4), desc="""
    Killing the &5Ender Dragon&r drops a &eDragon Heart&r. Fuse it with Draconium blocks
    and cores to get &eAwakened Draconium&r.

    It's the key to the Draconic tier.""")

q("draconic_core", "Draconic Core", deps="awakened", icon="draconicevolution:awakened_core", tier=5,
  tasks=item("draconicevolution:awakened_core"), desc="""
    Wyvern Cores, Awakened Draconium and a Nether Star fused into a &eDraconic Core&r.
    The heart of the Draconic tier.""")

q("draconic_gear", "Draconic Armour", deps=["draconic_core", "cataclysm/ignis"],
  icon="draconicevolution:draconic_chestpiece", tier=5, tasks=item("draconicevolution:draconic_chestpiece"),
  desc="""
    The &5Draconic&r chestpiece: huge shields, netherite inside, room for lots of modules.
    In Strata it comes after beating &cIgnis&r too.

    &6Flight:&r its flight module runs on the armour's &epower&r. It's an endgame
    reward, and you'll need a big energy core to keep it charged.""")

q("chaos", "Chaos Shards", deps=["draconic_core", "cataclysm/ender_guardian"], icon="draconicevolution:chaos_shard",
  tier=5, tasks=item("draconicevolution:chaos_shard"), desc="""
    Far out in the End are &eChaos Islands&r, guarded by the &cChaos Guardian&r, a dragon
    far tougher than the first. Its shards are needed for the Chaotic tier and the
    Draconic Reactor.

    Bring your best gear and friends.""")

q("reactor", "Draconic Reactor", deps="chaos", icon="draconicevolution:reactor_core", tier=5,
  size=1.5, shape="diamond", tasks=item("draconicevolution:reactor_core"), desc="""
    The &eDraconic Reactor&r makes more power than anything else in the pack, and it
    can go very, very wrong. Build it far from home, with stabilizers, injectors and a
    lot of care.""")

# --- Extended Crafting ------------------------------------------------------------------
q("ec_black_iron", "EC: Black Iron", deps="intro", icon="extendedcrafting:black_iron_ingot",
  tasks=item("extendedcrafting:black_iron_ingot", 8), desc="""
    &bExtended Crafting&r is built on &eBlack Iron&r: an iron ingot and black dye.
    You'll also need &eBlack Iron Slates&r for every table.""",
  rewards=[give("minecraft:black_dye", 16), give("minecraft:iron_ingot", 16)])

q("ec_basic", "EC: Basic Table", deps="ec_black_iron", icon="extendedcrafting:basic_table", tier=2,
  tasks=item("extendedcrafting:basic_table"), desc="""
    The &eBasic Crafting Table&r only has a 3x3 grid, but you need it to make the
    bigger ones. Each table tier needs its own &ecatalyst&r and &ecomponents&r.""",
  rewards=[give("minecraft:redstone", 32)])

q("ec_advanced", "EC: Advanced Table", deps="ec_basic", icon="extendedcrafting:advanced_table", tier=3,
  tasks=item("extendedcrafting:advanced_table"), desc="""
    &eAdvanced Crafting Table&r: a &e5x5&r grid. Big recipes start here.""",
  rewards=[give("minecraft:gold_block", 2)])

q("ec_elite", "EC: Elite Table", deps="ec_advanced", icon="extendedcrafting:elite_table", tier=4,
  tasks=item("extendedcrafting:elite_table"), desc="""
    &eElite Crafting Table&r: a &e7x7&r grid. &eCrystaltine&r ingots (with a Nether Star)
    are made here.""",
  rewards=[give("minecraft:diamond_block", 2)])

q("ec_crystaltine", "EC: Crystaltine", deps="ec_elite", icon="extendedcrafting:crystaltine_ingot", tier=4,
  tasks=item("extendedcrafting:crystaltine_ingot", 4), desc="""
    &eCrystaltine&r is diamonds, lapis, gold, iron and a Nether Star crafted on the
    Elite table. You'll need it for the Ultimate tier.""")

q("ec_core", "EC: Combination Crafting", deps="ec_elite", icon="extendedcrafting:crafting_core", tier=4,
  tasks=[item("extendedcrafting:crafting_core"), item("extendedcrafting:pedestal", 8)], desc="""
    The &eCrafting Core&r with &ePedestals&r around it combines items using power.
    The &eQuantum Compressor&r squeezes huge piles of one item into a &eSingularity&r.""")

q("ec_ultimate", "EC: Ultimate Table", deps=["ec_crystaltine", "the_end/dragon", "cataclysm/netherite_monstrosity"],
  icon="extendedcrafting:ultimate_table", tier=5, size=1.5, shape="diamond",
  tasks=item("extendedcrafting:ultimate_table"), desc="""
    The &5Ultimate Crafting Table&r: a &e9x9&r grid for Strata's biggest recipes.
    It comes after the &5Ender Dragon&r and the &cNetherite Monstrosity&r.

    If you got here, you've seen most of what Strata has. Well done!""")

q("where_next", "Where next?", deps="intro", icon="minecraft:oak_sign", desc="""
    &cBosses & Combat&r: the Cataclysm bosses guard what this chapter needs.
    &5The End&r: the Dragon, and the Chaos Islands beyond.
    &bMekanism&r and &bOritech&r: the power you'll need.""")
