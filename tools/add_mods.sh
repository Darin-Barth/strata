#!/usr/bin/env bash
# Phase 1: add every Keep mod that has a confirmed 1.21.1 NeoForge build.
# Modrinth first, then CurseForge-only projects (by full URL: bare CF slugs can hit the wrong project).
# Usage (from repo root): bash tools/add_mods.sh
set -u
export PATH="$HOME/go/bin:$PATH"
LOG=tools/add-log.txt
: > "$LOG"

MR=(
  kubejs almostunified curios polymorph
  create create-aeronautics sable create-propulsion-simulated create-aeroworks create-tweaked-controllers
  create-big-cannons createaddition create-new-age create-diesel-generators create-enchantment-industry
  slice-and-dice create-central-kitchen create-steam-n-rails-1.21.1 create-additional-logistics numismatics create-trading-floor
  copycats create-deco create-connected create-bits-n-bobs create-transmission
  mekanism mekanism-generators mekanism-tools applied-mekanistics ae2 appflux
  immersiveengineering industrial-foregoing pneumaticcraft-repressurized powah extreme-reactors
  integrated-dynamics excessive-utilities mystical-agriculture productivebees
  ars-nouveau irons-spells-n-spellbooks ars-n-spells occultism ars-ocultas ars-energistique ars-creo
  vampirism vampirism-integrations vampirism-irons-spells-compatibility werewolves vampires-delight
  vampires-need-umbrellas
  tectonic regions-unexplored streams-reflowing incendium nullscape
  yungs-api yungs-better-strongholds yungs-better-mineshafts yungs-better-nether-fortresses
  yungs-better-dungeons yungs-better-desert-temples yungs-better-jungle-temples yungs-better-ocean-monuments
  yungs-better-witch-huts yungs-better-end-island yungs-bridges yungs-extras yungs-cave-biomes
  towns-and-towers when-dungeons-arise dungeons-and-taverns idas explorify lootr
  l_enders-cataclysm mowzies-mobs deeperdarker
  apotheosis explorers-compass natures-compass waystones better-combat apothic-combat combat-roll
  gravestone-mod artifacts relics-mod reliquified-artifacts royalvariations
  cobblemon integrated-cobblemon rctmod cobblestructures cobblemon-simple-pokecenters cobblemonextrastructures
  farmers-delight serene-seasons tide bountiful aquaculture inventory-pets naturalist friends-and-foes-forge
  critters-and-companions creeper-overhaul enderman-overhaul illager-invasion
  handcrafted chipped macaws-bridges macaws-doors macaws-fences-and-walls macaws-lights-and-lamps
  macaws-paintings macaws-roofs macaws-trapdoors macaws-windows macaws-furniture macaws-paths-and-pavings
  supplementaries every-compat another-furniture
  sophisticated-backpacks sophisticated-storage functional-storage toms-storage comforts
  emi jade appleskin inventory-profiles-next fallingtree controlling just-enough-resources-jer carry-on
  mouse-tweaks xaeros-minimap xaeros-world-map simple-voice-chat simple-backups
  sodium iris complementary-reimagined distanthorizons fresh-animations entity-model-features
  entitytexturefeatures continuity fusion-connected-textures atmospherics sound-physics-remastered
  ambientsounds cameraoverhaul
  modernfix ferrite-core immediatelyfast entityculling badoptimizations lithium noisium chunky clumps lmd spark
  # Round 1 decisions (docs/open-questions.md)
  drive-by-wire-sable redomesticate jei spice-of-life-onion neovitae aether alexs-mobs-continued
  bosses-of-mass-destruction-forge plushie enders-delight twilight-delight arsdelight
  l_enders-cataclysm-delight the-aethers-delight sdlink
  # Undeclared deps found in the first server boot
  kambrik terrablender
  custom-window-title caelus vanillabackport integrated-villages
  # Wave 3 (Oct 24)
  effortless-building building-wands rechiseled rechiseled-create framedblocks mech-trowel
  guard-villagers easy-villagers trade-cycling smarter-farmers-farmers-replant deep-aether
  create-stuff-additions create-stuff-n-additions-x-sable-aeronautics-compat aquamirae
  # Wave 4 (Oct 24): gap-analysis picks (docs/mod-gap-analysis.md)
  embers-floating-islands sky-whale-ship moogs-voyager-structures kobolds hopo-better-ruined-portals
  when-dungeons-arise-seven-seas integrated-seven-seas upgrade-aquatic tidal-towns oceans-delight
  illager-warship illager-war-trireme mns-moogs-nether-structures nether-depths-upgrade my-nethers-delight
  eternal-nether mes-moogs-end-structures endrem aether-villages aether-treasure-reforging horseman
  horse-expert xaeros-minimap-world-map-waystones-compatibility-forge simply-swords extended-crafting
  legendary-monsters create-ore-excavation ars-additions theurgy brewin-and-chewin lets-do-vinery
  amendments enchantment-descriptions torchmaster crafting-tweaks jade-addons-forge crash-assistant
  ping-wheel ping-to-map-xaeros neruina packet-fixer structure-layout-optimizer async-locator-refined
  fastsuite dynamic-fps moreculling sodium-extra
)

