from dsl import *

C = chapter("nether", "The Nether", group="explore", icon="minecraft:netherrack",
            subtitle="Fire, fortresses and netherite")
q = C.quest

q("intro", "What is the Nether?", deps="welcome/nether", icon="minecraft:netherrack", size=1.5,
  shape="gear", desc="""
    The Nether is a burning underworld under a ceiling of rock. In Strata it's much richer:
    &eIncendium&r and &eEternal Nether&r add new biomes, mobs and big structures,
    and &eYUNG's&r rebuilds the Nether fortresses.

    Bring: a stack of blocks, food, a bow, and a &eflint and steel&r to relight your portal.
    Lava is everywhere. Fire resistance potions are your best friend.""",
  rewards=[give("minecraft:cooked_beef", 16), give("minecraft:flint_and_steel")])

q("expert", "Tougher Down Here", deps="intro", icon="minecraft:skeleton_skull", desc="""
    The Nether is a step up from home: wither skeletons, blazes, ghasts and the mobs from
    &eIncendium&r and &eEternal Nether&r hit harder than anything in the Overworld.

    Upgrade your armor soon, and keep a shield in your off-hand.
    Your own &eWorld Tier&r (Alt+L) still decides how tough mobs around you get.""",
  rewards=[give("minecraft:golden_apple", 2)])

q("gold", "Piglin Manners", deps="intro", icon="minecraft:golden_helmet",
  tasks=item("minecraft:golden_helmet"), desc="""
    Piglins attack anyone not wearing &6gold&r. One piece of gold armor keeps most of them calm.
    Don't open their chests or mine gold near them, though!

    Toss them a gold ingot to barter for random goodies.""",
  rewards=[give("minecraft:gold_ingot", 8)])

q("ruined_portals", "Ruined Portals", deps="intro", icon="minecraft:crying_obsidian", desc="""
    Broken portals are scattered through the Overworld and the Nether, and &eHopo's Better
    Ruined Portals&r makes them bigger and more interesting.

    Their chests often have gold, and the leftover obsidian helps you build a second portal.""",
  rewards=[give("minecraft:obsidian", 10)])

# --- fortresses -------------------------------------------------------------------------
q("fortress", "Better Nether Fortress", deps="expert", icon="minecraft:nether_bricks", tier=3,
  tasks=structure("betterfortresses:fortress", title="Explore a Nether fortress"), desc="""
    &eYUNG's Better Nether Fortresses&r are huge brick mazes with bridges, towers and halls.
    Blazes and wither skeletons live here.

    The wither skeletons here drop the skulls that summon &5the Wither&r, keeper of the Wither Eye.""",
  rewards=[give("minecraft:golden_carrot", 16)])

q("blaze", "Blaze Rods", deps="fortress", icon="minecraft:blaze_rod", tier=2,
  tasks=item("minecraft:blaze_rod", 8), desc="""
    Blazes float around fortresses shooting fireballs. Snowballs hurt them a lot!

    Blaze rods make brewing stands and blaze powder. Fire resistance potions
    (magma cream + awkward potion) make the Nether much easier.""",
  rewards=[give("minecraft:magma_cream", 4), give("minecraft:nether_wart", 8)])

q("wither_skulls", "Skulls of the Wither", deps="fortress", icon="minecraft:wither_skeleton_skull",
  tier=3, optional=True, tasks=item("minecraft:wither_skeleton_skull", 3), desc="""
    Wither skeletons sometimes drop their skull. Three skulls and four soul sand
    summon &5the Wither&r, a dangerous boss. Fight it far from your base!

    It drops a Nether Star, and it can drop a &5Wither Eye&r for the End portal.""",
  rewards=[give("minecraft:soul_sand", 4)])

q("bastion", "Bastion Remnants", deps="gold", icon="minecraft:gilded_blackstone", tier=3,
  tasks=structure("minecraft:bastion_remnant", title="Find a bastion"), desc="""
    Bastions are piglin castles full of gold, and full of angry piglin brutes.

    The treasure room can hold a &5Cursed Eye&r for the End portal,
    and bastion chests are where you find the &eNetherite Upgrade&r smithing template.""",
  rewards=[give("minecraft:gold_block", 2)])

# --- new places -------------------------------------------------------------------------
q("incendium", "Incendium", deps="expert", icon="minecraft:crimson_nylium",
  tasks=biome("incendium:withered_forest", title="Visit a Withered Forest"), desc="""
    &eIncendium&r rebuilds the Nether's biomes: withered forests, volcanic deltas, ash barrens,
    toxic heaps, quartz flats and more. Each has its own look and dangers.

    Use the &eNature's Compass&r here too.""",
  rewards=[give("minecraft:glowstone", 8)])

