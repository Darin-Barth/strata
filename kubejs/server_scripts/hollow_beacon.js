// The Pale Beacon, the Hollow's safe zone, and the Lost Signal story pages
// (docs/hollow-progression.md sections 3-4). Blocks and items: startup_scripts/hollow_beacon.js.
//   Placed only in the Hollow, it starts dark. Each Hollow Ember lights it for one in-game day
//   (24,000 ticks, 20 minutes), up to 7 days stored; unfed, it goes dark again.
//   While lit, within 24 blocks (48 with the Ravenous' echolocation organ): sanity comes back, no
//   dread events (hollow_dread.js), no horror spawns (here and hollow_ravenous.js), beds work
//   (hollow_rules.js), and the Ravenous can't eat it (#minecraft:screech_blocks). Upgraded, it also
//   warns everyone inside when a horror mob comes within 64 blocks.
// Beacons are stored in the server's persistent data, keyed "x,y,z".
// KubeJS server scripts share one scope: every top-level name here starts with "hollowBeacon".
const hollowBeaconLit = 'strata:pale_beacon'
const hollowBeaconDark = 'strata:pale_beacon_dormant'
const hollowBeaconEmber = 'strata:hollow_ember'
const hollowBeaconOrgan = 'the_ravenous:the_ravenous_echolocation_organ'
const hollowBeaconDimension = 'strata:hollow'
const hollowBeaconDay = 24000
const hollowBeaconMaxDays = 7
const hollowBeaconRadius = 24
const hollowBeaconUpgradedRadius = 48
const hollowBeaconWarnRadius = 64
const hollowBeaconWarnCooldownMs = 30 * 1000
const hollowBeaconSanityPerSecond = 0.01
const hollowBeaconHorror = ['cave_dweller', 'weeping_angels', 'the_ravenous',
  'grim_and_bleak', 'graveyard', 'mutantmonsters', 'sanity_renewed']
const hollowBeaconBlockPos = Java.loadClass('net.minecraft.core.BlockPos')
const hollowBeaconAABB = Java.loadClass('net.minecraft.world.phys.AABB')
const hollowBeaconParams = Java.loadClass('net.minecraft.world.level.storage.loot.parameters.LootContextParams')
const hollowBeaconTag = Java.loadClass('net.minecraft.nbt.CompoundTag')

// In memory: [{ key, x, y, z, fuel (game time it runs out), up (upgraded) }], loaded from persistent data.
let hollowBeaconList = null
const hollowBeaconWarned = {}

const hollowBeaconDim = entity => { const d = entity.level.dimension; return String(d && d.location ? d.location() : d) }
const hollowBeaconLevel = server => server.getLevel(hollowBeaconDimension)
const hollowBeaconNow = server => { const l = hollowBeaconLevel(server); return l ? Number(l.levelData.getGameTime()) : 0 }

const hollowBeaconLoad = server => {
  if (hollowBeaconList) return hollowBeaconList
  hollowBeaconList = []
  const all = server.persistentData.getCompound('strata_pale_beacons')
  all.getAllKeys().forEach(key => {
    let t = all.getCompound(key)
    let p = String(key).split(',').map(Number)
    hollowBeaconList.push({ key: String(key), x: p[0], y: p[1], z: p[2], fuel: Number(t.getLong('fuel')), up: t.getBoolean('up') })
  })
  return hollowBeaconList
}

const hollowBeaconSave = server => {
  const all = new hollowBeaconTag()
  hollowBeaconLoad(server).forEach(b => {
    let t = new hollowBeaconTag()
    t.putLong('fuel', b.fuel)
    t.putBoolean('up', b.up)
    all.put(b.key, t)
  })
  server.persistentData.put('strata_pale_beacons', all)
}

const hollowBeaconAt = (server, x, y, z) => {
  const key = `${x},${y},${z}`
  const list = hollowBeaconLoad(server)
  for (let i = 0; i < list.length; i++) if (list[i].key === key) return list[i]
  return null
}

const hollowBeaconRadiusOf = b => b.up ? hollowBeaconUpgradedRadius : hollowBeaconRadius

