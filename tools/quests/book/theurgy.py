from dsl import *

C = chapter("theurgy", "Theurgy", group="magic", icon="theurgy:liquefaction_cauldron",
            subtitle="Alchemy: find ores, triple them, turn one thing into another")
q = C.quest

q("intro", "What is Theurgy?", icon="theurgy:mercury_shard", size=1.5, shape="gear", desc="""
    &6Theurgy&r is classic &ealchemy&r. Every item is made of three principles:
    &eSulfur&r (what it is), &eSalt&r (its body) and &eMercury&r (its energy).

    Split an ore into its principles and put them back together, and you get &aseveral ingots
    from one raw ore&r. Later you can even turn one material into another.
    It all runs on simple fuel like coal: no power grid needed.""")

q("hermetica", "The Hermetica", deps="intro", icon="theurgy:the_hermetica_icon", desc="""
    Craft a book with 2 sand to get &eThe Hermetica&r, Theurgy's guide. It walks you through
    every machine step by step, with pictures. Keep it handy: alchemy has a few steps.""",
  rewards=[give("minecraft:book", 2), give("minecraft:sand", 16)])

q("rod", "Divination Rods", deps="intro", icon="theurgy:divination_rod_t1",
  tasks=item("theurgy:divination_rod_t1"), desc="""
    A &eGlass Divination Rod&r (glass and sticks) finds blocks for you.
    &eSneak-click&r a block (say, iron ore) to tune it, then &ehold right-click&r to search:
    it turns purple when it finds one and sends a glowing ball toward it.

    Iron, diamond and netherite rods are upgrades. Rods pre-tuned with an ore's Sulfur
    (Abundant, Common, Rare, Precious) last much longer.""",
  rewards=[give("minecraft:glass", 16), give("minecraft:stick", 16)])

q("brazier", "Pyromantic Brazier", deps="hermetica", icon="theurgy:pyromantic_brazier",
  tasks=item("theurgy:pyromantic_brazier", 4), desc="""
    Every heated alchemy machine sits on a &ePyromantic Brazier&r. Put fuel like coal in it.
    You'll want 4 to start: one each for the Calcination Oven, Distiller, Liquefaction Cauldron
    and Incubator.""",
  rewards=[give("minecraft:coal", 32), give("minecraft:charcoal", 16)])

q("salt", "Salt: Calcination", deps="brazier", icon="theurgy:calcination_oven",
  tasks=[item("theurgy:calcination_oven"), item("theurgy:alchemical_salt_mineral")], tier=2, desc="""
    Right-click the &eCalcination Oven&r with minerals (ores, raw metal, ingots, or renewable
    &echarcoal&r), heat the brazier below, and collect &eMineral Salt&r.""",
  rewards=[give("minecraft:charcoal", 32)])

q("mercury", "Mercury: Distillation", deps="brazier", icon="theurgy:distiller",
  tasks=[item("theurgy:distiller"), item("theurgy:mercury_shard", 4)], tier=2, desc="""
    The &eMercury Distiller&r pulls &eMercury Shards&r out of almost anything: crops, food,
    ores, stone, sand. Cheap items need a bunch for one shard; valuable ones give more.""",
  rewards=[give("minecraft:wheat", 32)])

q("solvent", "Sal Ammoniac", deps="brazier", icon="theurgy:sal_ammoniac_accumulator",
  tasks=[item("theurgy:sal_ammoniac_accumulator"), item("theurgy:sal_ammoniac_tank"),
         item("theurgy:sal_ammoniac_bucket")], tier=2, desc="""
    The solvent for liquefaction. Put the &eAccumulator&r on top of the &eTank&r and fill it
    with water buckets (up to 10). Slowly the tank fills with &eSal Ammoniac&r; take it out with
    a bucket.

    A &eSal Ammoniac Crystal&r (mined from its ore) dropped into the accumulator speeds it up a lot.""",
  rewards=[give("minecraft:water_bucket"), give("minecraft:bucket", 2)])

