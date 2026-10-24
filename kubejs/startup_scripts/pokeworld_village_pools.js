// Pokémon world: keep Overworld villages free of Cobblemon buildings and NPCs.
// Cobblemon puts Pokécenters, berry farms and habitats into the vanilla village house pools
// (its own copy of minecraft:village/*/houses.json, plus code at ServerAboutToStart). This runs
// after it (lowest priority, still before any chunk generates) and strips every cobblemon:
// element from those pools. Pokémon world villages (pokeworld:village_*) alias the houses pool
// to pokeworld:village/*/houses, which keeps the Pokécenters. The villager pools are a guard
// for CobbleDollars: 2.0.0-beta-6.1 has Cobble Merchant village code that never runs and no
// merchant template, so nothing is removed there today.
// Other mods' village additions (Waystones, Bountiful, Farmer's Delight, ...) stay.
const Registries = Java.loadClass('net.minecraft.core.registries.Registries')
const ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
const EventPriority = Java.loadClass('net.neoforged.bus.api.EventPriority')
const ServerAboutToStartEvent = Java.loadClass('net.neoforged.neoforge.event.server.ServerAboutToStartEvent')

// Pass real Java objects: string arguments here go through KubeJS's registry scanner, which
// deadlocks with mods still constructing on other threads (seen with Create, Oct 24 2026).
NativeEvents.onEvent(EventPriority.LOWEST, ServerAboutToStartEvent, event => {
  const pools = event.server.registryAccess().registryOrThrow(Registries.TEMPLATE_POOL)
  const Collectors = Java.loadClass('java.util.stream.Collectors')
  const isPokemonPiece = e => /cobblemon:|cobbledollars:/.test(String(e))
  let removed = 0
  // forEach, not for...of: Rhino rejects const declarations inside a loop body.
  ;['plains', 'desert', 'savanna', 'snowy', 'taiga'].forEach(type => {
    ;['houses', 'villagers'].forEach(kind => {
      const pool = pools.get(ResourceLocation.parse(`minecraft:village/${type}/${kind}`))
      if (!pool) return
      // getElements / getElementCounts come from Cobblemon's StructurePoolAccessor mixin.
      const elements = pool.getElements()
      const before = elements.size()
      elements.removeIf(e => isPokemonPiece(e))
      removed += before - elements.size()
      pool.setElementCounts(pool.getElementCounts().stream()
        .filter(p => !isPokemonPiece(p.getFirst()))
        .collect(Collectors.toList()))
    })
  })
  console.info(`[pokeworld] removed ${removed} Cobblemon/CobbleDollars pieces from Overworld village pools`)
})
