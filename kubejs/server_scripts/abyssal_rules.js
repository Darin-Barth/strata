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
// arrives somewhere without a Lifepod nearby, one is built around them: a sealed 9x8x9 room of
// unbreakable hull with windows, lights, a small supply chest and a moon pool (a water hole in
// the floor, the way out). Frame and portal blocks are left alone; the room's water becomes air.
//
// Portals link 1:1 by X/Z at roughly the same height, but the sea floor sits around Y 300 and
// Overworld portals around Y 60-120, so BBL Portals usually builds the arrival portal inside the
// rock under the sea (Darin, Oct 26: "everything is deepslate, no water"). Then the Lifepod goes
// up onto the sea floor instead, with its own lit dark prismarine return portal; the Overworld
// portal is re-linked to it and the buried portal removed, so later trips arrive in the pod.
const abyssalHullId = 'strata:lifepod_hull'
const abyssalBlocks = Java.loadClass('net.minecraft.world.level.block.Blocks')
const abyssalAxis = Java.loadClass('net.minecraft.core.Direction$Axis')
const abyssalPos = Java.loadClass('net.minecraft.core.BlockPos')
const abyssalRL = Java.loadClass('net.minecraft.resources.ResourceLocation')
const abyssalResourceKey = Java.loadClass('net.minecraft.resources.ResourceKey')
const abyssalRegistries = Java.loadClass('net.minecraft.core.registries.Registries')
const abyssalPortalArea = Java.loadClass('com.benbenlaw.portals.portal.frame.VanillaPortalAreaHelper')
const abyssalPortalsMod = Java.loadClass('com.benbenlaw.portals.Portals')
const abyssalTopY = 558

const abyssalPodNear = (level, cx, cy, cz) => {
  for (let dx = -6; dx <= 6; dx++) for (let dy = -4; dy <= 7; dy++) for (let dz = -6; dz <= 6; dz++) {
    if (String(level.getBlock(cx + dx, cy + dy, cz + dz).id) === abyssalHullId) return true
  }
  return false
}

