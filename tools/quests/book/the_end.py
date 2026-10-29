from dsl import *

C = chapter("the_end", "The End", group="explore", icon="minecraft:dragon_head",
            subtitle="Twelve eyes, a huge stronghold and the Ender Dragon")
q = C.quest

q("intro", "What is the End?", deps="nether/intro", icon="minecraft:end_stone", size=1.5,
  shape="gear", desc="""
    The End is a dark dimension of floating end-stone islands, home of the &5Ender Dragon&r.

    Getting there is a real quest in Strata. The portal is deep inside a giant
    &eIntegrated Stronghold&r, and it needs &e12 different magic eyes&r from
    &eEnd Remastered&r, taken from bosses, treasure rooms and your own workshops.

    This chapter tells you exactly where every eye is.""",
  rewards=[give("minecraft:ender_pearl", 4)])

q("eyes", "Not Your Usual Eyes", deps="intro", icon="endrem:old_eye", size=1.25, desc="""
    &cVanilla Eyes of Ender don't open the portal here&r (they're still an ingredient).

    The portal has &e12 frames&r, and each one needs a &edifferent&r End Remastered eye.
    You can get &e15 eyes&r, and every one has a &eguaranteed&r source. No lucky drops:

    &c5 from bosses&r: beat the keeper, take its eye.
    &e5 from places&r: one treasure chest in one kind of structure always holds the eye.
    &b2 you build&r: one on a Create assembly line, one with Ars Nouveau magic.
    &73 spares&r: crafted from mob drops, to use instead of eyes you can't or won't get.

    Everyone gets their own copy: every player who fights a boss gets its eye in their Boss
    Loot Bag, and treasure chests have loot for each player. One finished portal works for everyone.""",
  rewards=[give("minecraft:map", 2)])

q("legend", "The Sixteen Eyes", deps="eyes", icon="endrem:cryptic_eye", shape="hexagon", optional=True,
  tasks=check("I've heard the legend"), desc="""
    &oLong ago, the way to the End was sealed. Its sight was split into sixteen eyes and
    scattered across the world, each given to a keeper who would never give it up:
    a pharaoh and a pirate crew, kings and monsters, a forge and a frozen temple.

    &oSome were lost so completely that they can only be made again,
    by a machine that remembers Redstone, or by magic that remembers the Evoker.

    &oFifteen have been found. The sixteenth, the &5Cryptic Eye&r&o, never has.

    Hover over any eye: its tooltip says who keeps it.""",
  rewards=[xp(50)])

q("seekers", "Seeker's Compasses", deps="eyes", icon="minecraft:compass", tier=2, desc="""
    Exploring is free, but if you'd rather go straight there, craft a &eSeeker's Compass&r
    for that place (look up "Seeker's Compass" in EMI). Each one costs a compass,
    an Eye of Ender and something that fits the place.

    &eRight-click&r it: the needle turns toward the nearest place that holds that eye, and a
    message says roughly how far. No coordinates: follow the needle. Right-click again
    any time to aim it from where you are now. It only works in the Overworld.

    Compasses: Pharaoh's Tomb, Jungle Temple, Foundry, Pirate Ship, Frostbitten Temple
    and Ocean Monument. The &eExplorer's Compass&r can't find these places.

    For the boss lairs use &eCataclysm's eyes&r: throw one and it flies toward its lair
    (&6Eye of Flame&r: Ignis, &6Eye of Monstrous&r: the Netherite Monstrosity,
    &6Eye of Mech&r: the Harbinger). See the Cataclysm chapter.""")

# --- bosses: always drop their eye ---------------------------------------------------------
q("eye_guardian", "Guardian Eye", deps="eyes", icon="endrem:guardian_eye", tier=3,
  tasks=item("endrem:guardian_eye"), desc="""
    &o"It has seen many warriors drown."

    Every &eElder Guardian&r drops a &eGuardian Eye&r. Each &eocean monument&r has three of
    them, so a group can take one each (only the player who kills it gets the eye).

    Bring &eWater Breathing&r, &eNight Vision&r and milk for their Mining Fatigue.
    Find a monument with a &eSeeker's Compass: Ocean Monument&r, a cartographer's
    Ocean Explorer Map, or by sailing the deep ocean. The easiest boss eye.""")

q("eye_wither", "Wither Eye", deps="eyes", icon="endrem:wither_eye", tier=4,
  tasks=item("endrem:wither_eye"), desc="""
    &o"Has witnessed destruction. Maybe it also witnessed your stuff disappear."

    &5The Wither&r always drops a &eWither Eye&r, one for everyone who fights it.
    Build it from 4 soul sand in a T with 3 &ewither skeleton skulls&r on top
    (wither skeletons in Nether fortresses drop the skulls).

    Summon it far from home: it blows up everything around it.""")

