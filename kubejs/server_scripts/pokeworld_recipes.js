// Pokémon world portal recipes (see startup_scripts/pokeworld_portal.js). Overworld materials
// only: nothing that now generates only in the Pokémon world (apricorns, evolution stones).
ServerEvents.recipes(event => {
  // Alph Stone: ancient carved sandstone (the block id is still poke_portal_frame).
  event.shaped('8x pokeworld:poke_portal_frame', [
    'SSS',
    'SDS',
    'SSS',
  ], {
    S: 'minecraft:chiseled_sandstone',
    D: 'minecraft:diamond',
  }).id('pokeworld:poke_portal_frame')

  event.shaped('pokeworld:johto_bell', [
    ' F ',
    'GBG',
    ' G ',
  ], {
    F: 'pokeworld:bell_fragment',
    G: 'minecraft:gold_ingot',
    B: 'minecraft:bell',
  }).id('pokeworld:johto_bell')
})
