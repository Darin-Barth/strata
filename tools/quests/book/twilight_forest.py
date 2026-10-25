from dsl import *

C = chapter("twilight_forest", "The Twilight Forest", group="explore",
            icon="twilightforest:twilight_portal_miniature_structure",
            subtitle="A magic forest and a chain of bosses")
q = C.quest

q("intro", "What is the Twilight Forest?", deps="welcome/iron_age", icon="twilightforest:raven_feather",
  size=1.5, shape="gear", desc="""
    A dimension where it's always dusk: giant trees, glowing mushrooms, fireflies, deer,
    squirrels and penguins. Also hedge mazes, hollow hills and towers.

    It's built like an adventure: each boss you beat lifts a curse on the next area.
    Cursed areas hurt you (blindness, hunger, fire, cold) until you've earned them.

    Being a different dimension, mobs here are a bit tougher than at home.""",
  rewards=[give("minecraft:bread", 16)])

q("portal", "Open the Portal", deps="intro", icon="minecraft:diamond", tier=2,
  tasks=dim("twilightforest:twilight_forest", title="Enter the Twilight Forest"), desc="""
    Dig a &e2x2 hole&r one block deep in grass or dirt and fill it with water.
    Ring the pool with &aflowers, grass or mushrooms&r on every side.
    Then stand back and &ethrow a diamond&r into the water.

    Lightning strikes and the pool turns into a portal. Hop in!""",
  rewards=[give("minecraft:torch", 32), give("minecraft:cooked_chicken", 8)])

q("map", "Magic Maps", deps="portal", icon="twilightforest:filled_magic_map",
  tasks=item("twilightforest:filled_magic_map"), desc="""
    Ravens drop feathers, torchberries hang in caves. Combine a &eraven feather&r,
    &etorchberries&r and &eglowstone dust&r into a Magic Map Focus,
    then surround it with paper to make a &eBlank Magic Map&r.

    Use it to draw a magic map: it shows biomes and every boss structure nearby.""",
  rewards=[give("minecraft:paper", 16)])

q("uncrafting", "The Uncrafting Table", deps="portal", icon="twilightforest:uncrafting_table",
  optional=True, desc="""
    Later you'll find a &eMaze Map Focus&r in the Labyrinth. With a crafting table it makes
    an &eUncrafting Table&r, which takes items apart again (for XP).
    Great for recycling armor you've outgrown.""")

q("food", "Twilight's Flavor & Delight", deps="portal", icon="twilightdelight:fiery_cooking_pot",
  optional=True, desc="""
    &eTwilight's Flavor & Delight&r turns Twilight ingredients into Farmer's Delight dishes:
    torchberry cakes, fried hydra chop, ghast burgers and more.

    Pick up boss drops and odd meats: most of them cook into something.""",
  rewards=[give("minecraft:cake")])

# --- the bosses -------------------------------------------------------------------------
q("naga", "The Naga", deps="portal", icon="twilightforest:naga_trophy", tier=3,
  tasks=kill("twilightforest:naga"), desc="""
    A huge snake circles a stone courtyard in the forest. It charges in straight lines,
    so dodge sideways and hit its head.

    Drops &eNaga Scales&r (armor) and its trophy.
    Beating it opens the shield around the &dLich Tower&r.""",
  rewards=[give("minecraft:golden_apple", 2)])

q("lich", "The Twilight Lich", deps="naga", icon="twilightforest:lich_trophy", tier=4,
  tasks=kill("twilightforest:lich"), desc="""
    At the top of a tall tower lives the &dLich&r. He hides behind magic shields
    and copies of himself. Hit the real one!

    He drops &eScepters&r (twilight, life draining, zombie, fortification).
    His defeat lifts the curses on the &aSwamp&r, &8Dark Forest&r and &bSnowy Forest&r.""",
  rewards=[give("minecraft:ender_pearl", 4)])

# swamp branch
q("minoshroom", "The Minoshroom", deps="lich", icon="twilightforest:minoshroom_trophy", tier=4,
  tasks=kill("twilightforest:minoshroom"), desc="""
    Under the swamp lies the &eLabyrinth&r, full of minotaurs and slimes.
    At its heart: the &eMinoshroom&r, a mushroom-headed minotaur with a big axe.

    It drops &eMeef Stroganoff&r. The Labyrinth also hides the Maze Map Focus.""",
  rewards=[give("minecraft:golden_carrot", 16)])

