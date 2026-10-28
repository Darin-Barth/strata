from dsl import *

# The Abyssal Plain (docs/abyssal-plain-design.md, "Progression"). Four tracks leave "rules":
# depth (top), base (middle), survey (bottom) and the boss ladder above them; all end at the Deep
# Station. Hand-placed (at=) to keep the tracks in their rows.
C = chapter("abyssal_plain", "The Abyssal Plain", group="explore", icon="strata:tidecaller",
            subtitle="Dive, build a base you can breathe in, wake the Leviathan")
q = C.quest

q("intro", "What is the Abyssal Plain?", icon="minecraft:heart_of_the_sea", at=(0.0, 4.5),
  shape="gear", size=1.5, rewards=give("minecraft:prismarine_crystals", 4), desc="""
    Far below every ocean lies the &bAbyssal Plain&r: a world of water with &cno surface&r. A rock ceiling caps the sea, so there's nowhere to swim up for air.

    Down there you need real engineering: diving suits, airlocks, air machines and, deep enough, &esubmarines&r (&eCreate: Deep Seas&r).

    The big goal: build a &bDeep Station&r on the floor of the Trench, and wake what sleeps down there.""")

q("tidecaller", "The Tidecaller", deps="intro", icon="strata:tidecaller", at=(1.75, 4.5), tier=2,
  tasks=item("strata:tidecaller"), rewards=give("minecraft:dark_prismarine", 8), desc="""
    Craft the &eTidecaller&r: a &eConduit&r in the middle, a &eSubmarine Ballast Tank&r above and below it, and &eprismarine crystals&r down both sides.

    The Conduit needs a &eHeart of the Sea&r (buried treasure maps hide in shipwrecks and ocean ruins) and 8 &enautilus shells&r (fishing, drowned, wandering traders). Ballast Tanks come from &eCreate: Deep Seas&r: press &eR&r on one for its recipe.""")

q("enter", "Into the Deep", deps="tidecaller", icon="minecraft:dark_prismarine", at=(3.5, 4.5), tier=3,
  tasks=dim("strata:abyssal_plain", title="Enter the Abyssal Plain"), rewards=give("minecraft:cooked_cod", 8), desc="""
    Build a frame of &eDark Prismarine&r the shape of a Nether portal (at least 4 wide and 5 tall) and use the &eTidecaller&r on it. Step in!

    The way home waits right where you arrive, and it leads back to the Overworld at the same spot.""")

q("lifepod", "The Lifepod", deps="enter", icon="minecraft:sea_lantern", at=(5.25, 4.5),
  rewards=give("minecraft:sea_lantern", 4), desc="""
    You arrive inside a &bLifepod&r: a small sealed room with air, lights, windows and a chest of supplies. Its walls can't be broken, so the sea can't get in.

    The way out is the &bmoon pool&r, the hole of water in the floor. Swim down through it and you're in the open sea. Come back the same way to catch your breath or to go home.

    Check the chest, then click the checkmark.""")

q("rules", "The Sea Always Wins", deps="lifepod", icon="minecraft:water_bucket", at=(7.0, 4.5), shape="hexagon",
  rewards=give("minecraft:glass", 16), desc="""
    The Abyssal Plain has its own rules:

    &bThe sea always wins:&r break a block next to water and the gap fills with water. No digging dry tunnels or air pockets!
    &bNo Conduit power:&r Conduits work everywhere else, but not down here.
    &bNo sponges:&r the sea is far too big for them.
    &bWater pressure:&r deeper than &e120 m&r (counted from the ceiling) the water starts to hurt you, and at &c180 m&r it crushes you.

    So you bring your own air: sealed rooms, pumps and air machines. Click the checkmark when you're ready.""")

# --- depth track ---
q("shelf", "The Shelves", deps="rules", icon="minecraft:kelp", at=(8.75, 1.5), tier=2,
  tasks=biome("strata:abyssal_shelf", title="Visit the Abyssal Shelf"), rewards=give("minecraft:dried_kelp_block", 4), desc="""
    The &bAbyssal Shelf&r is the shallow edge of the sea: kelp forests, coral and fish. It's in the top &e120 m&r, so plain gear is fine here.

    Bring a way to breathe (water breathing potions, a Create backtank, spells) and plenty of light: glowing life is the only light down here.""")

q("suit", "Copper Diving Suit", deps="shelf", icon="create:copper_diving_helmet", at=(10.5, 1.5), tier=3,
  tasks=[item("create:copper_diving_helmet"), item("create_submarine:diving_chestplate"), item("create_submarine:diving_leggings"),
         item("create:copper_diving_boots"), item("create:copper_backtank")],
  rewards=give("minecraft:copper_ingot", 16), desc="""
    Going deeper than &e120 m&r needs the full &eCopper Diving Suit&r: Create's &eCopper Diving Helmet&r and &eBoots&r, plus Deep Seas' &eDiving Chestplate&r and &eLeggings&r.

    Wearing all four holds out against the water down to &e280 m&r. Keep a filled &eCopper Backtank&r in your inventory: the helmet breathes from it. Carry a spare!""")

