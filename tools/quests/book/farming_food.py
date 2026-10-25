from dsl import *

C = chapter("farming_food", "Farming & Food", group="life", icon="farmersdelight:cooking_pot",
            subtitle="Grow it, cook it, share it. Eating well makes you stronger!")
q = C.quest

q("intro", "What is Farmer's Delight?", icon="farmersdelight:cooking_pot", size=1.5, shape="gear", desc="""
    Welcome to the kitchen! &eFarmer's Delight&r turns food into a real hobby:
    new crops, a cutting board, a skillet, a cooking pot and big feasts to share.

    Cooked meals fill you up much more than plain bread, and many give nice effects.
    Even better: eating lots of &adifferent&r foods gives you extra hearts (see "A Varied Diet").

    Nothing here is hard. Follow the quests one at a time and you'll be a chef in no time!""",
  rewards=[give("minecraft:bread", 8), give("minecraft:wheat_seeds", 16)])

# --- crops ------------------------------------------------------------------------------
q("knife", "Every Chef Needs a Knife", deps="intro", icon="farmersdelight:flint_knife",
  tasks=item("farmersdelight:flint_knife"), desc="""
    Knives are the heart of Farmer's Delight. They cut food on the cutting board,
    and they're also handy weapons.

    A &eFlint Knife&r is the cheapest. Iron, gold and diamond knives come later.
    Tip: breaking tall grass with a knife can give you &eStraw&r.""",
  rewards=[give("minecraft:flint", 4), give("minecraft:carrot", 8)])

q("wild_crops", "Wild Veggies", deps="knife", icon="farmersdelight:wild_cabbages",
  tasks=[item("farmersdelight:cabbage"), item("farmersdelight:tomato"), item("farmersdelight:onion")],
  desc="""
    Look for wild plants out in the world: &eWild Cabbage&r, &eWild Onion&r and
    &eTomato Shrubs&r grow in different biomes. Break them for crops and seeds.

    Plant the seeds on farmland like wheat. Onions are planted whole, like potatoes.
    Hover a crop and press &eU&r to see everything you can cook with it.""",
  rewards=[give("farmersdelight:cabbage_seeds", 8), give("farmersdelight:tomato_seeds", 8),
           give("farmersdelight:onion", 4)])

q("rice", "Rice Paddies", deps="wild_crops", icon="farmersdelight:rice_panicle",
  tasks=item("farmersdelight:rice", 8), desc="""
    &eWild Rice&r grows in shallow water near rivers and swamps.

    Rice is planted &ein water&r, one block deep, on top of dirt or grass.
    When it's tall and golden, harvest the panicles. Rice goes into sushi, fried rice and more.""",
  rewards=[give("minecraft:bone_meal", 16)])

q("tomato_rope", "Tomatoes on a Rope", deps="wild_crops", icon="farmersdelight:rope", optional=True,
  tasks=adv("farmersdelight:main/harvest_ropelogged_tomato", title="Harvest a tomato that climbed a rope"),
  desc="""
    Tomatoes love to climb! Place a &eRope&r above a tomato plant and it grows up the rope,
    giving you more tomatoes from one spot.

    Ropes are made from straw. You can also climb ropes yourself.""",
  rewards=[give("farmersdelight:tomato", 8)])

q("rich_soil", "Rich Soil", deps="rice", icon="farmersdelight:rich_soil",
  tasks=item("farmersdelight:rich_soil"), desc="""
    Craft &eOrganic Compost&r and place it on the ground. Over time it turns into
    &eRich Soil&r all by itself.

    Rich soil makes crops grow faster. Mushrooms planted on it grow into big colonies
    you can harvest again and again.""", tier=2,
  rewards=[give("farmersdelight:organic_compost", 4), give("minecraft:brown_mushroom", 4)])

q("seasons", "The Turning Seasons", deps="wild_crops", icon="sereneseasons:calendar",
  tasks=item("sereneseasons:calendar"), desc="""
    The overworld has &aspring, summer, autumn and winter&r (Serene Seasons).
    Each season lasts a few weeks of in-game days.

    Crops planted &cout of season&r grow very slowly. Hover over a seed: its tooltip lists the
    seasons it likes. Deep underground (below about &eY 48&r) crops grow all year round.

    A &eCalendar&r shows the current season and day. A &eSeason Sensor&r gives a redstone signal.

    Village farmers here are smarter too: they harvest and replant modded crops.""",
  rewards=[give("minecraft:pumpkin_seeds", 8), give("minecraft:melon_seeds", 8)])

q("cutting_board", "The Cutting Board", deps="knife", icon="farmersdelight:cutting_board",
  tasks=item("farmersdelight:cutting_board"), desc="""
    Place the &eCutting Board&r, put an item on it, then right-click it with your knife.

    It slices meat, chops cabbage into leaves, turns pumpkins into slices and strips bark
    from logs. Other tools work too: try an axe on a log!""",
  rewards=[give("minecraft:pumpkin", 2), give("minecraft:beef", 6)])

