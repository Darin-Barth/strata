// The Abyssal Plain (strata:abyssal_plain), the underwater dimension: Tidecaller recipe, the
// Lifepod you arrive in, the flood rule, no Conduit power, no sponges, Abyssal Pearl drops.
// Design: docs/abyssal-plain-design.md.
// KubeJS server scripts share one scope: every top-level name here starts with "abyssal".
// Facing: `yaw`/`pitch` are KubeJS's names on a dedicated server, where the game's own getYRot()/getXRot() are
// hidden; in single player a client mod shadows `yaw` (it reads as undefined) and only the getters work.
const abyssalYaw = e => { const v = e.yaw; return typeof v === 'number' ? v : e.getYRot() }
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
  const r = abyssalYaw(player) * Math.PI / 180
  const x = player.x - Math.sin(r) * 24, z = player.z + Math.cos(r) * 24, y = player.y - 6
  event.server.runCommandSilent(`execute in ${abyssalDimensionId} run summon cataclysm:the_leviathan ${x.toFixed(1)} ${y.toFixed(1)} ${z.toFixed(1)}`)
  event.server.runCommandSilent(`execute in ${abyssalDimensionId} positioned ${player.x} ${player.y} ${player.z} run tellraw @a[distance=..200] {"text":"Something vast stirs in the trench...","color":"dark_aqua","italic":true}`)
  event.cancel()
})

// --- The Lifepod -----------------------------------------------------------------------------
// With no surface, stepping through the portal would mean drowning, and most of the sea floor is
// deeper than a diver in plain gear survives. So nobody arrives where the portal would put them:
// the first trip from a place finds the nearest Abyssal Shelf (the shallow biome, floor within
// 120 m of the ceiling) and a Lifepod is set down there, as if it had come down from above and hit
// the shelf: a short gouge and some wreckage lie behind it. Every later trip from around the same
// place (and anyone else whose nearest shelf it is) arrives in that pod.
//
// The pod is an upright capsule (textures: tools/build_lifepod.py): a round white hull nine blocks
// across with an orange stripe, an inflated orange flotation collar around its base, a rounded
// shoulder and cap with the top hatch, a mast with a beacon (to find it in the dark), portholes on
// three sides and LIFEPOD stencilled on the front. It stands on four struts, so the moon pool in
// the middle of the deck opens onto clear water. Inside: the Return to Surface console with the
// supply chest and a crafting table, seats along both walls, lockers and a radio at the back.
// Every pod block is unbreakable.
//
// There is no portal back; the console returns you to the Overworld outside the portal you came
// in by (BBL's return link could land you somewhere else entirely). The arrival portal BBL builds
// (usually inside the rock under the sea) and its link are left alone.
const abyssalTopY = 558
const abyssalPodPrefix = 'strata:lifepod_'
const abyssalTag = Java.loadClass('net.minecraft.nbt.CompoundTag')
const abyssalPodsKey = 'strata_lifepods_v2'      // capsule pods; older cube and tube pods are forgotten
const abyssalSitesKey = 'strata_lifepod_sites'   // arrival area (128-block cell) -> pod
// Half-widths of round outlines 5, 7, 9 and 11 blocks across, by row.
const abyssalRound = {
  5: [1, 2, 2, 2, 1],
  7: [1, 2, 3, 3, 3, 2, 1],
  9: [2, 3, 4, 4, 4, 4, 4, 3, 2],
  11: [2, 3, 4, 5, 5, 5, 5, 5, 4, 3, 2],
}
const abyssalInRound = (d, x, z) => {
  const r = (d - 1) / 2
  return Math.abs(z) <= r && Math.abs(x) <= abyssalRound[d][z + r]
}

