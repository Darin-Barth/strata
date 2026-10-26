// The Hollow's psychological events (Darin, Oct 25). Only for players inside strata:hollow, and
// none of them can hurt anyone. Sounds are played to the one player they target.
//   footsteps  steps come up behind you and stop when you turn around
//   whisper    your own name, whispered
//   phantom    a creeper hiss, a door, a heartbeat... with nothing there
//   torch      a nearby torch goes out, then relights a few seconds later
//   watcher    a dark figure at the edge of your view that vanishes when you look at it
//   fog        a few seconds of Darkness, as if the fog thickened
// Compasses and clocks spin by themselves: the Hollow's dimension type isn't "natural".
// Rough pacing: after a 30 s quiet start, one event every ~1.5-3 minutes per player.
// KubeJS server scripts share one scope: every top-level name here starts with "hollowDread".
const hollowDreadState = {}
const hollowDreadWatchers = {}
const hollowDreadQuietStartMs = 30 * 1000
const hollowDreadCooldownMs = 60 * 1000
const hollowDreadTorches = ['minecraft:torch', 'minecraft:wall_torch', 'minecraft:soul_torch', 'minecraft:soul_wall_torch']
const hollowDreadPhantoms = [
  ['minecraft:entity.creeper.primed', 0.8, 1.0],
  ['minecraft:block.wooden_door.open', 0.7, 0.9],
  ['minecraft:block.wooden_door.close', 0.7, 0.8],
  ['minecraft:block.chest.open', 0.6, 0.8],
  ['minecraft:ambient.cave', 1.0, 1.0],
  ['minecraft:entity.zombie.ambient', 0.6, 0.7],
  ['minecraft:entity.enderman.stare', 0.35, 0.8],
  ['minecraft:entity.warden.heartbeat', 1.0, 1.0],
]
const hollowDreadWhispers = [n => `...${n}...`, n => `${n}...`, n => `...behind you, ${n}...`, n => `...${n}... come here...`,
  n => `...we see you, ${n}...`]

const hollowDreadDim = entity => { const d = entity.level.dimension; return String(d && d.location ? d.location() : d) }
const hollowDreadRand = (a, b) => a + Math.random() * (b - a)
const hollowDreadPick = list => list[Math.floor(Math.random() * list.length)]
const hollowDreadAngle = (a, b) => Math.abs(((a - b) % 360 + 540) % 360 - 180)
const hollowDreadSound = (player, sound, x, y, z, volume, pitch) =>
  player.server.runCommandSilent(`execute as ${player.username} run playsound ${sound} hostile @s ${x.toFixed(2)} ${y.toFixed(2)} ${z.toFixed(2)} ${volume} ${pitch}`)
// Unit vector the player faces (vanilla's formula from yaw/pitch).
const hollowDreadLook = player => {
  const yaw = player.yaw * Math.PI / 180, pitch = player.pitch * Math.PI / 180
  return [-Math.sin(yaw) * Math.cos(pitch), -Math.sin(pitch), Math.cos(yaw) * Math.cos(pitch)]
}
const hollowDreadOk = player => player.isAlive() && hollowDreadDim(player) === 'strata:hollow'