q("plain", "The Plain", deps="suit", icon="hybrid_aquatic:glass_sponge", at=(12.25, 1.5), tier=3,
  tasks=[biome("strata:abyssal_plain", title="Visit the Abyssal Plain biome"), item("hybrid_aquatic:glass_sponge")], desc="""
    Below the shelves lies the &bAbyssal Plain&r itself, about &e245 m&r below the ceiling: flats of clay and mud, glass sponges, whale bones and ruins.

    Keep an eye out for the hot &cHydrothermal Fields&r (vents and magma) and the glowing &bBioluminescent Gardens&r.

    The seafloor rock hides the richest &eosmium&r anywhere, and the vents grow &efluorite&r: dig in from a sealed base.

    Bring back a &eGlass Sponge&r. It's only for decorating: it won't soak up any water.""")

# --- base track ---
q("air", "First Air", deps="rules", icon="create_submarine:decompression_chamber", at=(8.75, 4.5), tier=3,
  tasks=[item("create_submarine:decompression_chamber"), item("create:mechanical_pump"), check()], desc="""
    A base down here is a &bpressure hull&r: a sealed room you pump dry.

    Build a closed room (no gaps!) and pump the water out with Create &eMechanical Pumps&r. A &eDecompression Chamber&r makes an airlock, so you can come and go without flooding the place.

    Remember, the sea always wins: careful when you mine near your walls. Click the checkmark once you have a dry room.""")

q("oxygen", "Breathing Room", deps="air", icon="create_submarine:oxygene_diffuser", at=(10.5, 4.5), tier=3,
  tasks=[item("create_submarine:electrolyzer"), item("create_submarine:oxygene_diffuser")], desc="""
    A dry room still runs out of air. The &eElectrolyzer&r makes oxygen and the &eOxygen Diffuser&r spreads it through your sealed space.

    Set them up and your base (or your submarine) stays breathable. Press &eR&r on them for recipes.""")

q("sub", "Your First Submarine", deps=["plain", "oxygen"], icon="create_submarine:command_sub", at=(14.0, 3.0), tier=4,
  tasks=[item("create_submarine:water_thruster"), item("create_submarine:command_sub")], desc="""
    Past &e280 m&r even the diving suit gives up. From here on you go by &bsubmarine&r.

    A Deep Seas submarine is a Create contraption: a sealed hull with &eBallast Tanks&r to dive and surface, &eWater Thrusters&r or a &ePropeller&r to move, and an &eOnboard Computer&r to steer. Put your air machines inside.

    Hull blocks have &cdepth ratings&r: the deeper you go, the stronger the hull must be. Ponder the Onboard Computer to learn the controls.""")

q("trench", "The Trench", deps="sub", icon="alexscaves:abyssmarine", at=(15.75, 3.0), tier=4,
  tasks=biome("strata:the_trench", title="Reach the Trench"), rewards=give("create_submarine:sonar"), desc="""
    &cThe Trench&r cuts deep into the Plain, about &e545 m&r down. Only a submarine gets you there.

    It's home to the &bDeep Ones&r, a drowned people with knights and mages, and to the &cHullbreaker&r, a monster that hunts submarines. The best ruins and the best loot are down here too.""")

# --- survey track ---
q("guide", "Field Guide", deps="rules", icon="minecraft:spyglass", at=(8.75, 7.5), tier=2,
  tasks=adv("fieldguide:first_discovery", title="Make your first discovery"), desc="""
    Everything down here is new to science. Look at creatures and plants through a &espyglass&r to scan them into your &eField Guide&r, then open the guide with its key (Options > Controls > Field Guide).

    Each discovery fills in a page of notes.""")

q("creatures", "Creatures of the Deep", deps="guide", icon="alexscaves:lanternfish", at=(10.5, 7.5), tier=3,
  tasks=[observe("alexscaves:lanternfish", title="Observe a Lanternfish"), observe("alexscaves:tripodfish", title="Observe a Tripodfish"),
         observe("hybrid_aquatic:anglerfish", title="Observe an Anglerfish")], desc="""
    Find and study three deep-sea creatures: look straight at each one for a moment.

    &eLanternfish&r swim in glowing schools, &eTripodfish&r stand on the seafloor on their long fins, and the &eAnglerfish&r waits in the dark behind its little light. Scan them into your Field Guide while you're at it!""")

q("scanner", "Scanner", deps="guide", icon="scannable:scanner", at=(12.25, 7.5), tier=0,
  tasks=item("scannable:scanner"), rewards=[xp(250), bag("uncommon"), give("scannable:chest_module")], desc="""
    A &eScanner&r (Scannable) pings everything around you and shows it through rock and murky water.

    Modules choose what it finds: &eMonsters&r, &eChests&r and &eRange&r are great for ruin hunting. It runs on FE, so charge it like any powered tool.""")

