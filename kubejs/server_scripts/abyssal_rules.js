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
  // The Tidecaller lights a dark-prismarine portal frame (Strata's layout).
  event.shaped('strata:tidecaller', [
    'PBP',
    'PCP',
    'PBP',
  ], {
    P: 'minecraft:prismarine_crystals',
    B: 'create_submarine:ballast_tank',
    C: 'minecraft:conduit',
  }).id('strata:tidecaller')
  // The boss ladder: the Karkinos' claw, the Hullbreaker's embryo and six Abyssal Pearls.
  event.shaped('strata:leviathan_lure', [
    'PKP',
    'PHP',
    'PIP',
  ], {
    P: 'strata:abyssal_pearl',
    K: 'hybrid_aquatic:karkinos_claw',
    H: 'minecraft:heart_of_the_sea',
    I: 'alexscaves:immortal_embryo',
  }).id('strata:leviathan_lure')
})

// The Leviathan Lure: used in the Trench below Y 120, it calls up Cataclysm's Leviathan, the
// Abyssal Plain's final boss. One at a time near the player; the lure is used up.
ItemEvents.rightClicked('strata:leviathan_lure', event => {
  const player = event.player
  if (!abyssalIn(player)) return
  if (String(player.block.biomeId) !== 'strata:the_trench' || player.y > 120) {
    player.displayClientMessage(Text.aqua('Nothing answers. It needs the deep: the Trench, below Y 120.').italic(), true)
    return
  }
  const around = player.level.getEntities(player, player.boundingBox.inflate(160))
  let leviathanNear = false
  for (let i = 0; i < around.size(); i++) if (String(around.get(i).type) === 'cataclysm:the_leviathan') leviathanNear = true
  if (leviathanNear) {
    player.displayClientMessage(Text.red('The Leviathan is already here.'), true)
    return
  }
  player.mainHandItem.count--
  const r = player.yaw * Math.PI / 180
  const x = player.x - Math.sin(r) * 24, z = player.z + Math.cos(r) * 24, y = player.y - 6
  event.server.runCommandSilent(`execute in ${abyssalDimensionId} run summon cataclysm:the_leviathan ${x.toFixed(1)} ${y.toFixed(1)} ${z.toFixed(1)}`)
  event.server.runCommandSilent(`execute in ${abyssalDimensionId} positioned ${player.x} ${player.y} ${player.z} run tellraw @a[distance=..200] {"text":"Something vast stirs in the trench...","color":"dark_aqua","italic":true}`)
  event.cancel()
})

// --- The Lifepod -----------------------------------------------------------------------------
// With no surface, stepping through the portal would mean drowning. The first time a player
// arrives somewhere without a Lifepod nearby, one is set down on the sea floor and the player is
// moved into it. It is a capsule lying along Z (textures: tools/build_lifepod.py): an octagonal
// white hull with an orange lower band and orange end caps, a round hatch on the front, portholes
// down both sides, an orange beacon on the roof at each end (to find it in the dark), on two
// skids. Inside: a deck, ceiling lamps, seats, a supply chest, a crafting table, the moon pool
// (the way out) and the Return to Surface console. Every pod block is unbreakable.
//
// Portals link 1:1 by X/Z at roughly the same height, but the sea floor sits around Y 300 and
// Overworld portals around Y 60-120, so BBL Portals usually builds the arrival portal inside the
// rock under the sea. That portal and its link are left alone: every trip arrives there and is
// moved up into the pod. There is no portal back; the console returns you to the Overworld
// outside the portal you came in by (BBL's return link could land you somewhere else entirely).
const abyssalTopY = 558
const abyssalPodPrefix = 'strata:lifepod_'
const abyssalTag = Java.loadClass('net.minecraft.nbt.CompoundTag')
// Half-width of the hull's octagonal cross-section, by row above the pod bottom.
const abyssalPodHalf = [2, 3, 4, 4, 4, 4, 4, 3, 2]
const abyssalInHull = (x, y) => y >= 0 && y <= 8 && Math.abs(x) <= abyssalPodHalf[y]

