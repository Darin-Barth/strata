// Dimension portals (BBL Portals). Each entry: a custom frame block, a custom igniter item and
// a destination. Portals link like nether portals but 1:1 (same X/Z), and the portal on the
// other side leads back to the Overworld. There is no pre-built portal: players craft the frame
// and the igniter. To add a dimension (e.g. the horror world), add an entry here plus its
// recipes (server_scripts/pokeworld_recipes.js), textures (assets/pokeworld/textures) and loot.
//
// Pokémon world:
//   Poké Portal Frame: 8 from red dye, redstone, iron, a diamond, white dye (Overworld-only).
//   Johto Bell: Bell + gold + Bell Fragment; reusable (BBL Portals never uses up the igniter).
//   Bell Fragment: rare chest loot in Overworld structures (data/neoforge/loot_modifiers).
const PORTALS = [
  {
    frame: 'pokeworld:poke_portal_frame',
    frameName: 'Poké Portal Frame',
    igniter: 'pokeworld:johto_bell',
    igniterName: 'Johto Bell',
    destination: 'pokeworld:pokeworld',
    tint: 0xE3350D,
  },
]

StartupEvents.registry('block', event => {
  PORTALS.forEach(p => {
    event.create(p.frame)
      .displayName(p.frameName)
      .soundType('metal')
      .mapColor('color_red')
      .hardness(5)
      .resistance(6)
      .requiresTool(true)
      .tagBlock('minecraft:mineable/pickaxe')
      .tagBlock('minecraft:needs_iron_tool')
  })
})

StartupEvents.registry('item', event => {
  PORTALS.forEach(p => {
    event.create(p.igniter).displayName(p.igniterName).maxStackSize(1).rarity('rare').glow(true)
  })
  event.create('pokeworld:bell_fragment').displayName('Bell Fragment').rarity('uncommon')
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
