"""Write phase-1 lookup results into docs/strata-mod-tracker.xlsx.

Sets column G (1.21.1 NeoForge) and fills a new column J ("Phase 1 lookup") with where the build was found.
Usage: python -I tools/update_tracker.py
"""
from copy import copy
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font

XLSX = Path(__file__).resolve().parent.parent / "docs" / "strata-mod-tracker.xlsx"
C, V, N = "Confirmed", "Verify", "Not available"

# Row name -> (status, lookup note). Rows not listed keep their current values (Cut rows, NeoForge loader).
R = {
    "KubeJS": (C, "MR kubejs 2101.7.2"),
    "FTB Quests": (C, "CF ftb-quests-forge 2101.1.37 (Modrinth hit was only a zh_cn translation)"),
    "Almost Unified": (C, "MR almostunified 1.4.2"),
    "Curios API": (C, "MR curios 9.5.1"),
    "Accessories + Accessories Compatibility Layer": (C, "MR accessories 1.1.0-beta.54 + accessories-compat-layer 0.1.13 (not added: Maybe)"),
    "Polymorph": (C, "MR polymorph 1.2.0 (beta). Not Polymorph+ (different mod)"),
    "Create": (C, "MR create 6.0.10"),
    "Create Aeronautics": (C, "MR create-aeronautics 1.3.2. Known: visual issues with Iris shaders"),
    "Sable": (C, "MR sable 2.0.6"),
    "Create Thrusters": (V, "AMBIGUOUS, not added: no mod with this exact name. Candidates: Create Aeronautics: Gadgets & Gizmos (ex Thrusters&Things), Create: Simulated Thrusters, Create: Linked Thrusters"),
    "Create Propulsion: Simulated": (C, "MR create-propulsion-simulated 1.1.5"),
    "Create Aeroworks": (C, "MR create-aeroworks 1.5.0"),
    "Drive By Wire": (N, "Original is Forge-only (no 1.21.1). Fork 'Drive-By-Wire with Sable' (MR drive-by-wire-sable 0.3.0) has a build. Not added: pick needed"),
    "Create Tweaked Controllers": (C, "MR create-tweaked-controllers 1.2.7"),
    "Create Offroad": (C, "Bundled inside Create Aeronautics (Simulated/Aeronautics/Offroad modules). Nothing separate to add"),
    "Create Big Cannons": (C, "MR create-big-cannons 5.11.7"),
    "Create Crafts & Additions": (C, "MR createaddition 1.7.2 (beta)"),
    "Create: New Age": (C, "MR create-new-age 1.2.0"),
    "Create: Better Motors": (C, "MR create-better-motors 4.0.0 (not added: Maybe)"),
    "Create Diesel Generators": (C, "MR create-diesel-generators 1.3.15"),
    "Create Enchantment Industry": (C, "MR create-enchantment-industry 2.5.4b"),
    "Create Slice & Dice": (C, "MR slice-and-dice 4.3.4"),
    "Create Central Kitchen": (C, "MR create-central-kitchen 2.6.2b"),
    "Create: Steam 'n' Rails": (C, "Official: 1.20.1 only. Using unofficial port 'Steam 'n' Rails Neoforge' (MR create-steam-n-rails-1.21.1 0.3.0-beta.2). Known: snow-track crash (port issue #361)"),
    "Create Additional Logistics": (C, "MR create-additional-logistics 1.4.5"),
    "Create Numismatics": (C, "MR numismatics 1.1.0"),
    "Create Trading Floor": (C, "MR create-trading-floor 3.0.16"),
    "Create Copycats+": (C, "MR copycats 3.0.9"),
    "Create Deco": (C, "MR create-deco 2.1.3"),
    "Create Connected": (C, "MR create-connected 1.3.3"),
    "Create: Bits 'n' Bobs": (C, "MR create-bits-n-bobs 2.3.5"),
    "Create: Transmission": (C, "MR create-transmission 1.2.2"),
    "Mekanism": (C, "MR mekanism 10.7.19"),
    "Mekanism Generators": (C, "MR mekanism-generators 10.7.19"),
    "Mekanism Tools": (C, "MR mekanism-tools 10.7.19"),
    "Applied Mekanistics": (C, "MR applied-mekanistics 1.6.3"),
    "Applied Energistics 2": (C, "MR ae2 19.2.18"),
    "ExtendedAE": (C, "CF ex-pattern-provider 2.2.41 (not ExtendedAE-Plus, a separate add-on)"),
    "Applied Flux": (C, "MR appflux 2.1.5"),
    "Immersive Engineering": (C, "MR immersiveengineering 12.4.2"),
    "Industrial Foregoing": (C, "MR industrial-foregoing 3.6.39 (beta)"),
    "PneumaticCraft: Repressurized": (C, "MR pneumaticcraft-repressurized 8.2.23"),
    "Powah": (C, "MR powah 6.2.10"),
    "Extreme Reactors": (C, "MR extreme-reactors 2.4.9"),
    "Integrated Dynamics": (C, "MR integrated-dynamics 1.38.1"),
    "Laser IO": (C, "CF laserio 1.9.11"),
    "Flux Networks": (C, "CF flux-networks 8.0.0"),
    "Excessive Utilities": (C, "MR excessive-utilities 1.11.0"),
    "Modern Industrialization or Oritech (pick one)": (C, "Both have builds: MR modern-industrialization 2.5.11, MR oritech 1.2.13 (not added: Maybe)"),
    "Mystical Agriculture": (C, "MR mystical-agriculture 8.0.29"),
    "Productive Bees": (C, "MR productivebees 13.13.0"),
    "Mob Grinding Utils": (C, "CF mob-grinding-utils 1.1.10"),
    "Ars Nouveau": (C, "MR ars-nouveau 5.13.3"),
    "Iron's Spells 'n Spellbooks": (C, "MR irons-spells-n-spellbooks 3.16.3"),
    "Ars 'n Spells": (C, "MR ars-n-spells 3.3.5"),
    "Iron & Nouveau": (C, "CF irons-nouveau 0.17.24"),
    "Occultism": (C, "MR occultism 1.224.5"),
    "Ars Ocultas": (C, "MR ars-ocultas 2.6.1"),
    "Botania": (N, "No 1.21.1 build on Modrinth or CurseForge (latest Botania is 1.20.1)"),
    "Ars Botania": (C, "Build exists (MR ars-botania 1.2.0 beta) but it REQUIRES Botania, which has no build. Not added"),
    "Ars Energistique": (C, "MR ars-energistique 2.1.1 (beta)"),
    "Ars Creo": (C, "MR ars-creo 5.4.0"),
    "Apotheosis x Iron's Spellbooks Compat": (C, "CF apotheosis-x-irons-spellbooks-compat 2.2.8"),
    "Neo Vitae": (C, "MR neovitae 1.1.48 (not added: Maybe)"),
    "Vampirism": (C, "MR vampirism 1.10.13"),
    "Vampirism Integrations": (C, "MR vampirism-integrations 1.10.2"),
    "Vampirism Iron's Spells Compatibility": (C, "MR vampirism-irons-spells-compatibility 0.0.10"),
    "Werewolves": (C, "MR werewolves 2.0.3.3"),
    "Vampire's Delight": (C, "MR vampires-delight 0.1.12b (beta)"),
    "Vampires Need Umbrellas": (C, "MR vampires-need-umbrellas 1.0.3"),
    "Vampiric Ageing": (C, "CF vampiric-ageing-a-vampirism-addon 1.4.21"),
    "Bloodlines": (C, "CF bloodlines 3.0.9 (files tagged 1.21 + 1.21.1)"),
    "Tectonic": (C, "MR tectonic 3.0.28"),
    "Regions Unexplored (6.0)": (C, "MR regions-unexplored 0.6.3"),
    "Streams Reflowing": (C, "MR streams-reflowing 2.15.2"),
    "Incendium": (C, "MR incendium 5.4.4 (project now titled 'Incendium Legacy')"),
    "Nullscape": (C, "MR nullscape 1.2.14"),
    "YUNG's suite (Better Strongholds, Mineshafts, Fortresses, etc.)": (C, "MR: API, Better Strongholds/Mineshafts/Nether Fortresses/Dungeons/Desert Temples/Jungle Temples/Ocean Monuments/Witch Huts/End Island, Bridges, Extras, Cave Biomes"),
    "Towns and Towers": (C, "MR towns-and-towers 1.13.11"),
    "When Dungeons Arise": (C, "MR when-dungeons-arise 2.1.68"),
    "Dungeons and Taverns": (C, "MR dungeons-and-taverns 4.4.4"),
    "Integrated Dungeons and Structures": (C, "MR idas 1.13.7"),
    "Explorify": (C, "MR explorify 1.6.5"),
    "Lootr": (C, "MR lootr 1.11.38"),
    "L_Ender's Cataclysm": (C, "MR l_enders-cataclysm 3.33"),
    "Integrated Cataclysm": (C, "CF integrated-cataclysm 1.0.6"),
    "Mowzie's Mobs": (C, "MR mowzies-mobs 1.8.2"),
    "Bosses of Mass Destruction": (N, "Original: no 1.21.1 NeoForge. Port 'Bosses of Mass Destruction Forge' (MR bosses-of-mass-destruction-forge 1.3.3) has one (not added: Maybe)"),
    "Twilight Forest": (C, "CF the-twilight-forest 4.8.3345 (Modrinth only has an unofficial Fabric port)"),
    "Deeper and Darker": (C, "MR deeperdarker 1.4.1"),
    "The Aether": (C, "MR aether 1.5.10 (not added: Maybe)"),
    "Undergarden": (C, "MR the-undergarden 0.9.6 beta (not added: Maybe)"),
    "Blue Skies": (N, "No 1.21.1 build on Modrinth or CurseForge"),
    "Apotheosis": (C, "MR apotheosis 8.9.0"),
    "Explorer's Compass": (C, "MR explorers-compass 3.4.0"),
    "Nature's Compass": (C, "MR natures-compass 3.4.0"),
    "Waystones": (C, "MR waystones 21.1.46"),
    "Majrusz's Progressive Difficulty Continued": (C, "CF majruszs-progressive-difficulty-continued 1.1.6 (the original has no 1.21.1 build). EXCLUDED from the CF API: packwiz can't auto-download it (needs a manual download or another distribution route)"),
    "Dimension Gated Difficulty": (N, "No 1.21.1 NeoForge build on CurseForge; not on Modrinth"),
    "Better Combat": (C, "MR better-combat 2.4.0"),
    "Apothic Combat": (C, "MR apothic-combat 1.2.1"),
    "Combat Roll": (C, "MR combat-roll 2.0.6"),
    "Gravestone / corpse mod": (C, "PICKED: GraveStone Mod (MR gravestone-mod 1.0.40, henkelmax)"),
    "Artifacts": (C, "MR artifacts 13.2.5"),
    "Relics": (C, "MR relics-mod 0.12.10 (beta)"),
    "Reliquified Artifacts": (C, "MR reliquified-artifacts 1.0.9 (beta)"),
    "Forsaken Relics": (C, "CF forsaken-relics 1.0.1"),
    "Royal Variations": (C, "MR royalvariations 2.0.4"),
    "Cobblemon": (C, "MR cobblemon 1.8.2"),
    "No Mons In My World": (N, "Fabric-only, no NeoForge port or equivalent (rechecked Oct 23). Rebuild when we make the Pokemon world: KubeJS spawn-event hook > small NeoForge mod > biome-tag datapack (see design doc, Pokemon world step 2)"),
    "Integrated Cobblemon": (C, "MR integrated-cobblemon 1.2.1"),
    "Radical Cobblemon Trainers": (C, "MR rctmod 0.19.2-beta"),
    "CobbleStructures": (C, "MR cobblestructures 1.1.0 (beta)"),
    "Cobblemon: Simple Pokecenters": (C, "MR cobblemon-simple-pokecenters 1.2.1"),
    "Cobblemon Extra Structures": (C, "MR cobblemonextrastructures 1.3.0"),
    "Cobblemon Kanto (map)": (C, "Not a mod-site project; not checked in phase 1 (Maybe)"),
    "Pokemon world portal (mod or KubeJS)": (V, "Open question: nothing to look up yet"),
    "Farmer's Delight + add-ons": (C, "MR farmers-delight 1.3.4 added. Add-ons not named yet"),
    "Serene Seasons": (C, "MR serene-seasons 10.1.0.9 (beta)"),
    "Spice of Life or Diet (pick one)": (C, "Spice of Life: Onion has a build (MR spice-of-life-onion 1.5.7). Diet has NO 1.21.1 build"),
    "Tide": (C, "MR tide 2.1.1 (project titled 'Tide 2')"),
    "Bountiful": (C, "MR bountiful 8.0.0-beta.2"),
    "Aquaculture 2": (C, "MR aquaculture 2.7.21"),
    "Inventory Pets": (C, "MR inventory-pets 2.2.8"),
    "Domestication Innovation": (N, "No 1.21.1 build. Fork 'Redomesticate' (MR redomesticate 1.11.2) has one. Not added: pick needed"),
    "Naturalist": (C, "MR naturalist 2.0.7"),
    "Friends & Foes": (C, "MR friends-and-foes-forge 5.0.3 (the Forge/NeoForge project, not the Fabric one)"),
    "Creatures and Beasts: Continued": (C, "CF creatures-and-beasts-continued 1.7.17"),
    "Critters and Companions": (C, "MR critters-and-companions 2.7.0"),
    "Alex's Mobs": (N, "Original: no 1.21.1. 'Alex's Mobs Continued' (MR alexs-mobs-continued 2.2.4) has one (not added: Maybe)"),
    "Creeper Overhaul": (C, "MR creeper-overhaul 4.0.6"),
    "Enderman Overhaul": (C, "MR enderman-overhaul 2.0.3"),
    "Illager Invasion": (C, "MR illager-invasion 21.1.6"),
    "Handcrafted": (C, "MR handcrafted 4.0.3"),
    "Chipped": (C, "MR chipped 4.0.2"),
    "Macaw's suite": (C, "MR: Bridges, Doors, Fences, Lights, Paintings, Roofs, Trapdoors, Windows, Furniture, Paths. CF: Macaw's Stairs"),
    "Supplementaries": (C, "MR supplementaries 4.0.2"),
    "Every Compat": (C, "MR every-compat 2.11.55 (Wood Good)"),
    "Another Furniture": (C, "MR another-furniture 4.0.3"),
    "Plushie mod": (C, "Plushie Mod (MR plushie 1.5.1) has a build (not added: Maybe)"),
    "Cosmetic Armor Reworked": (C, "CF cosmetic-armor-reworked (original). Modrinth only has a fork"),
    "Sophisticated Backpacks": (C, "MR sophisticated-backpacks 3.26.14"),
    "Sophisticated Storage": (C, "MR sophisticated-storage 1.6.9"),
    "Functional Storage": (C, "MR functional-storage 1.5.7 (beta)"),
    "Tom's Simple Storage": (C, "MR toms-storage 2.4.2"),
    "Comforts": (C, "MR comforts 9.0.5"),
    "EMI": (C, "MR emi 1.1.24"),
    "Jade": (C, "MR jade 15.10.6"),
    "AppleSkin": (C, "MR appleskin 3.0.9"),
    "Inventory Profiles Next": (C, "MR inventory-profiles-next 2.2.5"),
    "FTB Ultimine": (C, "CF ftb-ultimine-forge 2101.1.15 (not the 'Ultimine Rewind' fork)"),
    "FallingTree": (C, "MR fallingtree 1.21.1.11"),
    "Controlling": (C, "MR controlling 19.0.5"),
    "Just Enough Resources": (C, "MR just-enough-resources-jer 1.6.0.54"),
    "Carry On": (C, "MR carry-on 2.2.6"),
    "Mouse Tweaks": (C, "MR mouse-tweaks 2.26.1"),
    "Xaero's Minimap + World Map": (C, "MR xaeros-minimap 26.6.0 + xaeros-world-map 1.47.0"),
    "FTB Chunks + FTB Teams": (C, "CF ftb-chunks-forge 2101.1.22 + ftb-teams-forge 2101.1.11"),
    "Simple Voice Chat": (C, "MR simple-voice-chat 2.6.25"),
    "Discord bridge mod": (V, "Not chosen. Discord Integration (dcintegration) has no 1.21.1 NeoForge build; pick needed"),
    "Simple Backups (or Docker backups)": (C, "MR simple-backups 4.0.30 added"),
    "Iris": (C, "MR iris 1.8.14-beta.1"),
    "Complementary Reimagined (shader)": (C, "MR complementary-reimagined r5.9.3 (shaderpack)"),
    "Distant Horizons": (C, "MR distanthorizons 3.3.3"),
    "Fresh Animations": (C, "MR fresh-animations 1.11.1 (resource pack)"),
    "Entity Model Features": (C, "MR entity-model-features 3.3.12"),
    "Entity Texture Features": (C, "MR entitytexturefeatures 7.2.6"),
    "Continuity": (C, "MR continuity 3.0.0"),
    "Fusion": (C, "MR fusion-connected-textures 1.3.16"),
    "Atmospherics": (C, "MR atmospherics 2.6.5.2"),
    "Sound Physics Remastered": (C, "MR sound-physics-remastered 1.5.2"),
    "AmbientSounds": (C, "MR ambientsounds 6.3.11"),
    "Falling Leaves": (C, "CF falling-leaves-forge 2.6.0 (CF also has an unrelated 'Falling Leaves')"),
    "Camera Overhaul": (C, "MR cameraoverhaul 2.1.2"),
    "Dynamic lighting mod": (C, "PICKED: LambDynamicLights (MR lambdynamiclights 4.8.11)"),
    "Sodium": (C, "MR sodium 0.8.13"),
    "ModernFix": (C, "MR modernfix 5.27.26"),
    "FerriteCore": (C, "MR ferrite-core 7.0.3"),
    "ImmediatelyFast": (C, "MR immediatelyfast 1.6.15"),
    "Entity Culling": (C, "MR entityculling 1.11.3"),
    "BadOptimizations": (C, "MR badoptimizations 2.4.1"),
    "AllTheLeaks": (C, "CF alltheleaks 1.1.13"),
    "Lithium": (C, "MR lithium 0.15.4"),
    "Noisium": (C, "MR noisium 2.3.0 (original). Forks NoisiumForked / Noisiumed also exist"),
    "Chunky": (C, "MR chunky 1.4.23"),
    "Clumps": (C, "MR clumps 19.0.0.1"),
    "Let Me Despawn": (C, "MR lmd 1.26.10.2"),
    "Spark": (C, "MR spark 1.10.124"),
}

