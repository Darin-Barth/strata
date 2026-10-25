from dsl import *

C = chapter("ars_nouveau", "Ars Nouveau", group="magic", icon="ars_nouveau:novice_spell_book",
            subtitle="Design your own spells, glyph by glyph")
q = C.quest

q("intro", "What is Ars Nouveau?", icon="ars_nouveau:novice_spell_book", size=1.5, shape="gear",
  desc="""
    &dArs Nouveau&r is the heart of magic in Strata. Instead of finding fixed spells,
    you &ebuild your own&r from little pieces called &eglyphs&r: "shoot a bolt that breaks blocks",
    "heal me and make me jump higher", and so on.

    Your power is &bSource&r, a magic liquid you collect in jars and spend in machines,
    and &bmana&r, the blue bar you spend on spells.

    The other magic mods (Iron's Spells, Occultism) plug into Ars, so this is a great place to start.""")

# --- getting started -----------------------------------------------------------------------
q("notebook", "The Tattered Tome", deps="intro", icon="ars_nouveau:worn_notebook",
  tasks=item("ars_nouveau:worn_notebook"), desc="""
    Craft the &eTattered Tome&r (a book and a lapis). It's Ars Nouveau's own guide:
    every block, glyph, ritual and creature has a page with recipes.

    It also has a key of its own ("Open Documentation", in Options > Controls).""",
  rewards=[give("minecraft:lapis_lazuli", 16)])

q("spellbook", "Your First Spell Book", deps="intro", icon="ars_nouveau:novice_spell_book",
  tasks=item("ars_nouveau:novice_spell_book"), desc="""
    The &eNovice Spell Book&r is a book plus an iron pickaxe, axe, shovel and sword.

    Open it (its key is in Options > Controls) to see the spell crafting screen.
    Each spell slot holds one spell; switch slots with the book's next/previous keys
    and cast with right-click.""",
  rewards=[give("minecraft:iron_ingot", 8)])

q("glyphs", "Forms, Effects and Augments", deps="spellbook", icon="ars_nouveau:blank_glyph", desc="""
    Every spell is a list of glyphs:

    &eForm&r (always first, only one): how the spell travels. &aProjectile&r flies, &aTouch&r
    hits what you click, &aSelf&r targets you.
    &eEffects&r: what happens. &aBreak&r, &aHarm&r, &aHeal&r, &aLight&r...
    &eAugments&r: tweak the glyph before them. &aAmplify&r makes it stronger, &aAOE&r wider.

    Try &eTouch + Break&r for a magic pickaxe. Each glyph costs mana; the bottom-left bar shows yours.""",
  rewards=[xp(150)])

q("archwood", "Archwood Trees", deps="intro", icon="ars_nouveau:blue_archwood_log",
  tasks=item("ars_nouveau:archwood_planks", 16), desc="""
    Ars Nouveau's magic trees come in four colors (blue, red, purple, green).
    A few grow almost anywhere, and whole &eArchwood Forests&r are full of them,
    along with glowing lights and magic creatures.

    You'll need lots of Archwood for the Ars machines. Keep a few &5Vexing (purple)&r logs:
    most ritual tablets use one.""",
  rewards=[give("minecraft:bone_meal", 16), give("minecraft:gold_ingot", 4)])

q("berries", "Sourceberries", deps="archwood", icon="ars_nouveau:sourceberry_bush", optional=True,
  tasks=item("ars_nouveau:sourceberry_bush", 4), desc="""
    Sourceberry bushes grow wild in the world. The berries are a snack, and planted bushes
    are worth planting: Starbuncles harvest them for you, and Sourceberry food makes lots of
    Source in a Mycelial Sourcelink.""")

