from dsl import *

C = chapter("ice_and_fire", "Ice and Fire", group="bosses", icon="iceandfire:dragon_skull_fire",
            subtitle="Dragons, dragonsteel and mythical beasts")
q = C.quest

q("intro", "What is Ice and Fire?", icon="iceandfire:dragonscales_red", size=1.5, shape="gear", desc="""
    &cIce and Fire&r fills the world with mythical creatures: &cfire&r, &bice&r and
    &elightning&r dragons, hydras, cyclopes, gorgons, sea serpents, sirens and more.

    Dragons are the big prize: their bones, blood and scales make the strongest gear here.
    They are also &cvery&r dangerous, and they burn, freeze and smash terrain.
    Don't build your base next to a roost.""",
  rewards=[give("minecraft:bread", 16)])

q("bestiary", "The Bestiary", deps="intro", icon="iceandfire:bestiary",
  tasks=item("iceandfire:bestiary"), desc="""
    &eManuscripts&r turn up in Ice and Fire lairs and chests. Three make a &eBestiary&r:
    a guide to every creature, how to fight it, and what it drops.

    More manuscripts unlock more pages: put the Bestiary and manuscripts into a
    &eBestiary Lectern&r.""",
  rewards=[give("minecraft:paper", 16)])

q("dragons", "Here Be Dragons", deps="intro", icon="iceandfire:dragon_skull_ice", tier=2, desc="""
    Dragons grow through &e5 stages&r. Most dragons you meet are &estage 3&r, living in
    &eroosts&r on the surface: piles of gold, scorched or frozen ground, bones.

    Older stage 4 and 5 dragons sleep in big &ecaves&r underground with their treasure,
    and female dragons guard their eggs there. Those are much harder.

    &cFire&r: deserts, jungles, savannas, badlands, plains and meadows.
    &bIce&r: snowy and frozen biomes. &eLightning&r: swamps, jungles, badlands, savannas.

    Bring fire or frost resistance, a bow, and lots of food.""",
  rewards=[give("minecraft:arrow", 64), give("minecraft:golden_carrot", 16)])

q("slay_fire", "Slay a Fire Dragon", deps="dragons", icon="iceandfire:fire_dragon_blood", tier=4,
  shape="hexagon", tasks=kill("iceandfire:fire_dragon"), desc="""
    Fire dragons breathe a stream of flame and, from stage 3, throw fire charges.
    Potions of fire resistance help. Watch for wind-ups: the tail slam and the breath
    both charge before they hit.""",
  rewards=[give("minecraft:diamond", 6)])

q("slay_ice", "Slay an Ice Dragon", deps="dragons", icon="iceandfire:ice_dragon_blood", tier=4,
  shape="hexagon", tasks=kill("iceandfire:ice_dragon"), desc="""
    Ice dragons breathe frost that can freeze you solid. Keep moving and keep your distance
    when they inhale.""",
  rewards=[give("minecraft:diamond", 6)])

q("slay_lightning", "Slay a Lightning Dragon", deps="dragons", icon="iceandfire:lightning_dragon_blood",
  tier=4, shape="hexagon", tasks=kill("iceandfire:lightning_dragon"), desc="""
    Lightning dragons strike with lightning instead of flame. Fight them away from your base.""",
  rewards=[give("minecraft:diamond", 6)])

q("spoils", "Dragon Spoils", deps=["slay_fire", "slay_ice", "slay_lightning"], any_dep=True,
  icon="iceandfire:dragonbone", tier=3, tasks=item("iceandfire:dragonbone", 16), desc="""
    A dead dragon drops &eDragon Bones&r, &eScales&r, its &eBlood&r, &eFlesh&r, its &eHeart&r
    and its &eSkull&r. Keep everything:

    &eBones&r: Dragon Bone tools and the bow, and the forge.
    &eScales&r: dragon scale armor.
    &eBlood&r: elemental Dragon Bone swords, and dragonsteel.
    &eHeart&r: the heart of a dragon forge.""",
  rewards=[give("minecraft:iron_ingot", 16)])

