from dsl import *

C = chapter("occultism", "Occultism", group="magic", icon="occultism:pentacle_summon",
            subtitle="Chalk circles, rituals and spirits that work for you")
q = C.quest

q("intro", "What is Occultism?", icon="occultism:book_of_binding_bound_foliot", size=1.5, shape="gear", desc="""
    Hidden behind our world is the &5Otherworld&r, full of spirits.
    &dOccultism&r teaches you to see it, draw &echalk circles&r (pentacles), and summon spirits
    with &erituals&r. Bound spirits &ework for you&r: crushing ores into extra dust,
    chopping trees, moving items, mining in their own dimension, or running a huge magic storage.

    Spirits come in four strengths: &aFoliot&r, &eDjinni&r, &6Afrit&r and &cMarid&r.""")

q("dream", "Demon's Dream", deps="intro", icon="occultism:datura",
  tasks=[item("occultism:datura_seeds"), item("occultism:datura")], desc="""
    Break grass to find &eDemon's Dream seeds&r and grow them. Eating the fruit can give you
    the &5Third Eye&r: you see Otherworld blocks hiding in plain sight, and you can harvest them
    while the effect lasts.

    Several fruit or seeds can be pressed into an essence that always works (with side effects).""",
  rewards=[give("minecraft:bone_meal", 16)])

q("dictionary", "Dictionary of Spirits", deps="dream", icon="occultism:dictionary_of_spirits",
  tasks=item("occultism:dictionary_of_spirits"), desc="""
    A book and a Demon's Dream seed make the &eDictionary of Spirits&r, Occultism's guide.
    Every ritual page shows its ingredients and a blue link that previews its pentacle in the world.
    You'll also use the Dictionary to write spirit names into Books of Binding (it isn't used up).""",
  rewards=[give("minecraft:book", 2)])

q("spirit_fire", "Spiritfire", deps="dream", icon="occultism:otherstone",
  tasks=item("occultism:otherstone", 16, title="Make Otherstone in Spiritfire"), desc="""
    Throw a &eDemon's Dream&r fruit on the ground and light it with flint and steel:
    &bSpiritfire&r! It doesn't hurt you, but items thrown in change:

    &eAndesite&r becomes &eOtherstone&r, &ediamonds&r become &eSpirit Attuned Gems&r,
    a &ebook&r becomes a Taboo Book, &ea feather&r an Awakened Feather, &eblack dye&r Purified Ink,
    and impure chalk becomes real chalk.""",
  rewards=[give("minecraft:andesite", 32), give("minecraft:flint_and_steel")])

q("gem", "Spirit Attuned Gem", deps="spirit_fire", icon="occultism:spirit_attuned_gem",
  tasks=item("occultism:spirit_attuned_gem"), desc="""
    A diamond burned in Spiritfire. It goes into the &eDivination Rod&r, Infused Lenses and
    the Infused Pickaxe.

    &eDivination Rod&r: sneak-click a block to tune it (oak wood finds Otherworld trees,
    netherrack finds Iesnium), then hold right-click to search.""",
  rewards=[give("minecraft:gold_ingot", 4), give("minecraft:glass", 8)])

q("chalk", "White Chalk", deps="spirit_fire", icon="occultism:chalk_white",
  tasks=item("occultism:chalk_white", 2), desc="""
    Craft &eimpure white chalk&r from Otherstone dust and Otherworld wood dust,
    then purify it in Spiritfire.

    Right-click blocks with chalk to draw. Only the &ecolor and position&r of the marks matter,
    not the little symbols. A &eChalk Brush&r cleans them up.""",
  rewards=[give("minecraft:white_dye", 8)])

