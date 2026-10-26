from dsl import *

C = chapter("the_end", "The End", group="explore", icon="minecraft:dragon_head",
            subtitle="Twelve eyes, a huge stronghold and the Ender Dragon")
q = C.quest

q("intro", "What is the End?", deps="nether/intro", icon="minecraft:end_stone", size=1.5,
  shape="gear", desc="""
    The End is a dark dimension of floating end-stone islands, home of the &5Ender Dragon&r.

    Getting there is a real quest in Strata. The portal is deep inside a giant
    &eIntegrated Stronghold&r, and it needs &e12 different magic eyes&r from
    &eEnd Remastered&r, gathered from all over the world.

    This chapter tells you where every eye comes from.""",
  rewards=[give("minecraft:ender_pearl", 4)])

q("eyes", "Not Your Usual Eyes", deps="intro", icon="endrem:old_eye", desc="""
    &cVanilla Eyes of Ender don't work here.&r They can't open the portal and won't fly
    toward the stronghold when thrown.

    Instead there are &e16 different End Remastered eyes&r. You need &e12 different ones&r:
    one for each of the 12 frames around the portal.
    The quests below show where to find them. Collect as a team!""",
  rewards=[give("minecraft:map", 2)])

# --- the eyes ---------------------------------------------------------------------------
q("temple_eyes", "Eyes of the Old World", deps="eyes", icon="endrem:old_eye", tier=3, optional=True,
  tasks=[item("endrem:old_eye"), item("endrem:rogue_eye"), item("endrem:lost_eye")], desc="""
    &eOld Eye&r: desert temple chests and dungeon chests.
    &eRogue Eye&r: jungle temple chests.
    &eLost Eye&r: mineshaft chests and dungeon chests.

    YUNG's desert temples, jungle temples and dungeons count.""")

q("coast_eyes", "Eyes of Sea and Snow", deps="eyes", icon="endrem:black_eye", tier=3, optional=True,
  tasks=[item("endrem:black_eye"), item("endrem:cold_eye"), item("endrem:corrupted_eye")], desc="""
    &eBlack Eye&r: buried treasure and shipwreck treasure chests (treasure maps help!).
    &eCold Eye&r: igloo chests (check for the hidden basement).
    &eCorrupted Eye&r: pillager outpost chests.""")

q("nether_eyes", "Eyes of the Nether", deps="eyes", icon="endrem:nether_eye", tier=3, optional=True,
  tasks=[item("endrem:nether_eye"), item("endrem:cursed_eye")], desc="""
    &eNether Eye&r: Nether fortress chests.
    &eCursed Eye&r: the treasure room of a bastion remnant.

    See the &cThe Nether&r chapter for both places.""")

q("monster_eyes", "Eyes of the Mighty", deps="eyes", icon="endrem:wither_eye", tier=4,
  optional=True, tasks=[item("endrem:magical_eye"), item("endrem:guardian_eye"),
                        item("endrem:wither_eye")], desc="""
    &eMagical Eye&r: dropped by &eEvokers&r (woodland mansions and raids), and found in
    woodland mansion chests.
    &eGuardian Eye&r: dropped by the &eElder Guardian&r in ocean monuments.
    &eWither Eye&r: dropped by &5the Wither&r.""")

q("crafted_eyes", "Eyes You Make", deps="eyes", icon="endrem:exotic_eye", tier=3, optional=True,
  tasks=[item("endrem:witch_eye"), item("endrem:undead_eye"), item("endrem:exotic_eye")], desc="""
    &eWitch Eye&r: an Eye of Ender plus a &eWitch Pupil&r (witches drop them).
    &eUndead Eye&r: an &eUndead Soul&r (from skeleton horses) with a phantom membrane,
    bone, rotten flesh and ghast tear.
    &eExotic Eye&r: an Eye of Ender with two &econduits&r, two glow ink sacs and four corals.

    So vanilla eyes are still useful as an ingredient! Press &eR&r on an eye for its recipe.""")

q("odd_eyes", "Strange Eyes", deps="eyes", icon="endrem:evil_eye", tier=3, optional=True,
  tasks=[item("endrem:evil_eye"), item("endrem:cryptic_eye")], desc="""
    &eEvil Eye&r: some &eCleric&r villagers sell one (emeralds and a rabbit's foot).
    &eCryptic Eye&r: very rarely appears in your inventory when you &eenchant&r
    something at an enchanting table. Keep enchanting!""")

# --- the stronghold ---------------------------------------------------------------------
q("stronghold", "Integrated Stronghold", deps="eyes", icon="minecraft:stone_bricks", tier=3,
  tasks=structure("integrated_stronghold:stronghold", title="Find the stronghold"), desc="""
    Since eyes don't fly, use the &eExplorer's Compass&r to find the stronghold.

    &eIntegrated Stronghold&r is &chuge&r: libraries, prisons, halls and
    Create-powered puzzles and traps. Bring lots of torches, food and friends,
    and set waypoints as you go so you can find the way out.""",
  rewards=[give("minecraft:torch", 64)])

q("portal", "Twelve Eyes", deps="stronghold", icon="endrem:ancient_portal_frame", tier=4,
  tasks=dim("minecraft:the_end", title="Enter the End"), desc="""
    Deep inside, the portal room has a ring of &e12 Ancient Portal Frames&r.
    Put a &edifferent&r End Remastered eye in each frame. When all 12 are in, the portal opens.

    &cThere's no easy way back&r until you beat the dragon (or die). Bring a bed? No!
    Beds explode in the End. Bring blocks, a bow, potions and a pumpkin
    to wear so endermen leave you alone.""")

q("dragon", "The Ender Dragon", deps="portal", icon="minecraft:dragon_head", tier=5, size=1.5,
  shape="diamond", tasks=kill("minecraft:ender_dragon"), desc="""
    The dragon heals from the &dEnd Crystals&r on top of the obsidian towers.
    Shoot or break the crystals first (some are in cages), then fight the dragon when it
    lands on the portal. &eYUNG's Better End Island&r makes the main island and its
    towers grander than usual.

    &cWhen the dragon dies, the whole server moves to Master difficulty.&r
    Regular mobs everywhere get much tougher. Bosses stay as they are.
    Make sure your friends are ready before you strike the final blow!""",
  rewards=[give("minecraft:diamond_block", 2)])

q("master", "Master Mode", deps="dragon", icon="minecraft:wither_skeleton_skull", desc="""
    You're in &cMaster&r difficulty now. Upgrade your gear, use Apotheosis gems and
    affixes, and keep your armor repaired.

    The dragon's defeat also opens the way to the late game: top-tier Draconic Evolution
    and Extended Crafting recipes need it (with a Cataclysm boss).""",
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

    &cBosses & Combat&r: the &5Ender Guardian&r (Cataclysm) unlocks cross-dimension wireless.
    &bAd Astra&r: rockets to other planets.
    &bTech&r: the late tiers of Mekanism, AE2 and Draconic Evolution.""")
