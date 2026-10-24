// Pokémon world: wild Pokémon spawn only in pokeworld:pokeworld.
// Cobblemon checks config.worldSpawningBlocklist for every natural spawn. This fills it with
// every loaded dimension except the Pokémon world, so dimensions added later are covered too.
// It only affects the natural spawner: sent-out, NPC-trainer and battle Pokémon are untouched.
// (Cobblemon 1.8.2's spawn-rule "location" component can't be used: it fails before evaluating
// its expression, so a location rule blocks spawns everywhere.)
const Cobblemon = Java.loadClass('com.cobblemon.mod.common.Cobblemon')
const HashSet = Java.loadClass('java.util.HashSet')
const ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
// KubeJS exposes level.dimension as a property (a ResourceLocation); fall back to a ResourceKey.
const dimensionId = level => { const d = level.dimension; return String(d && d.location ? d.location() : d) }
let spawnBlocklistApplied = false

ServerEvents.tick(event => {
  if (spawnBlocklistApplied) return
  spawnBlocklistApplied = true
  const blocked = new HashSet()
  event.server.getAllLevels().forEach(level => {
    const id = dimensionId(level)
    if (id !== 'pokeworld:pokeworld') blocked.add(ResourceLocation.parse(id))
  })
  Cobblemon.INSTANCE.getConfig().setWorldSpawningBlocklist(blocked)
  console.info(`[pokeworld] Cobblemon wild spawns blocked in ${blocked.size()} dimensions`)
})