q("bowls", "Ritual Bowls", deps="chalk", icon="occultism:golden_sacrificial_bowl",
  tasks=[item("occultism:golden_sacrificial_bowl"), item("occultism:sacrificial_bowl", 4)], desc="""
    &eSacrificial Bowls&r (Otherstone) hold the ritual ingredients. They can go &eanywhere&r
    within 8 blocks of the center.

    The &eGolden Ritual Bowl&r sits in the middle of the pentacle. You start a ritual by
    right-clicking it with the activation item, usually a bound Book of Binding.""",
  rewards=[give("minecraft:gold_ingot", 8), give("minecraft:candle", 8)])

q("binding", "Books of Binding", deps=["bowls", "dictionary"], icon="occultism:book_of_binding_bound_foliot",
  tasks=item("occultism:book_of_binding_bound_foliot"), tier=2, desc="""
    A &eBook of Binding: Foliot&r is a Taboo Book, Purified Ink, an Awakened Feather and blue dye.
    Craft it with your Dictionary of Spirits to write a spirit's name in: now it's &ebound&r
    and ready to summon a Foliot.""",
  rewards=[give("minecraft:feather", 8), give("minecraft:black_dye", 8)])

q("first_ritual", "Your First Ritual: Foliot Crusher", deps="binding", icon="occultism:iron_dust",
  tasks=item("occultism:iron_dust", 2, title="Crush ore into Iron Dust"), tier=2, desc="""
    Draw &eAviar's Circle&r (the Foliot pentacle) in white chalk around the golden bowl,
    put an iron, gold, copper and silver ingot in the bowls, and right-click the golden bowl
    with your bound Foliot book.

    A &aFoliot Crusher&r appears. Drop ores near it: it crushes &eone ore into two dusts&r.
    Pair it with a Transporter and a Janitor spirit to automate it.""",
  rewards=[give("minecraft:raw_iron", 16), give("minecraft:raw_copper", 16)])

q("workers", "More Foliot Helpers", deps="first_ritual", icon="occultism:book_of_calling_foliot_lumberjack",
  optional=True, desc="""
    Other Foliot rituals call a &eLumberjack&r, a &eFarmer&r, a &eTransporter&r (moves items between
    chests) and a &eJanitor&r (picks up items). They come with a &eBook of Calling&r: right-click air to
    set it up, sneak-click a block to give the spirit its work area or drop-off chest.

    Spirits slowly &edecay&r and go home over time. Store one in a Magic Lamp or Book of Calling,
    or (with Ars Ocultas) in a Containment Jar where it never decays.""",
  rewards=[give("minecraft:chest", 4)])

q("goggles", "Otherworld Goggles", deps="first_ritual", icon="occultism:otherworld_goggles",
  tasks=item("occultism:otherworld_goggles"), tier=3, desc="""
    A Foliot bound into &eInfused Lenses&r lends you its sight. The &eOtherworld Goggles&r give a
    permanent Third Eye and show even more hidden blocks (no more nauseous fruit!).

    They let you &esee&r, not harvest: for that you need an Infused or Iesnium Pickaxe.""",
  rewards=[give("minecraft:leather", 8), give("minecraft:diamond", 2)])

q("djinni", "Calling a Djinni", deps="first_ritual", icon="occultism:book_of_binding_bound_djinni",
  tasks=item("occultism:book_of_binding_bound_djinni"), tier=3, desc="""
    &eDjinn&r are stronger spirits. Their rituals need new pentacles and colored chalk
    (look up each ritual in the Dictionary). A Djinni Crusher turns one ore into three dusts,
    and Djinn make soul gems, the Infused Pickaxe and the storage system's heart.""",
  rewards=[give("minecraft:purple_dye", 8), give("minecraft:quartz", 16)])

q("familiars", "Familiars", deps="djinni", icon="occultism:familiar_ring",
  tasks=item("occultism:familiar_ring"), tier=3, desc="""
    &eFamiliar rituals&r summon spirits in animal bodies that follow you and give buffs:
    the &eGreedy&r familiar picks up items, the &eBat&r gives night vision, and many more
    (see the Familiar Rituals category).

    Catch a familiar in a &eFamiliar Ring&r (a soul gem with a Djinni, made by ritual) and wear it
    as a curio to keep its buff. Ars Ocultas also lets Occultism's dragon be an Ars familiar.""",
  rewards=[give("minecraft:gold_ingot", 4)])