q("pot", "Cooking Pot Time", deps="cutting_board", icon="farmersdelight:cooking_pot",
  tasks=adv("farmersdelight:main/place_cooking_pot", title="Place a Cooking Pot"), desc="""
    The &eCooking Pot&r makes soups, stews and meals. It needs &cheat underneath&r:
    a campfire, or a &eStove&r (which can also cook six things on top).

    Put the ingredients in, and a bowl if the meal needs one. Wait a moment and the
    meal appears on the right. Shift-click it out.

    Not sure what you can make? Hover the pot and press &eU&r.""",
  rewards=[give("minecraft:bowl", 16), give("minecraft:campfire")])

q("skillet", "Sizzle!", deps="pot", icon="farmersdelight:skillet",
  tasks=item("farmersdelight:skillet"), desc="""
    The &eSkillet&r cooks food fast. Place it on something hot and drop food in,
    or hold it in your hand and right-click to cook while standing near heat.

    It's also a surprisingly good frying-pan weapon. Bonk!""",
  rewards=[give("minecraft:chicken", 6), give("minecraft:egg", 8)])

q("five_dishes", "Cook Five Dishes", deps="skillet", icon="farmersdelight:vegetable_soup",
  size=1.5, shape="heart", tier=3,
  tasks=[item("farmersdelight:mixed_salad"), item("farmersdelight:vegetable_soup"),
         item("farmersdelight:fried_rice"), item("farmersdelight:pumpkin_soup"),
         item("farmersdelight:bacon_sandwich")],
  desc="""
    Time to show off! Cook these five dishes.

    Salads and sandwiches are crafted, soups and fried rice come from the pot.
    Press &eR&r on each one to see its recipe.

    Each new dish you eat also counts toward your &aFood Diversity&r. Tasty &oand&r useful.""",
  rewards=[give("farmersdelight:apple_pie"), give("farmersdelight:sweet_berry_cheesecake"),
           give("minecraft:cake")])

q("feast", "A Feast for Friends", deps="five_dishes", icon="farmersdelight:roast_chicken_block",
  tasks=adv("farmersdelight:main/place_feast", title="Place a feast"), tier=3, desc="""
    Feasts are big meals you &eplace on a table&r: Roast Chicken, Stuffed Pumpkin,
    Honey Glazed Ham, Shepherd's Pie and Rice Roll Medley.

    Right-click a feast with an empty bowl to serve a portion. One feast feeds the
    whole group, so cook one and invite everyone over!""",
  rewards=[give("minecraft:honey_bottle", 4), give("plushies:pig_plushie")])

q("pet_food", "Treats for Pets", deps="pot", icon="farmersdelight:dog_food", optional=True,
  tasks=item("farmersdelight:dog_food"), desc="""
    &eDog Food&r feeds and heals tamed wolves, and &eHorse Feed&r heals horses.
    Spoil your friends! See the &aPets & Critters&r chapter.""",
  rewards=[give("minecraft:bone", 8)])

# --- eating well ------------------------------------------------------------------------
q("diet", "A Varied Diet", deps="pot", icon="solonion:food_book",
  tasks=item("solonion:food_book"), desc="""
    &eSpice of Life&r rewards a varied diet. It remembers the last foods you ate:
    the more &adifferent&r foods, the higher your &eFood Diversity&r.

    As it rises you unlock bonuses: &cextra hearts&r first, then things like strength,
    regeneration and speed. Eating the same thing over and over lowers it,
    and it resets when you die.

    The &eFood Book&r (book + potato) shows your diversity and what's next.
    There's also an &eSOL&r button in your inventory. A &eLunchbag&r carries lots of snacks.""",
  rewards=[give("minecraft:golden_carrot", 4), give("minecraft:baked_potato", 8)])

q("kitchen_book", "Cooking for Blockheads", deps="pot", icon="cookingforblockheads:recipe_book",
  tasks=item("cookingforblockheads:recipe_book"), desc="""
    Too many recipes? The &eCooking for Blockheads&r book shows food you can make
    &eright now&r from what's in your inventory.

    Later it becomes the brain of a whole kitchen.""",
  rewards=[give("minecraft:sugar", 16), give("minecraft:milk_bucket")])

q("kitchen", "Build a Kitchen", deps="kitchen_book", icon="cookingforblockheads:cooking_table", tier=2,
  tasks=item("cookingforblockheads:cooking_table"), desc="""
    The &eCooking Table&r is the centre of a multiblock kitchen. Connect counters,
    a fridge, a sink (free water), an oven, a spice rack and a tool rack to it.

    Open the table and click any dish to cook it from everything stored in the whole kitchen.
    Dye the blocks to match your house!""",
  rewards=[give("minecraft:white_dye", 8), give("minecraft:iron_ingot", 8)])