# --- Decisions after phase 1 (docs/open-questions.md answers, Oct 23, 2026) ---

# Rows renamed to the mod actually chosen. Old name -> new name (applied once, then R uses the new name).
RENAMES = {
    "Create Thrusters": "Create Aeronautics: Gadgets & Gizmos",
    "Drive By Wire": "Drive-By-Wire with Sable",
    "Domestication Innovation": "Redomesticate",
    "Alex's Mobs": "Alex's Mobs Continued",
    "Bosses of Mass Destruction": "Bosses of Mass Destruction (Forge port)",
    "Spice of Life or Diet (pick one)": "Spice of Life: Onion",
    "Plushie mod": "Plushie Mod",
    "Gravestone / corpse mod": "GraveStone Mod",
    "Dynamic lighting mod": "LambDynamicLights",
    "Discord bridge mod": "Simple Discord Link",
}
for old, new in RENAMES.items():
    if old in R:
        R[new] = R.pop(old)

R.update({
    "Create Aeronautics: Gadgets & Gizmos": (C, "Was 'Create Thrusters'. MR create-aeronautics-gadgets-and-gizmos 1.2.10, PINNED (2.0 is in rapid pre-release)"),
    "Drive-By-Wire with Sable": (C, "Was 'Drive By Wire' (original Forge-only). MR drive-by-wire-sable 0.3.0"),
    "Redomesticate": (C, "Was 'Domestication Innovation' (abandoned 2023). MR redomesticate 1.11.2"),
    "Alex's Mobs Continued": (C, "Original has no 1.21.1 build. MR alexs-mobs-continued 2.2.4"),
    "Bosses of Mass Destruction (Forge port)": (C, "Original is Fabric-first. MR bosses-of-mass-destruction-forge 1.3.3 (+ CERBON's API). Test 11"),
    "Spice of Life: Onion": (C, "Diet has no 1.21.1 build. MR spice-of-life-onion 1.5.7. Test with vampires (test 7)"),
    "Plushie Mod": (C, "MR plushie 1.5.1"),
    "Neo Vitae": (C, "MR neovitae 1.1.48"),
    "The Aether": (C, "MR aether 1.5.10 (+ owo-lib)"),
    "Undergarden": (C, "MR the-undergarden 0.9.6 beta. Out for now (beta); revisit later"),
    "Botania": (N, "No 1.21.1 build. Cut: Ars, Iron's, Occultism, Vampirism and Neo Vitae cover magic"),
    "Ars Botania": (C, "Requires Botania (no build). Cut with Botania"),
    "Blue Skies": (N, "No 1.21.1 build. Cut"),
    "Dimension Gated Difficulty": (N, "No 1.21.1 build. Cut: not needed, Majrusz's Continued has one"),
    "Continuity": (C, "Cut: on NeoForge it needs Sinytra Connector + Forgified Fabric API. Fusion covers connected textures"),
    "Simple Discord Link": (C, "Was 'Discord bridge mod'. MR sdlink 3.4.5 (server-only) + CraterLib 3.1.3"),
    "Xaero's Minimap + World Map": (C, "MR xaeros-minimap 26.6.0 + xaeros-world-map 1.47.0. FTB Chunks also has its own map/minimap: turn its minimap off client-side and check claim display (test 13)"),
    "Farmer's Delight + add-ons": (C, "MR farmers-delight 1.3.4. Add-ons: see the Delight rows"),
})

