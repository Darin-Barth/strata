from dsl import *

C = chapter("storage", "Storage", group="life", icon="sophisticatedstorage:chest",
            subtitle="Bigger chests, drawers, a storage terminal and mail for friends")
q = C.quest

q("intro", "Where Does It All Go?", icon="minecraft:chest", size=1.5, shape="gear", desc="""
    Modded Minecraft means a &elot&r of stuff. Luckily there are great ways to store it:

    &eSophisticated Storage&r: chests and barrels that upgrade and get bigger.
    &eFunctional Storage&r: drawers that hold huge amounts of one item.
    &eTom's Simple Storage&r: one screen to see and search all your chests.

    Start small: a few good chests are plenty for a while.""",
  rewards=[give("minecraft:chest", 4), give("minecraft:oak_log", 16)])

# --- backpack -----------------------------------------------------------------------------
q("backpack_tier", "A Bigger Backpack", deps=["intro", "welcome/backpack"], icon="sophisticatedbackpacks:iron_backpack",
  tasks=item("sophisticatedbackpacks:iron_backpack"), tier=2, desc="""
    Your backpack can grow! Craft your backpack with metal around it to upgrade it:
    &ecopper&r, &eiron&r, &egold&r, &ediamond&r and finally &enetherite&r.
    Everything inside stays put, and each tier adds more slots and upgrade slots.

    Press &eR&r on the Iron Backpack to see the recipe.""",
  rewards=[give("minecraft:iron_ingot", 16), give("minecraft:gold_ingot", 8)])

q("backpack_upgrades", "Backpack Upgrades", deps="backpack_tier", icon="sophisticatedbackpacks:magnet_upgrade",
  tasks=item("sophisticatedbackpacks:magnet_upgrade"), desc="""
    Upgrades go in the slots on the side of your backpack. Favorites:

    &eMagnet&r: pulls nearby items into the backpack.
    &eCrafting&r: a crafting grid inside your backpack.
    &eRestock&r and &eDeposit&r: fill up from, or empty into, a chest you click.
    &eTool Swapper&r: picks the right tool for the block you're mining.

    Most upgrades start from an &eUpgrade Base&r.""",
  rewards=[give("sophisticatedbackpacks:upgrade_base", 3)])

q("backpack_crafting", "Craft on the Go", deps="backpack_upgrades", icon="sophisticatedbackpacks:crafting_upgrade",
  optional=True, tasks=item("sophisticatedbackpacks:crafting_upgrade"), desc="""
    A crafting table that lives in your backpack. Never carry a crafting table again!""",
  rewards=[give("sophisticatedbackpacks:upgrade_base", 2)])

# --- sophisticated storage ----------------------------------------------------------------
q("soph_chest", "Sophisticated Chests", deps="intro", icon="sophisticatedstorage:chest",
  tasks=item("sophisticatedstorage:chest"), desc="""
    &eSophisticated Storage&r chests and barrels work like normal ones, but they can be
    upgraded and fitted with upgrades, just like your backpack.

    Paint them with the &ePaintbrush&r or restyle them at the &eDecoration Table&r.""",
  rewards=[give("minecraft:oak_planks", 32)])

q("tier_upgrade", "Upgrade in Place", deps="soph_chest", icon="sophisticatedstorage:basic_to_iron_tier_upgrade",
  tasks=item("sophisticatedstorage:basic_to_iron_tier_upgrade"), tier=2, desc="""
    &eTier Upgrades&r turn a chest or barrel into a bigger one &ewithout emptying it&r.
    Just right-click the chest with the upgrade.

    Got old vanilla chests? A &eBasic Tier Upgrade&r turns them into sophisticated ones.""",
  rewards=[give("minecraft:iron_ingot", 16)])

q("storage_upgrades", "Smart Chests", deps="tier_upgrade", icon="sophisticatedstorage:hopper_upgrade",
  optional=True, tasks=item("sophisticatedstorage:compacting_upgrade"), desc="""
    Chest upgrades: &eCompacting&r turns nuggets into ingots and ingots into blocks,
    &eSmelting&r cooks what you put in, &eHopper&r pulls items in and out, &eVoid&r deletes junk.""",
  rewards=[give("minecraft:redstone", 16)])

q("packing_tape", "Moving House", deps="soph_chest", icon="sophisticatedstorage:packing_tape",
  optional=True, tasks=item("sophisticatedstorage:packing_tape"), desc="""
    Use &ePacking Tape&r on a full chest, then break it: it keeps everything inside,
    so you can carry a whole chest to your new base. Each roll has a few uses.""",
  rewards=[give("minecraft:slime_ball", 4)])

