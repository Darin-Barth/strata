// Pokémon world portal: build destination portals on the surface, never in caves or under the sea.
// BBL Portals searches up to 32 blocks around the matching spot, top-down per column, and builds on
// the first solid block with open (non-liquid) space above it. Over water that skips the sea and
// lands in a cave below it. Setting the search floor to sea level keeps it on land; if no dry land
// is in range (open ocean) it falls back to the entry height, on a small landing pad of frame blocks.
// The two portals are linked both ways (BBL's PortalLinkingStorage), so going back returns to the
// portal you came from as long as both frames stand.
// The floors aren't in BBL's KubeJS builder, so set them on its PortalLink at server start.
const PokePortalRegistry = Java.loadClass('com.benbenlaw.portals.util.CustomPortalApiRegistry')
const PokePortalInteger = Java.loadClass('java.lang.Integer')
let pokePortalFloorsSet = false

ServerEvents.tick(event => {
  if (pokePortalFloorsSet) return
  pokePortalFloorsSet = true
  const server = event.server
  let pokeSea = null
  let overworldSea = null
  server.getAllLevels().forEach(level => {
    const d = level.dimension
    const id = String(d && d.location ? d.location() : d)
    if (id === 'pokeworld:pokeworld') pokeSea = level.getSeaLevel()
    if (id === 'minecraft:overworld') overworldSea = level.getSeaLevel()
  })
  PokePortalRegistry.getAllPortalLinks().forEach(link => {
    if (String(link.dimID) !== 'pokeworld:pokeworld') return
    // Lowest solid block the portal may stand on: one below sea level, so it sits at sea level or higher.
    link.portalSearchYBottom = PokePortalInteger.valueOf(pokeSea - 1)
    link.returnPortalSearchYBottom = PokePortalInteger.valueOf(overworldSea - 1)
    console.info(`[pokeworld] portal search floors: Pokémon world Y ${link.portalSearchYBottom}, Overworld Y ${link.returnPortalSearchYBottom}`)
  })
})