# Status column (F) changes. Rows not listed keep their status.
STATUS = {
    "Botania": "Cut", "Ars Botania": "Cut", "Blue Skies": "Cut", "Dimension Gated Difficulty": "Cut",
    "Continuity": "Cut", "Spice of Life: Onion": "Keep", "Neo Vitae": "Keep", "The Aether": "Keep",
    "Alex's Mobs Continued": "Keep", "Bosses of Mass Destruction (Forge port)": "Keep", "Plushie Mod": "Keep",
}

# New rows: (Mod, Category, Pillar, Needs, Side, Status, 1.21.1 NeoForge, Flags, Notes, Lookup)
NEW_ROWS = [
    ("Just Enough Items (JEI)", "QoL", "Core", None, "Both", "Keep", C, None,
     "Runs alongside EMI so JEI plugins (JER) work", "MR jei 19.69.0 (+ MezzConfig)"),
    ("Quark + Zeta", "Building", "Life", "Zeta", "Both", "Keep", C, "Config",
     "Required by Integrated Cataclysm. Overlapping modules disabled in config/quark-common.toml",
     "MR quark 4.1-487 + zeta 1.1-40"),
    ("Ender's Delight", "Food and farming", "Life", "Farmer's Delight", "Both", "Keep", C, None,
     "End foods", "MR enders-delight 1.3.1"),
    ("Twilight's Flavor & Delight", "Food and farming", "Life", "Farmer's Delight, Twilight Forest", "Both", "Keep", C, None,
     "Twilight Forest foods", "MR twilight-delight 3.2.8"),
    ("Ars Nouveau's Flavors & Delight", "Food and farming", "Life", "Farmer's Delight, Ars Nouveau", "Both", "Keep", C, None,
     "Ars Nouveau foods", "MR arsdelight 2.2.5"),
    ("L_Ender's Cataclysm Delight", "Food and farming", "Life", "Farmer's Delight, Cataclysm", "Both", "Keep", C, None,
     "Cataclysm boss-drop foods", "MR l_enders-cataclysm-delight 1.0.10b"),
    ("Aether's Delight", "Food and farming", "Life", "Farmer's Delight, The Aether", "Both", "Keep", C, None,
     "Aether foods. Beta, last updated Oct 2025", "MR the-aethers-delight 0.1.4.2 (beta)"),
]


