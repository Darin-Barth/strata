from dsl import *

C = chapter("pets_critters", "Pets & Critters", group="life", icon="minecraft:bone",
            subtitle="Tame a friend, meet the wildlife, collect plushies")
q = C.quest

q("intro", "What's Out There?", icon="plushies:wolf_plushie", size=1.5, shape="gear", desc="""
    Strata's world is full of animals: otters, red pandas, ducks, frogs that run
    their own villages, butterflies, snails, giraffes and lots more.

    Many can be &etamed&r, some can be &ebred&r, and a few will even live in your pocket.
    This chapter is a gentle tour. Go at your own pace and say hi to everyone!""",
  rewards=[give("minecraft:bone", 8), give("minecraft:cod", 8), give("alexsmobs:animal_dictionary")])

# --- your first pet ---------------------------------------------------------------------
q("tame", "A Best Friend", deps="intro", icon="minecraft:bone",
  tasks=adv("minecraft:husbandry/tame_an_animal", title="Tame any animal"), desc="""
    Wolves love &ebones&r, cats love &eraw fish&r, parrots love seeds.
    Keep feeding until you see hearts.

    In Strata you can also tame &efoxes&r and win over &ehorses&r with patience (Redomesticate).
    Your swings pass right through your own pets, so you won't bonk them by accident.""",
  rewards=[give("minecraft:name_tag"), give("minecraft:lead", 2)])

q("pet_bed", "A Bed for Your Pet", deps="tame", icon="redomesticate:pet_bed_red",
  tasks=check("Craft and place a Pet Bed"), desc="""
    Here's the most important pet tip: give your pet a &ePet Bed&r.

    If a pet with a bed dies, it &arespawns at its bed&r instead of being gone forever.
    Look at a bed (Jade shows it) to see whose bed it is.

    Pet beds come in every color. Put one somewhere cozy at home.""",
  rewards=[give("minecraft:white_wool", 8), give("plushies:cat_plushie")])

q("drum", "Sit! Stay! Follow!", deps="pet_bed", icon="redomesticate:drum", optional=True,
  tasks=item("redomesticate:drum"), desc="""
    The &eCommand Drum&r tells your nearby pets to &ewander&r, &estay&r or &efollow&r,
    all at once. Great when you have a whole pack.

    Redomesticate also adds pet-only enchantments that turn up as books in loot.
    Check them out with &eU&r if you find one.""",
  rewards=[give("minecraft:bone", 16)])

q("feather_stick", "Play Time", deps="pet_bed", icon="redomesticate:feather_on_a_stick", optional=True,
  tasks=item("redomesticate:feather_on_a_stick"), desc="""
    A &eFeather on a Stick&r. Wave it around and see who comes running!""",
  rewards=[give("minecraft:salmon", 8)])

q("breed", "Baby Animals", deps="tame", icon="minecraft:wheat",
  tasks=adv("minecraft:husbandry/breed_an_animal", title="Breed two animals"), desc="""
    Feed two adult animals of the same kind their favorite food and a baby pops out.

    Not sure what an animal eats? Hover over a food and press &eU&r: the
    &eBreeding&r and &eTaming&r tabs (Just Enough Breeding) show who likes it.""",
  rewards=[give("minecraft:wheat", 32), give("minecraft:carrot", 16)])

q("horse", "Horse Sense", deps="breed", icon="horseexpert:monocle",
  tasks=item("horseexpert:monocle"), desc="""
    Horses are your first fast way to travel. But which horse is best?

    Wear the &eMonocle&r and look at a horse, donkey or other mount to see its
    &ehealth, speed and jump height&r. Breed the fastest ones for even faster foals.""",
  rewards=[give("minecraft:saddle"), give("minecraft:golden_carrot", 8)])

q("horn", "Call Your Horse", deps="horse", icon="horseman:copper_horn", tier=2,
  tasks=item("horseman:copper_horn"), desc="""
    &eSneak + use&r the &eCopper Horn&r on your horse to bind it.
    Then &euse&r the horn and your horse comes to you, as long as it can hear the horn:
    it has to be nearby and in the same dimension.

    Horses can also be hitched with a lead, and mounted horses handle more smoothly here.""",
  rewards=[give("farmersdelight:horse_feed", 4), give("minecraft:apple", 8)])

