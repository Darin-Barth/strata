// The Abyssal Plain (strata:abyssal_plain), the underwater dimension: Tidecaller recipe, the
// Lifepod you arrive in, the flood rule, no Conduit power, no sponges, Abyssal Pearl drops.
// Design: docs/abyssal-plain-design.md.
// KubeJS server scripts share one scope: every top-level name here starts with "abyssal".
const abyssalDimensionId = 'strata:abyssal_plain'
const abyssalDimensionOf = entity => { const d = entity.level.dimension; return String(d && d.location ? d.location() : d) }
const abyssalIn = entity => abyssalDimensionOf(entity) === abyssalDimensionId
const abyssalNeighbours = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
const abyssalIsWater = block => !block.blockState.getFluidState().isEmpty()

ServerEvents.recipes(event => {
  // The Tidecaller lights a dark-prismarine portal frame (Darin's layout, Oct 26).
  event.shaped('strata:tidecaller', [
    'PBP',
    'PCP',
    'PBP',
  ], {
    P: 'minecraft:prismarine_crystals',
    B: 'create_submarine:ballast_tank',
    C: 'minecraft:conduit',
  }).id('strata:tidecaller')
})

// --- The Lifepod -----------------------------------------------------------------------------
// With no surface, stepping through the portal would mean drowning. The first time a player
// arrives somewhere without a Lifepod nearby, one is built around them: a sealed 9x8x9 room of
// unbreakable hull with windows, lights, a small supply chest and a moon pool (a water hole in
// the floor, the way out). Frame and portal blocks are left alone; the room's water becomes air.
const abyssalBuildLifepod = (player) => {
  const level = player.level
  const cx = Math.floor(player.x), cy = Math.floor(player.y), cz = Math.floor(player.z)
  for (let dx = -6; dx <= 6; dx++) for (let dy = -4; dy <= 7; dy++) for (let dz = -6; dz <= 6; dz++) {
    if (String(level.getBlock(cx + dx, cy + dy, cz + dz).id) === 'strata:lifepod_hull') return false
  }
  const replaceable = b => b.id === 'minecraft:air' || abyssalIsWater(b)
  for (let dx = -4; dx <= 4; dx++) for (let dy = -2; dy <= 5; dy++) for (let dz = -4; dz <= 4; dz++) {
    const b = level.getBlock(cx + dx, cy + dy, cz + dz)
    const shell = Math.abs(dx) === 4 || Math.abs(dz) === 4 || dy === -2 || dy === 5
    if (shell) {
      if (!replaceable(b)) continue
      const window = dy >= 0 && dy <= 2 && (Math.abs(dx) <= 1 || Math.abs(dz) <= 1) && (Math.abs(dx) === 4 || Math.abs(dz) === 4)
      b.set(window ? 'strata:lifepod_window' : 'strata:lifepod_hull')
    } else if (abyssalIsWater(b)) {
      b.set('minecraft:air')
    }
  }
  // Moon pool: a 2x2 water hole in the floor corner, down to the sea.
  for (let dx = 2; dx <= 3; dx++) for (let dz = 2; dz <= 3; dz++) level.getBlock(cx + dx, cy - 2, cz + dz).set('minecraft:water')
  // Lights in the roof corners.
  const lights = [[-3, -3], [-3, 3], [3, -3], [3, 3]]
  for (let i = 0; i < lights.length; i++) level.getBlock(cx + lights[i][0], cy + 4, cz + lights[i][1]).set('minecraft:sea_lantern')
  // A few supplies: lights you can use underwater and some food. Nothing that skips progression.
  player.server.runCommandSilent(`execute in ${abyssalDimensionId} run setblock ${cx - 3} ${cy - 1} ${cz - 3} minecraft:chest{CustomName:'"Lifepod Supplies"',Items:[{Slot:0b,id:"minecraft:sea_pickle",count:8},{Slot:1b,id:"minecraft:cooked_cod",count:8},{Slot:2b,id:"minecraft:dried_kelp",count:16}]} replace`)
  player.tell(Text.aqua('Lifepod deployed. The sea starts at the moon pool.').italic())
  return true
}

PlayerEvents.tick(event => {
  const player = event.player
  if (player.age % 10 !== 0) return
  const data = player.persistentData
  if (abyssalIn(player)) {
    if (!data.getBoolean('strata_abyss_inside')) {
      data.putBoolean('strata_abyss_inside', true)
      abyssalBuildLifepod(player)
    }
    // No Conduit power down here: bases have to be engineered (Darin, Oct 26).
    if (player.age % 20 === 0) player.server.runCommandSilent(`effect clear ${player.username} minecraft:conduit_power`)
  } else if (data.getBoolean('strata_abyss_inside')) {
    data.putBoolean('strata_abyss_inside', false)
  }
})

// --- The sea always wins ------------------------------------------------------------------------
// A broken block next to water becomes water, so there's no digging dry tunnels or air pockets.
// Sealed rooms (pumped dry, or a Deep Seas hull) stay dry: their blocks don't touch the sea.
BlockEvents.broken(event => {
  const level = event.block.level
  if (abyssalDimensionOf(event.block) !== abyssalDimensionId) return
  const x = event.block.x, y = event.block.y, z = event.block.z
  event.server.scheduleInTicks(1, () => {
    const b = level.getBlock(x, y, z)
    if (b.id !== 'minecraft:air') return
    for (let i = 0; i < abyssalNeighbours.length; i++) {
      const n = abyssalNeighbours[i]
      if (abyssalIsWater(level.getBlock(x + n[0], y + n[1], z + n[2]))) { b.set('minecraft:water'); return }
    }
  })
})

// Sponges would dry any space instantly.
BlockEvents.placed(event => {
  if (!event.player || !abyssalIn(event.player)) return
  const id = String(event.block.id)
  if (id === 'minecraft:sponge' || id === 'minecraft:wet_sponge') {
    event.player.displayClientMessage(Text.aqua('The sea is far too big for a sponge.').italic(), true)
    event.cancel()
  }
})

// --- Abyssal Pearls -------------------------------------------------------------------------------
// Rare from deep-sea creatures, guaranteed from the big ones. Also in the ruins' chests (loot
// modifiers). A late-game gate material.
const abyssalDeepNamespaces = ['hybrid_aquatic', 'alexscaves']
const abyssalBig = { 'alexscaves:hullbreaker': [2, 3], 'hybrid_aquatic:karkinos': [1, 2], 'cataclysm:the_leviathan': [4, 6] }
EntityEvents.death(event => {
  const entity = event.entity
  const player = event.source.player
  if (!player || !abyssalIn(entity)) return
  const id = String(entity.type)
  let count = 0
  if (abyssalBig[id]) count = abyssalBig[id][0] + Math.floor(Math.random() * (abyssalBig[id][1] - abyssalBig[id][0] + 1))
  else if (abyssalDeepNamespaces.indexOf(id.split(':')[0]) >= 0 && Math.random() < 0.04) count = 1
  if (count <= 0) return
  event.server.runCommandSilent(`execute in ${abyssalDimensionId} run summon minecraft:item ${entity.x} ${entity.y + 0.5} ${entity.z} {Item:{id:"strata:abyssal_pearl",count:${count}}}`)
})
