from dsl import *

C = chapter("combat_gear", "Combat & Gear", group="bosses", icon="simplyswords:iron_claymore",
            subtitle="Weapons, dodging, Apotheosis loot, gems and enchanting")
q = C.quest

q("intro", "What is Combat & Gear?", icon="minecraft:iron_sword", size=1.5, shape="gear", desc="""
    Fighting in Strata feels different from vanilla:

    &eBetter Combat&r: every weapon type swings its own way, with combos and reach.
    &eCombat Roll&r: a quick dodge-roll.
    &eApotheosis&r: random loot with &6rarities&r, gems you socket into gear, and a much
    deeper enchanting table.

    This chapter walks you through all of it. Start anywhere.""",
  rewards=[give("minecraft:cooked_beef", 16)])

# --- Better Combat + Simply Swords --------------------------------------------------------
q("better_combat", "Every Weapon Swings Differently", deps="intro", icon="simplyswords:iron_longsword",
  tasks=item("simplyswords:iron_longsword"), desc="""
    With &eBetter Combat&r, hold attack and keep swinging: each weapon has a &ecombo&r of
    different swings (slash, stab, overhead), and its own &ereach&r (shown on the tooltip as
    Attack Range).

    Swings hit everything in their arc, so a wide slash can clip several mobs at once.
    Craft an &eIron Longsword&r (Simply Swords) and try a combo on a zombie.""",
  rewards=[give("minecraft:iron_ingot", 8)])

q("two_handed", "Big Swings", deps="better_combat", icon="simplyswords:iron_claymore", tier=2,
  tasks=item("simplyswords:iron_claymore"), desc="""
    Some weapons are &eTwo-Handed&r (it says so on the tooltip): claymores, katanas,
    twinblades, greathammers. You can't use your off-hand with them, but they hit hard
    and reach far.

    One-handed weapons can be &edual-wielded&r: put a second one in your off-hand and your
    swings alternate between hands.

    &eFeint&r cancels a swing you started. Set its key in Options > Controls.""",
  rewards=[give("minecraft:iron_ingot", 12)])

q("combat_roll", "Dodge Roll", deps="better_combat", icon="minecraft:leather_boots", desc="""
    &eCombat Roll&r: press &eR&r by default (or rebind it in Options > Controls) to dash a few blocks
    in the direction you're moving. An arrow on your HUD shows when it's ready again.

    &eThe rules here:&r a roll takes &e4 seconds&r to recharge, needs more than
    &e3 drumsticks&r of food, and costs a little hunger. It moves you out of the way,
    but you're &cnot invulnerable&r while rolling, so roll early.

    Enchantments help: &eAcrobat&r (chestplate, faster recharge), &eLongfooted&r (boots, longer
    rolls) and &eMulti-Roll&r (helmet, extra rolls).""",
  rewards=[give("minecraft:cooked_porkchop", 16)])

q("simply_swords", "Simply Swords", deps="two_handed", icon="simplyswords:runic_tablet", tier=2,
  tasks=item("simplyswords:runic_tablet", title="Find a Runic Tablet"), desc="""
    &eSimply Swords&r adds 15 weapon types (chakram, glaive, halberd, rapier, scythe...)
    in iron, gold, diamond and netherite. Look them up with &eU&r on an iron ingot.

    Dungeon chests can hold &6unique&r named weapons with special powers, and &eRunic Tablets&r.
    Bring a tablet back: it's the smithing template for runic weapons.""",
  rewards=[give("minecraft:diamond", 3)])

q("runic", "Runic Weapons", deps="simply_swords", icon="simplyswords:runic_longsword", tier=4,
  optional=True, tasks=item("simplyswords:runic_longsword"), desc="""
    In a &eSmithing Table&r: Runic Tablet + a &enetherite&r Simply Swords weapon + a diamond
    gives its &erunic&r version, which carries a rune power.

    Every weapon type works the same way. Pick the one whose combo you like best.""",
  rewards=[give("minecraft:netherite_scrap", 2)])