// Pods are kept in server data as "x,y,z" keys: centre X/Z and the bottom row Y.
const abyssalPods = server => {
  const all = server.persistentData.getCompound('strata_lifepods')
  const out = []
  all.getAllKeys().forEach(key => {
    let p = String(key).split(',').map(Number)
    out.push({ x: p[0], y: p[1], z: p[2] })
  })
  return out
}
const abyssalAddPod = (server, x, y, z) => {
  const all = server.persistentData.getCompound('strata_lifepods')
  all.put(`${x},${y},${z}`, new abyssalTag())
  server.persistentData.put('strata_lifepods', all)
}

// The first water above (x, fromY, z), or -1 if the column has none up to the ceiling.
const abyssalWaterAbove = (level, x, fromY, z) => {
  for (let y = fromY; y < abyssalTopY; y++) if (abyssalIsWater(level.getBlock(x, y, z))) return y
  return -1
}

// The lowest water block of the sea above the ground at (x, z), starting at y0: down through the
// water if y0 is in the sea, up through the rock if y0 is buried. -1 if there's no sea.
const abyssalFloorAt = (level, x, y0, z) => {
  if (!abyssalIsWater(level.getBlock(x, y0, z))) return abyssalWaterAbove(level, x, y0 + 1, z)
  let y = y0
  while (y > -40 && abyssalIsWater(level.getBlock(x, y - 1, z))) y--
  return y
}

// Pod blocks may replace anything but portals, their frames and blocks holding items.
const abyssalPodSet = (level, x, y, z, id, props) => {
  const b = level.getBlock(x, y, z)
  const old = String(b.id)
  if (old === 'portals:custom_portal' || old === 'minecraft:dark_prismarine' || b.entity) return
  if (props) b.set(id, props)
  else b.set(id)
}

// Builds the pod with its centre column at (cx, cz) and its bottom row at by (skids at by - 1).
// Returns where the player stands.
const abyssalBuildPod = (level, server, cx, by, cz) => {
  const at = (x, y, z, id, props) => abyssalPodSet(level, cx + x, by + y, cz + z, id, props)
  const shellOf = (x, y) => !abyssalInHull(x - 1, y) || !abyssalInHull(x + 1, y) || !abyssalInHull(x, y - 1) || !abyssalInHull(x, y + 1)
  for (let z = -6; z <= 6; z++) for (let y = 0; y <= 8; y++) for (let x = -4; x <= 4; x++) {
    if (!abyssalInHull(x, y)) continue
    let ax = Math.abs(x)
    if (Math.abs(z) === 6) {  // end caps: white, with an orange rim
      at(x, y, z, abyssalPodPrefix + (shellOf(x, y) ? 'hull_orange' : 'hull'))
      continue
    }
    if (shellOf(x, y)) {
      let id = 'hull'
      if (y <= 1) id = 'hull_orange'
      else if (y === 2) id = 'hull_stripe'
      else if (ax === 4 && y === 4 && z % 3 === 0) id = 'window'
      else if (y === 8 && x === 0 && Math.abs(z) === 4) id = 'beacon'
      at(x, y, z, abyssalPodPrefix + id)
    } else if (y === 1) {
      at(x, y, z, abyssalPodPrefix + 'deck')
    } else if (y === 7 || (y === 6 && ax === 3)) {
      at(x, y, z, abyssalPodPrefix + (y === 7 && x === 0 && z % 3 === 0 ? 'lamp' : 'hull'))
    } else {
      at(x, y, z, 'minecraft:air')
    }
  }
  // Front hatch (with its handle) and the rear cap, standing out from the end caps.
  for (let y = 2; y <= 6; y++) for (let x = -2; x <= 2; x++) {
    if (Math.abs(x) + Math.abs(y - 4) > 2) continue
    at(x, y, 7, abyssalPodPrefix + (x === 0 && y === 4 ? 'hatch_wheel' : 'hatch'))
    at(x, y, -7, abyssalPodPrefix + 'hull_orange')
  }
  // Skids with cross beams, on posts down to the ground.
  for (let z = -5; z <= 5; z++) for (let x = -2; x <= 2; x++) {
    if (Math.abs(x) === 2 || (Math.abs(z) === 5)) at(x, -1, z, abyssalPodPrefix + 'frame')
  }
  for (let x = -2; x <= 2; x += 4) for (let z = -5; z <= 5; z += 5) {
    for (let y = -2; y >= -14; y--) {
      let b = level.getBlock(cx + x, by + y, cz + z)
      if (b.id !== 'minecraft:air' && !abyssalIsWater(b)) break
      b.set(abyssalPodPrefix + 'frame')
    }
  }
  // Moon pool: a 2x2 hole of water through the floor at the back, down to the sea.
  for (let x = -1; x <= 0; x++) for (let z = -4; z <= -3; z++) {
    at(x, 1, z, 'minecraft:water')
    at(x, 0, z, 'minecraft:water')
  }
  // Seats along both walls, under the portholes.
  for (let z = -1; z <= 1; z++) {
    at(-3, 2, z, 'minecraft:smooth_quartz_stairs', { facing: 'west' })
    at(3, 2, z, 'minecraft:smooth_quartz_stairs', { facing: 'east' })
  }
  // The front: the Return to Surface console (two blocks tall) with a lit sign above it, the
  // supply chest on its left and a crafting table on its right.
  at(0, 2, 5, abyssalPodPrefix + 'console')
  at(0, 3, 5, abyssalPodPrefix + 'console')
  at(2, 2, 5, 'minecraft:crafting_table')
  const X = cx, Y = by, Z = cz
  server.runCommandSilent(`execute in ${abyssalDimensionId} run setblock ${X} ${Y + 4} ${Z + 5} minecraft:spruce_wall_sign[facing=north]{front_text:{has_glowing_text:1b,color:"cyan",messages:['""','"RETURN TO"','"SURFACE"','""']}}`)
  // A few supplies: lights you can use underwater and some food. Nothing that skips progression.
  server.runCommandSilent(`execute in ${abyssalDimensionId} run setblock ${X - 2} ${Y + 2} ${Z + 5} minecraft:chest[facing=north]{CustomName:'"Lifepod Supplies"',Items:[{Slot:0b,id:"minecraft:sea_pickle",count:8},{Slot:1b,id:"minecraft:cooked_cod",count:8},{Slot:2b,id:"minecraft:dried_kelp",count:16}]}`)
  abyssalAddPod(server, cx, by, cz)
  return { x: cx + 0.5, y: by + 2, z: cz - 1.5 }
}

