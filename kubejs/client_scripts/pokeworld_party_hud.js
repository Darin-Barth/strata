// Pokémon world: the Cobblemon party HUD shows only in pokeworld:pokeworld.
// Each time the player changes dimension, set Cobblemon's "Hide Party" toggle: hidden
// outside the Pokémon world, shown inside it. The Hide Party key still works in between.
const HidePartyBinding = Java.loadClass('com.cobblemon.mod.common.client.keybind.keybinds.HidePartyBinding')
let lastDimension = null

ClientEvents.tick(event => {
  const level = Client.level
  if (!level) {
    lastDimension = null
    return
  }
  // KubeJS exposes level.dimension as a property (a ResourceLocation); fall back to a ResourceKey.
  const d = level.dimension
  const dimension = String(d && d.location ? d.location() : d)
  if (dimension === lastDimension) return
  lastDimension = dimension
  HidePartyBinding.INSTANCE.setShouldHide(dimension !== 'pokeworld:pokeworld')
})