# --- ruins track ---
q("ruins_plain", "Ruins of the Plain", deps=["plain", "scanner"], icon="minecraft:prismarine_bricks", at=(14.0, 7.5), tier=3,
  tasks=[structure("strata:abyssal/mos_ruins_atlantis", title="Find the ruins of Atlantis"),
         structure("strata:abyssal/joshie_prismarine_trial_chamber", title="Find the Prismarine Trial Chamber")], desc="""
    A whole civilisation drowned here long ago. Its ruins lie across the Plain:

    &eAtlantis&r: the broken streets and temples of an ancient city.
    &ePrismarine Trial Chamber&r: a trial chamber built by the drowned people. Expect a fight, and look for &dAbyssal Pearls&r in its chests.""")

q("ruins_trench", "Ruins of the Trench", deps=["ruins_plain", "trench"], icon="minecraft:dark_prismarine", at=(17.5, 6.0), tier=4,
  tasks=[structure("strata:abyssal/joshie_colossuem", title="Find the Colosseum"),
         structure("strata:abyssal/joshie_sunken_city", title="Find the Sunken City")], desc="""
    The deepest ruins are in the Trench:

    &eThe Colosseum&r: an arena with a guardian waiting at its heart. Its chests can hold &dAbyssal Pearls&r.
    &eThe Sunken City&r: the drowned capital, still guarded.

    The &bDeep Ones&r build ruins of their own down here too, and their chests can also hold pearls.""")

# --- boss ladder ---
q("karkinos", "Karkinos", deps="plain", icon="hybrid_aquatic:karkinos_claw", at=(14.0, -1.5), tier=4,
  tasks=[item("hybrid_aquatic:ominous_hook"), kill("hybrid_aquatic:karkinos")], desc="""
    &cKarkinos&r is a giant crab and the first big hunt of the deep.

    It doesn't wander about: you call it. Craft an &eOminous Hook&r from the claws of nine different crabs (press &eR&r on it), hold it in your &eoffhand&r and go fishing. Something much bigger than a fish bites.

    &6Drops:&r the &eKarkinos Claw&r, and &dAbyssal Pearls&r when it dies in the Abyssal Plain.""")

q("hullbreaker", "The Hullbreaker", deps=["karkinos", "trench"], icon="alexscaves:immortal_embryo", at=(17.5, -1.5), tier=4,
  tasks=kill("alexscaves:hullbreaker"), desc="""
    The &cHullbreaker&r roams the Trench and hunts anything that moves, submarines most of all. It's huge, fast and hits like a train.

    Draw it away from your sub, and bring friends.

    &6Drops:&r the &eImmortal Embryo&r, scrap metal and &dAbyssal Pearls&r.""")

q("pearls", "Abyssal Pearls", deps="hullbreaker", icon="strata:abyssal_pearl", at=(19.25, -1.5), tier=3,
  tasks=item("strata:abyssal_pearl", 6), desc="""
    &dAbyssal Pearls&r are the rarest treasure of the deep. The Leviathan Lure needs &e6&r.

    Deep creatures sometimes drop one, &cKarkinos&r and the &cHullbreaker&r always do, and ruin chests (the trial chamber, the Colosseum, Deep One ruins) can hold them. They only drop in the Abyssal Plain.""")

q("lure", "The Leviathan Lure", deps="pearls", icon="strata:leviathan_lure", at=(21.0, -1.5), tier=0,
  tasks=item("strata:leviathan_lure"), rewards=[xp(500), bag("rare")], desc="""
    Craft the &eLeviathan Lure&r: six &dAbyssal Pearls&r, the &eKarkinos Claw&r, a &eHeart of the Sea&r and the &eImmortal Embryo&r.

    Take it into &cthe Trench&r, below &eY 120&r, and use it. The lure is used up, and only one Leviathan comes at a time.""")

q("leviathan", "The Leviathan", deps="lure", icon="cataclysm:tidal_claws", at=(22.75, -1.5), tier=5,
  shape="hexagon", size=1.5, tasks=kill("cataclysm:the_leviathan"), rewards=give("minecraft:heart_of_the_sea"), desc="""
    Something vast answers the lure. &cThe Leviathan&r is the Abyssal Plain's final boss: fast, armored, and it can't be hurt outside the water. Down here, that's never a problem.

    &6Drops:&r &eTidal Claws&r (a grappling hook), the &eAbyssal Egg&r and &e4 to 6&r &dAbyssal Pearls&r. It counts for the Cataclysm chapter too.""")

# --- the big goal ---
q("station", "Deep Station", deps=["leviathan", "trench", "oxygen"], icon="create_submarine:oxygene_diffuser", at=(22.75, 3.0),
  tier=5, shape="gear", size=2.0, rewards=give("strata:abyssal_pearl", 3), desc="""
    The big goal: a &bDeep Station&r on the floor of the Trench.

    Build a sealed, pumped-dry base down there with an airlock, working air, light, storage and a dock for your submarine. Only the strongest hull blocks hold at that depth.

    Show it off to your friends, then click the checkmark. Welcome home, deep-sea explorer!""")
