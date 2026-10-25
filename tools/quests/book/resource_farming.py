from dsl import *

C = chapter("resource_farming", "Resource Farming", group="tech",
            icon="mysticalagriculture:inferium_essence",
            subtitle="Grow your ores, keep bees that make metal, and farm mobs")
q = C.quest

q("intro", "What is Resource Farming?", icon="mysticalagriculture:iron_seeds", deps="welcome/iron_age",
  size=1.5, shape="gear", desc="""
    Mining gets old. These mods let you &egrow&r your resources instead:

    &bMystical Agriculture&r: crops that drop essence for iron, diamonds and more.
    &bProductive Bees&r: bees whose combs spin into metals and gems.
    &bMob Grinding Utils&r: efficient mob farms that also collect the XP.""")

# --- Mystical Agriculture ---------------------------------------------------------------
q("ma_inferium", "MA: Inferium", deps="intro", icon="mysticalagriculture:inferium_essence",
  tasks=item("mysticalagriculture:inferium_essence", 32), desc="""
    Mine &eInferium Ore&r underground for &eInferium Essence&r, the base of everything in
    Mystical Agriculture. You'll also find &eProsperity Ore&r, which drops
    &eProsperity Shards&r.""",
  rewards=[give("minecraft:bone_meal", 32)])

q("ma_seeds", "MA: Inferium Seeds", deps="ma_inferium", icon="mysticalagriculture:inferium_seeds",
  tasks=item("mysticalagriculture:inferium_seeds", 2), desc="""
    Surround a wheat seed with 8 Inferium Essence to get &eInferium Seeds&r.
    Plant them on farmland: they grow more essence.

    &eInferium Farmland&r (farmland + essence) makes the crops drop a bit more.""",
  rewards=[give("mysticalagriculture:inferium_essence", 16)])

q("ma_tiers", "MA: Essence Tiers", deps="ma_seeds", icon="mysticalagriculture:prudentium_essence", tier=2,
  tasks=[item("mysticalagriculture:infusion_crystal"), item("mysticalagriculture:prudentium_essence", 8)],
  desc="""
    Essence comes in five tiers: &aInferium&r, &ePrudentium&r, &6Tertium&r, &bImperium&r and
    &5Supremium&r. Four of one tier around an &eInfusion Crystal&r makes one of the next.

    Better resources need higher-tier essence for their seeds.""",
  rewards=[give("mysticalagriculture:prosperity_shard", 8)])

q("ma_altar", "MA: Infusion Altar", deps="ma_tiers", icon="mysticalagriculture:infusion_altar", tier=2,
  tasks=[item("mysticalagriculture:infusion_altar"), item("mysticalagriculture:infusion_pedestal", 8)], desc="""
    Resource seeds are made on the &eInfusion Altar&r with 8 &ePedestals&r around it.
    Put the seed base on the altar, the ingredients on the pedestals and right-click
    the altar with a &eWand&r.

    &eProsperity Seed Base&r (prosperity shards around a wheat seed) starts most seeds.""",
  rewards=[give("mysticalagriculture:prosperity_shard", 16)])

q("ma_iron", "MA: Iron Seeds", deps="ma_altar", icon="mysticalagriculture:iron_seeds", tier=3,
  tasks=item("mysticalagriculture:iron_seeds"), desc="""
    Your first real resource crop! Iron Seeds grow &eIron Essence&r; 8 essence in a
    ring in the crafting grid makes 6 iron ingots.

    Press &eU&r on any essence to see what it crafts into.""",
  rewards=[give("minecraft:iron_ingot", 16)])

q("ma_growth", "MA: Growing Faster", deps="ma_iron", icon="mysticalagriculture:inferium_growth_accelerator",
  tasks=item("mysticalagriculture:inferium_growth_accelerator"), desc="""
    &eGrowth Accelerators&r placed under your farmland speed up the crops above.
    Stack several in a column for more effect. The &eHarvester&r machine picks
    everything for you.""",
  rewards=[give("mysticalagriculture:inferium_essence", 32)])

q("ma_diamond", "MA: Diamond Seeds", deps="ma_iron", icon="mysticalagriculture:diamond_seeds", tier=4,
  tasks=item("mysticalagriculture:diamond_seeds"), desc="""
    Diamonds that grow on plants. Diamond seeds need high-tier essence, so build up
    your essence farms first.""")

