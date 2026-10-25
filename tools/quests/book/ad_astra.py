from dsl import *

C = chapter("ad_astra", "Ad Astra", group="explore", icon="ad_astra:tier_1_rocket",
            subtitle="Rockets, space suits and other planets")
q = C.quest

q("intro", "What is Ad Astra?", deps="welcome/iron_age", icon="ad_astra:astrodux", size=1.5,
  shape="gear", desc="""
    &eAd Astra&r lets you build rockets and fly to the &7Moon&r, &cMars&r, &6Venus&r,
    &eMercury&r and finally &bGlacio&r in another solar system.

    Space has no air: you need a &espace suit&r full of oxygen, and every launch burns &efuel&r.
    Each planet has a new metal that builds the next rocket.

    Open the &eAstrodux&r guide book for the full details.""",
  rewards=[give("ad_astra:astrodux")])

# --- getting ready ----------------------------------------------------------------------
q("furnace", "Etrionic Blast Furnace", deps="intro", icon="ad_astra:etrionic_blast_furnace",
  tasks=item("ad_astra:etrionic_blast_furnace"), desc="""
    Ad Astra machines run on power (FE). The &eCoal Generator&r is the simplest start,
    but any generator from the Tech chapters works.

    The &eEtrionic Blast Furnace&r smelts four things at once and alloys iron and coal into
    &esteel&r. Steel from other mods (Immersive Engineering, Mekanism) is the same steel here.""",
  rewards=[give("minecraft:coal", 32)])

q("compressor", "Plates", deps="furnace", icon="ad_astra:compressor", tier=2,
  tasks=item("ad_astra:compressor"), desc="""
    The &eCompressor&r squeezes ingots into &eplates&r. Rockets are mostly steel plates.""",
  rewards=[give("minecraft:iron_ingot", 16)])

q("workbench", "NASA Workbench", deps="compressor", icon="ad_astra:nasa_workbench", tier=2,
  tasks=item("ad_astra:nasa_workbench"), desc="""
    Rockets are too big for a crafting table. The &eNASA Workbench&r builds them from parts:
    a nose cone, plates, fins, tanks and an engine.""",
  rewards=[give("minecraft:redstone", 32)])

q("oxygen", "Air to Breathe", deps="compressor", icon="ad_astra:oxygen_loader", tier=2,
  tasks=item("ad_astra:oxygen_loader"), desc="""
    The &eOxygen Loader&r turns water into oxygen (it needs power).
    Fill your space suit and some &eGas Tanks&r with it before every trip.""",
  rewards=[give("minecraft:water_bucket")])

q("suit", "Space Suit", deps="oxygen", icon="ad_astra:space_suit", tier=2,
  tasks=[item("ad_astra:space_helmet"), item("ad_astra:space_suit"), item("ad_astra:space_pants"),
         item("ad_astra:space_boots")], desc="""
    Wear the whole &eSpace Suit&r and fill it with oxygen. Without it you'll suffocate
    and freeze on the Moon.

    The &eTI-69&r shows the oxygen, temperature and gravity where you stand.""",
  rewards=[give("ad_astra:ti_69")])

q("fuel", "Rocket Fuel", deps="furnace", icon="ad_astra:fuel_bucket", tier=2,
  tasks=item("ad_astra:fuel_refinery"), desc="""
    &eOil&r spouts up out of the ocean in some places (look for oil wells).
    The &eFuel Refinery&r turns oil into &eFuel&r.

    A launch takes about &e3 buckets&r of fuel. Always carry another 3 for the trip home!""",
  rewards=[give("minecraft:bucket", 3)])

q("rocket1", "Tier 1 Rocket", deps=["workbench", "fuel"], icon="ad_astra:tier_1_rocket", tier=3,
  tasks=[item("ad_astra:tier_1_rocket"), item("ad_astra:launch_pad")], desc="""
    Build a &eTier 1 Rocket&r in the NASA Workbench and a &eLaunch Pad&r to put it on.
    Fuel it up (sneak + right-click the rocket to open its inventory).

    Before you launch, pack a &espare launch pad&r, fuel for the return, oxygen tanks,
    food and soul torches (normal torches go out on the Moon).""")

# --- the moon ---------------------------------------------------------------------------
q("moon", "One Small Step", deps=["rocket1", "suit"], icon="ad_astra:moon_globe", tier=3,
  tasks=dim("ad_astra:moon", title="Land on the Moon"), desc="""
    Climb in and press &ejump&r to launch. Pick the Moon on the planet screen.

    You land in a lander. Don't lose it: your rocket is inside!
    The Moon is cold and airless: water freezes and plants die without an
    &eOxygen Distributor&r in a sealed room.""",
  rewards=[give("minecraft:cooked_beef", 16)])