q("eye_cursed", "Cursed Eye", deps="eyes", icon="endrem:cursed_eye", tier=4,
  tasks=item("endrem:cursed_eye"), desc="""
    &o"Ignis swore to guard it, and the oath burned itself into him."

    &6Ignis&r, the burning knight of the &cBurning Arena&r (Nether), always drops the
    &eCursed Eye&r, one for everyone who fights him. Find the arena with an &6Eye of Flame&r;
    the &eCataclysm&r chapter shows how to call him up.""")

q("eye_nether", "Nether Eye", deps="eyes", icon="endrem:nether_eye", tier=4,
  tasks=item("endrem:nether_eye"), desc="""
    &o"Lost by a demon in the war between the Aether and the Nether."

    The &cNetherite Monstrosity&r keeps it locked in its forge-heart. It lives in the
    &cSoul Black Smith&r in the Nether: find it with an &6Eye of Monstrous&r.
    It always drops the &eNether Eye&r, one for everyone who fights it.""")

q("eye_corrupted", "Corrupted Eye", deps="eyes", icon="endrem:corrupted_eye", tier=5,
  tasks=item("endrem:corrupted_eye"), desc="""
    &o"The eye of a greedy king, wired into the Harbinger by those who wanted his fortune."

    &7The Harbinger&r sleeps deep in the &7Ancient Factory&r (find it with an &6Eye of Mech&r)
    and only wakes for a &eNether Star&r, so beat the Wither first. It always drops the
    &eCorrupted Eye&r, one for everyone who fights it. The hardest eye of all.""")

# --- places: one treasure chest always holds the eye ---------------------------------------
q("eye_old", "Old Eye", deps="eyes", icon="endrem:old_eye", tier=3,
  tasks=item("endrem:old_eye"), desc="""
    &o"Buried with the Pharaoh, who swore to watch over the desert until the end of days."

    Every &edesert temple&r hides a &ePharaoh's Tomb&r: a throne room deep inside, with
    the Pharaoh's two treasure chests. Both always hold an &eOld Eye&r.
    The temple gives you &cMining Fatigue&r, so you can't dig around its traps:
    find the way in. Seeker's Compass: &ePharaoh's Tomb&r (gold and sandstone).""")

q("eye_evil", "Evil Eye", deps="eyes", icon="endrem:evil_eye", tier=3,
  tasks=item("endrem:evil_eye"), desc="""
    &o"A holy talisman against bad luck, hidden behind a hundred traps."

    Every &ejungle temple&r has one &etreasure room&r, past arrow traps, pits and a lever
    puzzle. Its chest always holds an &eEvil Eye&r.
    Seeker's Compass: &eJungle Temple&r (emeralds and mossy cobblestone).""")

q("eye_lost", "Lost Eye", deps="eyes", icon="endrem:lost_eye", tier=3,
  tasks=item("endrem:lost_eye"), desc="""
    &o"Forged by the first blacksmiths in the fires of the Foundry."

    The &cFoundry&r is a huge underground forge-dungeon (When Dungeons Arise), full of lava,
    furnaces and its old workers. Its &etreasure chests&r, in the big crossing halls,
    always hold a &eLost Eye&r. Bring fire resistance.
    Seeker's Compass: &eFoundry&r (iron and blast furnaces).""")

q("eye_black", "Black Eye", deps="eyes", icon="endrem:black_eye", tier=3,
  tasks=item("endrem:black_eye"), desc="""
    &o"It gave sight to the legendary Black Pearl. Pirate captains still fight over it."

    Pirates sail the oceans: the &eCorsair Corvette&r, the &ePirate Junk&r and the ghostly
    &eUndead Pirate Ship&r. The captain's &etreasure chests&r always hold a &eBlack Eye&r.
    Expect a crew that shoots back. Seeker's Compass: &ePirate Ship&r (gold and boats).""")

q("eye_cold", "Cold Eye", deps="eyes", icon="endrem:cold_eye", tier=3,
  tasks=item("endrem:cold_eye"), desc="""
    &o"The Iceologers sealed it in ice before they vanished."

    The &bFrostbitten Temple&r in the snowy lands always holds a &eCold Eye&r in its
    treasure chest, but the &bFrostbitten Golem&r guards it.
    &eIgloos&r: about half of them hide a cellar (break the carpet in the floor to find
    the trapdoor), and that chest also holds a Cold Eye.
    Seeker's Compass: &eFrostbitten Temple&r (blue ice and snow).""")