q("ma_awakened", "MA: Awakened Supremium", deps="ma_diamond", icon="mysticalagriculture:awakened_supremium_essence",
  tier=5, tasks=[item("mysticalagriculture:awakening_altar"), item("mysticalagriculture:awakened_supremium_essence")],
  desc="""
    The very top of Mystical Agriculture. The &eAwakening Altar&r (with its pedestals and
    elemental essences) turns a block of Supremium into &5Awakened Supremium&r, for the
    best tools, armour and growth accelerators.""")

# --- Productive Bees --------------------------------------------------------------------
q("pb_cage", "PB: Catching Bees", deps="intro", icon="productivebees:bee_cage",
  tasks=item("productivebees:bee_cage", 4), desc="""
    &bProductive Bees&r has dozens of bee types. Catch any bee by right-clicking it with
    a &eBee Cage&r. Bees live in nests all over the world: in trees, sand, stone,
    the Nether and the End.""",
  rewards=[give("minecraft:honeycomb", 8)])

q("pb_hive", "PB: Advanced Beehive", deps="pb_cage", icon="productivebees:advanced_oak_beehive", tier=2,
  tasks=item("productivebees:advanced_oak_beehive"), desc="""
    An &eAdvanced Beehive&r houses your bees and collects their combs in its inventory.
    Put filled bee cages in it to move bees in, and empty cages to take them out.

    Bees need flowers nearby (or their own favourite blocks) to work.""",
  rewards=[give("minecraft:poppy", 8), give("minecraft:dandelion", 8)])

q("pb_centrifuge", "PB: Centrifuge", deps="pb_hive", icon="productivebees:centrifuge", tier=2,
  tasks=item("productivebees:centrifuge"), desc="""
    Combs aren't useful on their own. Spin them in a &eCentrifuge&r for wax, honey and
    whatever the bee makes: iron, gold, redstone, even diamonds.

    The &ePowered Centrifuge&r runs faster on power.""",
  rewards=[give("minecraft:glass_bottle", 16)])

q("pb_resource", "PB: Resource Bees", deps="pb_centrifuge", icon="productivebees:configurable_honeycomb",
  tier=3, tasks=item("productivebees:configurable_honeycomb", 16), desc="""
    &eResource bees&r make combs of metals and gems. Get them by finding the right nest,
    by &ebreeding&r two bees (Breeding Chamber, or with flowers in the world), or by
    feeding a bee certain items to change its type.

    Press &eR&r on a bee's spawn egg or comb in EMI to see how to get it.""")

q("pb_breeding", "PB: Breeding", deps="pb_resource", icon="productivebees:breeding_chamber", tier=3,
  tasks=item("productivebees:breeding_chamber"), desc="""
    The &eBreeding Chamber&r breeds two caged bees into a new type automatically.
    &eHoney Treats&r are used for bee breeding and genetics.""")

# --- Mob Grinding Utils -----------------------------------------------------------------
q("mgu_fan", "MGU: Moving Mobs", deps="intro", icon="mob_grinding_utils:fan",
  tasks=[item("mob_grinding_utils:fan"), item("mob_grinding_utils:spikes", 4)], desc="""
    &bMob Grinding Utils&r gives you parts for mob farms.
    The &eMob Fan&r blows mobs along. &eIron Spikes&r hurt mobs standing on them.

    Pair it with a dark room or a spawner to farm drops.""",
  rewards=[give("minecraft:iron_ingot", 8)])

q("mgu_masher", "MGU: Mob Masher", deps="mgu_fan", icon="mob_grinding_utils:saw", tier=2,
  tasks=[item("mob_grinding_utils:saw"), item("mob_grinding_utils:absorption_hopper")], desc="""
    The &eMob Masher&r kills mobs that get pushed into it. Upgrades add Looting, Sharpness
    and more.

    The &eAbsorption Hopper&r picks up the drops &eand the XP&r in an area, and stores
    the XP as a fluid.""")

q("mgu_xp", "MGU: Bottled XP", deps="mgu_masher", icon="mob_grinding_utils:xpsolidifier", tier=2,
  tasks=[item("mob_grinding_utils:tank"), item("mob_grinding_utils:xpsolidifier")], desc="""
    Store liquid XP in a &eSingularity Tank&r. The &eXP Solidifier&r turns it into
    &eXP Jelly Babies&r you can eat later, which is handy for waystone trips and enchanting.""",
  rewards=[give("minecraft:experience_bottle", 16)])

q("where_next", "Where next?", deps=["ma_iron", "pb_centrifuge", "mgu_masher"], any_dep=True,
  icon="minecraft:oak_sign", desc="""
    &bApplied Energistics 2&r: autocraft essence into ingots.
    &bMekanism&r: process extra ores you grew.
    &bEndgame&r: Extended Crafting eats lots of resources.""")