// True if the entity is in the Hollow within range of a lit beacon. Also used by hollow_dread.js,
// hollow_ravenous.js and hollow_rules.js.
const hollowBeaconNear = entity => {
  if (hollowBeaconDim(entity) !== hollowBeaconDimension) return false
  const server = entity.server
  const now = hollowBeaconNow(server)
  return hollowBeaconLoad(server).some(b => {
    if (b.fuel <= now) return false
    let r = hollowBeaconRadiusOf(b)
    let dx = entity.x - (b.x + 0.5), dy = entity.y - (b.y + 0.5), dz = entity.z - (b.z + 0.5)
    return dx * dx + dy * dy + dz * dz <= r * r
  })
}

// Same check for a block position (spawn attempts).
const hollowBeaconCovers = (server, x, y, z) => {
  const now = hollowBeaconNow(server)
  return hollowBeaconLoad(server).some(b => {
    if (b.fuel <= now) return false
    let r = hollowBeaconRadiusOf(b)
    let dx = x - b.x, dy = y - b.y, dz = z - b.z
    return dx * dx + dy * dy + dz * dz <= r * r
  })
}

const hollowBeaconDaysLeft = (b, now) => Math.max(0, (b.fuel - now) / hollowBeaconDay)

const hollowBeaconTell = (player, text) => player.displayClientMessage(Text.of(text).color(0xC9D6E3).italic(), true)

ServerEvents.tags('item', event => {
  event.add('strata:bone_staffs', ['graveyard:black_bone_staff', 'graveyard:cyan_bone_staff', 'graveyard:purple_bone_staff',
    'graveyard:red_bone_staff', 'graveyard:white_bone_staff'])
})

ServerEvents.recipes(event => {
  event.shaped('strata:pale_beacon', [
    'ECE',
    'SLA',
    'EEE',
  ], {
    E: hollowBeaconEmber,
    C: 'grim_and_bleak:holy_cross',
    S: '#strata:bone_staffs',
    L: 'strata:pale_lantern',
    A: 'grim_and_bleak:templar_artifact',
  }).id('strata:pale_beacon')
})

// Placed: only in the Hollow, and it starts dark.
BlockEvents.placed(hollowBeaconLit, event => {
  const player = event.player
  if (hollowBeaconDim(event.block) !== hollowBeaconDimension) {
    if (player) hollowBeaconTell(player, 'The beacon stays cold. It only answers the dark of the Hollow.')
    event.cancel()
    return
  }
  const server = event.server
  const pos = event.block.pos
  const key = `${pos.x},${pos.y},${pos.z}`
  hollowBeaconLoad(server).push({ key: key, x: pos.x, y: pos.y, z: pos.z, fuel: 0, up: false })
  hollowBeaconSave(server)
  server.scheduleInTicks(1, () => {
    let level = hollowBeaconLevel(server)
    if (level && String(level.getBlock(pos).id) === hollowBeaconLit) level.getBlock(pos).set(hollowBeaconDark)
  })
  if (player) hollowBeaconTell(player, 'The beacon is cold. Feed it a Hollow Ember.')
})

