from dsl import *

C = chapter("irons_spells", "Iron's Spells 'n Spellbooks", group="magic", icon="irons_spellbooks:gold_spell_book",
            subtitle="Scrolls, spell books and nine schools of magic")
q = C.quest

q("intro", "What is Iron's Spells?", icon="irons_spellbooks:scroll", size=1.5, shape="gear", desc="""
    &dIron's Spells 'n Spellbooks&r is ready-made magic: fireballs, healing circles, lightning,
    summons and more. Spells come on &escrolls&r that you find, loot or craft,
    and you write them into a &espell book&r to cast them again and again.

    Every spell belongs to a &eschool&r, and armor, rings and runes make your favorite school stronger.
    Explore! Magic towers and ruins are full of loot, each guarded by a mage.""")

# --- first steps -----------------------------------------------------------------------------
q("essence", "Arcane Essence", deps="intro", icon="irons_spellbooks:arcane_essence",
  tasks=item("irons_spellbooks:arcane_essence", 4), desc="""
    &eArcane Essence&r is the basic Iron's material. You find it in chests, especially in
    magic structures, and spellcasting mobs drop it.

    Craft a book with one Arcane Essence to get the mod's guide book.""",
  rewards=[give("minecraft:book", 2), give("minecraft:leather", 8)])

q("scrolls", "Scrolls", deps="intro", icon="irons_spellbooks:scroll",
  tasks=item("irons_spellbooks:scroll", title="Find or loot any scroll"), desc="""
    A &escroll&r holds one spell at one level. Right-click to cast it once for free (no mana),
    but then it's gone. Better: save it and write it into a spell book.

    Scrolls drop from mobs, sit in chests, and can be crafted later at the Scroll Forge.""",
  rewards=[give("minecraft:paper", 16)])

q("spell_book", "Your First Spell Book", deps="essence", icon="irons_spellbooks:copper_spell_book",
  tasks=item("irons_spellbooks:copper_spell_book"), desc="""
    The &eFlimsy Journal&r is the starter spell book: paper, string and copper.
    Bigger books hold more spells. Equip it in your &espellbook&r accessory slot (Curios) so you
    can cast while holding a sword.""",
  rewards=[give("minecraft:copper_ingot", 16), give("minecraft:string", 8)])

q("inscription", "The Inscription Table", deps=["spell_book", "scrolls"], icon="irons_spellbooks:inscription_table",
  tasks=item("irons_spellbooks:inscription_table"), tier=2, desc="""
    Put your spell book and a scroll in the &eInscription Table&r to write the spell in.
    You can take it back out as a scroll later, but that clears the slot.

    To cast: pick a spell with the &espell wheel&r (its key is in Options > Controls),
    then use the "Cast Selected Spell" key, also in Options > Controls.""",
  rewards=[give("irons_spellbooks:arcane_essence", 4)])

q("mana", "Mana", deps="inscription", icon="irons_spellbooks:mana_ring",
  tasks=item("irons_spellbooks:wandering_magician_chestplate"), desc="""
    Spells from a book cost &bmana&r and have a short cooldown. Mana refills over time.

    &eWandering Magician&r armor (leather armor + Arcane Essence) is an easy early way to get more
    max mana: craft the chestplate. Rings and amulets add more.

    &dShared with Ars Nouveau:&r Ars 'n Spells joins the two mods' mana into one pool, so your
    Ars spells and Iron's spells drink from the same bar (by default it's Iron's mana bar).""",
  rewards=[give("minecraft:leather", 16)])

