from dsl import *

C = chapter("neo_vitae", "Neo Vitae", group="magic", icon="neovitae:ara_vitae",
            subtitle="Blood magic: an altar, your Anima and a lot of sacrifice")
q = C.quest

q("intro", "What is Neo Vitae?", icon="neovitae:blood_orb_weak", size=1.5, shape="gear", desc="""
    &4Neo Vitae&r is the new version of &4Blood Magic&r. Your own blood (and the life of mobs
    you slay) goes into an altar, the &eAra Vitae&r, which refines it into &cEssentia Vitae&r (EV).

    EV pays for everything: crafting at the altar, &esigils&r (magic tools), rituals and more.
    Your personal EV pool is your &eAnima&r; an &eOrb of Vitae&r links you to it.

    It costs health, so keep food and a safe spot nearby.""")

q("guide", "Scriptura Vitae", deps="intro", icon="neovitae:guide_book",
  tasks=item("neovitae:guide_book"), desc="""
    A book with 4 redstone around it makes &eScriptura Vitae&r, Neo Vitae's guide.
    Neo Vitae has its own names for familiar Blood Magic things; the guide's glossary explains them.""",
  rewards=[give("minecraft:redstone", 16)])

q("altar", "The Ara Vitae", deps="intro", icon="neovitae:ara_vitae",
  tasks=item("neovitae:ara_vitae"), desc="""
    The &eAra Vitae&r (Altar of Life) is deepslate around a furnace with 3 gold ingots.
    Right-click it to put an item in; right-click empty-handed to take it out.

    The basin holds 10,000 EV at first. Its crimson level shows how full it is.""",
  rewards=[give("minecraft:deepslate", 32), give("minecraft:gold_ingot", 4)])

q("orb", "Your First Orb", deps="altar", icon="neovitae:blood_orb_weak",
  tasks=item("neovitae:blood_orb_weak"), tier=2, desc="""
    Lay a &ediamond&r on the empty altar. With no EV of its own, it draws blood from players
    standing nearby (it never kills anyone) and turns the diamond into the
    &eNovicius Orb of Vitae&r.

    &cThere's no sacrificial dagger in Neo Vitae:&r right-click the orb to sacrifice one heart
    (200 EV). Near an altar the blood goes into the basin; away from one, it's stored in the orb.""",
  rewards=[give("minecraft:cooked_beef", 16), give("minecraft:golden_carrot", 8)])

q("harvest", "Harvest of the Slain", deps="orb", icon="minecraft:iron_sword", desc="""
    Kill mobs with your orb in your &eoff-hand&r: their life goes into the orb
    (10 EV per point of the mob's max health; a zombie gives 200).
    Much kinder to your own hearts!

    The orb in your off-hand can also raise a &eSanguine Ward&r that blocks arrows and fireballs
    in front of you while you hold the key (right-click by default).""",
  rewards=[give("minecraft:arrow", 32)])

q("slates", "The Slates", deps="orb", icon="neovitae:tabula_rasa",
  tasks=item("neovitae:tabula_rasa", 4), desc="""
    &eSlates&r are the base of most Neo Vitae crafts. Put &edeepslate&r on the altar:
    1,000 EV makes a &eTabula Rasa&r. Better slates need bigger altars:
    Tabula Robur (tier 1), Animata (tier 2), Spiritus (tier 3), Aetherea (tier 4).

    Short of deepslate? Cobblestone on the altar turns into cobbled deepslate for 50 EV.""",
  rewards=[give("minecraft:cobbled_deepslate", 32)])

q("tabula_vitae", "The Tabula Vitae", deps="slates", icon="neovitae:tabula_vitae",
  tasks=item("neovitae:tabula_vitae"), tier=2, desc="""
    The &eTabula Vitae&r crafts with EV straight from your Anima, through the orb placed in it.
    It makes &ereagents&r for sigils, scribe tools for arrays, anointments for weapons,
    double ore processing, and &eThrowing Daggers&r.""",
  rewards=[give("minecraft:iron_ingot", 8), give("minecraft:string", 8)])

q("daggers", "Throwing Daggers", deps="tabula_vitae", icon="neovitae:throwing_dagger",
  tasks=item("neovitae:throwing_dagger", 16), desc="""
    16 &eThrowing Daggers&r from 2 iron ingots and a string at the Tabula Vitae.
    Mobs wounded by them leave &5Spiritus&r, the fuel of the Hellfire Forge.""",
  rewards=[give("minecraft:iron_ingot", 8)])

q("arrays", "Alchemy Arrays", deps="tabula_vitae", icon="neovitae:arcane_scribe_tool",
  tasks=[item("neovitae:arcane_scribe_tool"), item("neovitae:sigil_divination")], desc="""
    Use an &eArcane Scribe Tool&r on the ground to draw an &eAlchemy Array&r, a circle that takes
    two items. Some combinations craft things, others cast effects.

    &eDivination Sigil&r: redstone, then a Tabula Rasa. Right-click it to see your Anima;
    look at the altar to read its tier and contents.""",
  rewards=[give("minecraft:redstone", 16), give("minecraft:gunpowder", 8)])

q("sigils", "Sigils", deps="arrays", icon="neovitae:sigil_water",
  tasks=item("neovitae:sigil_water"), tier=2, desc="""
    &eSigils&r are tools powered by your Anima. The &eWater Sigil&r makes a water source for
    100 EV a use (its reagent is sugar and two water buckets at the Tabula Vitae, then an array
    with a Tabula Rasa). If your Anima is empty, it takes the cost from your health!

    Others: Lava, Void, Green Grove (growth), Fast Miner, Magnetism, Blood Lamp, Holding...
    The &eAir Sigil&r flings you through the air for 50 EV a burst (mind the landing).""",
  rewards=[give("minecraft:sugar", 16), give("minecraft:bucket", 2)])

