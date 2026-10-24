// Pokémon world portal recipes (see startup_scripts/pokeworld_portal.js). Overworld materials
// only: nothing that now generates only in the Pokémon world (apricorns, evolution stones).
ServerEvents.recipes(event => {
  event.shaped('8x pokeworld:poke_portal_frame', [
    'RSR',
    'IDI',
    'WWW',
  ], {
    R: 'minecraft:red_dye',
    S: 'minecraft:redstone',
    I: 'minecraft:iron_ingot',
    D: 'minecraft:diamond',
    W: 'minecraft:white_dye',
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