# --- Apotheosis loot ---------------------------------------------------------------------
q("affix", "Gear With Colours", deps="intro", icon="apotheosis:mysterious_scrap_metal",
  tasks=adv("apotheosis:progression/haven", title="Pick up an affix item"), desc="""
    &eApotheosis&r gear drops from mobs, sits in chests, and is sold by wandering traders.
    Its name colour is its &erarity&r:

    &7Common&r (grey): one bonus stat.
    &aUncommon&r (green): two stats, maybe a socket.
    &9Rare&r (blue): two stats plus a special effect, up to two sockets.
    &5Epic&r (purple): three stats, an effect and an &eAbility&r, always a socket.
    &6Mythic&r (orange): four stats, two effects, an Ability and extra bonuses.

    A beam of light shines up from good drops. Pick one up! Your stats (crit chance,
    life steal...) are on the small button at the &etop right&r of your inventory.""",
  rewards=[give("minecraft:experience_bottle", 8)])

q("elites", "Elites and Invaders", deps="affix", icon="minecraft:zombie_head", desc="""
    &6Apothic Elites&r are named, empowered versions of normal mobs. They're rare near spawn
    and more common far out and in other dimensions. They can drop affix gear.

    &cApothic Invaders&r arrive with a loud noise, a chat message and a beam of light.
    They're mini-bosses that always drop a special affix item and often gems.
    Invaders never appear while your World Tier is &eHaven&r.""")

q("world_tiers", "World Tiers (Ctrl+T)", deps="affix", icon="minecraft:beacon", tier=2,
  tasks=adv("apotheosis:progression/frontier", title="Unlock Frontier"), desc="""
    Press &eCtrl+T&r for the &eWorld Tier&r screen. Tiers are &eper player&r:
    &aHaven&r > &eFrontier&r > &6Ascent&r > &cSummit&r > &5Pinnacle&r.

    A higher tier makes mobs around &eyou&r tougher and loot better (it also raises the max
    enchanting level). Unlocking a tier doesn't switch it on: you choose when, and can
    switch back. Hover a tier's icon to see what unlocks it.

    &eFrontier&r unlocks when you wear four affix armor pieces and hold an affix weapon.""",
  rewards=[give("minecraft:golden_apple", 2)])

q("ascent", "World Tier: Ascent", deps="world_tiers", icon="minecraft:gold_block", tier=3,
  optional=True, tasks=adv("apotheosis:progression/ascent", title="Unlock Ascent"), desc="""
    Wear a full set of &aUncommon&r affix armor, hold an Uncommon weapon, and defeat an
    &cApothic Invader&r.

    Only activate it when you're ready: Invaders and Elites get more common.""")

q("summit", "World Tier: Summit", deps="ascent", icon="minecraft:wither_skeleton_skull", tier=4,
  optional=True, tasks=adv("apotheosis:progression/summit", title="Unlock Summit"), desc="""
    A full set of &9Rare&r affix gear, and the &cWither&r defeated.

    The last tier, &5Pinnacle&r, needs a full set of &5Epic&r gear and the Ender Dragon
    defeated: the best loot and the toughest mobs.""")

q("gem_dust", "Not a Diamond", deps="affix", icon="apotheosis:gem_dust", tier=2,
  tasks=item("apotheosis:gem_dust"), desc="""
    &eGems&r drop from mobs and bosses and sit in chests. Socket one into gear for a strong
    bonus (each gem says which items it fits).

    &eSocketing:&r put the item and the gem in a &eSmithing Table&r, or just right-click the
    gem onto the item in your inventory. The item needs a free socket.

    Your first &eGem Dust&r: drop a spare gem on the ground and let an &eanvil&r fall on it.""",
  rewards=[give("minecraft:anvil")])