q("schools", "The Schools of Magic", deps="inscription", icon="minecraft:blaze_rod", desc="""
    Each school has a theme and a &efocus&r item used to craft its scrolls, runes and gear:

    &cFire&r (blaze rod): burning damage. &bIce&r (frozen bone): damage and slowing.
    &eLightning&r (Bottle o' Lightning): big single hits. &6Holy&r (Divine Pearl): healing and buffs.
    &5Ender&r (ender pearl): arcane damage and movement. &4Blood&r (Blood Vial): necromancy and life drain.
    &aEvocation&r (emerald): tricks and summons. &2Nature&r (poisonous potato): poisons and debuffs.

    &8Eldritch&r is forbidden: you learn it only from &eEldritch Manuscripts&r found in the world.""",
  rewards=[give("minecraft:emerald", 4), give("minecraft:blaze_rod", 2)])

q("staff", "Graybeard Staff", deps="schools", icon="irons_spellbooks:graybeard_staff",
  tasks=item("irons_spellbooks:graybeard_staff"), optional=True, desc="""
    A &ecasting implement&r: right-click to cast your selected spell, with bonuses for mages.
    This one is a wooden shovel, an iron ingot and an Arcane Essence.""")

# --- mid game --------------------------------------------------------------------------------
q("scroll_forge", "The Scroll Forge", deps=["schools", "welcome/nether"], icon="irons_spellbooks:scroll_forge",
  tasks=item("irons_spellbooks:scroll_forge"), tier=3, desc="""
    Make your own scrolls! The &eScroll Forge&r (polished deepslate and crying obsidian)
    uses &eink&r, paper and a school &efocus&r. The focus picks the school;
    the ink picks the rarity (and so the spell's level).

    Ink is found in magic chests and dropped by spellcasting mobs (rare ink especially).
    In the &eAlchemist Cauldron&r you can brew ink up a rarity: common ink + copper makes
    uncommon, + iron makes rare, + gold makes epic.""",
  rewards=[give("minecraft:paper", 32), give("minecraft:ink_sac", 8)])

q("apprentice_book", "Apprentice's Spell Book", deps="scroll_forge", icon="irons_spellbooks:gold_spell_book",
  tasks=item("irons_spellbooks:gold_spell_book"), tier=3, desc="""
    A bigger book from gold, Arcane Essence and &eHogskin&r (dropped by Hoglins in the Nether).
    More slots means more spells on your wheel.""",
  rewards=[give("minecraft:gold_ingot", 8)])

q("cloth", "Arcane Cloth and Runes", deps="scroll_forge", icon="irons_spellbooks:magic_cloth",
  tasks=[item("irons_spellbooks:magic_cloth", 4), item("irons_spellbooks:blank_rune")], tier=2, desc="""
    &eArcane Cloth&r (wool wrapped in Arcane Essence) is the base of real mage armor.
    &eRunestones&r are found in magic structures; a blank rune surrounded by a school's focus
    becomes that school's rune. Class mages always drop a rune of their school.""",
  rewards=[give("minecraft:white_wool", 8), give("irons_spellbooks:arcane_essence", 4)])

q("school_armor", "School Armor", deps="cloth", icon="irons_spellbooks:pyromancer_chestplate",
  tasks=item("irons_spellbooks:pyromancer_chestplate", title="Any school chestplate (Pyromancer shown)"),
  tier=3, desc="""
    Each school has its own armor set (Pyromancer, Cryomancer, Electromancer, Priest, Plagued,
    Cultist, Archevoker, Shadow-Walker...). They boost that school's spell power and your mana.
    The recipe is a wizard armor piece, the school's rune and Arcane Essence.

    The task shows a Pyromancer Robe; click it with &eR&r to see all of them, any is fine to aim for.""",
  rewards=[give("irons_spellbooks:arcane_essence", 8)])

q("cauldron", "The Alchemist Cauldron", deps="scroll_forge", icon="irons_spellbooks:alchemist_cauldron",
  tasks=item("irons_spellbooks:alchemist_cauldron"), tier=2, desc="""
    Recycle scrolls you don't want, brew &eink&r into stronger ink, and brew Iron's elixirs
    (Oakskin, Evasion, Invisibility...).
    It needs &eCinder Essence&r, dropped by &cAncient Knights&r: they wake up when you break
    armor piles in the Nether.""")

