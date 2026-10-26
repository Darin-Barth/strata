from dsl import *

C = chapter("pokemon_world", "The Kakuto Region", group="explore", icon="pokeworld:johto_bell",
            subtitle="Build a portal, pick a partner, catch them all")
q = C.quest

q("intro", "What is the Kakuto Region?", deps="welcome/path_pokemon", icon="cobblemon:poke_ball",
  size=1.5, shape="gear", desc="""
    Somewhere beyond a bell's chime is the &eKakuto Region&r, a whole world just for &dPokémon&r (Cobblemon).
    It looks like a calm, classic Minecraft world, but wild Pokémon live everywhere:
    in the grass, the trees, the caves and the sea.

    Wild Pokémon only appear there. Once you've caught some, they can come with you
    anywhere, even home to your base.

    First, you need to build the way in. You already have a &eBell Fragment&r!""",
  rewards=[give("minecraft:cookie", 8)])

# --- the portal -------------------------------------------------------------------------
q("bell", "The Johto Bell", deps="intro", icon="pokeworld:johto_bell", tier=2,
  tasks=item("pokeworld:johto_bell"), desc="""
    Craft the &eJohto Bell&r: a regular &eBell&r, &e3 gold ingots&r and your
    &eBell Fragment&r on top.

    Village bells can be picked up with a pickaxe (the villagers won't mind... much).
    The Johto Bell is &areusable&r: ringing the portal never uses it up.""",
  rewards=[give("minecraft:diamond")])

q("frames", "Poké Portal Frames", deps="bell", icon="pokeworld:poke_portal_frame", tier=2,
  tasks=item("pokeworld:poke_portal_frame", 10), desc="""
    Craft red-and-white &ePoké Portal Frame&r blocks: red dye, redstone, iron,
    a diamond and white dye make &e8&r at a time.

    You need enough for a frame the shape of a Nether portal: at least 4 wide and 5 tall.
    Leave the corners out if you're short.""",
  rewards=[give("minecraft:red_dye", 6), give("minecraft:white_dye", 6)])

q("portal", "Ring the Bell", deps="frames", icon="pokeworld:johto_bell", tier=3,
  tasks=dim("pokeworld:pokeworld", title="Enter the Kakuto Region"), desc="""
    Build the frame (like a Nether portal, but with Poké Portal Frames) and use the
    &eJohto Bell&r on it. The portal fills with red light. Step in!

    A matching portal is built on the other side, and it leads straight back to the
    Overworld at the same spot. Your Pokémon party HUD only shows inside the Kakuto Region.""",
  rewards=[give("cobblemon:oran_berry", 8)])

q("starter", "Choose Your Partner", deps="portal", icon="cobblemon:poke_ball", size=1.5,
  shape="heart", desc="""
    The first time you arrive, a screen opens to pick your &dstarter Pokémon&r.
    Take your time: every region's starters are there. This is your partner for the journey!

    Closed the screen by accident? It opens again the next time you log in there.
    Your Pokémon's keys (send out, select) are in Options > Controls.""",
  rewards=[give("cobblemon:red_apricorn", 8), give("cobblemon:potion", 4)])

# --- catching ---------------------------------------------------------------------------
q("balls", "Poké Balls", deps="starter", icon="cobblemon:poke_ball",
  tasks=item("cobblemon:poke_ball", 8), desc="""
    &eApricorn trees&r grow all over the Kakuto Region. Red apricorns make &ePoké Balls&r
    (4 at a time); other colors make other balls. Press &eR&r on a ball to see its recipe.

    Grab some &eapricorn sprouts&r too, so you can grow your own trees at home.""",
  rewards=[give("cobblemon:red_apricorn_seed", 2)])

q("first_catch", "Gotcha!", deps="balls", icon="cobblemon:great_ball", tier=2,
  tasks=adv("cobblemon:catching/first_catch", title="Catch your first Pokémon"), desc="""
    Find a wild Pokémon and send out your partner to battle it.
    When it's weak, throw a Poké Ball at it. Wiggle... wiggle... click!

    Craft a &ePokédex&r (press &eR&r on it for the recipe) to keep track of every
    Pokémon you've seen and caught.""",
  rewards=[give("cobblemon:great_ball", 4)])

q("full_party", "A Full Team", deps="first_catch", icon="cobblemon:poke_ball", tier=2,
  tasks=adv("cobblemon:catching/full_party", title="Have six Pokémon in your party"), desc="""
    Catch more until your party is full: &esix Pokémon&r.
    Mix their types (water, fire, grass, flying...) so you're ready for any battle.""",
  rewards=[give("cobblemon:super_potion", 4), give("cobblemon:revive", 2)])

q("pokecenter", "The Pokécenter", deps="first_catch", icon="cobblemon:healing_machine", tier=2,
  tasks=adv("cobblemon:agriculture/use_healing_machine", title="Heal at a Healing Machine"),
  desc="""
    Pokécenters stand in Kakuto villages and on their own. Inside is a
    &eHealing Machine&r: put your team in and they're good as new.

    There's a &ePC&r too, to store the Pokémon that don't fit in your party.
    You can craft your own PC (and later a Healing Machine) for your base.""",
  rewards=[give("cobblemon:sitrus_berry", 4)])