# --- source ----------------------------------------------------------------------------------
q("imbuement", "The Imbuement Chamber", deps="archwood", icon="ars_nouveau:imbuement_chamber",
  tasks=item("ars_nouveau:imbuement_chamber"), tier=2, desc="""
    The &eImbuement Chamber&r soaks items in Source to make new ones.
    With no jars around it slowly gathers Source on its own, so it works from day one.

    Put an &eamethyst shard&r or &elapis&r inside and wait: out comes a &bSource Gem&r.""",
  rewards=[give("minecraft:amethyst_shard", 16)])

q("gems", "Source Gems", deps="imbuement", icon="ars_nouveau:source_gem",
  tasks=item("ars_nouveau:source_gem", 8), desc="""
    Source Gems go into almost every Ars recipe. Keep a chamber running in your base.

    Later, Source Jars nearby (2 blocks away) make the chamber work much faster.""",
  rewards=[give("minecraft:gold_ingot", 8), give("minecraft:lapis_lazuli", 16)])

q("scribe", "The Scribe's Table", deps=["glyphs", "archwood"], icon="ars_nouveau:scribes_table",
  tasks=item("ars_nouveau:scribes_table"), tier=2, desc="""
    New glyphs are made at the &eScribe's Table&r. Use your spell book on it, pick a glyph,
    then throw the items it shows onto the table. It also costs some &aXP&r.

    The table can pull items from chests next to it.""",
  rewards=[give("minecraft:experience_bottle", 16)])

q("learn_glyph", "Learning Glyphs", deps="scribe", icon="ars_nouveau:glyph_light",
  tasks=item("ars_nouveau:glyph_light", title="Scribe the Light glyph"), desc="""
    Scribe the &eLight&r glyph (a lantern and a torch) and use it to learn it.
    Now any spell can place magic lights: &eProjectile + Light&r lights up a cave from afar.

    Every glyph you learn also raises your mana regeneration a little.
    Share your glyphs with friends with an &eAnnotated Codex&r.""",
  rewards=[give("minecraft:lantern", 4), give("minecraft:experience_bottle", 8)])

q("jar", "Source Jars", deps="gems", icon="ars_nouveau:source_jar",
  tasks=item("ars_nouveau:source_jar", 2), desc="""
    &eSource Jars&r store Source. Machines like the Imbuement Chamber and the
    Enchanting Apparatus pull from jars near them, and rituals drink from them too.

    A comparator next to a jar shows how full it is.""",
  rewards=[give("minecraft:glass", 16)])

q("sourcelink", "Making Source", deps="jar", icon="ars_nouveau:volcanic_sourcelink",
  tasks=item("ars_nouveau:volcanic_sourcelink"), desc="""
    &eSourcelinks&r turn things into Source and push it into jars within a few blocks:

    &cVolcanic&r: burns fuel (Archwood logs give extra). It also heats stone into lava!
    &aAgronomic&r: crops and trees growing nearby (not bonemeal).
    &6Mycelial&r: eats food. &dVitalic&r: animals breeding and mobs dying nearby.
    &bAlchemical&r: drinks potions.

    Start with the Volcanic one and a chest of logs.""",
  rewards=[give("minecraft:coal_block", 4), give("minecraft:oak_log", 32)])

q("apparatus", "The Enchanting Apparatus", deps="gems", icon="ars_nouveau:enchanting_apparatus",
  tasks=[item("ars_nouveau:enchanting_apparatus"), item("ars_nouveau:arcane_core"),
         item("ars_nouveau:arcane_pedestal", 4)], tier=2, desc="""
    Ars's big crafting altar. Place the &eArcane Core&r, the &eEnchanting Apparatus&r on top,
    and &eArcane Pedestals&r within 3 blocks. Put the side items on the pedestals,
    then right-click the apparatus with the center item.

    All three need &eSourcestone&r (stone around a Source Gem). Some recipes also use Source
    from jars nearby.""",
  rewards=[give("ars_nouveau:sourcestone", 32), give("minecraft:diamond", 2)])