// Pods are kept in server data as "x,y,z" keys: centre X/Z and the Y of the hull's underside.
const abyssalPods = server => {
  const all = server.persistentData.getCompound(abyssalPodsKey)
  const out = []
  all.getAllKeys().forEach(key => {
    let p = String(key).split(',').map(Number)
    out.push({ x: p[0], y: p[1], z: p[2] })
  })
  return out
}
const abyssalAddPod = (server, x, y, z) => {
  const all = server.persistentData.getCompound(abyssalPodsKey)
  all.put(`${x},${y},${z}`, new abyssalTag())
  server.persistentData.put(abyssalPodsKey, all)
}
const abyssalPodStand = p => ({ x: p.x + 0.5, y: p.y + 2, z: p.z + 1.5 })

// The lowest water block of the sea at (x, z), looking down from under the ceiling. -1 if the
// column has no sea.
const abyssalFloorAt = (level, x, z) => {
  let y = abyssalTopY
  while (y > -40 && !abyssalIsWater(level.getBlock(x, y, z))) y--
  if (y <= -40) return -1
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

// Builds the pod around the centre column (cx, cz) with the hull's underside at by.
const abyssalBuildPod = (level, server, cx, by, cz) => {
  const at = (x, y, z, id, props) => abyssalPodSet(level, cx + x, by + y, cz + z, id.indexOf(':') < 0 ? abyssalPodPrefix + id : id, props)
  for (let z = -5; z <= 5; z++) for (let x = -5; x <= 5; x++) {
    let in7 = abyssalInRound(7, x, z), in9 = abyssalInRound(9, x, z), in5 = abyssalInRound(5, x, z)
    // Underside, deck and the collar around them.
    if (in7) at(x, 0, z, 'hull_orange')
    if (in9) at(x, 1, z, in7 ? 'deck' : 'hull_orange')
    else if (abyssalInRound(11, x, z)) {
      at(x, 1, z, 'collar')
      at(x, 2, z, 'collar_slab', { type: 'bottom', waterlogged: 'true' })
    }
    // The wall (one block thick) and the cabin's air.
    for (let y = 2; y <= 5; y++) {
      if (!in9) continue
      if (in7) at(x, y, z, 'minecraft:air')
      else at(x, y, z, y === 5 ? 'hull_stripe' : 'hull')
    }
    // Ceiling, rounded shoulder and cap.
    if (in7) at(x, 6, z, 'hull')
    else if (in9) at(x, 6, z, 'hull_slab', { type: 'bottom', waterlogged: 'true' })
    if (in5) at(x, 7, z, 'hull_slab', { type: 'bottom', waterlogged: 'true' })
  }
  // Ceiling lamps, the top hatch, the mast with its beacon.
  for (let i = -2; i <= 2; i += 2) {
    at(i, 6, 0, 'lamp')
    at(0, 6, i, 'lamp')
  }
  at(0, 7, 0, 'hatch_wheel')
  at(-1, 7, -1, 'hull')
  at(-1, 8, -1, 'mast', { waterlogged: 'true' })
  at(-1, 9, -1, 'mast', { waterlogged: 'true' })
  at(-1, 10, -1, 'beacon')
  // Beacon lights on the collar and portholes (two tall) on three sides.
  for (let i = -5; i <= 5; i += 10) {
    at(i, 2, 0, 'beacon')
    at(0, 2, i, 'beacon')
  }
  for (let y = 3; y <= 4; y++) {
    at(-4, y, 0, 'window')
    at(4, y, 0, 'window')
  }
  at(0, 3, 4, 'window')
  // LIFEPOD across the front (south), under the stripe; read from outside, west is on the left.
  at(-1, 4, 4, 'marking_0')
  at(0, 4, 4, 'marking_1')
  at(1, 4, 4, 'marking_2')
  // Four struts down to the ground, each on a foot.
  for (let x = -3; x <= 3; x += 6) for (let z = -3; z <= 3; z += 6) {
    at(x, 0, z, 'frame')
    for (let y = -1; y >= -12; y--) {
      let b = level.getBlock(cx + x, by + y, cz + z)
      if (b.id !== 'minecraft:air' && !abyssalIsWater(b)) break
      let below = level.getBlock(cx + x, by + y - 1, cz + z)
      if (below.id !== 'minecraft:air' && !abyssalIsWater(below)) b.set(abyssalPodPrefix + 'frame')
      else b.set(abyssalPodPrefix + 'mast', { waterlogged: 'true' })
    }
  }
  // The moon pool in the middle of the deck, with a hatch rim.
  at(0, 0, 0, 'minecraft:water')
  at(0, 1, 0, 'minecraft:water')
  at(1, 1, 0, 'hatch'); at(-1, 1, 0, 'hatch'); at(0, 1, 1, 'hatch'); at(0, 1, -1, 'hatch')
  at(1, 0, 0, 'hatch'); at(-1, 0, 0, 'hatch'); at(0, 0, 1, 'hatch'); at(0, 0, -1, 'hatch')
  // Seats along both walls.
  for (let z = -1; z <= 1; z++) {
    at(-3, 2, z, 'minecraft:smooth_quartz_stairs', { facing: 'west' })
    at(3, 2, z, 'minecraft:smooth_quartz_stairs', { facing: 'east' })
  }
  // The back (north): the Return to Surface console (two blocks tall) under a lit sign, the supply
  // chest on its left and a crafting table on its right. The front (south): lockers and the radio.
  at(0, 2, -3, 'console')
  at(0, 3, -3, 'console')
  at(1, 2, -3, 'minecraft:crafting_table')
  at(-1, 2, 3, 'locker'); at(1, 2, 3, 'locker'); at(-1, 3, 3, 'locker'); at(1, 3, 3, 'locker')
  at(0, 2, 3, 'minecraft:jukebox')
  const X = cx, Y = by, Z = cz
  server.runCommandSilent(`execute in ${abyssalDimensionId} run setblock ${X} ${Y + 4} ${Z - 3} minecraft:spruce_wall_sign[facing=south]{front_text:{has_glowing_text:1b,color:"cyan",messages:['""','"RETURN TO"','"SURFACE"','""']}}`)
  // A few supplies: lights you can use underwater and some food. Nothing that skips progression.
  server.runCommandSilent(`execute in ${abyssalDimensionId} run setblock ${X - 1} ${Y + 2} ${Z - 3} minecraft:chest[facing=south]{CustomName:'"Lifepod Supplies"',Items:[{Slot:0b,id:"minecraft:sea_pickle",count:8},{Slot:1b,id:"minecraft:cooked_cod",count:8},{Slot:2b,id:"minecraft:dried_kelp",count:16}]}`)
  abyssalAddPod(server, cx, by, cz)
}

// The crash: a gouge in the sea floor behind the pod (north of it) and bits of wreckage along it.
const abyssalCrashScar = (level, cx, cz) => {
  const wreck = ['minecraft:white_concrete', 'minecraft:orange_concrete', 'minecraft:iron_bars', 'minecraft:cut_copper_slab', 'minecraft:white_concrete']
  for (let i = 7; i <= 26; i++) {
    let half = i < 18 ? 1 : 0
    for (let dx = -half; dx <= half; dx++) {
      let x = cx + dx + Math.floor((i - 7) / 6), z = cz - i
      let f = abyssalFloorAt(level, x, z)
      if (f < 0) continue
      let ground = level.getBlock(x, f - 1, z)
      if (String(ground.id).indexOf(abyssalPodPrefix) === 0 || ground.entity) continue
      // Clear what grew there, scrape the floor, drop the odd piece of wreckage.
      for (let y = f; y < f + 16; y++) {
        let b = level.getBlock(x, y, z)
        if (abyssalIsWater(b) && String(b.id) === 'minecraft:water') break
        b.set('minecraft:water')
      }
      ground.set(Math.random() < 0.6 ? 'minecraft:gravel' : 'minecraft:coarse_dirt')
      if (Math.random() < 0.16) {
        let id = wreck[Math.floor(Math.random() * wreck.length)]
        if (id === 'minecraft:iron_bars' || id === 'minecraft:cut_copper_slab') level.getBlock(x, f, z).set(id, { waterlogged: 'true' })
        else level.getBlock(x, f, z).set(id)
      }
    }
  }
}

// The nearest shelf to (px, pz): a spot inside the Abyssal Shelf biome. Null if there is none
// within 6,000 blocks.
const abyssalShelfNear = (level, px, pz) => {
  const BlockPos = Java.loadClass('net.minecraft.core.BlockPos')
  const found = level.findClosestBiome3d(holder => String(holder.unwrapKey().get().location()) === 'strata:abyssal_shelf',
    new BlockPos(px, 500, pz), 6000, 32, 64)
  if (found === null) return null
  const at = found.getFirst()
  return { x: at.getX(), z: at.getZ() }
}

// Where someone arriving at (px, pz) stands in their Lifepod, building it first if this area has
// none yet. Null if no place for one was found.
const abyssalPodSpot = (level, server, px, pz) => {
  const sites = server.persistentData.getCompound(abyssalSitesKey)
  const cell = `${px >> 7},${pz >> 7}`
  if (sites.contains(cell)) {
    let p = String(sites.getString(cell)).split(',').map(Number)
    return abyssalPodStand({ x: p[0], y: p[1], z: p[2] })
  }
  let site = abyssalShelfNear(level, px, pz)
  if (site === null) {
    console.error(`Abyssal Plain: no shelf found near ${px} ${pz}; the Lifepod goes where the portal is`)
    site = { x: px, z: pz }
  }
  // Another area's pod on the same shelf is shared.
  let pod = null
  const pods = abyssalPods(server)
  for (let i = 0; i < pods.length; i++) {
    if (Math.abs(pods[i].x - site.x) <= 96 && Math.abs(pods[i].z - site.z) <= 96) { pod = pods[i]; break }
  }
  let built = false
  if (pod === null) {
    // Walk a little way into the shelf from its edge (toward higher ground), then stand the pod
    // on the highest floor under its footprint, two blocks clear of it.
    let best = site, bestFloor = abyssalFloorAt(level, site.x, site.z)
    for (let i = 0; i < 8; i++) {
      let x = site.x + Math.round(Math.cos(i * Math.PI / 4) * 40), z = site.z + Math.round(Math.sin(i * Math.PI / 4) * 40)
      let f = abyssalFloorAt(level, x, z)
      if (f > bestFloor) { best = { x: x, z: z }; bestFloor = f }
    }
    let floor = -1
    for (let x = -5; x <= 5; x++) for (let z = -5; z <= 5; z++) {
      let f = abyssalFloorAt(level, best.x + x, best.z + z)
      if (f > floor) floor = f
    }
    if (floor < 0) {
      console.error(`Abyssal Plain: no sea floor found for a Lifepod near ${best.x} ${best.z}`)
      return null
    }
    pod = { x: best.x, y: Math.min(floor + 2, abyssalTopY - 14), z: best.z }
    abyssalCrashScar(level, pod.x, pod.z)
    abyssalBuildPod(level, server, pod.x, pod.y, pod.z)
    built = true
  }
  sites.putString(cell, `${pod.x},${pod.y},${pod.z}`)
  server.persistentData.put(abyssalSitesKey, sites)
  const spot = abyssalPodStand(pod)
  spot.built = built
  return spot
}

const abyssalArrive = (player) => {
  const spot = abyssalPodSpot(player.level, player.server, Math.floor(player.x), Math.floor(player.z))
  if (!spot) return
  if (spot.built) player.tell(Text.aqua('Lifepod deployed on the nearest shelf. The sea starts at the moon pool; the console takes you back to the surface.').italic())
  player.server.runCommandSilent(`execute in ${abyssalDimensionId} run tp ${player.username} ${spot.x} ${spot.y} ${spot.z} 180 0`)
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
  data.putFloat('strata_surface_yaw', abyssalYaw(player))
  data.putBoolean('strata_surface', true)
}

BlockEvents.rightClicked('strata:lifepod_console', event => {
  const player = event.player
  if (!player || String(event.hand) !== 'MAIN_HAND') return
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
  event.cancel() // last: in KubeJS cancel() ends the handler (with it first, the console did nothing)
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
    // No Conduit power down here (bases have to be engineered): startup_scripts/abyssal_vampire_air.js
    // refuses the effect, along with every other free way to breathe.
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
