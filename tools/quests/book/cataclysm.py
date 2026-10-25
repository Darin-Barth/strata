from dsl import *

C = chapter("cataclysm", "L_Ender's Cataclysm", group="bosses", icon="cataclysm:monstrous_horn",
            subtitle="Eight great bosses, their lairs, and the late game they unlock")
q = C.quest

q("intro", "What is Cataclysm?", icon="cataclysm:altar_of_fire", size=1.5, shape="gear", desc="""
    &cL_Ender's Cataclysm&r adds huge boss fights, each in its own lair:
    a forge in the Nether, an arena of fire, a pyramid, a factory, a sunken city, a frozen prison,
    a sky-high temple and a citadel in the End.

    &6Why it matters:&r killing these bosses is how Strata unlocks the late game.
    Top Mekanism and AE2 tiers and &ecross-dimension wireless&r wait behind them.

    Bosses keep their designed strength. Bring good gear, food, and friends.""",
  rewards=[give("minecraft:golden_apple", 2)])

q("eyes", "Eyes That Point the Way", deps=["intro", "welcome/nether"], icon="cataclysm:monstrous_eye",
  tier=2, tasks=item("cataclysm:monstrous_eye"), desc="""
    Each lair has its own &eEye&r. Throw it like an Eye of Ender and it flies toward the
    nearest lair of that kind. Press &eR&r on each to see the recipe:

    &cMonstrous&r (Soul Forge), &6Flame&r (Burning Arena), &eDesert&r (Cursed Pyramid),
    &7Mech&r (Ancient Factory), &3Abyss&r (Sunken City), &bCurse&r (Frosted Prison),
    &9Storm&r (Acropolis), &5Void&r (Ruined Citadel).

    Start with the &cEye of Monstrous&r.""",
  rewards=[give("minecraft:ender_eye", 4)])

# --- Nether line ---------------------------------------------------------------------------
q("netherite_monstrosity", "The Netherite Monstrosity", deps="eyes", icon="cataclysm:infernal_forge",
  tier=4, size=1.5, shape="hexagon", tasks=kill("cataclysm:netherite_monstrosity"), desc="""
    A giant war machine guarding the &cSoul Forge&r, a blackstone smithy in the Nether.

    It's slow but hits like a truck and throws lava. Keep moving, stay out of the lava,
    and never fight it in a corner.

    &6Drops:&r the &eInfernal Forge&r (a hammer-pickaxe), the &eMonstrous Horn&r and a Lava Power Cell.
    &6Unlocks:&r late Mekanism and AE2 quest lines.""",
  rewards=[give("minecraft:netherite_scrap", 4), give("minecraft:diamond", 8)])

q("monstrous_helm", "Monstrous Helm", deps="netherite_monstrosity", icon="cataclysm:monstrous_helm",
  tier=3, optional=True, tasks=item("cataclysm:monstrous_helm"), desc="""
    Smithing Table: Netherite Upgrade template + netherite helmet + &eMonstrous Horn&r.
    When you drop below half health the helm knocks
    back everything nearby and gives you extra defence and regeneration.""")

q("ignis_ashes", "Burning Ashes", deps="netherite_monstrosity", icon="cataclysm:burning_ashes", tier=2,
  tasks=item("cataclysm:burning_ashes"), desc="""
    Ignis has to be called. You need &eBurning Ashes&r: craft them from 4 &eDying Embers&r,
    dropped by &eIgnited Berserkers&r in Nether fortresses. Ignited Revenants drop ashes directly.

    Then craft an &6Eye of Flame&r to find the &cBurning Arena&r in the Nether Wastes.""",
  rewards=[give("minecraft:magma_cream", 8)])

q("ignis", "Ignis, the Flame", deps="ignis_ashes", icon="cataclysm:ignitium_ingot",
  tier=5, size=1.5, shape="hexagon", tasks=kill("cataclysm:ignis"), desc="""
    Place the Burning Ashes on the &eAltar of Fire&r in the arena and Ignis rises: a burning
    knight who gets more dangerous as the fight goes on.

    Fire resistance helps, but it won't save you from everything.

    &6Drops:&r &eIgnitium Ingots&r (armor and weapons above netherite).
    &6Unlocks:&r late Mekanism and AE2 quest lines.""",
  rewards=[give("minecraft:netherite_ingot", 2), give("minecraft:golden_apple", 4)])