def main():
    wb = openpyxl.load_workbook(XLSX)
    ws = wb["Mods"]
    ws.cell(1, 10, "Phase 1 lookup").font = Font(bold=True)
    ws.column_dimensions["J"].width = 70
    for row in range(2, ws.max_row + 1):
        name = ws.cell(row, 1).value
        if name in RENAMES:
            ws.cell(row, 1, RENAMES[name])
            name = RENAMES[name]
        if name in STATUS:
            ws.cell(row, 6, STATUS[name])
    existing = {ws.cell(r, 1).value for r in range(2, ws.max_row + 1)}
    for values in NEW_ROWS:
        if values[0] in existing:
            continue
        r = ws.max_row + 1
        for col, v in enumerate(values, start=1):
            c = ws.cell(r, col, v)
            c._style = copy(ws.cell(r - 1, col)._style)
    seen = set()
    for row in range(2, ws.max_row + 1):
        name = ws.cell(row, 1).value
        if name in R:
            status, note = R[name]
            ws.cell(row, 7, status)
            c = ws.cell(row, 10, note)
            c.alignment = Alignment(wrap_text=True, vertical="top")
            seen.add(name)
    missing = [n for n in R if n not in seen]
    unlisted = [ws.cell(r, 1).value for r in range(2, ws.max_row + 1)
                if ws.cell(r, 6).value in ("Keep", "Maybe") and ws.cell(r, 1).value not in R
                and ws.cell(r, 1).value not in {n[0] for n in NEW_ROWS}]
    wb.save(XLSX)
    print("names not found in sheet:", missing)
    print("Keep/Maybe rows without a result:", unlisted)


if __name__ == "__main__":
    main()