// Feed it an Ember, upgrade it with the organ, or check how long it has left.
const hollowBeaconUse = event => {
  const player = event.player
  if (!player || String(event.hand) !== 'MAIN_HAND') return
  const server = event.server
  const pos = event.block.pos
  let b = hollowBeaconAt(server, pos.x, pos.y, pos.z)
  if (!b) {  // a beacon from before tracking, or data lost: adopt it
    b = { key: `${pos.x},${pos.y},${pos.z}`, x: pos.x, y: pos.y, z: pos.z, fuel: 0, up: false }
    hollowBeaconLoad(server).push(b)
  }
  const now = hollowBeaconNow(server)
  const held = player.mainHandItem
  const id = String(held.id)
  if (id === hollowBeaconEmber) {
    let start = Math.max(b.fuel, now)
    if (start + hollowBeaconDay > now + hollowBeaconMaxDays * hollowBeaconDay) {
      hollowBeaconTell(player, `The beacon is full: ${hollowBeaconMaxDays} days of light stored.`)
    } else {
      b.fuel = start + hollowBeaconDay
      if (!player.isCreative()) held.shrink(1)
      if (String(event.block.id) === hollowBeaconDark) event.block.set(hollowBeaconLit)
      server.runCommandSilent(`execute in ${hollowBeaconDimension} run playsound minecraft:block.beacon.activate block @a ${pos.x + 0.5} ${pos.y + 0.5} ${pos.z + 0.5} 1 0.7`)
      hollowBeaconTell(player, `The beacon burns pale. Light left: ${hollowBeaconDaysLeft(b, now).toFixed(1)} days.`)
    }
  } else if (id === hollowBeaconOrgan) {
    if (b.up) {
      hollowBeaconTell(player, 'The beacon already listens.')
    } else {
      b.up = true
      if (!player.isCreative()) held.shrink(1)
      server.runCommandSilent(`execute in ${hollowBeaconDimension} run playsound minecraft:entity.warden.sonic_charge block @a ${pos.x + 0.5} ${pos.y + 0.5} ${pos.z + 0.5} 1 0.8`)
      hollowBeaconTell(player, `The beacon listens now: its light reaches ${hollowBeaconUpgradedRadius} blocks, and it warns you of what comes.`)
    }
  } else if (held.isEmpty()) {
    let left = hollowBeaconDaysLeft(b, now)
    hollowBeaconTell(player, left > 0 ? `Light left: ${left.toFixed(1)} days.` : 'The beacon is cold. Feed it a Hollow Ember.')
  } else {
    return
  }
  hollowBeaconSave(server)
  event.cancel()
}
BlockEvents.rightClicked(hollowBeaconLit, hollowBeaconUse)
BlockEvents.rightClicked(hollowBeaconDark, hollowBeaconUse)

// Broken: forget it. The dark block has no drops of its own, so it drops the beacon item here.
const hollowBeaconBroken = event => {
  const server = event.server
  const pos = event.block.pos
  const key = `${pos.x},${pos.y},${pos.z}`
  const list = hollowBeaconLoad(server)
  for (let i = list.length - 1; i >= 0; i--) {
    if (list[i].key === key) { list.splice(i, 1); hollowBeaconSave(server) }
  }
  if (String(event.block.id) === hollowBeaconDark && !(event.player && event.player.isCreative())) {
    event.block.popItem('strata:pale_beacon')
  }
}
BlockEvents.broken(hollowBeaconLit, hollowBeaconBroken)
BlockEvents.broken(hollowBeaconDark, hollowBeaconBroken)