q("bone_sword", "Dragon Bone Sword", deps="spoils", icon="iceandfire:dragonbone_sword_fire", tier=3,
  optional=True, tasks=item("iceandfire:dragonbone_sword"), desc="""
    Craft a &eDragon Bone Sword&r, then add dragon blood to it (shapeless) for a
    &cFlamed&r, &bIced&r or &eLightning&r version with an elemental bite.""")

q("dragonforge", "The Dragon Forge", deps="spoils", icon="iceandfire:dragonforge_fire_core_disabled",
  tier=3, desc="""
    A &eDragon Forge&r turns iron into &6dragonsteel&r. You need, all of one element:

    &e1 forge core&r (8 forge bricks around a dragon heart), &e1 aperture&r (bricks + iron),
    &e8 blocks of dragon bone&r and &e17 forge bricks&r (stone bricks + scale blocks).
    The Bestiary's Dragonforge pages show the 3-layer build.

    It runs on &edragon breath&r: put a tame dragon, or a wild one held with &eChain Lines&r
    on a Dragon Bone Wall, right in front of the aperture.""",
  rewards=[give("minecraft:stone_bricks", 32), give("minecraft:iron_block", 2)])

q("steel_fire", "Fire Dragonsteel", deps="dragonforge", icon="iceandfire:dragonsteel_fire_ingot", tier=4,
  optional=True, tasks=item("iceandfire:dragonsteel_fire_ingot"), desc="""
    Iron ingot + &cFire Dragon Blood&r in a fire forge. Fire dragonsteel sets attackers
    aflame and knocks them far back.""",
  rewards=[give("minecraft:iron_ingot", 16)])

q("steel_ice", "Ice Dragonsteel", deps="dragonforge", icon="iceandfire:dragonsteel_ice_ingot", tier=4,
  optional=True, tasks=item("iceandfire:dragonsteel_ice_ingot"), desc="""
    Iron ingot + &bIce Dragon Blood&r in an ice forge. Ice dragonsteel freezes targets
    in a block of ice.""",
  rewards=[give("minecraft:iron_ingot", 16)])

q("steel_lightning", "Lightning Dragonsteel", deps="dragonforge", icon="iceandfire:dragonsteel_lightning_ingot",
  tier=4, optional=True, tasks=item("iceandfire:dragonsteel_lightning_ingot"), desc="""
    Iron ingot + &eLightning Dragon Blood&r in a lightning forge.

    All dragonsteel armor also protects you well against dragon breath.""",
  rewards=[give("minecraft:iron_ingot", 16)])

# --- raising a dragon --------------------------------------------------------------------
q("eggs", "A Clutch of Eggs", deps="dragons", icon="iceandfire:dragonegg_red", tier=2, desc="""
    Female dragons in &ecaves&r guard their eggs. Beat the mother (a stage 4 or 5 dragon)
    and take one home.

    &cFire&r egg: place it on a fire that keeps burning (netherrack).
    &bIce&r egg: place it in water.
    &eLightning&r egg: under open sky, in the rain.

    It takes a long while. The baby belongs to whoever placed the egg.""")

q("raise", "Raising a Dragon", deps="eggs", icon="iceandfire:dragon_meal", tier=3,
  tasks=item("iceandfire:dragon_meal"), desc="""
    Baby dragons eat meat. &eDragon Meal&r (bones and meat) makes them grow much faster.
    Right-click your dragon to see its age, stage and hunger.

    A &eDragon Command Staff&r (a dragon skull on sticks) tells it to stay or wander.
    Two grown tame dragons can even be bred for more eggs (see the Bestiary).""",
  rewards=[give("minecraft:cooked_mutton", 32), give("minecraft:bone", 32)])

q("dragon_rider", "Dragon Rider", deps=["raise", "the_end/dragon"], icon="iceandfire:dragon_horn",
  tier=5, size=1.5, shape="hexagon", desc="""
    Riding a dragon is the reward at the very end of this road: a dragon you hatched,
    fed and raised to full size yourself, after the Ender Dragon has fallen.

    Sneak and right-click a big enough tame dragon to mount it. Jump to take off,
    sneak to come down; your breath-attack key is in Options > Controls.

    A dragon gets hungry, and even a tame one wrecks the land where it fights.
    In Strata, dragons are the late-game mount, not a shortcut.""")