# --- more crops and drinks --------------------------------------------------------------
q("croptopia", "Croptopia: So Many Crops", deps="wild_crops", icon="croptopia:strawberry", desc="""
    &eCroptopia&r adds dozens of crops and fruit trees: strawberries, corn, coffee, bananas,
    lemons and many more. You'll find its seeds and fruit trees out in the world
    as you explore different biomes.

    It has its own cooking tools too (frying pan, food press, mortar and pestle).
    Every new crop is a new food for your diet!""",
  rewards=[give("croptopia:strawberry_seed", 4), give("croptopia:corn_seed", 4),
           give("croptopia:tea_seed", 4), give("croptopia:coffee_seed", 4)])

q("grapes", "Grapes of Joy", deps="croptopia", icon="vinery:red_grape",
  tasks=item("vinery:red_grape", 8), desc="""
    &e[Let's Do] Vinery&r is all about grapes and wine. Wild grape bushes grow in
    many biomes (red and white, plus jungle, savanna and taiga kinds).

    Plant the seeds. Planting them on a &eGrapevine Stem&r gives a bigger harvest,
    and jungle grapes like to climb a &eLattice&r.""",
  rewards=[give("vinery:white_grape_seeds", 4)])

q("press", "Squish!", deps="grapes", icon="vinery:grapevine_pot",
  tasks=item("vinery:grapevine_pot"), desc="""
    Grapes become juice in a &eGrapevine Pot&r. Apples have their own &eApple Press&r.
    Juice is tasty by itself, but it's even better as wine.""",
  rewards=[give("minecraft:apple", 16)])

q("wine", "A Fine Vintage", deps="press", icon="vinery:red_wine", tier=2,
  tasks=item("vinery:red_wine"), desc="""
    Fill a &eFermentation Barrel&r with juice, add the extra ingredients and an empty
    &eWine Bottle&r, and wait.

    Wine keeps getting better with age, so store some in a wine rack and forget about it.
    Different wines give different effects. Press &eR&r on a wine to see what it needs.""",
  rewards=[give("vinery:wine_bottle", 4), give("minecraft:sugar", 16)])

q("brewing", "Brewin' and Chewin'", deps="pot", icon="brewinandchewin:keg", optional=True, tier=2,
  tasks=item("brewinandchewin:keg"), desc="""
    The &eKeg&r ferments drinks (mead, kombucha, rice wine) and makes cheese,
    jam and pickles. It cares about temperature:
    some recipes want it warm, others cold.

    Big cheese wheels age slowly when you place them. Pizza and quiche are worth the wait!""",
  rewards=[give("minecraft:honey_bottle", 4), give("minecraft:milk_bucket")])

# --- delights from other worlds ---------------------------------------------------------
q("delights", "Delights Everywhere", deps="five_dishes", icon="endersdelight:chorus_pie", desc="""
    Almost every world in Strata has its own Farmer's Delight add-on. When you visit, bring
    your knife and a pot:

    &5End&r: chorus pies and shulker dishes (Ender's Delight).
    &cNether&r: hot sauce, hoglin feasts and spicy peppers (My Nether's Delight).
    &aTwilight Forest&r, &bAether&r: their own meals (Twilight's Flavor, Aether's Delight).
    &dArs Nouveau&r: magical fruit pies and teas. &4Vampirism&r: blood-themed treats.
    Cataclysm bosses even drop ingredients for wild dishes (L_Ender's Cataclysm Delight).

    Every one is a new food for your diet!""",
  rewards=[give("minecraft:bowl", 16)])

q("nether_food", "Spicy!", deps="delights", icon="mynethersdelight:bullet_pepper", optional=True,
  tasks=item("mynethersdelight:bullet_pepper", 4), desc="""
    &eBullet Peppers&r grow in the Nether. They spice up My Nether's Delight recipes,
    which bring hot dogs, chili dogs and hoglin feasts.""",
  rewards=[give("minecraft:cooked_porkchop", 8)])

q("end_food", "Strange Snacks", deps="delights", icon="endersdelight:chorus_pie", optional=True, tier=2,
  tasks=item("endersdelight:chorus_pie"), desc="""
    End cooking! Chorus fruit becomes a pie in Ender's Delight.
    Some End foods have funny side effects. Read the tooltip before you eat!""",
  rewards=[give("minecraft:golden_apple")])

q("where_next", "Where Next?", deps=["feast", "diet"], icon="minecraft:oak_sign", shape="hexagon", desc="""
    Your kitchen is open for business! Where to now?

    &aPets & Critters&r: tame a friend and feed it treats.
    &aBuilding & Decorating&r: give your kitchen a cosy home.
    &aFishing&r: fish are great food (Ocean's Delight has seafood recipes).
    &bCreate&r chapters: automate your farm and kitchen with machines later on.""",
  rewards=[give("plushies:chicken_plushie"), give("minecraft:cake")])
