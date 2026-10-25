from dsl import *

C = chapter("deeper_darker", "Deeper and Darker", group="explore", icon="minecraft:sculk_shrieker",
            subtitle="The Warden, its city and the Otherside")
q = C.quest

q("intro", "What is Deeper and Darker?", deps="welcome/iron_age", icon="minecraft:sculk",
  size=1.5, shape="gear", desc="""
    Far below the surface, in the &8Deep Dark&r, sculk spreads over everything.
    &eDeeper and Darker&r goes further: beat the &3Warden&r and you can open a portal to
    the &3Otherside&r, a whole dimension of sculk.

    &cThis is one of the most dangerous places in Strata.&r Go when you're well geared,
    and preferably with friends.""",
  rewards=[give("minecraft:torch", 32)])

q("sneaky", "Quiet Please", deps="intro", icon="minecraft:sculk_sensor", desc="""
    Sculk &eSensors&r hear footsteps, block breaking and thrown items.
    Sculk &eShriekers&r call the Warden if they're set off too often.

    &eSneak&r to walk silently. Wool and carpet soak up vibrations, so they're quiet to walk on.
    Darkness is part of the place: bring night vision if you can.""",
  rewards=[give("minecraft:white_wool", 16)])

q("city", "An Ancient City", deps="sneaky", icon="minecraft:reinforced_deepslate", tier=3,
  tasks=structure("minecraft:ancient_city", title="Find an Ancient City"), desc="""
    Ancient Cities sit deep under the mountains, near Y -50. They're huge, dark and silent.

    Their chests are some of the best in the game: &eSwift Sneak&r books, echo shards,
    smithing templates, and even a &dBell Fragment&r for the Pokémon World portal.
    In the middle stands a giant frame of &8reinforced deepslate&r. Remember it.""",
  rewards=[give("minecraft:golden_carrot", 16)])

q("echo", "Echo Shards", deps="city", icon="minecraft:echo_shard", tier=2,
  tasks=item("minecraft:echo_shard", 4), desc="""
    Echo shards are found in ancient city chests. Eight of them and a compass make a
    &eRecovery Compass&r, which points to where you last died.

    You'll need them for Warden gear too.""",
  rewards=[give("minecraft:compass")])

q("warden", "The Warden", deps="city", icon="minecraft:sculk_catalyst", tier=5,
  tasks=kill("minecraft:warden"), desc="""
    The &3Warden&r is blind, smells you and hears every move. Its sonic boom goes through
    shields and walls. Most players should run, not fight!

    If you do fight: bring the best armor you have, strength potions and friends.
    Deeper and Darker gives it a &eHeart of the Deep&r and &eWarden Carapace&r to drop.""")

q("portal", "The Otherside", deps="warden", icon="deeperdarker:heart_of_the_deep", tier=4,
  tasks=dim("deeperdarker:otherside", title="Enter the Otherside"), desc="""
    Use the &eHeart of the Deep&r on the big reinforced deepslate frame in an ancient city.
    It fills with a dark portal to the &3Otherside&r.

    The Otherside has no sun, little light and lots of sculk monsters.
    Mark the portal with a waypoint so you can find your way home.""",
  rewards=[give("minecraft:glowstone", 16)])

q("compass", "Ancient Compass", deps="warden", icon="deeperdarker:ancient_compass", tier=3,
  tasks=item("deeperdarker:ancient_compass"), desc="""
    Four pieces of &eWarden Carapace&r around a compass make an &eAncient Compass&r.
    In the Otherside it points to the nearest &eAncient Temple&r.""")

q("temple", "The Ancient Temple", deps=["portal", "compass"], icon="deeperdarker:gloomslate",
  tier=4, tasks=structure("deeperdarker:ancient_temple", title="Explore an Ancient Temple"),
  desc="""
    The Otherside's great temples hold its best treasure (and its guards).
    Search the basement, the fountain and the top of the temple.""",
  rewards=[give("minecraft:diamond", 4)])

q("mobs", "Otherside Wildlife", deps="portal", icon="deeperdarker:sculk_bone", tier=3,
  tasks=[item("deeperdarker:sculk_bone", 4), item("deeperdarker:resonarium", 4)], desc="""
    Otherside mobs drop the materials you need here:
    &eShattered&r drop sculk bones, &eSludges&r drop resonarium,
    leeches and snappers drop soul dust.

    Watch out for &cStalkers&r. Their name says it all.""",
  rewards=[give("minecraft:cooked_beef", 16)])

q("resonarium", "Resonarium Gear", deps="mobs", icon="deeperdarker:resonarium_plate", tier=3,
  tasks=item("deeperdarker:resonarium_plate"), desc="""
    Craft a &eResonarium Plate&r. With a &eResonarium Upgrade&r template (ancient city and
    stronghold chests) it upgrades &firon&r gear in a smithing table.""")

q("reinforced", "Reinforced Echo Shard", deps="warden", icon="deeperdarker:reinforced_echo_shard",
  tier=4, tasks=item("deeperdarker:reinforced_echo_shard"), desc="""
    An echo shard wrapped in Warden Carapace and phantom membranes.
    This is the upgrade material for &3Warden&r gear.""")

q("warden_gear", "Warden Armor", deps="reinforced", icon="deeperdarker:warden_chestplate", tier=5,
  tasks=item("deeperdarker:warden_chestplate"), desc="""
    Find a &eWarden Upgrade&r smithing template in ancient city chests, then upgrade a
    &enetherite&r chestplate with a Reinforced Echo Shard. Warden gear is better than netherite.

    Copy the template with diamonds and sculk so you can do the whole set.""")

q("staff", "Sonorous Staff", deps=["warden", "mobs"], icon="deeperdarker:sonorous_staff", tier=4,
  optional=True, tasks=item("deeperdarker:sonorous_staff"), desc="""
    Soul crystals, sculk bones and a Heart of the Deep make a &eSonorous Staff&r:
    your own sonic boom, just like the Warden's.""")

q("where_next", "Where Next?", deps="portal", icon="minecraft:compass", shape="hexagon", tier=2,
  desc="""
    You've seen the darkest place in the pack. Other big trips:

    &5The End&r: Warden gear is a great way to face the Ender Dragon.
    &cThe Pokémon World&r: ancient city chests are a good place to find a Bell Fragment.
    &cBosses & Combat&r: Cataclysm's bosses.""")
