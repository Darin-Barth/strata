from dsl import *

C = chapter("vampirism", "Vampirism", group="magic", icon="vampirism:vampire_fang",
            subtitle="Optional: become a vampire, a hunter or a werewolf, or ignore it all")
q = C.quest

q("intro", "What is Vampirism?", icon="vampirism:vampire_fang", size=1.5, shape="gear", desc="""
    &4Vampirism&r adds vampires, vampire hunters and (with the Werewolves add-on) werewolves.
    They live in the world either way: vampire mobs at night and in dark forests, hunter camps,
    and villages that one side controls.

    &aIt's completely optional.&r You can become a &4Vampire&r, a &6Hunter&r or a &2Werewolf&r,
    or just stay human and ignore it. You can only belong to one side at a time,
    and each one has a way back out (see below).""")

q("choose", "Pick a Side (or Don't)", deps="intro", icon="minecraft:oak_sign", desc="""
    &4Vampire&r: drink blood instead of eating, get strong and fast at night, and learn powers like
    bat form and teleporting. But the sun burns, and garlic and holy water hurt.
    &6Hunter&r: a human with garlic in their blood: crossbows, stakes, holy water and special gear.
    &2Werewolf&r: change into a wolf form for power and speed; silver is your weakness.
    &7Human&r: skip this chapter. Nothing forces you in.

    The &eVampirism Menu&r and &eSkill Screen&r keys are in Options > Controls.""")

# --- vampire ------------------------------------------------------------------------------------
q("become_vampire", "Moving Beyond Humanity", deps="choose", icon="vampirism:vampire_fang", optional=True,
  tasks=adv("vampirism:vampire/become_vampire", title="Become a Vampire"), tier=2, desc="""
    Let a vampire &ebite&r you (or right-click with a &eVampire Fang&r) to get &4Sanguinare Vampiris&r.
    When it runs out (about a Minecraft day) you're a vampire.

    &aChanged your mind?&r Drink milk, or talk to a hunter NPC, before it ends.""",
  rewards=[give("minecraft:glass_bottle", 8)])

q("blood", "Blood, Not Bread", deps="become_vampire", icon="vampirism:blood_bottle", optional=True,
  tasks=adv("vampirism:vampire/first_blood", title="Drink blood"), desc="""
    Vampires live on &cblood&r. Hold the "Suck blood" key (Options > Controls) behind a villager
    or some animals to drink. Glass bottles on your hotbar fill into &eBlood Bottles&r when your
    blood bar is full; drink them later.

    Store extra blood in a &eBlood Container&r. Zombies leave you alone now, but hunters don't!
    Stay out of water and, at higher levels, out of the sun.""",
  rewards=[give("minecraft:glass_bottle", 16)])

q("vampire_levels", "Vampire Levels", deps="blood", icon="vampirism:altar_inspiration", optional=True,
  tasks=item("vampirism:altar_inspiration"), tier=2, desc="""
    You level up with rituals &eat night&r: first at the &eAltar of Inspiration&r (planks around a
    Blood Container) fed with blood, later at the bigger &eAltar of Infusion&r with pillars.
    Each level brings more health, speed and strength, plus a skill point.

    Spend points in the Skill Screen: bat form, freezing enemies, teleporting, invisibility, sunscreen...
    Vampire Teleport is one of those earned skills, not a free command.""",
  rewards=[give("minecraft:oak_planks", 32)])

q("delight", "Vampire's Delight", deps="blood", icon="vampiresdelight:blood_pie", optional=True,
  tasks=item("vampiresdelight:blood_pie"), desc="""
    Vampires can't enjoy normal food, so &eVampire's Delight&r cooks for them: blood pies,
    blood wine, blood sausages and more, made with Farmer's Delight tools.
    There are also treats for humans and hunters (garlic soup, garlic bread).""",
  rewards=[give("minecraft:wheat", 16)])

q("umbrella", "Vampires Need Umbrellas", deps="vampire_levels", icon="vampiresneedumbrellas:iron_umbrella",
  optional=True, tasks=item("vampiresneedumbrellas:iron_umbrella"), desc="""
    Sun getting to you? An &eumbrella&r keeps the sun off a vampire. Iron, gold, diamond and
    netherite ones last longer and longer, in 16 colors.""",
  rewards=[give("minecraft:iron_ingot", 6)])

q("ageing", "Vampiric Ageing", deps="vampire_levels", icon="vampiricageing:blood_tester", optional=True, desc="""
    With &eVampiric Ageing&r, vampires also gain an &eAge Rank&r over time: survive, infect other
    creatures and drain blood to grow older and stronger. Hit another vampire with a
    &eBlood Tester&r to see how old it is.""")

q("bloodlines", "Bloodlines", deps="vampire_levels", icon="bloodlines:bloodline_fang_noble", optional=True,
  tier=3, desc="""
    &eBloodlines&r lets high-level vampires join a bloodline with its own skill tree:
    &eNoble&r, &eZealot&r (Deep Dark shrines), &eEctotherm&r (cold and water), &eBloodknight&r
    and &eGravebound&r. Each has strong powers and real weaknesses, and some ways of joining can kill
    you if they go wrong. Look up the fangs, elixirs and injections with &eR&r before you try.

    Leave a bloodline with a &ePurity Injection&r at an Injection Chair.""")