q("storage", "Dimensional Storage", deps="djinni", icon="occultism:storage_controller",
  tasks=item("occultism:storage_controller"), tier=3, desc="""
    Spirits can hold a whole &estorage dimension&r. The &eDimensional Storage Actuator&r is a
    &eDimensional Matrix&r (a Djinni ritual) on top of a &eStorage Actuator Base&r (a Foliot ritual).

    Right-click it to open one huge sorted inventory: 128 item types and 256,000 items to start.
    Storage Stabilizers placed around it add more. Breaking it keeps everything inside the item.""",
  rewards=[give("minecraft:quartz_block", 6), give("minecraft:ender_pearl", 2)])

q("iesnium", "Iesnium", deps=["goggles", "welcome/nether"], icon="occultism:iesnium_ingot",
  tasks=item("occultism:iesnium_ingot", 4), tier=3, desc="""
    A rare Otherworld metal that looks like netherrack. Wear your goggles in the &cNether&r,
    tune a Divination Rod to netherrack to find it, and mine it with an Infused Pickaxe.
    Raw Iesnium smelts into ingots.

    Iesnium makes a tough pickaxe, magic lamps for &espirit miners&r, and more.""",
  rewards=[give("minecraft:coal_block", 4)])

q("miners", "Spirit Miners", deps="iesnium", icon="occultism:miner_foliot_unspecialized",
  tasks=[item("occultism:dimensional_mineshaft"), item("occultism:miner_foliot_unspecialized")], tier=4,
  desc="""
    The &eDimensional Mineshaft&r is a portal for spirits only, into a mining dimension.
    Put a spirit in a &eMagic Lamp&r into it and it mines ores for you, lag free.
    The &aMiner Foliot&r is the first (it needs an Iesnium Pickaxe); Djinni, Afrit and Marid miners
    dig better ores.""",
  rewards=[give("minecraft:iron_block", 4)])

q("afrit", "Afrit Essence", deps="djinni", icon="occultism:afrit_essence",
  tasks=item("occultism:afrit_essence"), tier=4, shape="diamond", desc="""
    To control the stronger spirits you need &cred chalk&r, made with &6Afrit Essence&r.
    You get it by summoning an &cunbound&r Afrit and defeating it. Unbound spirits are dangerous:
    gear up, and keep the ritual far from your base.

    Afrit crushers turn one ore into four dusts.""",
  rewards=[give("minecraft:golden_apple", 2), give("minecraft:fire_charge", 8)])

q("marid", "Marid Essence", deps="afrit", icon="occultism:marid_essence",
  tasks=item("occultism:marid_essence"), tier=5, size=1.5, shape="hexagon", desc="""
    The most powerful spirits need &bblue chalk&r from &cMarid Essence&r. Like the Afrit,
    you summon a Marid unbound and defeat it. Bring friends.

    Marid crushers turn one ore into six dusts, and Marid miners are the best spirit miners.""",
  rewards=[give("minecraft:diamond_block", 1)])

q("ocultas", "Ars Ocultas", deps="workers", icon="ars_ocultas:altar", optional=True, desc="""
    &dArs Ocultas&r links Occultism to Ars Nouveau: spirits work inside Ars &eContainment Jars&r
    without decaying (a jarred Crusher picks up ores within a 7x7 area and crushes them),
    and the Imbuement Chamber can turn silver into gold and back. See the Ars Nouveau chapter.""")

q("where_next", "Where Next?", deps="djinni", icon="minecraft:oak_sign", desc="""
    &dArs Nouveau&r: spirits in jars, plus spells. &dTheurgy&r: by the same author, alchemy that
    turns one ore into several ingots (its divination rods find ores).
    &dNeo Vitae&r: blood magic with its own rituals.""")