q("berries", "Berry Patch", deps="balls", icon="cobblemon:oran_berry", optional=True,
  tasks=adv("cobblemon:agriculture/harvest_apricorn", title="Harvest an apricorn"), desc="""
    Plant your apricorn sprouts and watch them grow into trees.
    Berry bushes grow in the Kakuto Region too: many heal or help in battle,
    and they look lovely in a garden.""",
  rewards=[give("minecraft:bone_meal", 16)])

q("evolution", "Evolution!", deps="full_party", icon="cobblemon:fire_stone", tier=3,
  tasks=adv("cobblemon:catching/first_evolution", title="Evolve a Pokémon"), desc="""
    Most Pokémon evolve by levelling up in battle. Some need an &eevolution stone&r instead:
    Fire, Water, Thunder, Leaf, Moon, Sun and more.

    Evolution stone ores are found underground in the Kakuto Region. Mine them,
    then use the stone on the Pokémon.""",
  rewards=[give("cobblemon:exp_candy_s", 4)])

q("ride", "Ride Along", deps="full_party", icon="minecraft:saddle", tier=2,
  tasks=adv("cobblemon:catching/ride_pokemon", title="Ride a Pokémon"), desc="""
    Some Pokémon can carry you on their back: on land, through water, or into the sky.

    Riding is allowed in &aevery dimension&r. Flying Pokémon get tired: they use
    &estamina&r, so you'll need to land and rest now and then.""",
  rewards=[give("minecraft:golden_carrot", 8)])

q("pasture", "Home Sweet Pasture", deps="pokecenter", icon="cobblemon:pasture", optional=True,
  tasks=adv("cobblemon:catching/use_pasture", title="Use a Pasture Block"), desc="""
    A &ePasture Block&r lets your Pokémon out of the PC to wander around your base.
    Build them a cozy garden in the Overworld: they'll be happy to live with you.""",
  rewards=[give("minecraft:oak_fence", 16)])

# --- trainers and gyms ------------------------------------------------------------------
q("trainers", "Trainer Card", deps="first_catch", icon="rctmod:trainer_card", tier=2,
  tasks=item("rctmod:trainer_card"), desc="""
    &eRadical Cobblemon Trainers&r: trainers wander the Kakuto Region. If one spots you,
    they'll want to battle!

    Your Pokémon's &elevel cap&r starts at &e15&r and rises as you beat trainers.
    Pokémon above the cap won't fight for you yet. The &eTrainer Card&r shows your progress.""",
  rewards=[give("cobblemon:potion", 4)])

q("dollars", "CobbleDollars", deps="trainers", icon="minecraft:emerald", desc="""
    Winning battles against wild Pokémon and trainers earns &eCobbleDollars&r.
    Your balance shows in the corner of the screen.

    Spend them with a &eCobble Merchant&r (a villager with that job) on Poké Balls,
    medicine and more. Merchants can also trade CobbleDollars and emeralds.""",
  rewards=[give("minecraft:emerald", 4)])

q("gym", "Your First Gym", deps=["trainers", "full_party"], icon="cobblemon:normal_gem", tier=3,
  tasks=structure("integrated_cobblemon:normal_gym", title="Visit the Normal Gym"), desc="""
    &eIntegrated Cobblemon&r gyms are scattered across the Kakuto Region, one for each type.
    Each gym has three trainers: &abeginner&r, &eintermediate&r and &chard&r.
    Beat all three to complete that gym's badge series. Gym chests have goodies too.

    Use the Explorer's Compass to find them. Try the &eNormal Gym&r first.""",
  rewards=[give("cobblemon:great_ball", 8)])

q("fire_gym", "The Fire Gym", deps=["gym", "nether/intro"], icon="cobblemon:fire_gem", tier=4,
  tasks=structure("integrated_cobblemon:fire_gym", title="Find the Fire Gym"), desc="""
    Not every gym is in the Kakuto Region! The &cFire Gym&r is down in &cthe Nether&r.
    Bring water-type Pokémon and fire resistance potions.""")

q("end_gyms", "Gyms Beyond the Stars", deps=["fire_gym", "the_end/portal"],
  icon="cobblemon:dragon_gem", tier=5,
  tasks=[structure("integrated_cobblemon:psychic_gym", title="Find the Psychic Gym"),
         structure("integrated_cobblemon:dragon_gym", title="Find the Dragon Gym")], desc="""
    The &dPsychic&r and &5Dragon&r gyms are out in &5the End&r.
    These are the toughest gyms of all. Good luck, Champion!""")

q("where_next", "Where Next?", deps="first_catch", icon="minecraft:compass", shape="hexagon",
  tier=2, desc="""
    The Kakuto Region is yours to explore at your own pace:

    Look for &eruins, towers and habitats&r: some hold rare Pokémon.
    Catch a flying partner and explore the &aOverworld&r from above.
    &cThe Nether&r and &5The End&r chapters lead to the far-away gyms.""")