q("cure_vampire", "Back to Human", deps="become_vampire", icon="vampirism:altar_cleansing", optional=True,
  desc="""
    Done being a vampire? Find an &eAltar of Cleansing&r in some village churches
    (or craft one from vampire fangs, a book and planks) and use it to become human again.
    &cYou lose all your vampire levels.&r""")

# --- hunter --------------------------------------------------------------------------------------
q("become_hunter", "Start Hunting", deps="choose", icon="vampirism:injection_garlic", optional=True,
  tasks=adv("vampirism:hunter/become_hunter", title="Become a Vampire Hunter"), tier=2, desc="""
    Find a village with a &eHunter Trainer&r. Garlic grows behind their house: craft a
    &eGarlic Injection&r (a Syringe made of glass, plus garlic) and use it on the
    &eInjection Chair&r inside. Garlic in your blood makes you immune to vampire bites.

    Plant some garlic, you'll need more.""",
  rewards=[give("minecraft:glass", 8)])

q("stake", "Stakes and Vampire Blood", deps="become_hunter", icon="vampirism:stake", optional=True,
  tasks=[item("vampirism:stake"), item("vampirism:vampire_blood_bottle", 3)], desc="""
    Finish vampire NPCs with a &eStake&r to collect &eVampire Blood&r.
    Give it to a hunter NPC to train from level 1 to 4.""",
  rewards=[give("minecraft:stick", 16)])

q("hunter_table", "Hunter Research", deps="stake", icon="vampirism:hunter_table", optional=True,
  tasks=item("vampirism:hunter_table"), tier=2, desc="""
    For higher levels, research vampires at a &eHunter Research Table&r (a vampire fang, a book,
    garlic and planks) to make &eHunter Intel&r, then pay a Hunter Trainer to train you.
    Blocks placed next to the table upgrade it for the top levels.

    Each level gives a skill point: crossbows and the Weapon Table, potions, disguise and more.
    Vampires hate &egarlic&r (a &eGarlic Diffuser&r keeps vampire mobs out of your base),
    &eholy water&r and fire.""",
  rewards=[give("minecraft:book", 2)])

q("leave_hunter", "Hanging Up the Crossbow", deps="become_hunter", icon="vampirism:injection_sanguinare",
  optional=True, desc="""
    To stop being a hunter, the guide says to get the garlic out of your blood: craft a
    &eSanguinare Injection&r (a Syringe and 8 vampire fangs) and use it on an &eInjection Chair&r.
    That starts turning you into a vampire; drink milk before it finishes to stay human instead.""")

# --- werewolf ------------------------------------------------------------------------------------
q("become_werewolf", "Teen Wolf", deps="choose", icon="werewolves:werewolf_tooth", optional=True,
  tasks=adv("werewolves:teen_wolf", title="Become a Werewolf"), tier=2, desc="""
    With &eWerewolves&r, a werewolf's scratch can give you &2Lupus Sanguinem&r. Sleep, and you
    wake up a werewolf. You change into wolf form (and are forced to at a full moon, until a skill
    frees you). Choose a path: &cBeast&r, &aSurvivalist&r or &eHuman&r.

    &cSilver&r is your weakness: silver weapons and bolts slow you and break your defense.""")

q("werewolf_levels", "Werewolf Rituals", deps="become_werewolf", icon="werewolves:stone_altar", optional=True,
  tasks=item("werewolves:stone_altar"), tier=2, desc="""
    Werewolves level up at night at a &eStone Altar&r with four Stone Altar Fire Bowls around it,
    with the items it asks for plus enough creatures slain (shown in the Vampirism Menu).""")

q("cure_werewolf", "Lifting the Curse", deps="become_werewolf", icon="werewolves:injection_un_werewolf",
  optional=True, desc="""
    Want your old life back? Use an empty &eSyringe&r on a werewolf to collect a strange fluid,
    which makes a &eStrange Injection&r. Use it at an Injection Chair to lift the curse.""")

# --- for everyone ------------------------------------------------------------------------------------
q("silver", "Silver for Everyone", deps="choose", icon="werewolves:silver_ingot",
  tasks=item("werewolves:silver_ingot", 4), desc="""
    Even humans should carry a little protection. &eSilver&r ore (from Werewolves) smelts into
    ingots for silver tools, armor and Silver Oil (on a sword, extra damage to werewolves).""",
  rewards=[give("minecraft:raw_iron", 8)])

q("forest", "The Vampire Forest", deps="choose", icon="vampirism:vampire_orchid",
  tasks=adv("vampirism:main/vampire_forest", title="Visit a Vampire Forest"), tier=2, desc="""
    Dark, misty forests full of vampires, with castles and crypts. Bring torches,
    holy water or a vampire friend. Somewhere deep inside sleep the &4Ancient Remains&r...

    &eVampirism Integrations&r makes other mods' villages work with Vampirism's factions too.""",
  rewards=[give("minecraft:torch", 32)])

q("where_next", "Where Next?", deps="choose", icon="minecraft:oak_sign", desc="""
    &dIron's Spells&r: vampires can cast &4Blood&r spells with their own blood, and &6Holy&r spells
    are a hunter's best friend. &dArs Nouveau&r and &dOccultism&r work for every side.""")