q("wand", "Dominion Wand", deps="apparatus", icon="ars_nouveau:dominion_wand",
  tasks=item("ars_nouveau:dominion_wand"), desc="""
    The &eDominion Wand&r links things together: Source Relays to jars, and Starbuncles
    to the chests they work with. Click the thing that gives, then the thing that receives.
    Sneak-click a relay to clear its links.""")

q("essences", "Elemental Essences", deps="apparatus", icon="ars_nouveau:fire_essence",
  tasks=item("ars_nouveau:fire_essence"), desc="""
    &eEssences&r are Source Gems imbued with extra items on pedestals next to the
    Imbuement Chamber. &cFire Essence&r: flint and steel, a torch and gunpowder.

    There are seven: Fire, Water, Earth, Air, Abjuration, Conjuration and Manipulation.
    Many higher glyphs and items need them; look them up with &eR&r.""",
  rewards=[give("minecraft:gunpowder", 16), give("minecraft:flint", 8)])

q("rituals", "Rituals", deps="apparatus", icon="ars_nouveau:ritual_brazier",
  tasks=item("ars_nouveau:ritual_brazier"), tier=2, desc="""
    Rituals are big one-time (or long-running) effects. Place a &eRitual Brazier&r,
    use a &eritual tablet&r on it, toss in any extra items to augment it,
    then right-click it with an empty hand to start.

    Rituals that need Source pull it from jars within 6 blocks. A redstone signal stops a running ritual.
    Tablets include growing crops, making it sunrise, digging, and calling a Wilden boss.""",
  rewards=[give("minecraft:gold_ingot", 8)])

q("familiar", "A Familiar Friend", deps="rituals", icon="ars_nouveau:familiar_starbuncle",
  tasks=item("ars_nouveau:familiar_starbuncle", title="Bind a Starbuncle familiar"), desc="""
    Familiars are little companions that follow you and give bonuses.
    Perform the &eRitual of Binding&r next to a Starbuncle to get its bound script, then use it.
    Pick your familiar from the &eFamiliars&r tab of your spell book.

    A Starbuncle familiar gives you &aSpeed&r. Drygmys, Whirlisprigs, Wixies, Bookwyrms and more
    can become familiars too.""",
  rewards=[give("minecraft:golden_carrot", 8)])

q("ocultas", "Ars Ocultas: Spirits in Jars", deps="rituals", icon="ars_nouveau:mob_jar",
  tasks=item("ars_nouveau:mob_jar"), optional=True, desc="""
    A &eContainment Jar&r holds a mob (catch one with the &eRitual of Containment&r).
    Jarred animals keep working: chickens lay eggs, cows give milk.

    With &dArs Ocultas&r, &dOccultism&r spirits work inside jars too and &enever decay&r,
    which makes great automation. It also lets the Imbuement Chamber turn silver into gold and back.
    See the Occultism chapter.""",
  rewards=[give("minecraft:glass_bottle", 8)])

# --- Starbuncles -------------------------------------------------------------------------------
q("starbuncle", "Starbuncles!", deps="wand", icon="ars_nouveau:starbuncle_charm", shape="heart",
  tasks=[item("ars_nouveau:starbuncle_shards", title="Get a Starbuncle Token"),
         item("ars_nouveau:starbuncle_charm")], desc="""
    &dStarbuncles&r are tiny, very cute item movers. Wild ones live in the woods and love
    &6gold nuggets&r. Hold a nugget so it lets you come close, then drop it one: it grabs the
    nugget, vanishes and leaves a &eStarbuncle Token&r.
    Turn the token into a charm in the Enchanting Apparatus with 4 gold ingots.

    Place the charm to summon your Starbuncle. With the Dominion Wand, click a chest then the
    Starbuncle (take from), or the Starbuncle then a chest (put into). It carries items between them,
    picks up drops and harvests Sourceberries. You can dye them!""",
  rewards=[give("minecraft:gold_nugget", 32), give("ars_nouveau:starbuncle_plush")])