q("ignitium", "Ignitium Gear", deps="ignis", icon="cataclysm:ignitium_helmet", tier=3, optional=True,
  tasks=item("cataclysm:ignitium_helmet"), desc="""
    In a Smithing Table, the &eIgnitium Upgrade&r template + an Ignitium Ingot turns netherite
    armor into Ignitium. Each piece has a perk: lava walking, flame reflex, and a helmet that
    brands enemies you look at.""")

# --- Overworld line ------------------------------------------------------------------------
q("necklace", "The Cursed Pyramid", deps="intro", icon="cataclysm:necklace_of_the_desert", tier=2,
  tasks=item("cataclysm:necklace_of_the_desert"), desc="""
    In the desert stands the &eCursed Pyramid&r (an &eEye of Desert&r finds it). Inside,
    use a &eBrush&r on the suspicious sand: one of the finds is the &eNecklace of the Desert&r.

    Watch for Koboletons: they steal your stuff.""",
  rewards=[give("minecraft:brush"), give("minecraft:emerald", 8)])

q("ancient_remnant", "The Ancient Remnant", deps="necklace", icon="cataclysm:remnant_skull",
  tier=4, size=1.5, shape="hexagon", tasks=kill("cataclysm:ancient_remnant"), desc="""
    Use the Necklace inside the pyramid to wake the &eAncient Remnant&r, a huge skeletal
    beast that calls sandstorms.

    &6Drops:&r &eSandstorm in a Bottle&r, the &eRemnant's Skull&r (summons a tameable
    Modern Remnant) and Ancient Metal.""",
  rewards=[give("minecraft:gold_block", 2), give("minecraft:emerald", 16)])

q("harbinger", "The Harbinger", deps=["netherite_monstrosity", "necklace"], icon="cataclysm:witherite_ingot",
  tier=4, size=1.5, shape="hexagon", tasks=kill("cataclysm:the_harbinger"), desc="""
    Deep underground lies the &7Ancient Factory&r (find it with an &eEye of Mech&r).
    The Harbinger sits dormant inside; it needs a &eNether Star&r to wake, so beat the
    Wither first.

    It fires missiles and lasers, so use cover.

    &6Drops:&r &eWitherite&r for the Wither Assault Shoulder Weapon, Laser Gatling and more.""",
  rewards=[give("minecraft:redstone_block", 8), give("minecraft:diamond", 6)])

q("sacrifice", "Abyssal Sacrifice", deps="harbinger", icon="cataclysm:abyssal_sacrifice", tier=3,
  tasks=item("cataclysm:abyssal_sacrifice"), desc="""
    The &3Sunken City&r lies at the bottom of a deep ocean (use an &eEye of Abyss&r).
    Water breathing and night vision are a must.

    To call its boss you need an &eAbyssal Sacrifice&r. Its pieces: an &eAthame&r from
    Deepling Priests or Warlocks, &eCrystallized Coral&r (from Coral Golem fragments),
    a Heart of the Sea, a nautilus shell and blocks of diamond, emerald, iron, gold and amethyst.""",
  rewards=[give("minecraft:turtle_helmet")])

q("leviathan", "The Leviathan", deps="sacrifice", icon="cataclysm:tidal_claws",
  tier=5, size=1.5, shape="hexagon", tasks=kill("cataclysm:the_leviathan"), desc="""
    Place the Sacrifice on the &eAltar of Abyss&r. The Leviathan is huge, fast underwater,
    and can't be hurt outside the water.

    &6Drops:&r &eTidal Claws&r (a grappling hook) and the &eAbyssal Egg&r.""",
  rewards=[give("minecraft:heart_of_the_sea"), give("minecraft:diamond_block", 2)])

q("maledictus", "Maledictus", deps="harbinger", icon="cataclysm:cursium_ingot",
  tier=4, size=1.5, shape="hexagon", tasks=kill("cataclysm:maledictus"), desc="""
    In snowy plains stands the &bFrosted Prison&r (use an &eEye of Curse&r). Fight through
    the Draugr; the &eAptrgangr&r drops the &eStrange Key&r that opens sealed doors.
    Deep inside, wake Maledictus at the &eCursed Tombstone&r.

    &6Drops:&r &eCursium Ingots&r (another armor set above netherite).""",
  rewards=[give("minecraft:diamond", 8), give("minecraft:golden_carrot", 16)])