// A pod built before the capsule design (a 9x8x9 cube whose floor is a plain hull block, with a
// return portal inside) sits right above the arrival portal: it's flooded and replaced.
const abyssalClearOldPod = (level, px, py, pz) => {
  for (let y = py; y < abyssalTopY; y++) {
    let id = String(level.getBlock(px, y, pz).id)
    if (id.indexOf(abyssalPodPrefix) !== 0) continue
    if (id !== abyssalPodPrefix + 'hull') return false
    for (let dx = -4; dx <= 4; dx++) for (let dy = 0; dy <= 7; dy++) for (let dz = -4; dz <= 4; dz++) {
      level.getBlock(px + dx, y + dy, pz + dz).set('minecraft:water')
    }
    return true
  }
  return false
}

// Where someone arriving at (px, py, pz) stands in the Lifepod, building the pod first if there's
// none near. Null if there's no sea floor to put one on.
const abyssalPodSpot = (level, server, px, py, pz) => {
  let spot = null
  const pods = abyssalPods(server)
  for (let i = 0; i < pods.length; i++) {
    let p = pods[i]
    if (Math.abs(p.x - px) <= 24 && Math.abs(p.z - pz) <= 24) { spot = { x: p.x + 0.5, y: p.y + 2, z: p.z - 1.5 }; break }
  }
  if (!spot) {
    abyssalClearOldPod(level, px, py, pz)
    // Buried arrival: the pod goes on the floor straight above. Arrival in open water: beside the
    // portal, so the two don't overlap.
    let buried = !abyssalIsWater(level.getBlock(px, py, pz)) && !abyssalIsWater(level.getBlock(px, py + 1, pz))
    let cx = buried ? px : px + 10
    let floor = -1
    for (let x = -4; x <= 4; x++) for (let z = -7; z <= 7; z++) {
      let f = abyssalFloorAt(level, cx + x, py, pz + z)
      if (f > floor) floor = f
    }
    if (floor < 0) {
      console.error(`Abyssal Plain: no sea floor found for a Lifepod near ${px} ${py} ${pz}`)
      return null
    }
    spot = abyssalBuildPod(level, server, cx, Math.min(floor + 1, abyssalTopY - 12), pz)
    spot.built = true
  }
  return spot
}

