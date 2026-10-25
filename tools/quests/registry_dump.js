// Scratch-only: log registry contents for the quest ID checker.
const Registries = Java.loadClass('net.minecraft.core.registries.Registries')
ServerEvents.loaded(event => {
  const access = event.server.registryAccess()
  const kinds = {
    items: Registries.ITEM,
    entities: Registries.ENTITY_TYPE,
    structures: Registries.STRUCTURE,
    biomes: Registries.BIOME,
  }
  for (let name in kinds) {
    let keys = access.registryOrThrow(kinds[name]).keySet()
    let n = 0
    keys.forEach(k => { console.info('STRATAREG ' + name + ' ' + k); n++ })
    console.info('STRATAREG-COUNT ' + name + ' ' + n)
  }
  event.server.levelKeys().forEach(k => console.info('STRATAREG dimensions ' + k.location()))
  console.info('STRATAREG-DONE')
})