q("scylla", "Scylla, the Storm Empress", deps=["leviathan", "maledictus"], icon="cataclysm:essence_of_the_storm",
  tier=5, size=1.5, shape="hexagon", tasks=kill("cataclysm:scylla"), desc="""
    Over warm oceans stands the &9Acropolis&r (use an &eEye of Storm&r). Scylla fights
    with water and lightning.

    &6Drops:&r &eEssence of the Storm&r and &eLacrima&r, for the Ceraunus and Astrape weapons.""",
  rewards=[give("minecraft:diamond_block", 2), give("minecraft:enchanted_golden_apple")])

# --- The End -------------------------------------------------------------------------------
q("ender_guardian", "The Ender Guardian", deps=["ignis", "the_end/dragon"], icon="cataclysm:gauntlet_of_guard",
  tier=5, size=1.5, shape="hexagon", tasks=kill("cataclysm:ender_guardian"), desc="""
    Out on the End's outer islands (past the Dragon's gateway) stands the &5Ruined Citadel&r.
    An &eEye of Void&r points the way. Ender Golems guard it, and so does the Ender Guardian.

    &6Drops:&r the &eGauntlet of Guard&r (pulls enemies to you).
    &6Unlocks:&r &ecross-dimension wireless&r (the AE2 Quantum Network Bridge).""",
  rewards=[give("minecraft:shulker_shell", 4), give("minecraft:diamond_block", 2)])

q("cataclysmfarer", "The Cataclysmfarer", deps=["ender_guardian", "scylla", "ancient_remnant"],
  any_dep=False, icon="cataclysm:music_disc_the_cataclysmfarer", tier=5, shape="diamond",
  tasks=adv("cataclysm:kill_all_bosses", title="Defeat every Cataclysm boss"), desc="""
    Beat every Cataclysm boss. You've reached the summit of Cataclysm!""",
  rewards=[give("minecraft:netherite_ingot", 2), give("minecraft:totem_of_undying")])

# --- add-ons ---------------------------------------------------------------------------------
q("integrated", "Integrated Cataclysm", deps="intro", icon="create:mechanical_crafter", desc="""
    In Strata the lairs are rebuilt with &eIntegrated Cataclysm&r: they use blocks from other
    mods, including working Create parts, and some Cataclysm gear is built with Create machines
    (for example the Harbinger's weapons on a &eMechanical Crafter&r).

    If a recipe looks odd, press &eR&r on it: this pack's version is the one shown.""")

q("presentation", "A Proper Entrance", deps="intro", icon="minecraft:painting", desc="""
    Two client-side extras: &eCinematic Cataclysm&r plays an intro cutscene for some bosses,
    and &eGTBC's Cataclysmic Boss UI&r shows a boss screen before the fight starts.""")

q("delight", "Cataclysm Delight", deps="netherite_monstrosity", icon="lendersdelight:netherite_monstrosity_meat",
  desc="""
    &eL_Ender's Cataclysm Delight&r adds over 50 foods made from Cataclysm creatures:
    crab legs, lionfish rolls, even a Netherite Monstrosity sandwich. Cook them with
    Farmer's Delight tools. Press &eU&r on a Cataclysm mob drop to see what it makes.""",
  rewards=[give("farmersdelight:cooking_pot")])

q("spellbooks", "Cataclysm: Spellbooks", deps="intro", icon="cataclysm_spellbooks:burning_manuscript", desc="""
    For spellcasters: &eCataclysm: Spellbooks&r links these bosses to &dIron's Spells&r.
    Bosses drop &emanuscripts&r that teach their spells (Ignis's Burning Manuscript,
    the Monstrosity's Encoded Print...), and there are new spellbooks and mage armor sets.

    See the &dIron's Spells&r chapter for how spellcasting works.""")

q("where_next", "Where Next?", deps=["netherite_monstrosity", "ignis"], icon="minecraft:compass",
  shape="diamond", desc="""
    With bosses down, go claim what they unlocked:

    &bMekanism&r and &bAE2&r: their late tiers open after the Netherite Monstrosity or Ignis.
    Cross-dimension wireless opens after the Ender Guardian.
    &cBoss Hunter&r: many more bosses from other mods.
    &cIce and Fire&r: dragons.""")
