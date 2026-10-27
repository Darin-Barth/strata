from dsl import *

C = chapter("welcome", "Welcome to Strata", group=None, icon="minecraft:compass",
            subtitle="Build. Fly. Explore. Start here!")
q = C.quest

q("welcome", "Welcome to Strata!", icon="ftbquests:book", size=1.5, shape="gear", desc="""
    &6Build. Fly. Explore.&r

    Strata is a big modpack with three paths: &bTech&r (machines, trains and airships),
    &dMagic&r (spells, rituals and spirits) and &aExploration&r (new dimensions, dungeons and bosses).
    There's also a cozy side (farming, cooking, pets, decorating) and a whole Pokémon region, Kakuto.

    This quest book is your guide. Each chapter on the left covers one big mod.
    Nothing is locked: jump to whatever looks fun. Quests inside a chapter open up in order.

    Open the book any time with the book button at the top-left of your inventory.
    Click the checkmark below to get started!""",
  rewards=[give("minecraft:bread", 16), give("minecraft:torch", 32)])

# --- the basics -------------------------------------------------------------------------
q("recipes", "What's That Recipe?", deps="welcome", icon="minecraft:crafting_table", desc="""
    With 400 mods you'll never remember every recipe. You don't have to!

    Hover over any item (in your inventory or the item list on the right) and press
    &eR&r to see how to make it, or &eU&r to see what it's used for.

    Type in the search bar to find items. Start with &e@&r to search by mod (&e@create&r).
    EMI also shows the best heights to mine each ore, what mobs and chests drop, and how to breed animals.""")

q("timber", "Timber!", deps="recipes", icon="minecraft:iron_axe",
  tasks=[item("minecraft:crafting_table"), item("minecraft:stick", 16)], desc="""
    Chop down a tree: break the bottom log and the whole tree falls (FallingTree).

    &eFTB Ultimine&r: hold the &e`&r key (below Esc) while mining to break a whole vein of ore
    or a patch of blocks at once. It costs extra hunger, so bring snacks.""",
  rewards=[give("minecraft:apple", 8)])

q("iron_age", "Iron Age", deps="timber", icon="minecraft:iron_pickaxe", tier=2,
  tasks=[item("minecraft:iron_pickaxe"), item("minecraft:iron_sword")], desc="""
    Iron opens almost every mod. Ores show up in big veins deep underground.

    &eTip:&r Jade (the little box at the top of your screen) tells you what you're looking at
    and which tool you need to break it.

    Weapons swing differently here (&eBetter Combat&r): each weapon has its own combo and reach.
    &eCombat Roll&r lets you dodge-roll out of trouble: press &eR&r by default, or rebind it in Options > Controls.""",
  rewards=[give("minecraft:iron_ingot", 16), give("minecraft:shield")])

q("backpack", "A Bag for Everything", deps="recipes", icon="sophisticatedbackpacks:backpack",
  tasks=item("sophisticatedbackpacks:backpack"), desc="""
    Inventory full already? Craft a &eSophisticated Backpack&r.

    Wear it on your back (or place it down) and press its key (&eB&r by default) to open it.
    Upgrades go in the slots on its side: pickup, magnet, auto-feeding, crafting, and more.
    Later, upgrade the backpack itself to iron, gold, diamond and netherite for more room.

    Inventory Profiles Next adds a &esort&r button to every chest.""",
  rewards=[give("sophisticatedbackpacks:pickup_upgrade"), give("sophisticatedbackpacks:feeding_upgrade")])

q("map", "Find Your Way", deps="welcome", icon="minecraft:filled_map", desc="""
    &eXaero's Minimap&r sits in the corner. Press &eM&r for the full world map.

    Add waypoints for your base, a cool village or a dungeon (&eU&r opens the waypoint list).
    Waystones you discover show up on the map too.

    &ePing Wheel&r: press the side mouse button to ping a spot for your friends.
    Voice chat is built in: hold &eV&r (Simple Voice Chat) to talk to players near you.""")

q("team", "Better Together", deps="welcome", icon="minecraft:cake", desc="""
    Make a team with your friends: open the &eTeams&r button at the top-left of your inventory,
    or type &e/ftbteams party create <name>&r and invite the others.

    Teammates share quest progress (complete a quest once for everyone) and land claims.
    Each player still claims their own rewards.""",
  rewards=[give("minecraft:cookie", 16)])

q("claims", "Home Sweet Claim", deps="team", icon="minecraft:oak_door", desc="""
    Protect your base with &eFTB Chunks&r. Open its map with the &eMap&r button at the
    top-left of your inventory.

    &eLeft-drag&r over chunks to claim them, &eright-drag&r to unclaim.
    &eShift + left-drag&r force-loads a chunk so your farms and machines keep running
    while you're away (you get a limited number, so pick the important ones).

    Claimed land is safe from griefing and explosions.""",
  rewards=[give("minecraft:white_bed")])

q("safety", "When Things Go Wrong", deps="claims", icon="tombstone:grave_key", desc="""
    Dying isn't the end:

    &eCorail Tombstone&r: your items wait in a grave where you died, and you respawn with a Grave's Key. Hold right-click with the key to teleport to your grave, or walk back and open it.
    &ePlayerRevive&r: when you go down, a friend has a little while to revive you.
    &eRedomesticate&r: if your tamed pet dies, it can be brought back, so it's never lost for good.""",
  rewards=[give("minecraft:golden_carrot", 8)])