q("salvaging", "Salvaging Table", deps="gem_dust", icon="apotheosis:salvaging_table", tier=2,
  tasks=item("apotheosis:salvaging_table"), desc="""
    Breaks affix gear (and gems) you don't want into &erarity materials&r:

    &7Mysterious Scrap Metal&r, &aTimeworn Fabric&r, &9Luminous Crystal Shard&r,
    &5Arcane Sands&r and &6Godforged Pearl&r, one per rarity.
    Gems salvage into Gem Dust. Don't throw old gear away: salvage it.""",
  rewards=[give("minecraft:lava_bucket"), give("minecraft:copper_ingot", 16)])

q("gem_cutting", "Gem Cutting Table", deps="salvaging", icon="apotheosis:gem_cutting_table", tier=2,
  tasks=item("apotheosis:gem_cutting_table"), desc="""
    Gems have a &epurity&r: Cracked, Chipped, Flawed, Normal, Flawless and &6Perfect&r.

    To upgrade a gem: put in the gem, a &esecond copy of the same gem and purity&r,
    Gem Dust and rarity materials. Higher purities cost more. Press &eR&r on a gem
    to see the exact cost.""",
  rewards=[give("minecraft:smooth_stone", 8)])

q("sockets", "More Sockets", deps="gem_dust", icon="apotheosis:sigil_of_socketing", tier=3,
  tasks=item("apotheosis:sigil_of_socketing"), desc="""
    A &eSigil of Socketing&r adds a socket to an item in the Smithing Table (up to two this way).
    It's made from Gem-Fused Slate (deepslate + gem dust).

    Changed your mind? A &eSigil of Withdrawal&r pops all the gems back out, and you keep
    both the item and the gems.""",
  rewards=[give("minecraft:deepslate", 32), give("minecraft:amethyst_shard", 4)])

q("reforging", "Reforging", deps="salvaging", icon="apotheosis:simple_reforging_table", tier=3,
  tasks=item("apotheosis:simple_reforging_table"), desc="""
    Don't like your item's bonuses? &eReforge&r it. Put the item in the middle, rarity
    materials top-left and &eSigils of Rebirth&r bottom-right, then pick one of three
    new versions. It costs a few levels.

    The Simple Reforging Table goes up to &9Rare&r and works on plain gear too.
    Upgrade it into a &eReforging Table&r (netherite + &5Arcane Sands&r) for Epic and Mythic.""",
  rewards=[give("minecraft:experience_bottle", 16)])

q("augmenting", "Augmenting Table", deps="reforging", icon="apotheosis:augmenting_table", tier=5,
  optional=True, tasks=item("apotheosis:augmenting_table"), desc="""
    The end-game table: upgrade one affix by 25% or reroll just that one, keeping the rest.
    Built from a &eNether Star&r and two &6Godforged Pearls&r; it runs on Sigils of
    Enhancement and a lot of levels. Worth it only for Mythic (maybe Epic) gear.""")

# --- enchanting --------------------------------------------------------------------------
q("enchanting", "A Deeper Enchanting Table", deps="intro", icon="minecraft:enchanting_table", tier=2,
  tasks=adv("apothic_enchanting:30ench", title="Enchant at level 30 or higher"), desc="""
    &eApothic Enchanting&r gives the table three stats (hover a shelf to see what it adds):

    &aEterna&r: the max level. Each vanilla bookshelf gives 2, so 15 reach level 30.
    &cQuanta&r: randomness. More swing, up or down.
    &dArcana&r: rarer enchantments and more of them.

    The table can go past 30, all the way to &e100&r. Click the &e?&r in the table's screen to
    see which enchantments you can roll. Candles add Arcana, skulls add Quanta.""",
  rewards=[give("minecraft:lapis_lazuli", 32), give("minecraft:bookshelf", 4)])