const abyssalArrive = (player) => {
  const spot = abyssalPodSpot(player.level, player.server, Math.floor(player.x), Math.floor(player.y), Math.floor(player.z))
  if (!spot) return
  if (spot.built) player.tell(Text.aqua('Lifepod deployed. The sea starts at the moon pool; the console takes you back to the surface.').italic())
  player.server.runCommandSilent(`execute in ${abyssalDimensionId} run tp ${player.username} ${spot.x} ${spot.y} ${spot.z} 0 0`)
}

// --- Return to Surface -------------------------------------------------------------------------
// While a player is in the Overworld, their last spot on the ground outside any portal is kept.
// The console puts them back there, facing away from the portal; with nothing kept (they came by
// another way), at the world spawn.
const abyssalPortalBlocks = ['portals:custom_portal', 'minecraft:nether_portal', 'minecraft:end_portal']
const abyssalKeepSurfaceSpot = player => {
  if (!player.onGround()) return
  const feet = String(player.block.id), head = String(player.block.up.id)
  if (abyssalPortalBlocks.indexOf(feet) >= 0 || abyssalPortalBlocks.indexOf(head) >= 0) return
  const data = player.persistentData
  data.putDouble('strata_surface_x', player.x)
  data.putDouble('strata_surface_y', player.y)
  data.putDouble('strata_surface_z', player.z)
  data.putFloat('strata_surface_yaw', player.yaw)
  data.putBoolean('strata_surface', true)
}

BlockEvents.rightClicked('strata:lifepod_console', event => {
  const player = event.player
  if (!player || String(event.hand) !== 'MAIN_HAND') return
  event.cancel()
  const data = player.persistentData
  const server = event.server
  let to
  if (data.getBoolean('strata_surface')) {
    let yaw = (data.getFloat('strata_surface_yaw') + 180) % 360
    to = `${data.getDouble('strata_surface_x').toFixed(2)} ${data.getDouble('strata_surface_y').toFixed(2)} ${data.getDouble('strata_surface_z').toFixed(2)} ${yaw.toFixed(1)} 0`
  } else {
    let s = server.overworld().sharedSpawnPos
    to = `${s.x + 0.5} ${s.y} ${s.z + 0.5}`
  }
  const b = event.block
  server.runCommandSilent(`execute in ${abyssalDimensionId} run playsound minecraft:block.conduit.deactivate block @a ${b.x + 0.5} ${b.y + 0.5} ${b.z + 0.5} 1 1.2`)
  server.runCommandSilent(`execute in minecraft:overworld run tp ${player.username} ${to}`)
  server.runCommandSilent(`execute in minecraft:overworld at ${player.username} run playsound minecraft:entity.player.splash.high_speed player ${player.username} ~ ~ ~ 1 1`)
  player.displayClientMessage(Text.aqua('You surface.').italic(), true)
})

PlayerEvents.tick(event => {
  const player = event.player
  if (player.tickCount % 10 !== 0) return
  const data = player.persistentData
  if (abyssalIn(player)) {
    if (!data.getBoolean('strata_abyss_inside')) {
      data.putBoolean('strata_abyss_inside', true)
      abyssalArrive(player)
    }
    // No Conduit power down here: bases have to be engineered.
    if (player.tickCount % 20 === 0) player.server.runCommandSilent(`effect clear ${player.username} minecraft:conduit_power`)
  } else {
    if (data.getBoolean('strata_abyss_inside')) data.putBoolean('strata_abyss_inside', false)
    if (abyssalDimensionOf(player) === 'minecraft:overworld') abyssalKeepSurfaceSpot(player)
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
      let n = abyssalNeighbours[i]
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