q("starbunclemania", "StarbuncleMania", deps="starbuncle", icon="starbunclemania:star_bucket",
  tasks=item("starbunclemania:star_bucket"), optional=True, desc="""
    &dStarbuncleMania&r gives Starbuncles accessories and new jobs:

    &eStarbucket&r: carries fluids between tanks. &eStarbAttery&r: carries power (FE).
    &eStarballoon&r: carries Mekanism gases. &eStarBin&r: deletes junk on the ground.
    Wixies get cooking pots, furnaces and cutting boards; plus lots of hats.

    Put the accessory on the Starbuncle, then link it with the Dominion Wand as usual.""",
  rewards=[give("minecraft:gold_ingot", 8)])

q("creo", "Ars Creo: Starbuncle Power", deps="starbuncle", icon="ars_creo:starbuncle_wheel",
  tasks=item("ars_creo:starbuncle_wheel"), optional=True, desc="""
    &eArs Creo&r connects Ars to &bCreate&r. The &eStarbuncle Wheel&r (a Starbuncle Charm and a
    Create water wheel) makes rotation; a gold block in front of it speeds it up.

    Spell Turrets fire when they ride on a contraption, and Create's Display Link can show
    how much Source is in a jar.""",
  rewards=[give("create:andesite_alloy", 16), give("create:shaft", 8)])

# --- power and add-ons -------------------------------------------------------------------------
q("apprentice", "The Mage's Spell Book", deps=["learn_glyph", "welcome/nether"],
  icon="ars_nouveau:apprentice_spell_book", tasks=item("ars_nouveau:apprentice_spell_book"), tier=3,
  desc="""
    Your novice book only holds &eTier 1&r glyphs. Upgrade it with obsidian, 3 diamonds,
    2 quartz blocks and 2 blaze rods (from the Nether) to unlock &eTier 2&r glyphs.
    All your spells move into the new book.

    Mana-powered movement opens up here: &eLeap&r, &eGlide&r (elytra-style flight for a while)
    and &eBlink&r (Self + Blink hops you forward). Each cast costs mana: earned travel, not free.""",
  rewards=[give("minecraft:blaze_rod", 4), give("minecraft:ender_pearl", 4)])

q("wilden", "The Wilden", deps="apprentice", icon="ars_nouveau:wilden_horn",
  tasks=[item("ars_nouveau:wilden_horn"), item("ars_nouveau:wilden_wing"), item("ars_nouveau:wilden_spike")],
  tier=3, desc="""
    &cWilden&r are wild magic beasts that roam at night near their dens.
    &eHunters&r (forests, with wolves) drop &eHorns&r, &eStalkers&r (forests, in groups) drop
    &eWings&r, and &eDefenders&r (cold biomes) drop &eSpikes&r.

    Bring friends. You'll need one of each drop for the next quest.""",
  rewards=[give("minecraft:cooked_beef", 16), give("minecraft:arrow", 32)])

q("chimera", "The Wilden Chimera", deps="wilden", icon="ars_nouveau:wilden_tribute",
  tasks=item("ars_nouveau:wilden_tribute"), tier=4, shape="diamond", desc="""
    Craft the &eSummon Wilden&r tablet and start it at a Ritual Brazier with a Wilden Spike,
    Horn and Wing thrown in: that calls the &cWilden Chimera&r, a mini-boss.

    &cWarning:&r it breaks blocks around the brazier. Build the arena far from your base!
    It resists cold. The guide suggests Tier 2 spells, buffs, Dispel and fast movement.
    It drops the &eWilden Tribute&r.""",
  rewards=[give("minecraft:golden_apple", 2), give("minecraft:diamond", 4)])

q("archmage", "The Archmage Spell Book", deps="chimera", icon="ars_nouveau:archmage_spell_book",
  tasks=item("ars_nouveau:archmage_spell_book"), tier=5, size=1.5, shape="hexagon", desc="""
    The last upgrade: your Mage's book plus 3 ender pearls, 2 emeralds, a Totem of Undying,
    a &eNether Star&r and the &eWilden Tribute&r. It unlocks &eTier 3&r glyphs:
    the strongest spells in Ars Nouveau.""",
  rewards=[give("ars_nouveau:source_gem_block", 4)])