q("stroganoff", "Mighty Stroganoff", deps="minoshroom", icon="twilightforest:meef_stroganoff",
  tier=2, tasks=adv("twilightforest:progress_labyrinth", title="Eat the Meef Stroganoff"), desc="""
    Eat the &eMeef Stroganoff&r. It gets your body used to the heat of the &cFire Swamp&r,
    so the burning curse there stops hurting you.""")

q("hydra", "The Hydra", deps="stroganoff", icon="twilightforest:hydra_trophy", tier=5,
  tasks=kill("twilightforest:hydra"), desc="""
    In the Fire Swamp, a three-headed &cHydra&r guards its lair. It breathes fire and
    lobs mortars. Hit the heads when they open their mouths.

    It drops &eFiery Blood&r (fiery armor and tools) and hydra chops.""")

# dark forest branch
q("pedestal", "Trophied Champion", deps="lich", icon="twilightforest:trophy_pedestal", tier=2,
  tasks=adv("twilightforest:progress_trophy_pedestal", title="Place a trophy on the pedestal"),
  desc="""
    In the &8Dark Forest&r, find the ruined stronghold entrance with a &eTrophy Pedestal&r.
    Place any boss trophy on it to claim your title and open the way down.""")

q("knights", "The Knight Phantoms", deps="pedestal", icon="twilightforest:knight_phantom_trophy",
  tier=4, tasks=kill("twilightforest:knight_phantom", 6, title="Defeat the 6 Knight Phantoms"),
  desc="""
    Deep in the Knight Stronghold, six ghostly knights rise from their tomb and attack together.
    Bring friends.

    Beat them all and the carminite devices in the &4Dark Tower&r start working for you.
    The stronghold also has &eKnightmetal&r for strong armor.""")

q("ur_ghast", "The Ur-Ghast", deps="knights", icon="twilightforest:ur_ghast_trophy", tier=5,
  tasks=kill("twilightforest:ur_ghast"), desc="""
    At the top of the Dark Tower, kill the little ghasts around the &eGhast Trap&r
    and turn it on to pull the &4Ur-Ghast&r down from the sky.

    It drops &eFiery Tears&r, the other half of fiery gear.""")

# snow branch
q("yeti", "The Alpha Yeti", deps="lich", icon="twilightforest:alpha_yeti_trophy", tier=4,
  tasks=kill("twilightforest:alpha_yeti"), desc="""
    In the Snowy Forest, a cave holds the &bAlpha Yeti&r. It throws ice and slams the ground.

    Its &eAlpha Yeti Fur&r makes &bArctic armor&r, which keeps out the Glacier's cold.""",
  rewards=[give("minecraft:leather", 16)])

q("snow_queen", "The Snow Queen", deps="yeti", icon="twilightforest:snow_queen_trophy", tier=5,
  tasks=kill("twilightforest:snow_queen"), desc="""
    On the Glacier stands the &bAurora Palace&r. At its top waits the &bSnow Queen&r.
    Wear your Arctic armor and stay warm.

    Clearing her skies is one of the three steps to the Highlands.""")

q("trophies", "Trophy Hunter", deps=["hydra", "ur_ghast", "snow_queen"],
  icon="twilightforest:naga_trophy", tier=5, size=1.5, shape="diamond",
  tasks=[item("twilightforest:naga_trophy"), item("twilightforest:lich_trophy"),
         item("twilightforest:minoshroom_trophy"), item("twilightforest:hydra_trophy"),
         item("twilightforest:knight_phantom_trophy"), item("twilightforest:ur_ghast_trophy"),
         item("twilightforest:alpha_yeti_trophy"), item("twilightforest:snow_queen_trophy")],
  desc="""
    Every boss drops a &etrophy&r: a little head to hang on your wall.
    Collect all eight and show them off at your base!

    With the Hydra, Ur-Ghast and Snow Queen gone, the acid rain over the &aHighlands&r clears.
    The Highlands (troll caves, giants in the clouds) are still being finished by the mod's
    makers, so this is the end of the main story.""")

q("where_next", "Where Next?", deps="lich", icon="minecraft:compass", shape="hexagon", tier=2,
  desc="""
    Twilight loot is great for the rest of the pack:

    &bThe Aether&r: another magic dimension, but up in the sky.
    &5Deeper and Darker&r: the Warden's world under the deep dark.
    &cBosses & Combat&r: Cataclysm's bosses, for when you're well geared.""")