q("hellshelf", "Hellshelves and Seashelves", deps=["enchanting", "welcome/nether"],
  icon="apothic_enchanting:hellshelf", tier=2, tasks=item("apothic_enchanting:hellshelf"), desc="""
    To get past level 30 you need better shelves. &eHellshelves&r (nether bricks, blaze rod,
    a potion of regeneration) or &eSeashelves&r (from the ocean) push Eterna to 45.

    Then &einfuse&r them: put a shelf in the enchanting table with enough stats and the third
    slot does an &eInfusion&r instead of an enchantment. Press &eR&r on an infused shelf to
    see the stats it needs.""",
  rewards=[give("minecraft:blaze_rod", 4), give("minecraft:nether_bricks", 16)])

q("infused", "Infusion", deps="hellshelf", icon="apothic_enchanting:infused_hellshelf", tier=3,
  tasks=item("apothic_enchanting:infused_hellshelf"), desc="""
    An &eInfused Hellshelf&r needs 45 Eterna and 30 Quanta at the table. Infused shelves
    upgrade into &eBlazing&r / &eGlowing&r Hellshelves (or Heart-Forged / Crystalline Seashelves)
    for level 60.

    After that: Deepshelves (deepslate, the Deep Dark, the Warden) for 80, and
    Endshelves (Dragon's Breath, a Dragon Head) for 100.""",
  rewards=[give("minecraft:experience_bottle", 24)])

q("library", "Enchantment Library", deps="enchanting", icon="apothic_enchanting:library", tier=3,
  optional=True, tasks=item("apothic_enchanting:library"), desc="""
    Feed spare enchanted books into an &eEnchantment Library&r: it stores them all in one
    block, and you take out the enchantment you need as a book.
    Put one in your base and give it every book you find.""",
  rewards=[give("minecraft:book", 16)])

# --- spawners ----------------------------------------------------------------------------
q("spawner", "Take the Spawner Home", deps="enchanting", icon="minecraft:spawner", tier=3,
  tasks=item("minecraft:spawner"), desc="""
    &eApothic Spawners&r: mine a dungeon spawner with a &eSilk Touch&r pickaxe to take it
    with you (it costs a big chunk of the pickaxe's durability).

    Mobs also have a small chance to drop their spawn egg with the &eCapturing&r enchantment.""",
  rewards=[give("minecraft:diamond", 2)])

q("spawner_mods", "Tune a Spawner", deps="spawner", icon="minecraft:clock", tier=3,
  tasks=adv("apothic_spawners:modifier", title="Modify a spawner"), desc="""
    Right-click a spawner with an item to change it:

    &eSugar&r / &eClock&r: spawns faster. &eFermented Spider Eye&r: more mobs per spawn.
    &eGhast Tear&r: more mobs allowed nearby. &ePiston&r: bigger spawn area.
    &eComparator&r: only runs on redstone. &eSoul Lantern&r: ignores light.

    Press &eU&r on the spawner to see every modifier. Hold Shift on the spawner's tooltip
    for its stats.""",
  rewards=[give("minecraft:sugar", 32), give("minecraft:fermented_spider_eye", 8)])

# --- cosmetics ---------------------------------------------------------------------------
q("cosmetic", "Looking Good", deps="intro", icon="minecraft:leather_chestplate", desc="""
    &eCosmetic Armor Reworked&r: your inventory has a &eCosmeticArmor&r button that opens a
    second set of armor slots. Whatever you put there is what other players &esee&r; your
    real armor still protects you.

    Wear your best-stat gear and still look the way you want.""",
  rewards=[give("minecraft:leather", 8)])

q("where_next", "Where Next?", deps=["better_combat", "affix", "enchanting"], icon="minecraft:compass",
  shape="diamond", desc="""
    Gear up, then go hunting:

    &cL_Ender's Cataclysm&r: the big boss line, and the key to late-game tech.
    &cIce and Fire&r: dragons, dragonsteel and other mythical beasts.
    &cBoss Hunter&r: bosses from many mods, all over the world.

    &dIron's Spells&r has its own Apotheosis gems and affixes for spellcasters.""")
