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
//   random variant (carved Unown, one big or two small, cracked and/or mossy): assets/pokeworld/blockstates|models|textures.
//   Johto Bell: Bell + gold + Bell Fragment; reusable (BBL Portals never uses up the igniter).
//   Bell Fragment: rare chest loot in Overworld structures (data/neoforge/loot_modifiers).
// The Hollow (horror dimension, docs/hollow-design.md):
//   Frame: resin bricks (Vanilla Backport); resin only comes from Overworld Pale Gardens.
//   Pale Lantern: Creaking Heart (Silk Touch) + soul lantern + resin clumps; reusable.
// The Abyssal Plain (underwater dimension, docs/abyssal-plain-design.md):
//   Frame: dark prismarine. Tidecaller: a Conduit between two Deep Seas ballast tanks, prismarine
//   crystals down both sides; reusable. You arrive in a Lifepod (server_scripts/abyssal_rules.js).
const PORTALS = [
  {
    frame: 'pokeworld:poke_portal_frame',
    frameName: 'Alph Stone',
    frameSound: 'stone',
    frameColor: 'sand',
    igniter: 'pokeworld:johto_bell',
    igniterName: 'Johto Bell',
    destination: 'pokeworld:pokeworld',
    // Its own animated texture ("Unown Drift": murky gold, Unown glyphs drifting up and lighting
    // one at a time), painted over BBL Portals' "default" slot (assets/portals/textures/block).
    // The tint multiplies that texture and colours the portal's dust: warm white, pale gold dust.
    portalTexture: 'default',
    tint: 0xFFF0C8,
    // Its texture twinkles (animated); no enchantment shimmer on top of that.
    noGlint: true,
  },
  {
    frame: 'minecraft:resin_bricks',
    existingFrame: true,
    igniter: 'strata:pale_lantern',
    igniterName: 'Pale Lantern',
    destination: 'strata:hollow',
    // Its own texture ("Dead Signal": grey TV static that freezes now and then and once drops to
    // black), painted over the "nether" slot. Ash-grey tint: grey dust like ash.
    portalTexture: 'nether',
    tint: 0xC8C4CC,
    // Its texture pulses (animated); no enchantment shimmer on top of that.
    noGlint: true,
  },
  {
    frame: 'minecraft:dark_prismarine',
    existingFrame: true,
    igniter: 'strata:tidecaller',
    igniterName: 'Tidecaller',
    destination: 'strata:abyssal_plain',
    // Its own animated texture ("marine snow": near-black water, drifting flecks, a blinking light),
    // painted over BBL Portals' unused "molten" slot (assets/portals/textures/block). The tint
    // multiplies that texture and colours the portal's dust, so keep it near white: pale flecks.
    portalTexture: 'molten',
    tint: 0xD8F0FF,
    // Stepping in: water rushing over you. Arriving: something huge, far off.
    inPortalSound: 'minecraft:ambient.underwater.enter',
    arrivalSound: 'minecraft:ambient.underwater.loop.additions.ultra_rare',
    // Sounds and particles around all three portals: startup_scripts/portal_ambience.js.
    noGlint: true,
  },
]

StartupEvents.registry('block', event => {
  // The Abyssal Plain's Lifepod (arrival chamber): unbreakable, so its air pocket can't be flooded.
  event.create('strata:lifepod_hull').displayName('Lifepod Hull').soundType('metal').mapColor('color_light_gray')
    .hardness(-1).resistance(3600000).requiresTool(false)
  event.create('strata:lifepod_window').displayName('Lifepod Window').soundType('glass').mapColor('color_light_blue')
    .hardness(-1).resistance(3600000).notSolid().defaultTranslucent()
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
  // Abyssal Plain: rare drop from the deep and its ruins; a late-game gate material.
  event.create('strata:abyssal_pearl').displayName('Abyssal Pearl').rarity('epic')
  // Summons the Leviathan (Cataclysm) in the Trench: the Abyssal Plain's final boss (abyssal_rules.js).
  event.create('strata:leviathan_lure').displayName('Leviathan Lure').rarity('epic').maxStackSize(1)
})

PortalEvents.register(event => {
  PORTALS.forEach(p => {
    const portal = event.create()
      .frameBlock(p.frame)
      .lightWithItem(p.igniter)
      .setDestination(p.destination)
      .returnDim('minecraft:overworld')
      .tint(p.tint)
    if (p.portalTexture) portal.portalTexture(p.portalTexture)
    if (p.inPortalSound) portal.inPortalAmbienceSound(p.inPortalSound, 0.8, 0.9)
    if (p.arrivalSound) portal.afterTeleportationAmbienceSound(p.arrivalSound, 1.0, 0.8)
  })
})
