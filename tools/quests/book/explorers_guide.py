from dsl import *

C = chapter("explorers_guide", "Explorer's Guide", group="explore",
            icon="explorerscompass:explorerscompass",
            subtitle="Compasses, dungeons, ruins and treasure")
q = C.quest

q("intro", "What is Exploring?", deps="welcome/path_explore", icon="minecraft:filled_map",
  size=1.5, shape="gear", desc="""
    The Overworld in Strata is big and wild: tall mountains (Tectonic), lots of new biomes
    (Regions Unexplored) and rivers that wind through it all.

    Hidden in it are hundreds of &edungeons, ruins, towers, villages and sky islands&r.
    Every one has loot, and many have their own monsters or bosses.

    This chapter shows you how to find them. Bring food, torches and a bed!""",
  rewards=[give("minecraft:torch", 32), give("minecraft:cooked_beef", 8)])

# --- finding your way -------------------------------------------------------------------
q("compass", "Point the Way", deps="intro", icon="explorerscompass:explorerscompass", desc="""
    Right-click your &eExplorer's Compass&r to open a list of every structure in the world.
    Type in the search box, pick one, and the compass needle points to the nearest one.
    It also tells you how far away it is.

    Picked a big one? Write the spot down as a waypoint (&eU&r) so you can find it again.""",
  rewards=[give("minecraft:map", 4)])

q("natures", "Nature's Compass", deps="compass", icon="naturescompass:naturescompass",
  tasks=item("naturescompass:naturescompass"), desc="""
    The &eNature's Compass&r does the same thing for &abiomes&r.
    Want cherry trees, a desert, or snowy peaks? Pick it from the list and follow the needle.

    Some structures only appear in certain biomes, so the two compasses work well together.""",
  rewards=[give("minecraft:bread", 16)])

q("new_biome", "Somewhere New", deps="natures", icon="minecraft:poppy",
  tasks=biome("regions_unexplored:poppy_fields", title="Visit Poppy Fields"), desc="""
    Use the Nature's Compass to find &ePoppy Fields&r, a sea of red flowers.

    When you walk into a new biome or dimension, its name fades in on your screen
    (&eTraveler's Titles&r). It's a nice way to know you've found somewhere new.""",
  rewards=[give("minecraft:bone_meal", 16)])

q("lootr", "Loot for Everyone", deps="compass", icon="lootr:lootr_chest", desc="""
    Chests in structures are &eLootr&r chests: every player gets their &aown&r loot from each one.
    If your friend opened it first, there's still a full chest waiting for you.

    So no racing for the loot. Explore together and everyone gets a share.""",
  rewards=[give("minecraft:chest", 4)])

# --- dungeons ---------------------------------------------------------------------------
q("desert_temple", "Better Desert Temple", deps="lootr", icon="minecraft:sandstone", tier=2,
  tasks=structure("betterdeserttemples:desert_temple", title="Explore a desert temple"), desc="""
    &eYUNG's&r mods rebuild the classic structures: desert temples, jungle temples,
    dungeons, mineshafts, witch huts, ocean monuments and Nether fortresses.

    Desert temples are now full tombs with traps, puzzles and a pharaoh's treasure.
    Watch your step, and keep an eye out for strange &5eyes&r in the chests
    (you'll need them later, see &5The End&r).""",
  rewards=[give("minecraft:golden_apple", 1)])

q("jungle_temple", "Better Jungle Temple", deps="desert_temple", icon="minecraft:mossy_cobblestone",
  tier=2, optional=True,
  tasks=structure("betterjungletemples:jungle_temple", title="Explore a jungle temple"), desc="""
    Deep in the jungle, &eYUNG's&r jungle temples hide traps, levers and secret rooms.
    Bring a few torches to mark where you've been.""",
  rewards=[give("minecraft:arrow", 32)])

q("arise", "When Dungeons Arise", deps="lootr", icon="minecraft:stone_bricks", tier=3,
  tasks=structure("dungeons_arise:lighthouse", title="Climb a lighthouse"), desc="""
    &eWhen Dungeons Arise&r adds huge hand-built dungeons: forts, mines, monasteries, towers,
    palaces and even ones floating in the sky.

    Start with a &eLighthouse&r on the coast. The big ones (look for "heavenly" in the
    Explorer's Compass list) are great targets for your first airship.""",
  rewards=[give("minecraft:iron_ingot", 16)])

q("seven_seas", "The Seven Seas", deps="arise", icon="minecraft:oak_boat", tier=3, optional=True,
  tasks=structure("dungeons_arise_seven_seas:victory_frigate", title="Board a Victory Frigate"),
  desc="""
    &eSeven Seas&r puts ships on the oceans: frigates, galleons, junks and yachts.
    Many are crewed by pirates who don't like visitors.

    Board one by boat (or drop in from above) and loot the captain's cabin.""",
  rewards=[give("minecraft:emerald", 8)])