# --- other creatures ---------------------------------------------------------------------
q("bestiary_beasts", "Other Beasts", deps="bestiary", icon="iceandfire:troll_tusk", desc="""
    Dragons aren't alone. The Bestiary covers all of these:

    &eHydra&r in swamp hills, &eCyclopes&r in sea caves on beaches, &eGorgons&r under
    beach temples, &eSea Serpents&r in the ocean, &eSirens&r on ocean rocks, &eDread&r undead
    from frozen Mausoleums, plus trolls, death worms, cockatrices, stymphalian birds,
    pixies and hippogryphs.

    Silver ore (for silver weapons, great against undead) and sapphires are new ores too.""")

q("hydra", "The Hydra", deps="bestiary_beasts", icon="iceandfire:hydra_heart", tier=4, shape="hexagon",
  tasks=kill("iceandfire:hydra"), desc="""
    Cut off a head and two grow back, unless the Hydra is &con fire&r. Burning stops the
    regrowth and its healing. It only dies with one head left.

    &6Drops:&r Hydra Fangs (life-stealing poison arrows) and the &eHydra Heart&r, which heals
    you more the more hurt you are, just by sitting in your hotbar.""",
  rewards=[give("minecraft:flint_and_steel"), give("minecraft:fire_charge", 16)])

q("cyclops", "The Cyclops", deps="bestiary_beasts", icon="iceandfire:cyclops_eye", tier=4, shape="hexagon",
  tasks=kill("iceandfire:cyclops"), desc="""
    A giant shepherd in a beach cave. One bite can kill. Shoot it in the &eeye&r to blind it,
    or sneak up wearing &eSheep Disguise&r armor.

    &6Drops:&r the &eEye of Cyclops&r and its skull.""",
  rewards=[give("minecraft:white_wool", 16)])

q("gorgon", "The Gorgon", deps="bestiary_beasts", icon="iceandfire:gorgon_head", tier=4, shape="hexagon",
  tasks=kill("iceandfire:gorgon"), desc="""
    &cDon't look at her eyes&r: her gaze turns you to stone. She waits under a temple on
    the shore, behind a trapdoor opened by hidden switches.

    Wear a &eBlindfold&r. Her head turns any creature you point it at to stone, once.""",
  rewards=[give("minecraft:golden_apple", 2)])

q("sea_serpent", "Sea Serpent", deps="bestiary_beasts", icon="iceandfire:sea_serpent_fang", tier=4,
  shape="hexagon", tasks=kill("iceandfire:sea_serpent"), desc="""
    Fast, savage, and happy to leap out of the water at your boat.

    &6Drops:&r scales and fangs: &eTide Guardian&r armor (water breathing, and more strength
    in water) and arrows that fly through water.""",
  rewards=[give("minecraft:prismarine_crystals", 16)])

q("dread_lich", "The Dread Lich", deps="bestiary_beasts", icon="iceandfire:dread_key", tier=4,
  shape="hexagon", tasks=kill("iceandfire:dread_lich"), desc="""
    In the coldest lands, &eMausoleums&r of unbreakable Dreadstone hold an ancient evil.
    Dread Liches roam outside, summoning thralls, ghouls and beasts.

    A Lich sometimes drops a &eGravemaster's Key&r, which opens a Mausoleum's gate.""",
  rewards=[give("iceandfire:silver_ingot", 8)])

q("where_next", "Where Next?", deps=["spoils", "bestiary_beasts"], any_dep=True, icon="minecraft:compass",
  shape="diamond", desc="""
    &cCombat & Gear&r: socket gems into your dragonsteel.
    &cL_Ender's Cataclysm&r and &cBoss Hunter&r: more giant fights.
    &5The End&r: the Ender Dragon, which you need before riding your own.""")
