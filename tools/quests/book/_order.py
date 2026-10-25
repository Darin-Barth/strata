# Chapter groups (key, title, icon) and the chapter modules in book order.
# A chapter with group=None sits above all groups (the Welcome chapter).
GROUPS = [
    ("tech", "Tech", "create:cogwheel"),
    ("magic", "Magic", "ars_nouveau:novice_spell_book"),
    ("explore", "Exploration", "minecraft:filled_map"),
    ("bosses", "Bosses & Combat", "minecraft:netherite_sword"),
    ("life", "Life & Cozy", "farmersdelight:cooking_pot"),
]

CHAPTERS = [
    "welcome",
    # tech
    "create_basics", "create_power", "create_trains", "create_airships", "create_extras",
    "immersive_engineering", "mekanism", "ae2", "more_machines", "logistics", "oritech",
    "resource_farming", "endgame",
    # magic
    "ars_nouveau", "irons_spells", "occultism", "neo_vitae", "theurgy", "vampirism",
    # exploration
    "explorers_guide", "nether", "twilight_forest", "aether", "deeper_darker", "ad_astra", "the_end",
    "pokemon_world",
    # bosses & combat
    "combat_gear", "cataclysm", "ice_and_fire", "boss_hunter",
    # life & cozy
    "farming_food", "pets_critters", "building", "storage", "fishing",
]