q("warship", "Illager Warships", deps="seven_seas", icon="minecraft:crossbow", tier=4,
  optional=True,
  tasks=structure("illagerwarship:warship", title="Board an Illager Warship"), desc="""
    Illagers have a navy too: big &cwarships&r on the open ocean and war triremes on
    warm seas. They're well armed, so bring a shield and a full stack of food.""",
  rewards=[give("minecraft:golden_carrot", 16)])

q("idas", "Castles and Taverns", deps="lootr", icon="minecraft:cobblestone_wall", tier=3,
  tasks=structure("idas:castle", title="Explore a castle"), desc="""
    &eIntegrated Dungeons and Structures&r adds castles, wizard towers, taverns, camps,
    sunken ships and much more. Some are friendly, some really aren't.

    Find a &eCastle&r and see who lives there.""",
  rewards=[give("minecraft:iron_ingot", 16)])

q("towns", "New Towns, New Faces", deps="lootr", icon="minecraft:bell", desc="""
    Villages come in many styles here: &eTowns and Towers&r and &eIntegrated Villages&r add
    regional villages and outposts.

    The countryside is dotted with little builds: farms, wells, camps, ruins and
    watchtowers (&eExplorify&r, &eMoog's&r structures, &eDungeons and Taverns&r).
    Small places often hide a chest or two.""",
  rewards=[give("minecraft:emerald", 6)])

q("sky", "Look Up!", deps="towns", icon="minecraft:feather", tier=2, desc="""
    Not everything is on the ground. &eEmber's Floating Islands&r and &eMoog's Soaring
    Structures&r hang in the sky, and &bsky whales&r drift high above the land.

    You can't reach them by walking. Build an airship (see the Create chapters) or
    find another clever way up. This is what Strata's "Fly" is all about.""")

q("whale", "Whale Watching", deps="sky", icon="minecraft:blue_wool", tier=3,
  tasks=structure("sky_whale_ship:whale", title="Land on a sky whale"), desc="""
    Sky whales float around Y 180 to 220. Spot one, fly up, and land on its back.
    Some carry a little ship or a lighthouse. Look for the loot!""",
  rewards=[give("minecraft:diamond", 2)])

# --- digging and trinkets ---------------------------------------------------------------
q("archeology", "Dig It Up", deps="intro", icon="minecraft:brush",
  tasks=item("betterarcheology:artifact_shards", title="Find Artifact Shards"), desc="""
    Look for &esuspicious sand&r and &esuspicious gravel&r in ruins, temples and dig sites.
    Brush it gently (hold right-click with a brush) to uncover what's buried.

    &eBetter Archeology&r adds &eArtifact Shards&r, fossils and more to find.
    An &eIron Brush&r (feather, iron, stick) is a nice upgrade.""",
  rewards=[give("minecraft:brush")])

q("arch_table", "The Archeology Table", deps="archeology", icon="betterarcheology:archeology_table",
  tier=2, tasks=item("betterarcheology:archeology_table"), desc="""
    Craft an &eArcheology Table&r (a brush, a shard and planks).

    Nine Artifact Shards craft an &eUnidentified Artifact&r. Study it at the table to find out
    what it is. Identified artifacts give you special powers.""",
  rewards=[give("minecraft:feather", 8), give("minecraft:iron_ingot", 4)])

q("artifact", "A Mystery Solved", deps="arch_table", icon="betterarcheology:unidentified_artifact",
  tier=2, tasks=item("betterarcheology:unidentified_artifact", title="Craft an Unidentified Artifact"), desc="""
    Craft an Unidentified Artifact from nine shards, then study it at the table. Read the result's tooltip to see what it does.

    Keep digging: there are lots of different ones to collect.""")

q("trinkets", "Trinkets and Treasures", deps="lootr", icon="artifacts:lucky_scarf", tier=2,
  desc="""
    Dungeon chests can hold &daccessories&r from &eArtifacts&r, &eRelics&r and
    &eForsaken Relics&r: rings, belts, amulets, hats and charms with special powers.

    Wear them in the &eaccessory slots&r (Curios) next to your inventory.
    Read the tooltips: Relics get stronger the more you use them.

    &cCareful:&r some chests are &cmimics&r. If a chest bites back, fight it!""",
  rewards=[give("minecraft:experience_bottle", 8)])

q("where_next", "Where Next?", deps=["desert_temple", "arise", "idas", "sky"],
  icon="minecraft:compass", shape="hexagon", tier=2, desc="""
    You know how to find anything now. Some bigger trips:

    &cThe Nether&r: fiery fortresses and citadels.
    &aThe Twilight Forest&r: a magic forest with a chain of bosses.
    &bThe Aether&r: islands in the sky.
    &5The End&r: find 12 eyes and open the stronghold portal.
    &cThe Pokémon World&r: if you've found a Bell Fragment.""")