CF=(
  ftb-quests-forge ftb-chunks-forge ftb-teams-forge ftb-ultimine-forge laserio flux-networks
  irons-nouveau apotheosis-x-irons-spellbooks-compat vampiric-ageing-a-vampirism-addon bloodlines
  integrated-cataclysm forsaken-relics the-twilight-forest
  mob-grinding-utils creatures-and-beasts-continued ex-pattern-provider alltheleaks macaws-stairs
  falling-leaves-forge cosmetic-armor-reworked
  # Friend's list (Oct 24)
  bossesrise qliphoth-awakening cinematic-cataclysm gtbcs-cataclysmic-boss-ui cataclysm-spellbooks
  apprentices-codex starbunclemania ars-trinkets playerrevive locked-in-slots mighty-mail
  what-are-they-up-to meccha-crafteleon hyperbox
  # Wave 3 (Oct 24). Chisels & Bits was tried and cut: it fails to load on 1.21.1
  building-gadgets more-red choicetheorems-overhauled-village iceandfire-ce
  # Wave 4. Both pull in Ars Nouveau's CurseForge copy: restore mods/ars-nouveau.pw.toml afterwards
  ars-elemental croptopia
)

for s in "${MR[@]}"; do
  out=$(packwiz mr add "$s" -y 2>&1 | grep -vE "Refreshing|^\s*$")
  echo "MR $s :: $(echo "$out" | tr '\n' ' ')" >> "$LOG"
done
for s in "${CF[@]}"; do
  out=$(packwiz cf add "https://www.curseforge.com/minecraft/mc-mods/$s" -y 2>&1 | grep -vE "Refreshing|^\s*$")
  echo "CF $s :: $(echo "$out" | tr '\n' ' ')" >> "$LOG"
done
# LambDynamicLights ships one multi-loader jar whose metadata lists Fabric API as required;
# Fabric API is not needed on NeoForge, so decline dependencies for it.
out=$(echo n | packwiz mr add lambdynamiclights 2>&1 | grep -vE "Refreshing|^\s*$")
echo "MR lambdynamiclights :: $(echo "$out" | tr '\n' ' ')" >> "$LOG"
# Gadgets & Gizmos: pinned to the last stable 1.x build (2.0 is in rapid pre-release).
out=$(packwiz mr add "https://modrinth.com/mod/create-aeronautics-gadgets-and-gizmos/version/MgD655V5" -y 2>&1 | grep -vE "Refreshing|^\s*$")
echo "MR create-aeronautics-gadgets-and-gizmos 1.2.10 :: $(echo "$out" | tr '\n' ' ')" >> "$LOG"
packwiz pin create-aeronautics-gadgets-and-gizmos >> "$LOG" 2>&1
packwiz refresh >> "$LOG" 2>&1
echo DONE >> "$LOG"