# --- pocket pets ------------------------------------------------------------------------
q("pocket_pet", "Pets in Your Pocket", deps="tame", icon="inventorypets:pet_chicken", tier=2,
  tasks=adv("inventorypets:1", title="Get your first Inventory Pet"), desc="""
    &eInventory Pets&r are tiny helpers that live in your inventory. Each one has a
    little power. You can't craft them here: you &afind&r them in chests. Dungeons,
    mineshafts and temples hold the cozy ones; strongholds, mansions and fortresses
    the handy ones; Nether fortresses and bastions the Nether Portal pet.
    The legendary ones are rare finds in End cities, ancient cities, bastion treasure and
    ominous trial vaults, and five of them can drop from a boss: the Cloud from the Sun Spirit,
    the Sun from Ignis, the Wither from the Harbinger, the Black Hole from the Ender Guardian
    and the Pufferfish from Scylla or the Leviathan.

    Some cute ones to look out for:

    &eChicken Pet&r: a speed boost, and it lays eggs for you.
    &eCow Pet&r: clears bad potion effects and fills buckets with milk.
    &eSiamese Pet&r: brings you little gifts.
    &eHeart Pet&r: heals your friends and pets.

    Each pet has a &afavorite food&r (look at its tooltip). Pets only eat from a
    &eFeed Bag&r in your inventory, never loose food, and only while the pet sits in your hotbar.""",
  rewards=[give("inventorypets:nugget_coal", 16), give("inventorypets:nugget_lapis", 8)])

q("feed_bag", "Snack Pack", deps="pocket_pet", icon="inventorypets:feed_bag",
  tasks=item("inventorypets:feed_bag"), desc="""
    Pets only eat from a &eFeed Bag&r: put their favorite food inside and keep the bag
    anywhere in your inventory. Loose food in your inventory is never eaten.""",
  rewards=[give("inventorypets:nugget_lapis", 8)])

q("pet_collector", "Pet Collector", deps="pocket_pet", icon="inventorypets:pet_siamese", tier=3,
  tasks=adv("inventorypets:5", title="Collect five Inventory Pets"), desc="""
    Collect five different pocket pets! Good ones for cozy players:
    the Sheep, Mooshroom, Banana, Jukebox, Bed and Crafting Table pets.

    Press &eU&r on a pet's food to see how to make it.""",
  rewards=[give("inventorypets:nugget_emerald", 8), give("plushies:sheep_plushie")])

q("pet_dungeon", "Find a Pet Dungeon", deps="pocket_pet", icon="inventorypets:nugget_diamond",
  size=1.5, shape="heart", tier=3,
  tasks=structure("inventorypets:tree_top", title="Visit a Tree Top"), desc="""
    Inventory Pets has its own little dungeons with pet goodies inside.
    &eTree Tops&r are hidden high up in big trees. Keep your eyes on the canopy!

    Watch out: they're guarded, and some chests are booby-trapped.""",
  rewards=[give("inventorypets:nugget_diamond", 4), give("minecraft:golden_apple")])

q("pet_dungeon_deep", "Underground Pet Dungeon", deps="pet_dungeon", icon="inventorypets:nugget_obsidian",
  optional=True, tier=3,
  tasks=structure("inventorypets:underground_dungeon", title="Visit an Underground Dungeon"), desc="""
    There are &eUnderground Dungeons&r too, plus sea caves and stranger ones.
    Bring torches and a friend.""",
  rewards=[give("inventorypets:nugget_obsidian", 8)])

# --- villagers ---------------------------------------------------------------------------
q("villager_block", "Villager in a Box", deps="intro", icon="easy_villagers:trader", tier=2,
  tasks=item("easy_villagers:villager", title="Pick up a villager"), desc="""
    &eSneak + right-click&r a villager to pick it up as an item (Easy Villagers)!
    No more pushing villagers through fields with boats.

    Put one into a &eTrader&r block for a neat one-block shop, or into a
    &eFarmer&r or &eBreeder&r block for little villager farms.

    &eGuard Villagers&r patrol villages and protect them from raids. Be nice to them.""",
  rewards=[give("minecraft:emerald", 16), give("minecraft:bread", 16)])

# --- wildlife -----------------------------------------------------------------------------
q("animal_book", "The Animal Dictionary", deps="intro", icon="alexsmobs:animal_dictionary",
  tasks=check("Read the Animal Dictionary"), desc="""
    &eAlex's Mobs&r adds dozens of real and strange animals: elephants, raccoons,
    hummingbirds, kangaroos, crows and many more. Some can be tamed!

    The &eAnimal Dictionary&r (you got one for starting this chapter) tells you about
    every one: where it lives, what it eats, and whether it's friendly.""",
  rewards=[give("alexsmobs:banana", 4), give("minecraft:book", 2)])