# --- built: Create and Ars Nouveau ---------------------------------------------------------
q("rogue_assembly", "Red-Hot Rogue Eye", deps="eyes", icon="strata:red_hot_rogue_eye", tier=3,
  tasks=item("strata:red_hot_rogue_eye"), desc="""
    &o"The machine eye that taught our ancestors Redstone. Only a working factory can forge another."

    The Rogue Eye is lost; you have to &eforge&r one on a Create &eSequenced Assembly&r line.
    Put an &eEye of Ender&r on a belt and run it past these machines, in this order, &etwice&r:

    1. &eDeployer&r holding a &ePrecision Mechanism&r
    2. &eDeployer&r holding an &eElectron Tube&r
    3. &eSpout&r with &e250 mB of lava&r (it heats the metal)
    4. &eMechanical Press&r

    It comes off the line as a glowing &6Red-Hot Rogue Eye&r. Press &eR&r on it in EMI to see the steps,
    and hold &eW&r over each machine for its Ponder scene. You'll need 2 of each part per eye.""")

q("eye_rogue", "Rogue Eye", deps="rogue_assembly", icon="endrem:rogue_eye", tier=3,
  tasks=item("endrem:rogue_eye"), desc="""
    Hot metal is still soft. &eHarden&r it the way smiths harden steel: &bquench&r it in water.

    Put &bwater&r (a source block or a flowing stream) in front of an &eEncased Fan&r and run the
    fan: its air stream past the water washes everything in it (Create's "Bulk Washing").
    Drop the Red-Hot Rogue Eye into the stream, or run a belt through it, and it hisses
    and hardens into the &eRogue Eye&r.""")

q("magical_binding", "Dormant Magical Eye", deps="eyes", icon="strata:dormant_magical_eye", tier=3,
  tasks=item("strata:dormant_magical_eye"), desc="""
    &o"Without this eye the Evoker has no power."

    The Magical Eye was lost with the Evokers' magic. &eBind&r a new one on Ars Nouveau's
    &eEnchanting Apparatus&r: an &eEye of Ender&r on the apparatus, and on the &eArcane
    Pedestals&r around it:

    the 7 essences (&cFire&r, &9Water&r, &2Earth&r, &fAir&r, &bAbjuration&r, &dConjuration&r,
    &6Manipulation&r) and a &eSource Gem Block&r.

    It uses &e5,000 source&r from nearby Source Jars and gives a &eDormant Magical Eye&r.
    Press &eR&r on it in EMI to see the recipe.""")

q("eye_magical", "Magical Eye", deps="magical_binding", icon="endrem:magical_eye", tier=3,
  tasks=item("endrem:magical_eye"), desc="""
    Now &ewake&r it. Put the Dormant Magical Eye in an &eImbuement Chamber&r, with
    &eArcane Pedestals&r next to the chamber holding an &eAmethyst Cluster&r, a &eGhast Tear&r
    and a &eSource Gem Block&r.

    The chamber slowly draws &e5,000 source&r from nearby Source Jars. When it's full,
    the eye opens: the &eMagical Eye&r.""")

# --- spares ------------------------------------------------------------------------------
q("spare_eyes", "Spare Eyes", deps="eyes", icon="endrem:exotic_eye", tier=2, optional=True,
  tasks=[item("endrem:undead_eye"), item("endrem:witch_eye"), item("endrem:exotic_eye")], desc="""
    Three eyes have nothing to guard them, so anyone can make them. Use them in place of
    any eyes you can't or won't get (a boss you'd rather skip, say). You only need 12.

    &eUndead Eye&r: an &eUndead Soul&r (skeleton horses drop them) with a phantom membrane,
    a bone, rotten flesh and a ghast tear.
    &eWitch Eye&r: an Eye of Ender and a &eWitch Pupil&r (witches drop them).
    &eExotic Eye&r: an Eye of Ender with two conduits, two glow ink sacs and four corals.

    Press &eR&r on an eye in EMI for its recipe.""")

# --- the stronghold ---------------------------------------------------------------------
q("stronghold", "Integrated Stronghold", deps="eyes", icon="minecraft:stone_bricks", tier=3,
  tasks=structure("integrated_stronghold:stronghold", title="Find the stronghold"), desc="""
    Since eyes don't fly, use the &eExplorer's Compass&r to find the stronghold.
    You don't need the eyes to go in: find it early and come back with them.

    &eIntegrated Stronghold&r is &chuge&r: libraries, prisons, halls and
    Create-powered puzzles and traps. Bring lots of torches, food and friends,
    and set waypoints as you go so you can find the way out.""",
  rewards=[give("minecraft:torch", 64)])