q("soph_controller", "Storage Controller", deps="tier_upgrade", icon="sophisticatedstorage:controller", tier=2,
  tasks=item("sophisticatedstorage:controller"), desc="""
    Build a wall of sophisticated chests and barrels touching each other, then place a
    &eStorage Controller&r against them. Now they're one big storage:
    put items in through the controller and they go to the right place.

    Hoppers and pipes can feed the controller too.""",
  rewards=[give("minecraft:diamond", 2)])

# --- drawers ------------------------------------------------------------------------------
q("drawer", "Drawers", deps="intro", icon="functionalstorage:oak_1",
  tasks=item("functionalstorage:oak_1"), desc="""
    A &eDrawer&r holds &elots&r of one kind of item, and shows it on the front.
    Right-click to put items in, left-click to take a stack out.

    Perfect for cobblestone, dirt, seeds and other things you collect by the hundreds.
    2-slot and 4-slot drawers hold several kinds.""",
  rewards=[give("functionalstorage:oak_2", 2)])

q("drawer_controller", "Drawer Controller", deps="drawer", icon="functionalstorage:storage_controller", tier=2,
  tasks=[item("functionalstorage:storage_controller"), item("functionalstorage:linking_tool")], desc="""
    A wall of drawers with a &eStorage Controller&r acts like one: put anything into the
    controller and it goes to the matching drawer.

    Use the &eLinking Tool&r: click the controller, then click your drawers to connect them.""",
  rewards=[give("functionalstorage:oak_4", 4)])

q("compacting_drawer", "Squish It Down", deps="drawer_controller", icon="functionalstorage:compacting_drawer",
  optional=True, tasks=item("functionalstorage:compacting_drawer"), desc="""
    A &eCompacting Drawer&r turns nuggets into ingots into blocks automatically,
    and gives you whichever size you need.""",
  rewards=[give("minecraft:iron_nugget", 32)])

q("drawer_upgrades", "Drawer Upgrades", deps="drawer_controller", icon="functionalstorage:copper_upgrade",
  optional=True, tasks=item("functionalstorage:copper_upgrade"), desc="""
    Storage upgrades (copper, gold, diamond, netherite) make each drawer hold far more.
    There are also &epuller&r, &epusher&r and &evoid&r upgrades.""",
  rewards=[give("minecraft:copper_ingot", 16)])

# --- terminal -----------------------------------------------------------------------------
q("terminal", "One Screen for Everything", deps="intro", icon="toms_storage:storage_terminal", tier=2,
  tasks=[item("toms_storage:inventory_connector"), item("toms_storage:storage_terminal")], desc="""
    &eTom's Simple Storage&r: place an &eInventory Connector&r touching your chests
    (or link more chests with &eInventory Cable&r), then put a &eStorage Terminal&r on it.

    The terminal shows &eeverything&r in all connected chests. Search, sort, and take
    what you need. Drawers and sophisticated chests work too!""",
  rewards=[give("toms_storage:inventory_cable", 16)])

q("crafting_terminal", "Crafting Terminal", deps="terminal", icon="toms_storage:crafting_terminal",
  tasks=item("toms_storage:crafting_terminal"), desc="""
    A terminal with a crafting grid. It pulls ingredients straight out of your storage.
    Press &eR&r on an item and use EMI's &e+&r button to fill the grid for you.""",
  rewards=[give("toms_storage:inventory_cable", 16)])

# --- friends and comfort ------------------------------------------------------------------
q("mail", "You've Got Mail!", deps="intro", icon="mighty_mail:oak_mail_box",
  tasks=[item("mighty_mail:oak_mail_box"), item("mighty_mail:post_box")], desc="""
    Send gifts to your friends! Place a &eMailbox&r at your house and give it a name.

    At a &ePost Box&r, pick a mailbox from the list (type &e@name&r to find a player),
    put items in the package, add a message, and press &eSend&r.
    Your friend finds the package waiting in their mailbox.""",
  rewards=[give("minecraft:paper", 16), give("plushies:parrot_plushie")])

q("qol", "Handy Helpers", deps="intro", icon="minecraft:shulker_box", desc="""
    Two small things that make life easier:

    &eShulker Box Tooltip&r: hover over a shulker box (and other containers)
    to peek inside without opening it.
    &eLocked In Slots&r: lock a hotbar or inventory slot so you never drop or move
    that item by mistake. Find its key in &eOptions > Controls&r.

    Inventory Profiles Next also adds a &esort&r button to every chest.""",
  rewards=[give("minecraft:chest", 2)])

q("where_next", "Where Next?", deps=["soph_controller", "terminal"], icon="minecraft:oak_sign", shape="hexagon",
  desc="""
    Your stuff is safe and tidy! When you outgrow chests:

    &bApplied Energistics 2&r (in the Tech chapters) stores items as data on drives.
    Thousands of items in one computer, with autocrafting!

    &aBuilding & Decorating&r: make your storage room look nice too.""",
  rewards=[give("minecraft:barrel", 4), give("minecraft:cake")])