const hollowDreadEvents = {
  footsteps: player => {
    const yaw0 = player.yaw
    const r = yaw0 * Math.PI / 180
    const bx = Math.sin(r), bz = -Math.cos(r)  // behind the player
    const steps = 4 + Math.floor(Math.random() * 3)
    const run = { stopped: false }
    for (let i = 0; i < steps; i++) {
      player.server.scheduleInTicks(9 * i + 1, () => {
        if (run.stopped || !hollowDreadOk(player)) return
        if (hollowDreadAngle(player.yaw, yaw0) > 90) { run.stopped = true; return }
        const dist = 7 - i
        hollowDreadSound(player, 'minecraft:block.grass.step', player.x + bx * dist, player.y, player.z + bz * dist, 0.7, 0.8)
      })
    }
  },
  whisper: player => {
    player.tell(Text.darkGray(hollowDreadPick(hollowDreadWhispers)(player.username)).italic())
    const a = Math.random() * Math.PI * 2
    hollowDreadSound(player, 'minecraft:ambient.soul_sand_valley.mood', player.x + Math.cos(a) * 3, player.y + 1, player.z + Math.sin(a) * 3, 0.6, 1.4)
  },
  phantom: player => {
    const s = hollowDreadPick(hollowDreadPhantoms)
    const a = Math.random() * Math.PI * 2, d = hollowDreadRand(5, 9)
    hollowDreadSound(player, s[0], player.x + Math.cos(a) * d, player.y, player.z + Math.sin(a) * d, s[1], s[2])
  },
  torch: player => {
    const level = player.level
    const px = Math.floor(player.x), py = Math.floor(player.y), pz = Math.floor(player.z)
    const found = []
    for (let dx = -7; dx <= 7; dx++) for (let dy = -3; dy <= 4; dy++) for (let dz = -7; dz <= 7; dz++) {
      const b = level.getBlock(px + dx, py + dy, pz + dz)
      if (hollowDreadTorches.indexOf(String(b.id)) >= 0) found.push(b)
    }
    if (found.length === 0) return false
    const b = hollowDreadPick(found)
    const id = String(b.id), props = b.properties, x = b.x, y = b.y, z = b.z
    b.set('minecraft:air')
    hollowDreadSound(player, 'minecraft:block.fire.extinguish', x + 0.5, y + 0.5, z + 0.5, 0.4, 1.6)
    player.server.scheduleInTicks(40 + Math.floor(Math.random() * 40), () => {
      const now = level.getBlock(x, y, z)
      if (String(now.id) === 'minecraft:air') now.set(id, props)
    })
    return true
  },
  watcher: player => {
    if (hollowDreadWatchers[player.username]) return false
    const level = player.level
    const side = Math.random() < 0.5 ? -1 : 1
    const yaw = (player.yaw + side * hollowDreadRand(55, 75)) * Math.PI / 180
    const d = hollowDreadRand(18, 26)
    const x = Math.floor(player.x - Math.sin(yaw) * d), z = Math.floor(player.z + Math.cos(yaw) * d)
    for (let y = Math.floor(player.y) + 8; y > Math.floor(player.y) - 12; y--) {
      const ground = level.getBlock(x, y - 1, z), feet = level.getBlock(x, y, z), head = level.getBlock(x, y + 2, z)
      if (ground.id !== 'minecraft:air' && feet.id === 'minecraft:air' && head.id === 'minecraft:air') {
        const e = level.createEntity('minecraft:enderman')
        e.setPosition(x + 0.5, y, z + 0.5)
        e.setNoAi(true)
        e.setSilent(true)
        e.setInvulnerable(true)
        e.addTag('hollow_watcher')
        e.setYRot((Math.atan2(player.z - z, player.x - x) * 180 / Math.PI) - 90)
        e.spawn()
        hollowDreadWatchers[player.username] = { entity: e, until: Date.now() + 15000 }
        return true
      }
    }
    return false
  },
  fog: player => {
    player.server.runCommandSilent(`effect give ${player.username} minecraft:darkness 5 0 true`)
    hollowDreadSound(player, 'minecraft:entity.warden.heartbeat', player.x, player.y, player.z, 0.6, 0.9)
  },
}
const hollowDreadWeights = [['footsteps', 3], ['whisper', 2], ['phantom', 3], ['torch', 2], ['watcher', 2], ['fog', 2]]

PlayerEvents.tick(event => {
  const player = event.player
  // The watcher vanishes when looked at (checked often), or quietly after 15 s.
  const w = hollowDreadWatchers[player.username]
  if (w && player.age % 4 === 0) {
    const e = w.entity
    if (!e.isAlive() || !hollowDreadOk(player) || Date.now() > w.until) {
      if (e.isAlive()) e.discard()
      delete hollowDreadWatchers[player.username]
    } else {
      const look = hollowDreadLook(player)
      const vx = e.x - player.x, vy = e.y + 2.2 - (player.y + 1.62), vz = e.z - player.z
      const len = Math.sqrt(vx * vx + vy * vy + vz * vz)
      const cos = (vx * look[0] + vy * look[1] + vz * look[2]) / len
      if (cos > Math.cos(20 * Math.PI / 180)) {
        player.server.runCommandSilent(`execute in strata:hollow run particle minecraft:large_smoke ${e.x} ${e.y + 1.5} ${e.z} 0.3 1 0.3 0.01 30 force ${player.username}`)
        hollowDreadSound(player, 'minecraft:entity.enderman.teleport', e.x, e.y + 1, e.z, 0.3, 0.5)
        e.discard()
        delete hollowDreadWatchers[player.username]
      }
    }
  }

  if (player.age % 40 !== 0) return
  if (!hollowDreadOk(player) || player.isCreative() || player.isSpectator()) return
  const arrived = player.persistentData.getLong('strata_hollow_arrived')
  if (arrived > 0 && Date.now() - arrived < hollowDreadQuietStartMs) return
  const state = hollowDreadState[player.username] || (hollowDreadState[player.username] = { next: 0 })
  if (Date.now() < state.next || Math.random() > 1 / 30) return
  let roll = Math.random() * hollowDreadWeights.reduce((s, x) => s + x[1], 0)
  let name = hollowDreadWeights[0][0]
  for (let i = 0; i < hollowDreadWeights.length; i++) {
    roll -= hollowDreadWeights[i][1]
    if (roll < 0) { name = hollowDreadWeights[i][0]; break }
  }
  const fired = hollowDreadEvents[name](player)
  if (fired !== false) state.next = Date.now() + hollowDreadCooldownMs + Math.random() * 60000
})

// Leftover watchers from a restart.
ServerEvents.loaded(event => {
  event.server.runCommandSilent('execute in strata:hollow run kill @e[tag=hollow_watcher]')
})