q("portal", "Twelve Eyes", deps="stronghold", icon="endrem:ancient_portal_frame", tier=4,
  tasks=dim("minecraft:the_end", title="Enter the End"), desc="""
    Deep inside, the portal room has a ring of &e12 Ancient Portal Frames&r.
    Put a &edifferent&r End Remastered eye in each frame (any 12 of the 15).
    When all 12 are in, the portal opens, for everyone.

    &cThere's no easy way back&r until you beat the dragon (or die). Bring a bed? No!
    Beds explode in the End. Bring blocks, a bow, potions and a pumpkin
    to wear so endermen leave you alone.""")

q("dragon", "The Ender Dragon", deps="portal", icon="minecraft:dragon_head", tier=5, size=1.5,
  shape="diamond", tasks=kill("minecraft:ender_dragon"), desc="""
    The dragon heals from the &dEnd Crystals&r on top of the obsidian towers.
    Shoot or break the crystals first (some are in cages), then fight the dragon when it
    lands on the portal. &eYUNG's Better End Island&r makes the main island and its
    towers grander than usual.

    Bring your friends: the dragon is the first real group fight.""",
  rewards=[give("minecraft:diamond_block", 2)])

q("master", "Dragonslayer", deps="dragon", icon="minecraft:wither_skeleton_skull", desc="""
    The dragon's defeat opens the way to the late game:
    the &5Pinnacle&r World Tier needs a Dragon kill, and &eDraconic Evolution&r's top cores need
    its dragon heart.

    Upgrade your gear, use Apotheosis gems and affixes, and keep your armor repaired.""",
  rewards=[give("minecraft:totem_of_undying")])

# --- the outer islands ------------------------------------------------------------------
q("outer", "The Outer Islands", deps="dragon", icon="minecraft:chorus_flower", tier=3,
  tasks=biome("nullscape:crystal_peaks", title="Visit the Crystal Peaks"), desc="""
    After the dragon dies, small &eEnd Gateways&r appear around the main island.
    Throw an ender pearl into one to reach the outer islands.

    &eNullscape&r reshapes the outer End: tall crystal peaks, void barrens and dark
    shadowlands. Chorus fruit teleports you a short way when eaten.""",
  rewards=[give("minecraft:ender_pearl", 8)])

q("mes", "Moog's End Structures", deps="outer", icon="minecraft:purpur_block", tier=2, desc="""
    The outer islands are dotted with &eMoog's End Structures&r: spires, towers, gardens,
    shrines and even crashed sky ships.

    The &bKakuto Region&r's psychic and dragon gyms are out here in the End too!""")

q("end_city", "End City", deps="outer", icon="minecraft:purpur_pillar", tier=4,
  tasks=structure("minecraft:end_city", title="Explore an End City"), desc="""
    Tall purple towers full of &eshulkers&r. Their bullets make you float, so fight near
    the ground or keep milk handy.

    Some End Cities have an &eEnd Ship&r floating next to them. That's where the
    &eElytra&r is.""",
  rewards=[give("minecraft:milk_bucket")])

q("shulker", "Shulker Boxes", deps="end_city", icon="minecraft:shulker_shell", tier=3,
  tasks=item("minecraft:shulker_box"), desc="""
    Shulkers drop &eShulker Shells&r. Two shells and a chest make a &eShulker Box&r:
    a chest that keeps its items when you break it.""")

q("elytra", "Elytra", deps="end_city", icon="minecraft:elytra", tier=4,
  tasks=item("minecraft:elytra"), desc="""
    The &eElytra&r lets you glide, and &efirework rockets&r boost you through the air.

    It &ccosts&r you: every flight wears down its durability, and every boost burns a rocket.
    Repair it with &ephantom membranes&r at an anvil (or Mending).
    Gliding is a fast way to travel, but airships still carry your friends and cargo.""")

q("where_next", "Where Next?", deps="dragon", icon="minecraft:compass", shape="hexagon", tier=2,
  desc="""
    The End is beaten, but the pack isn't:

    &cBosses & Combat&r: the &5Ender Guardian&r (Cataclysm) drops the Void Core for the biggest storage.
    &bAd Astra&r: rockets to other planets.
    &bTech&r: the late tiers of Mekanism, AE2 and Draconic Evolution.""")
