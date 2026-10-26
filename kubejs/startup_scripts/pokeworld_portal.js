// Dimension portals (BBL Portals). Each entry: a frame block, an igniter item and a destination.
// Portals link like nether portals but 1:1 (same X/Z), and the portal on the other side leads
// back to the Overworld. There is no pre-built portal: players build the frame and craft the
// igniter. To add a dimension, add an entry here plus its recipes (server_scripts/*_recipes.js),
// textures (assets/<ns>/textures) and loot.
//
// Pokémon world:
//   Alph Stone (block id pokeworld:poke_portal_frame, kept so built frames survive): ancient carved
//   sandstone after Johto's Ruins of Alph; 8 from chiseled sandstone around a diamond. Its frame
//   blocks connect into one carved border (Fusion, already in the pack for Rechiseled) and pick a
//   random variant (plain, glyphs, mossy): assets/pokeworld/blockstates|models|textures.
//   Johto Bell: Bell + gold + Bell Fragment; reusable (BBL Portals never uses up the igniter).
//   Bell Fragment: rare chest loot in Overworld structures (data/neoforge/loot_modifiers).
// The Hollow (horror dimension, docs/hollow-design.md):
//   Frame: resin bricks (Vanilla Backport); resin only comes from Overworld Pale Gardens.
//   Pale Lantern: Creaking Heart (Silk Touch) + soul lantern + resin clumps; reusable.
const PORTALS = [
  {
    frame: 'pokeworld:poke_portal_frame',
    frameName: 'Alph Stone',
    frameSound: 'stone',
    frameColor: 'sand',
    igniter: 'pokeworld:johto_bell',
    igniterName: 'Johto Bell',
    destination: 'pokeworld:pokeworld',
    tint: 0xE3350D,
    // Its texture twinkles (animated); no enchantment shimmer on top of that.
    noGlint: true,
  },
  {
    frame: 'minecraft:resin_bricks',
    existingFrame: true,
    igniter: 'strata:pale_lantern',
    igniterName: 'Pale Lantern',
    destination: 'strata:hollow',
    tint: 0x3B2A33,
    // Its texture pulses (animated); no enchantment shimmer on top of that.
    noGlint: true,
  },
]

StartupEvents.registry('block', event => {
  PORTALS.filter(p => !p.existingFrame).forEach(p => {
    event.create(p.frame)
      .displayName(p.frameName)
      .soundType(p.frameSound)
      .mapColor(p.frameColor)
      .hardness(5)
      .resistance(6)
      .requiresTool(true)
      .tagBlock('minecraft:mineable/pickaxe')
      .tagBlock('minecraft:needs_iron_tool')
  })
})

StartupEvents.registry('item', event => {
  PORTALS.forEach(p => {
    event.create(p.igniter).displayName(p.igniterName).maxStackSize(1).rarity('rare').glow(!p.noGlint)
  })
  event.create('pokeworld:bell_fragment').displayName('Bell Fragment').rarity('uncommon')
  // Dropped by the Hollow's horror mobs and found in its chests (server_scripts/hollow_rules.js).
  // Its texture pulses (animated), so no enchantment shimmer.
  event.create('strata:hollow_ember').displayName('Hollow Ember').rarity('rare')
})

PortalEvents.register(event => {
  PORTALS.forEach(p => {
    event.create()
      .frameBlock(p.frame)
      .lightWithItem(p.igniter)
      .setDestination(p.destination)
      .returnDim('minecraft:overworld')
      .tint(p.tint)
  })
})