q("sulfur", "Sulfur: Liquefaction", deps="solvent", icon="theurgy:liquefaction_cauldron",
  tasks=[item("theurgy:liquefaction_cauldron"), item("theurgy:alchemical_sulfur_iron", 3)], tier=2, desc="""
    Fill the &eLiquefaction Cauldron&r with a Sal Ammoniac bucket, put in a &eraw iron&r, heat it:
    out comes &eIron Sulfur&r, several from one raw ore. This is where the multiplying happens.""",
  rewards=[give("minecraft:raw_iron", 8)])

q("incubator", "Incubation: More Ingots from Ore", deps=["sulfur", "salt", "mercury"], icon="theurgy:incubator",
  tasks=[item("theurgy:incubator"), item("theurgy:incubator_salt_vessel"),
         item("theurgy:incubator_mercury_vessel"), item("theurgy:incubator_sulfur_vessel")],
  tier=3, desc="""
    The &eIncubator&r puts the three principles back together. Fill its &eSulfur&r, &eSalt&r and
    &eMercury&r vessels, heat it, and collect &a2 iron ingots&r for every raw iron you liquefied
    (&a3&r if you liquefy the ore block itself: mine it with Silk Touch).

    It works for most ores and raw metals. Look up any Sulfur with &eU&r to see what it makes.""",
  rewards=[give("minecraft:iron_block", 2)])

q("reformation", "Reformation", deps="incubator", icon="theurgy:reformation_target_pedestal",
  tasks=[item("theurgy:reformation_source_pedestal"), item("theurgy:reformation_target_pedestal"),
         item("theurgy:reformation_result_pedestal")], tier=3, desc="""
    The &eReformation Array&r changes one Sulfur into another of the &esame type and tier&r
    (lapis into quartz, diamond into emerald...), using Sulfuric Flux. Then incubate the new Sulfur
    as usual. The Hermetica shows how to build and power the array.""",
  rewards=[give("minecraft:lapis_lazuli", 16), give("minecraft:quartz", 16)])

q("transmutation", "Transmutation", deps="reformation", icon="theurgy:fermentation_vat",
  tasks=item("theurgy:fermentation_vat"), tier=4, desc="""
    To change a material's &etype&r (gem into metal), first ferment its Sulfur into &eNiter&r in the
    &eFermentation Vat&r (with water and sugar or crops). Niter is a "concept" like "common metal",
    and it can be reformed into a different type. Roughly 2 metals make 1 gem and back.""",
  rewards=[give("minecraft:sugar", 32)])

q("exaltation", "Exaltation", deps="transmutation", icon="theurgy:digestion_vat",
  tasks=[item("theurgy:digestion_vat"), item("theurgy:purified_gold")], tier=5, desc="""
    The last secret: raising a material's &etier&r, like turning iron into gold.
    The &eDigestion Vat&r turns 4 Niter of a lower tier into 1 of the next, with &ePurified Gold&r
    as a catalyst (purify gold in the Digestion Vat with salt and water first). Costly, but you can
    make almost anything.""",
  rewards=[give("minecraft:gold_block", 2)])

q("logistics", "Mercurial Logistics", deps="incubator", icon="theurgy:copper_wire", optional=True,
  tasks=item("theurgy:logistics_item_extractor"), desc="""
    Theurgy can move items and fluids along &eMercurial Copper Wires&r: extractors pull from a
    container, inserters push in, and wires (with connection nodes for long runs) link them.
    Filters and frequencies split one wire network into several. Handy for automating your alchemy.""",
  rewards=[give("minecraft:copper_ingot", 16)])

q("where_next", "Where Next?", deps="incubator", icon="minecraft:oak_sign", desc="""
    &dOccultism&r (same author): spirits that crush ores too, and a Divination Rod for Otherworld blocks.
    &dArs Nouveau&r: magic that runs on Source. Or feed your extra ingots into the &bTech&r chapters!""")