// Builds the pod centred on (cx, cy, cz); the player stands at cy - 1.
const abyssalBuildPod = (level, server, cx, cy, cz) => {
  const replaceable = b => b.id === 'minecraft:air' || abyssalIsWater(b)
  for (let dx = -4; dx <= 4; dx++) for (let dy = -2; dy <= 5; dy++) for (let dz = -4; dz <= 4; dz++) {
    let b = level.getBlock(cx + dx, cy + dy, cz + dz)
    let shell = Math.abs(dx) === 4 || Math.abs(dz) === 4 || dy === -2 || dy === 5
    if (shell) {
      if (!replaceable(b)) continue
      let window = dy >= 0 && dy <= 2 && (Math.abs(dx) <= 1 || Math.abs(dz) <= 1) && (Math.abs(dx) === 4 || Math.abs(dz) === 4)
      b.set(window ? 'strata:lifepod_window' : abyssalHullId)
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
  server.runCommandSilent(`execute in ${abyssalDimensionId} run setblock ${cx - 3} ${cy - 1} ${cz - 3} minecraft:chest{CustomName:'"Lifepod Supplies"',Items:[{Slot:0b,id:"minecraft:sea_pickle",count:8},{Slot:1b,id:"minecraft:cooked_cod",count:8},{Slot:2b,id:"minecraft:dried_kelp",count:16}]} replace`)
}

// The first water above (x, fromY, z), or -1 if the column has none up to the ceiling.
const abyssalWaterAbove = (level, x, fromY, z) => {
  for (let y = fromY; y < abyssalTopY; y++) if (abyssalIsWater(level.getBlock(x, y, z))) return y
  return -1
}

// Arrival under the sea floor: pod on the floor above (px, pz) with a lit return portal, the
// Overworld portal re-linked to it, the buried portal removed. Returns the pod centre Y, or null
// if (px, py, pz) isn't buried (open water, or no sea above).
const abyssalRaisePod = (level, server, px, py, pz) => {
  if (abyssalIsWater(level.getBlock(px, py, pz)) || abyssalIsWater(level.getBlock(px, py + 1, pz))) return null
  const seaAbove = abyssalWaterAbove(level, px, py + 2, pz)
  if (seaAbove < 0) return null
  // Sit the pod just above the highest point of the floor under its footprint.
  let floor = seaAbove
  for (let dx = -4; dx <= 4; dx++) for (let dz = -4; dz <= 4; dz++) {
    let w = abyssalWaterAbove(level, px + dx, py + 2, pz + dz)
    if (w > floor) floor = w
  }
  const cy = Math.min(floor + 3, abyssalTopY - 8)
  abyssalBuildPod(level, server, px, cy, pz)
  // Return portal: a 4x5 dark prismarine frame on the pod's +Z wall, 2x3 opening.
  for (let dx = -2; dx <= 1; dx++) for (let dy = -1; dy <= 3; dy++) {
    let edge = dx === -2 || dx === 1 || dy === -1 || dy === 3
    level.getBlock(px + dx, cy + dy, pz + 3).set(edge ? 'minecraft:dark_prismarine' : 'minecraft:air')
  }
  const area = new abyssalPortalArea().init(level, new abyssalPos(px - 1, cy, pz + 3), abyssalAxis.X, abyssalBlocks.DARK_PRISMARINE)
  if (!area.isValidFrame()) {
    console.error(`Abyssal Plain: the Lifepod return portal frame at ${px} ${cy} ${pz + 3} isn't valid`)
  } else {
    area.lightPortal(abyssalBlocks.DARK_PRISMARINE)
    // Re-link whichever Overworld portal led to the buried one.
    let storage = abyssalPortalsMod.PORTAL_LINKING_STORAGE
    let links = storage ? storage.PORTAL_LINKS.get(abyssalRL.parse(abyssalDimensionId)) : null
    if (links) {
      let it = links.entrySet().iterator()
      let oldKey = null, overworld = null
      while (it.hasNext()) {
        let e = it.next(), k = e.getKey()
        if (Math.abs(k.x - px) <= 6 && Math.abs(k.z - pz) <= 6 && Math.abs(k.y - py) <= 8) { oldKey = k; overworld = e.getValue() }
      }
      if (overworld) {
        links.remove(oldKey)
        storage.createLink(overworld.pos(), overworld.dimension(), area.getRectangle().minCorner,
          abyssalResourceKey.create(abyssalRegistries.DIMENSION, abyssalRL.parse(abyssalDimensionId)))
        storage.setDirty()
      }
    }
  }
  // The buried portal goes (its frame stays in the rock).
  for (let dx = -4; dx <= 4; dx++) for (let dy = -4; dy <= 5; dy++) for (let dz = -4; dz <= 4; dz++) {
    let b = level.getBlock(px + dx, py + dy, pz + dz)
    if (String(b.id) === 'portals:custom_portal') b.set('minecraft:air')
  }
  return cy
}

const abyssalArrive = (player) => {
  const level = player.level
  const px = Math.floor(player.x), py = Math.floor(player.y), pz = Math.floor(player.z)
  if (abyssalPodNear(level, px, py, pz)) return
  const cy = abyssalRaisePod(level, player.server, px, py, pz)
  if (cy !== null) {
    player.server.runCommandSilent(`execute in ${abyssalDimensionId} run tp ${player.username} ${px + 0.5} ${cy - 1} ${pz - 1.5} 0 0`)
  } else {
    abyssalBuildPod(level, player.server, px, py, pz)
  }
  player.tell(Text.aqua('Lifepod deployed. The sea starts at the moon pool.').italic())
}

PlayerEvents.tick(event => {
  const player = event.player
  if (player.tickCount % 10 !== 0) return
  const data = player.persistentData
  if (abyssalIn(player)) {
    if (!data.getBoolean('strata_abyss_inside')) {
      data.putBoolean('strata_abyss_inside', true)
      abyssalArrive(player)
    }
    // No Conduit power down here: bases have to be engineered (Darin, Oct 26).
    if (player.tickCount % 20 === 0) player.server.runCommandSilent(`effect clear ${player.username} minecraft:conduit_power`)
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