q("runes", "Altar Tier 1", deps="slates", icon="neovitae:rune_blank",
  tasks=item("neovitae:rune_blank", 8), tier=2, desc="""
    Ring the altar with &e8 Blank Runes&r (deepslate around a Tabula Rasa and your orb)
    to reach &eTier 1&r. The four side runes can be swapped for special ones:

    &eSpeed&r: faster crafting. &eCapacity&r: bigger basin. &eSacrifice&r / &eSelf-Sacrifice&r:
    more EV from mobs / from you. &eCharging&r, &eOrb&r, &eAcceleration&r, &eDisplacement&r: see the guide.""",
  rewards=[give("minecraft:deepslate", 64)])

q("apprentice_orb", "Discipulus Orb", deps="runes", icon="neovitae:blood_orb_apprentice",
  tasks=item("neovitae:blood_orb_apprentice"), tier=3, desc="""
    A &eblock of redstone&r on a Tier 1 altar (5,000 EV) makes the &eDiscipulus Orb&r,
    a bigger Anima. Your old orb's network carries over: it's still you.""",
  rewards=[give("minecraft:redstone_block", 4)])

q("forge", "The Hellfire Forge", deps="daggers", icon="neovitae:hellfire_forge",
  tasks=[item("neovitae:hellfire_forge"), item("neovitae:spiritus_gem_petty")], tier=2, desc="""
    The &eHellfire Forge&r runs on &5Spiritus&r. Craft a &ePetty Spiritus Gem&r in it
    (redstone, gold, glass, lapis): the gem soaks up Spiritus from mobs you hit with daggers
    or Sentient weapons, and feeds the forge.

    The forge makes better gems, Sentient tools, explosive mining charges and more.""",
  rewards=[give("minecraft:lapis_lazuli", 16), give("minecraft:gold_ingot", 4)])

q("sentient", "Sentient Sword", deps="forge", icon="neovitae:sentient_sword",
  tasks=item("neovitae:sentient_sword"), tier=3, desc="""
    Put an iron sword in the forge with a Petty Spiritus Gem: the &eSentient Sword&r.
    It harvests Spiritus far better than daggers, and grows stronger with the Spiritus you carry.
    &eSentient Armor&r (iron armor bound in an array) learns from what you do and grows stronger.""",
  rewards=[give("minecraft:iron_ingot", 8)])

q("tier2", "Altar Tier 2", deps="apprentice_orb", icon="neovitae:blood_orb_magician",
  tasks=item("neovitae:blood_orb_magician"), tier=3, desc="""
    &eTier 2&r: a wider ring of runes one level down (24 in all) with stone pillars at the
    corners capped with &eBlood Stained Glass&r. The Divination Sigil confirms the tier.

    A &egold block&r on the Tier 2 altar (25,000 EV) makes the &eVeneficus Orb&r.""",
  rewards=[give("minecraft:gold_block", 2), give("minecraft:glass", 16)])

q("rituals", "Rituals", deps="tier2", icon="neovitae:master_ritual_stone",
  tasks=[item("neovitae:master_ritual_stone"), item("neovitae:ritual_diviner")], tier=3, desc="""
    Rituals are big circles of &eRitual Stones&r around a &eMaster Ritual Stone&r.
    The &eRitual Diviner&r places the stones for you (pick a ritual, right-click the master stone).
    Wake it with an &eActivation Crystal&r (Weak: a Lava Crystal on a Tier 2 altar).

    Rituals cost EV to start and often keep drawing EV while they run: crop growth, pumping,
    tree felling, the &eWell of Suffering&r (EV from mobs) and many more.""",
  rewards=[give("minecraft:obsidian", 16), give("minecraft:diamond", 2)])

q("demon_realm", "Edge of the Demon Realm", deps="rituals", icon="neovitae:weak_blood_shard",
  tasks=item("neovitae:weak_blood_shard"), tier=4, shape="diamond", desc="""
    The ritual &eBreaching the Edge of Demon Realm&r opens a way into a dangerous dungeon.
    Inside grows &eTau Fruit&r: refine it in the &eAthanor&r into &eWeak Blood Shards&r,
    the key to Tier 3 and stronger anointments. Come armed!""",
  rewards=[give("minecraft:golden_apple", 3)])

q("master_orb", "Magus Orb", deps="demon_realm", icon="neovitae:blood_orb_master",
  tasks=item("neovitae:blood_orb_master"), tier=5, size=1.5, shape="hexagon", desc="""
    Tier 3 altar (pillars crowned with Bloodstone Bricks), then a &eWeak Blood Shard&r on it
    (40,000 EV) makes the &eMagus Orb&r. Beyond lie Tier 4 and 5, the Demon Realm's deeper
    dungeons, Hellforged metal and the Divinus Orb.""",
  rewards=[give("minecraft:diamond_block", 1)])

q("where_next", "Where Next?", deps="runes", icon="minecraft:oak_sign", desc="""
    &dArs Nouveau&r and &dIron's Spells&r: spells and mana. &dOccultism&r: spirits and chalk rituals.
    Neo Vitae's &eTeleposers&r can swap blocks and players between two linked points for EV:
    earned travel with a real cost (see the guide).""")