// Once a second: burn out, sanity, warnings.
let hollowBeaconTicks = 0
ServerEvents.tick(event => {
  if (++hollowBeaconTicks % 20 !== 0) return
  const server = event.server
  const level = hollowBeaconLevel(server)
  if (!level) return
  const list = hollowBeaconLoad(server)
  if (list.length === 0) return
  const now = hollowBeaconNow(server)
  const players = []
  level.players.forEach(p => players.push(p))
  let changed = false
  for (let i = list.length - 1; i >= 0; i--) {
    let b = list[i]
    let pos = new hollowBeaconBlockPos(b.x, b.y, b.z)
    if (!level.isLoaded(pos)) continue
    let id = String(level.getBlock(pos).id)
    if (id !== hollowBeaconLit && id !== hollowBeaconDark) { list.splice(i, 1); changed = true; continue }
    if (id === hollowBeaconLit && b.fuel <= now) {
      level.getBlock(pos).set(hollowBeaconDark)
      server.runCommandSilent(`execute in ${hollowBeaconDimension} run playsound minecraft:block.beacon.deactivate block @a ${b.x + 0.5} ${b.y + 0.5} ${b.z + 0.5} 1 0.7`)
      players.forEach(p => {
        if (p.distanceToSqr(b.x + 0.5, b.y + 0.5, b.z + 0.5) < 64 * 64) hollowBeaconTell(p, 'The Pale Beacon gutters out. Feed it a Hollow Ember.')
      })
      continue
    }
    if (id === hollowBeaconDark && b.fuel > now) level.getBlock(pos).set(hollowBeaconLit)
    if (b.fuel <= now) continue
    let r = hollowBeaconRadiusOf(b)
    let inside = players.filter(p => p.distanceToSqr(b.x + 0.5, b.y + 0.5, b.z + 0.5) <= r * r)
    // Sanity: Renewed stores insanity from 0 (sane) to 1; bring it down.
    inside.forEach(p => {
      try {
        let s = p['sanity_renewed$getSanity']()
        if (s.getSanity() > 0) s.setSanity(Math.max(0, s.getSanity() - hollowBeaconSanityPerSecond))
      } catch (e) {}
    })
    if (b.up && inside.length > 0 && !(Date.now() < (hollowBeaconWarned[b.key] || 0))) {
      let box = new hollowBeaconAABB(b.x - hollowBeaconWarnRadius, b.y - hollowBeaconWarnRadius, b.z - hollowBeaconWarnRadius,
        b.x + hollowBeaconWarnRadius, b.y + hollowBeaconWarnRadius, b.z + hollowBeaconWarnRadius)
      let found = null
      let near = level.getEntities(null, box)
      for (let j = 0; j < near.size() && !found; j++) {
        let e = near.get(j)
        if (e.isLiving() && e.isAlive() && hollowBeaconHorror.indexOf(String(e.type).split(':')[0]) >= 0) found = e
      }
      if (found) {
        hollowBeaconWarned[b.key] = Date.now() + hollowBeaconWarnCooldownMs
        let ang = Math.atan2(found.x - b.x, -(found.z - b.z)) * 180 / Math.PI
        let dirs = ['north', 'north-east', 'east', 'south-east', 'south', 'south-west', 'west', 'north-west']
        let dir = dirs[Math.round(((ang + 360) % 360) / 45) % 8]
        inside.forEach(p => {
          hollowBeaconTell(p, `The beacon flickers: something is coming from the ${dir}.`)
          server.runCommandSilent(`execute as ${p.username} run playsound minecraft:block.bell.resonate block @s ${p.x} ${p.y} ${p.z} 0.6 0.6`)
        })
      }
    }
  }
  if (changed) hollowBeaconSave(server)
})

// No horror mob spawns inside a lit beacon's light.
EntityEvents.checkSpawn(event => {
  const entity = event.entity
  if (hollowBeaconDim(entity) !== hollowBeaconDimension) return
  if (hollowBeaconHorror.indexOf(String(entity.type).split(':')[0]) < 0) return
  if (hollowBeaconCovers(event.server, Math.floor(entity.x), Math.floor(entity.y), Math.floor(entity.z))) event.cancel()
})

// Lost Signal: the Pale Survey's log pages turn up in chests opened in the Hollow, in order, about
// one chest in three and one page per chest. Lootr fills chests per player, so each player finds a
// full set of their own.
LootJS.modifiers(event => {
  event.addTableModifier(LootType.CHEST).matchDimension('strata:hollow').customAction((ctx, loot) => {
    let player = ctx.getParamOrNull(hollowBeaconParams.THIS_ENTITY)
    if (!player || !player.isPlayer()) return
    // Only real containers: some mods roll "chest" loot at the player's feet every few seconds
    // (Incendium does), which would use up pages nobody receives.
    let origin = ctx.getParamOrNull(hollowBeaconParams.ORIGIN)
    if (!origin) return
    let be = player.level.getBlockEntity(hollowBeaconBlockPos.containing(origin.x(), origin.y(), origin.z()))
    if (!be || typeof be.getContainerSize !== 'function') return
    let data = player.persistentData
    let found = data.getInt('strata_survey_pages')
    if (found >= 6 || Math.random() >= 1 / 3) return
    loot.addItem(Item.of(`strata:pale_survey_page_${found + 1}`))
    data.putInt('strata_survey_pages', found + 1)
  })
})