q("castle", "The Forbidden Castle", deps="incendium", icon="minecraft:red_nether_bricks", tier=4,
  tasks=structure("incendium:forbidden_castle", title="Enter the Forbidden Castle"), desc="""
    Incendium's biggest structure. Its halls are packed with tough enemies and great loot.
    Go with friends and plenty of potions.

    Other Incendium places to find: the Sanctum, the Nether Reactor, the Infernal Altar
    and piglin villages.""")

q("citadel", "Eternal Nether: The Citadel", deps="incendium", icon="eternalnether:warped_nether_bricks",
  tier=3, tasks=structure("eternalnether:citadel", title="Find a Warped Citadel"), desc="""
    &eEternal Nether&r adds the warped &bCitadel&r, the &6Piglin Manor&r
    and the &8Catacomb&r, each with its own mobs.

    Look for captured &ePiglin Prisoners&r and set them free.
    Wither Skeleton Knights and withered skeleton horses roam here too: stay on your toes.""",
  rewards=[give("minecraft:ender_pearl", 4)])

q("prisoner", "Saving Private Swine", deps="citadel", icon="minecraft:iron_bars", tier=2,
  tasks=adv("eternalnether:rescue_piglin_prisoner", title="Rescue a Piglin Prisoner"), desc="""
    Find a captured piglin and set it free. Somebody has to be the hero!""",
  rewards=[give("minecraft:gold_ingot", 12)])

q("catacomb", "The Catacomb", deps="citadel", icon="eternalnether:withered_bone", tier=3,
  optional=True, tasks=structure("eternalnether:catacomb", title="Explore a Catacomb"), desc="""
    Deep, dark tunnels full of withered undead. The Catacomb is no place to go alone.""",
  rewards=[give("minecraft:bone_block", 8)])

q("mns", "Odd Places", deps="incendium", icon="minecraft:basalt", desc="""
    &eMoog's Nether Structures&r adds lots of smaller builds: bridges over lava, giant skulls,
    arenas, wells, houses and even a train.

    Stop and poke around: many have a chest.""")

# --- netherite --------------------------------------------------------------------------
q("debris", "Ancient Debris", deps="expert", icon="minecraft:ancient_debris", tier=3,
  tasks=item("minecraft:ancient_debris", 4), desc="""
    The toughest ore in the game hides low in the Nether (around Y 15) and doesn't burn in lava.
    Mine around it carefully: it's often next to lava.

    Smelt it into &eNetherite Scrap&r. Four scrap plus four gold make one netherite ingot.""",
  rewards=[give("minecraft:tnt", 8)])

q("ingot", "Netherite Ingot", deps="debris", icon="minecraft:netherite_ingot", tier=3,
  tasks=item("minecraft:netherite_ingot"), desc="""
    Craft your first &eNetherite Ingot&r (4 scrap + 4 gold).
    Netherite is used by lots of mods for their better tools and machines.""",
  rewards=[give("minecraft:gold_ingot", 8)])

q("netherite_gear", "Netherite Gear", deps=["ingot", "bastion"], icon="minecraft:netherite_pickaxe",
  tier=4, tasks=item("minecraft:netherite_pickaxe"), desc="""
    Put a diamond tool, a netherite ingot and a &eNetherite Upgrade&r template in a
    &esmithing table&r. Your tool keeps its enchantments and gets stronger.

    Copy the template (seven diamonds, the template and netherrack make two)
    so you don't need another bastion trip.
    Netherite items don't burn in lava.""",
  rewards=[give("minecraft:diamond", 4)])

q("lava_fishing", "Fishing in Lava", deps="debris", icon="netherdepthsupgrade:lava_fishing_rod",
  tier=2, tasks=item("netherdepthsupgrade:lava_fishing_rod"), desc="""
    &eNether Depths Upgrade&r fills the lava with fish. Craft a &eLava Fishing Rod&r
    (blaze rods, chain and netherite scrap) and cast it into a lava lake.

    Bonefish, searing cod, blazefish and more. Some are great food, some are ingredients.""",
  rewards=[give("minecraft:cooked_cod", 8)])

q("cooking", "Nether Cooking", deps="intro", icon="mynethersdelight:nether_bricks_stove", optional=True,
  tasks=item("mynethersdelight:nether_bricks_stove"), desc="""
    &eMy Nether's Delight&r brings Farmer's Delight cooking to the Nether:
    hoglin and strider dishes, spicy peppers and a stove made of nether bricks.""",
  rewards=[give("minecraft:cooked_porkchop", 8)])

q("where_next", "Where Next?", deps=["fortress", "netherite_gear"], icon="minecraft:compass",
  shape="hexagon", tier=2, desc="""
    The Nether opens up a lot:

    &bNetherite&r and Nether materials feed the mid tiers of the Tech chapters.
    &5The End&r: Ignis keeps the Cursed Eye and the Monstrosity the Nether Eye, two of the eyes you need.
    &cCataclysm&r: the Ignis and the Netherite Monstrosity wait in their own lairs.
    &cThe Kakuto Region&r: the &cFire Gym&r is down here in the Nether.""")