q("desh", "Desh", deps="moon", icon="ad_astra:raw_desh", tier=3,
  tasks=item("ad_astra:desh_ingot", 16), desc="""
    &eDesh&r ore is found under the Moon's surface. Desh builds better machines,
    space stations and the &eTier 2 Rocket&r.

    Look for the &eLunarians&r: moon villagers living underground. They trade useful
    space gear for emeralds.""")

q("cheese", "Is It Made of Cheese?", deps="moon", icon="ad_astra:cheese", optional=True,
  tasks=item("ad_astra:cheese"), desc="""
    Yes! There's &echeese ore&r on the Moon. Mine it and smelt it.""",
  rewards=[give("ad_astra:cheese", 8)])

q("rover", "Moon Rover", deps="desh", icon="ad_astra:tier_1_rover", tier=3, optional=True,
  tasks=item("ad_astra:tier_1_rover"), desc="""
    The &eRover&r drives fast over rough ground, seats two and has a radio.
    It runs on fuel.""")

q("station", "Space Station", deps="desh", icon="ad_astra:steel_plateblock", tier=3, optional=True,
  desc="""
    From the planet screen you can build a &eSpace Station&r in orbit if you have the
    materials. It's a starter platform you can expand into a base among the stars.
    In orbit there's no gravity: you float around, so build carefully.""")

# --- further out (boss gated) -----------------------------------------------------------
q("rocket2", "Tier 2 Rocket: Mars", deps=["desh", "cataclysm/ignis"], icon="ad_astra:tier_2_rocket",
  tier=4, tasks=[item("ad_astra:tier_2_rocket"), dim("ad_astra:mars", title="Land on Mars")],
  desc="""
    The &eTier 2 Rocket&r is built from Desh parts and reaches &cMars&r.
    Strata gates this rocket behind &cIgnis&r (Cataclysm): beat it first.

    On Mars, mine &eOstrum&r for even better gear.""")

q("netherite_suit", "Netherite Space Suit", deps="rocket2", icon="ad_astra:netherite_space_suit",
  tier=4, tasks=[item("ad_astra:netherite_space_helmet"), item("ad_astra:netherite_space_suit"),
                 item("ad_astra:netherite_space_pants"), item("ad_astra:netherite_space_boots")],
  desc="""
    Venus and Mercury are &cburning hot&r. The &eNetherite Space Suit&r gives permanent
    fire resistance and more protection. You'll die fast without it there.""")

q("rocket3", "Tier 3 Rocket: Venus and Mercury",
  deps=["netherite_suit", "cataclysm/netherite_monstrosity"], icon="ad_astra:tier_3_rocket",
  tier=5, tasks=[item("ad_astra:tier_3_rocket"), dim("ad_astra:venus", title="Land on Venus"),
                 dim("ad_astra:mercury", title="Land on Mercury")], desc="""
    Ostrum parts build the &eTier 3 Rocket&r, which can stand the heat of &6Venus&r
    and &eMercury&r. Gated behind the &cNetherite Monstrosity&r (Cataclysm).

    Venus has &eCalorite&r, the last rocket metal. Mercury's sun makes solar panels shine.""")

q("rocket4", "Tier 4 Rocket: Glacio", deps=["rocket3", "cataclysm/ender_guardian"],
  icon="ad_astra:tier_4_rocket", tier=5, size=1.5, shape="diamond",
  tasks=[item("ad_astra:tier_4_rocket"), dim("ad_astra:glacio", title="Land on Glacio")], desc="""
    The &eTier 4 Rocket&r, built from Calorite, leaves our solar system for
    &bProxima Centauri&r. Gated behind the &5Ender Guardian&r (Cataclysm).

    &bGlacio&r is freezing cold, but it has air: you can take your helmet off.""")

q("jet_suit", "The Jet Suit", deps="rocket4", icon="ad_astra:jet_suit", tier=5, optional=True,
  desc="""
    The very best Ad Astra armor is the &eJet Suit&r: more protection, more oxygen and
    &bflight&r. Flight burns the suit's stored &epower&r, so recharge it in an Energizer.
    It's one of the most expensive things in the pack, a true late-game reward.""")

q("where_next", "Where Next?", deps="moon", icon="minecraft:compass", shape="hexagon", tier=2,
  desc="""
    Space is a long road with boss gates on the way:

    &cBosses & Combat&r: Ignis, the Netherite Monstrosity and the Ender Guardian (Cataclysm)
    unlock the bigger rockets.
    &bTech&r: better generators make space machines easier to run.""")