q("tavern", "A Tavern Town", deps="welcome", icon="minecraft:bell",
  tasks=structure("integrated_villages:tavern_village", title="Visit the tavern village"), desc="""
    You start next to a village with a big tavern. It's a good first home base.

    Villagers trade useful stuff. &eGuard Villagers&r protect them from raids.
    Look for the &eBounty Board&r: villagers post small jobs (bring items, defeat mobs)
    and pay in emeralds and loot.""",
  rewards=[give("minecraft:emerald", 8)])

q("bounty", "Odd Jobs", deps="tavern", icon="bountiful:bountyboard",
  tasks=item("bountiful:bountyboard"), desc="""
    Craft your own &eBounty Board&r for your base, or use one in a village.
    Right-click it to see the jobs on offer. Finish a bounty by handing in what it asks for.
    New bounties appear over time.""", tier=2)

# --- the rules of Strata ----------------------------------------------------------------
q("rules", "Rules of the Road", deps="map", icon="minecraft:writable_book", desc="""
    Strata is built around travel, so a few things are different here:

    &cNo free teleporting.&r There's no /home, /back, /rtp or /tpa.
    &cFlight costs something:&r fuel, power, mana, stamina or durability.
    No "wear it and fly forever" items.

    That's why trains, airships, elytra, mounts and roads are worth building.
    You can still earn teleporting later: Mekanism teleporters, Ars Nouveau warps and
    blink spells all have a cost.""")

q("waystones", "Waystones", deps="rules", icon="waystones:waystone",
  tasks=item("waystones:waystone", title="Find or craft a Waystone"), desc="""
    Waystones stand in many villages. Right-click one to activate it: it stays on your list.
    Using a waystone takes you to any other one you've activated.

    &eThe catch:&r each trip costs &aXP&r. The farther you go, the more it costs,
    and jumping to another dimension costs extra. Short hops are cheap; long trips add up.

    You can also craft your own (look it up with &eR&r).""",
  rewards=[give("minecraft:experience_bottle", 16)], tier=2)

q("difficulty", "The World Gets Harder", deps="iron_age", icon="minecraft:zombie_head", desc="""
    Strata's difficulty rises in steps, for everyone on the server at once:

    &aNormal&r: the start.
    &eExpert&r: after anyone first enters &cthe Nether&r. Mobs hit a bit harder.
    &cMaster&r: after the &5Ender Dragon&r is defeated.

    Other dimensions (the End, Twilight Forest, Deeper and Darker) are tougher than home.
    Bosses always keep their own designed strength.
    Rare &6elite&r mobs (Apotheosis) carry better gear and drop it. They're rare near spawn.""")

q("nether", "Into the Nether", deps="difficulty", icon="minecraft:netherrack", tier=3,
  tasks=dim("minecraft:the_nether"), desc="""
    Build a portal from obsidian and light it. Bring armor, food and blocks!

    Entering the Nether moves the server to &eExpert&r difficulty.
    It also unlocks the middle tier of wireless tech: Flux Networks, AE2 wireless terminals
    and Mekanism quantum entangloporters.

    See the &cThe Nether&r chapter for what's out there.""")

# --- pick a path ------------------------------------------------------------------------
q("pick_path", "Pick a Path", deps=["iron_age", "backpack"], icon="minecraft:oak_sign", size=1.5,
  shape="hexagon", tier=2, desc="""
    You've got the basics. Now choose what sounds fun. You can do all of them, in any order,
    with friends or alone. Each path below points to a chapter.""")

q("path_tech", "Path: Tech", deps="pick_path", icon="create:cogwheel",
  tasks=item("create:andesite_alloy"), desc="""
    Like building machines? Start with &eCreate&r: spinning shafts, belts, presses, trains
    and real airships you build block by block.

    Make your first &eAndesite Alloy&r, then open &bCreate: Getting Moving&r.""",
  rewards=[give("create:andesite_alloy", 16)])

q("path_magic", "Path: Magic", deps="pick_path", icon="ars_nouveau:novice_spell_book",
  tasks=item("ars_nouveau:novice_spell_book"), desc="""
    Want to cast spells? &eArs Nouveau&r lets you design your own spells from glyphs.

    Craft a &eNovice Spell Book&r, then open the &dArs Nouveau&r chapter.
    Iron's Spells, Occultism and more hook into it later.""",
  rewards=[give("ars_nouveau:source_gem", 4)])

q("path_explore", "Path: Exploration", deps="pick_path", icon="explorerscompass:explorerscompass",
  tasks=item("explorerscompass:explorerscompass"), desc="""
    The world is huge and full of dungeons, ruins, towers and sky islands.

    An &eExplorer's Compass&r points to the nearest structure you choose; a &eNature's Compass&r
    finds biomes. Open &aExplorer's Guide&r for where to start.""",
  rewards=[give("minecraft:map", 4)])

q("path_cozy", "Path: Cozy Life", deps="pick_path", icon="farmersdelight:cooking_pot",
  tasks=item("farmersdelight:cooking_pot"), desc="""
    Prefer farming, cooking, pets and decorating? Strata has lots of it.

    Craft a &eCooking Pot&r and open &aFarming & Food&r.
    Pets & Critters and Building & Decorating are right next to it.""",
  rewards=[give("minecraft:wheat_seeds", 16), give("minecraft:carrot", 8)])

q("path_pokemon", "Path: Pokémon (the Kakuto Region)", deps="pick_path", icon="pokeworld:johto_bell",
  tasks=item("pokeworld:bell_fragment"), desc="""
    Pokémon live in their own world, reached through a portal you build yourself.

    First you need a &eBell Fragment&r: they're rare finds in chests of dungeons, temples,
    mineshafts, ancient cities and woodland mansions.
    Open the &cKakuto Region&r chapter for the rest.""",
  rewards=[give("minecraft:gold_ingot", 3)])
