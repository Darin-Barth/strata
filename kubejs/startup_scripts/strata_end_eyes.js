// End portal eyes (docs/end-eyes.md): in-between items for the two crafted eyes.
// Recipes and textures: tools/build_end_eyes.py; compasses: server_scripts/strata_end_eyes.js.
StartupEvents.registry('item', event => {
  // Create sequenced assembly: Eye of Ender -> (2 loops) -> Uncured Rogue Eye -> soul-fire fan -> Rogue Eye
  event.create('strata:incomplete_rogue_eye').displayName('Incomplete Rogue Eye').maxStackSize(1)
    .tooltip(Text.gray('Half-built on a Create assembly line'))
  event.create('strata:uncured_rogue_eye').displayName('Uncured Rogue Eye').rarity('uncommon')
    .tooltip(Text.gray('Still soft. Blow it through soul fire with an Encased Fan to cure it'))
  // Ars Nouveau: Enchanting Apparatus -> Dormant Magical Eye -> Imbuement Chamber -> Magical Eye
  event.create('strata:dormant_magical_eye').displayName('Dormant Magical Eye').rarity('uncommon')
    .tooltip(Text.gray('Bound, but asleep. Wake it in an Imbuement Chamber'))
})
