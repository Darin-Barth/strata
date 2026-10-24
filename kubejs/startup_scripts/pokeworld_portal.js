// Pokémon world portal (BBL Portals). Build a nether-portal-shaped frame of red concrete
// (any size from 4x5) and light it with flint and steel. It links like a nether portal,
// but 1:1: you arrive at the same X/Z in the Pokémon world, and a portal there leads back
// to the Overworld.
PortalEvents.register(event => {
  event.create()
    .frameBlock('minecraft:red_concrete')
    .setDestination('pokeworld:pokeworld')
    .returnDim('minecraft:overworld')
    .tint(0xE3350D)
})