q("capture_net", "Bug Catcher", deps="animal_book", icon="naturalist:capture_net",
  tasks=item("naturalist:capture_net"), desc="""
    &eNaturalist&r fills forests, swamps and savannas with snails, ducks, butterflies,
    fireflies, bears, giraffes and more.

    A &eCapture Net&r (bamboo and string) catches small critters like butterflies
    so you can carry them home to your garden.""",
  rewards=[give("minecraft:honeycomb", 4), give("minecraft:sweet_berries", 16)])

q("friends", "Friends and Foes", deps="animal_book", icon="friendsandfoes:copper_button", tier=2,
  tasks=adv("friendsandfoes:adventure/summon_copper_golem", title="Build a Copper Golem"), desc="""
    &eFriends & Foes&r brings back mobs from the Minecraft mob votes: flower cows
    (&eMooblooms&r), little &eGlares&r that find dark spots, crabs, penguins and more.

    Build a &eCopper Golem&r the way you'd build a snow golem, from a copper block,
    a carved pumpkin and a lightning rod. It wanders around pressing copper buttons!""",
  rewards=[give("minecraft:copper_block", 2), give("friendsandfoes:buttercup", 4)])

q("flower_crown", "Flower Crown", deps="capture_net", icon="cnb:flower_crown", optional=True,
  tasks=item("cnb:flower_crown"), desc="""
    &eCreatures and Beasts&r adds lizards, sporelings, cute cindershells and more.
    Pick three &eMinipad Flowers&r from lily ponds and craft a pretty &eFlower Crown&r.""",
  rewards=[give("minecraft:lily_pad", 4)])

q("critters", "Tiny Companions", deps="capture_net", icon="crittersandcompanions:koi_fish", desc="""
    &eCritters and Companions&r adds the cutest little animals: &eotters&r,
    &ered pandas&r, &eferrets&r, &ekoi fish&r, &edragonflies&r, sea bunnies,
    tiny Shima Enaga birds and more.

    Some can be tamed and will follow you around. Go meet them!""",
  rewards=[give("minecraft:salmon", 8), give("minecraft:bamboo", 16)])

q("ribbits", "The Frog Village", deps="critters", icon="ribbits:toadstool", tier=2,
  tasks=structure("ribbits:ribbit_village", title="Visit a Ribbit village"), desc="""
    Deep in the swamps live the &eRibbits&r: friendly frog people with their own
    little villages among the toadstools and lily pads.

    There are fishermen, gardeners, a merchant and even a sorcerer. Say hello!""",
  rewards=[give("ribbits:swamp_lantern", 4), give("ribbits:swamp_daisy", 4)])

q("kobolds", "Kobold Den", deps="ribbits", icon="kobolds:kobold_iron_pickaxe", optional=True, tier=2,
  tasks=structure("kobolds:kobold_den", title="Find a Kobold den"), desc="""
    &eKobolds&r are small lizard-folk who live in dens. There are warriors, engineers,
    enchanters and even pirates. Not all of them are friendly, so look before you leap.""",
  rewards=[give("minecraft:emerald", 8)])

q("royals", "Long Live the King?", deps="friends", icon="royalvariations:spiritual_crown", optional=True,
  tier=3, tasks=adv("royalvariations:royal_variations", title="Defeat any royal mob"), desc="""
    Very rarely you'll meet a &6royal&r zombie, skeleton, creeper or enderman wearing a crown.
    These kings are mini-bosses, much tougher than normal mobs.

    Fight them with friends and good gear. Their drops are worth it.""",
  rewards=[give("minecraft:golden_apple", 2)])

# --- plushies -----------------------------------------------------------------------------
q("plushie", "Plushies!", deps="intro", icon="plushies:axolotl_plushie", shape="heart",
  tasks=check("Craft any plushie"), desc="""
    Soft, squishy plushies of almost every mob in the game, from cats and foxes
    to wardens and dragons. Made from wool and string.

    Search &e@plushies&r in the item list, press &eR&r on one you like, and craft it.
    Put them on shelves, beds and windowsills. Collect them all!""",
  rewards=[give("plushies:red_fox_plushie"), give("plushies:frog_plushie"), give("minecraft:white_wool", 16)])

q("where_next", "Where Next?", deps=["pet_bed", "pet_dungeon"], icon="minecraft:oak_sign", shape="hexagon",
  desc="""
    You've made lots of new friends! What now?

    &aFarming & Food&r: cook Dog Food and Horse Feed for your pets.
    &aBuilding & Decorating&r: build your pets a cozy home.
    &aFishing&r: cats love fish, and there are hundreds to catch.
    &aExplorer's Guide&r: the farther you go, the stranger the animals.""",
  rewards=[give("plushies:panda_plushie"), give("plushies:bee_plushie")])
