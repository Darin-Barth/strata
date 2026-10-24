// Pokémon world: keep Overworld villages free of Cobblemon buildings.
// Cobblemon puts Pokécenters, berry farms and habitats into the vanilla village house pools
// twice: its own copy of minecraft:village/*/houses.json, and code at ServerAboutToStart.
// This runs after it (lowest priority, still before any chunk generates) and strips every
// cobblemon: element from those five pools. Pokémon world villages (pokeworld:village_*)
// alias the houses pool to pokeworld:village/*/houses, Cobblemon's version, so they keep
// their Pokécenters. Other mods' village additions (Waystones, Farmer's Delight, ...) stay.
const Registries = Java.loadClass('net.minecraft.core.registries.Registries')
const ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
const EventPriority = Java.loadClass('net.neoforged.bus.api.EventPriority')
const ServerAboutToStartEvent = Java.loadClass('net.neoforged.neoforge.event.server.ServerAboutToStartEvent')

// Pass real Java objects: string arguments here go through KubeJS's registry scanner, which
// deadlocks with mods still constructing on other threads (seen with Create, Oct 24 2026).
NativeEvents.onEvent(EventPriority.LOWEST, ServerAboutToStartEvent, event => {
  const pools = event.server.registryAccess().registryOrThrow(Registries.TEMPLATE_POOL)
  const Collectors = Java.loadClass('java.util.stream.Collectors')
  let removed = 0
  // forEach, not for...of: Rhino rejects const declarations inside a loop body.
  ;['plains', 'desert', 'savanna', 'snowy', 'taiga'].forEach(type => {
    const pool = pools.get(ResourceLocation.parse(`minecraft:village/${type}/houses`))
    if (!pool) return
    // getElements / getElementCounts come from Cobblemon's StructurePoolAccessor mixin.
    const elements = pool.getElements()
    const before = elements.size()
    elements.removeIf(e => String(e).includes('cobblemon:'))
    removed += before - elements.size()
    pool.setElementCounts(pool.getElementCounts().stream()
      .filter(p => !String(p.getFirst()).includes('cobblemon:'))
      .collect(Collectors.toList()))
  })
  console.info(`[pokeworld] removed ${removed} Cobblemon pieces from Overworld village pools`)
})