# --- late game -------------------------------------------------------------------------------
q("anvil", "The Arcane Anvil", deps="school_armor", icon="irons_spellbooks:arcane_anvil",
  tasks=item("irons_spellbooks:arcane_anvil"), tier=4, desc="""
    The strongest Iron's workstation: &elevel up scrolls&r (scroll + ink of the next rarity),
    upgrade armor and spell books, and &eimbue weapons&r with a spell.

    Late game also brings &eMithril&r (needs a netherite pickaxe). A few veins hide below
    y = -38 at home; it grows richest in the dark of &5the Hollow&r and &eupgrade orbs&r (an orb plus 8 runes).""",
  rewards=[give("minecraft:amethyst_block", 4), give("minecraft:diamond", 2)])

q("best_books", "The Best Books", deps="anvil", icon="irons_spellbooks:netherite_spell_book",
  tasks=item("irons_spellbooks:netherite_spell_book"), tier=5, desc="""
    The &eAncient Codex&r is made from netherite and the &eRuined Book&r found in Ancient Cities.
    The &eDragonskin Spell Book&r needs Dragonskin, dropped by the Ender Dragon.
    Named spell books with special bonuses also hide around the world.""",
  rewards=[give("minecraft:netherite_scrap", 2)])

# --- bridges and add-ons -----------------------------------------------------------------------
q("ars_bridge", "Ars 'n Spells and Iron & Nouveau", deps="mana", icon="ars_n_spells:spell_loom",
  tasks=item("ars_n_spells:spell_loom"), tier=2, desc="""
    Two bridge mods tie Iron's to &dArs Nouveau&r:

    &eArs 'n Spells&r: one shared mana pool. The &eSpell Loom&r (or the Spell Transcription ritual)
    writes an Ars spell onto a &eBlank Scroll&r (Blank Parchment + Source Gem). Bind that scroll
    into an Iron's spell book and your Ars spell shows up on the spell wheel.

    &eIron & Nouveau&r: adds Ars glyphs that cast Iron's spells (Firebolt, Icicle, Heal,
    Chain Lightning, Summon Vex...), so you can mix them into your own Ars spells.""",
  rewards=[give("ars_nouveau:source_gem", 4), give("minecraft:obsidian", 3)])

q("apothic", "Apotheosis x Iron's Spells", deps="spell_book", icon="apotheosis:gem_dust", optional=True, desc="""
    With this bridge, &eApotheosis&r gems also fit &espell books and staves&r, and gear can
    roll magic affixes like "on hit, cast a spell". Keep an eye on rare loot!""")

q("cataclysm", "Cataclysm: Spellbooks", deps="anvil", icon="cataclysm_spellbooks:burning_manuscript",
  tier=4, optional=True, desc="""
    &eCataclysm: Spellbooks&r adds spells and mage gear themed on the &cL_Ender's Cataclysm&r bosses.
    Their manuscripts and tablets teach new spell sets: for example the &eBurning Manuscript&r
    holds the blazing spells of Ignis. Beat the bosses (see the Cataclysm chapter) to find them.""",
  rewards=[give("minecraft:golden_apple", 2)])

q("vampire_compat", "Vampires and Spells", deps="schools", icon="irons_spellbooks:blood_vial", optional=True,
  desc="""
    If you play &4Vampirism&r: a vampire can pay for &4Blood&r school spells with their own blood
    instead of mana. &6Holy&r spells hit Vampirism's vampires extra hard, and holy healing doesn't
    sit well with vampire players. See the Vampirism chapter.""")

q("where_next", "Where Next?", deps="scroll_forge", icon="minecraft:oak_sign", desc="""
    &dArs Nouveau&r: build your own spells from glyphs, sharing your mana.
    &dOccultism&r: spirits and rituals. &dNeo Vitae&r: blood magic.
    &cBosses&r: mage towers, the Cataclysm bosses and the Ender Dragon drop the best magic loot.""")