q("elemental", "Ars Elemental", deps="essences", icon="ars_elemental:lesser_fire_focus",
  tasks=item("ars_elemental:lesser_fire_focus"), tier=3, optional=True, desc="""
    &eArs Elemental&r adds a school to each element. A &eLesser Focus&r (an amethyst shard
    imbued with 3 essences and 3 gold) powers up spells of its element; the full Focus needs a
    &eMark of Mastery&r.

    It also adds elemental mage armor, bangles, spell prisms and lenses,
    and new familiars (Sirens, Flashjacks).""",
  rewards=[give("minecraft:gold_ingot", 6), give("minecraft:amethyst_shard", 8)])

q("additions", "Ars Additions: Charms", deps="apparatus", icon="ars_additions:night_vision_charm",
  tasks=item("ars_additions:night_vision_charm"), optional=True, desc="""
    &eArs Additions&r adds &echarms&r: small trinkets made in the Enchanting Apparatus that
    protect you from one thing (darkness, falling, fire, drowning, the void and more).
    &eCharm of Darkvision&r is a glass bottle with a lantern and a torch.

    It also adds the &eEnder Source Jar&r, lanterns and chains, and handy rituals.""",
  rewards=[give("minecraft:glass_bottle", 8), give("minecraft:lantern", 4)])

q("trinkets", "Ars Trinkets: Mana Rings", deps="apparatus", icon="ars_trinkets:essence_ring_3",
  tasks=item("ars_trinkets:essence_ring_3"), tier=3, optional=True, desc="""
    &eArs Trinkets&r adds colored &eessences&r made in the Imbuement Chamber: a copper block
    becomes Copper Essence, which is imbued up to Iron, then Silver, and higher.
    Eight essences around a &eRing of Potential&r
    make a &eMana Ring&r with more max mana; lotuses, monocles and runes work the same way.""",
  rewards=[give("minecraft:copper_block", 8), give("minecraft:iron_block", 4)])

q("arseng", "Ars Énergistique", deps="apparatus", icon="arseng:me_source_jar",
  tasks=item("arseng:me_source_jar"), tier=3, optional=True, desc="""
    &eArs Énergistique&r stores Source in your &bAE2&r network. The &eME Source Jar&r
    (a Source Jar with an ME Interface and Manipulation Essence) lets the network see Source,
    and Source cells hold huge amounts.

    Needs an AE2 network first: see the AE2 chapter.""",
  rewards=[give("minecraft:quartz", 16)])

q("delight", "Ars Nouveau's Flavors & Delight", deps="berries", icon="arsdelight:source_berry_cookie",
  tasks=item("arsdelight:source_berry_cookie"), optional=True, desc="""
    Magic food! &eArs Delight&r adds dishes made from Sourceberries, Archwood bark,
    the magic fruits of Archwood trees, and even Wilden and Chimera meat.
    Most are made in Farmer's Delight's Cooking Pot or on its Cutting Board.""",
  rewards=[give("minecraft:sugar", 16), give("minecraft:wheat", 16)])

q("where_next", "Where Next?", deps="apprentice", icon="minecraft:oak_sign", desc="""
    You're a real mage now. Keep going:

    &dIron's Spells 'n Spellbooks&r: ready-made spells from scrolls. With Ars 'n Spells,
    both mods share &eone mana pool&r.
    &dOccultism&r: summon spirits that work for you (they live happily in Containment Jars).
    &dNeo Vitae&r: blood magic. &dTheurgy&r: alchemy that multiplies ores.

    &eArs Conflux&r is installed too: it helps the add-on glyphs work together and adds a
    &eNearby Allies&r glyph for group buffs.""")
