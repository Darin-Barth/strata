// Generate ahead of explorers while the server is empty (Darin, Nov 15). Generating new land is the one thing that
// still stalls the server while people explore: finishing each new chunk runs on the main thread. This script notes
// where players go beyond the pregenerated Overworld and, while nobody is online, has Chunky generate those areas
// (and a margin around them), so the next trip out there loads finished land. It pauses the moment someone joins.
// - Every 30 s each Overworld player further than pregenAheadEdge blocks from the world spawn marks the 512-block
//   cell they stand in. Each marked cell becomes one Chunky task: a square of radius pregenAheadRadius around the
//   cell's centre (already generated chunks are skipped quickly).
// - Tasks only start after the server has been empty for a minute. A task Chunky was running for someone else
//   (started by hand) is never touched: this script only pauses and continues tasks it started itself.
// - State (queue, current task, finished cells) is in the server's KubeJS persistent data.
// Chunky is a server-only mod: without it (single player) the script does nothing.
// Ops: /pregenahead shows the state; /pregenahead clear empties the queue and cancels the script's own task.
// KubeJS server scripts share one scope: every top-level name here starts with "pregenAhead".
const pregenAheadWorld = 'minecraft:overworld'
const pregenAheadEdge = 4500
const pregenAheadRadius = 768
const pregenAheadMaxQueue = 64
const pregenAheadKey = 'strata_pregen_ahead'
let pregenAheadEmptyTicks = 0

function pregenAheadApi() {
  if (!Platform.isLoaded('chunky')) return null
  return Java.loadClass('org.popcraft.chunky.ChunkyProvider').get().getApi()
}

function pregenAheadState(server) {
  let data = server.persistentData.getCompound(pregenAheadKey)
  return {
    queue: String(data.getString('queue')).split(';').filter(s => s.length > 0),
    done: String(data.getString('done')).split(';').filter(s => s.length > 0),
    current: String(data.getString('current'))
  }
}

function pregenAheadSave(server, state) {
  let data = server.persistentData.getCompound(pregenAheadKey)
  data.putString('queue', state.queue.join(';'))
  data.putString('done', state.done.slice(-500).join(';'))
  data.putString('current', state.current)
  server.persistentData.put(pregenAheadKey, data)
}

function pregenAheadMark(server, state) {
  let spawn = server.overworld().getSharedSpawnPos()
  let changed = false
  server.players.forEach(player => {
    if (String(player.level.dimension) !== pregenAheadWorld) return
    let dx = player.x - spawn.getX()
    let dz = player.z - spawn.getZ()
    if (dx * dx + dz * dz < pregenAheadEdge * pregenAheadEdge) return
    let cell = (Math.floor(player.x / 512) * 512 + 256) + ',' + (Math.floor(player.z / 512) * 512 + 256)
    if (state.current === cell || state.queue.indexOf(cell) >= 0 || state.done.indexOf(cell) >= 0) return
    if (state.queue.length >= pregenAheadMaxQueue) return
    state.queue.push(cell)
    changed = true
  })
  return changed
}

function pregenAheadStep(server) {
  let api = pregenAheadApi()
  if (api == null) return
  let state = pregenAheadState(server)
  let online = server.players.size()
  let changed = online > 0 && pregenAheadMark(server, state)
  let running = api.isRunning(pregenAheadWorld)
  if (online > 0) {
    pregenAheadEmptyTicks = 0
    if (running && state.current.length > 0) {
      api.pauseTask(pregenAheadWorld)
      console.info('[pregen ahead] paused ' + state.current + ' (a player is online)')
    }
  } else {
    pregenAheadEmptyTicks += 200
    if (!running && pregenAheadEmptyTicks >= 1200) {
      if (state.current.length > 0) {
        if (api.continueTask(pregenAheadWorld)) {
          console.info('[pregen ahead] continuing ' + state.current)
        } else {
          console.info('[pregen ahead] finished ' + state.current + ', ' + state.queue.length + ' left')
          state.done.push(state.current)
          state.current = ''
          changed = true
        }
      }
      if (state.current.length === 0 && state.queue.length > 0) {
        let cell = state.queue.shift()
        let parts = cell.split(',')
        if (api.startTask(pregenAheadWorld, 'square', Number(parts[0]), Number(parts[1]), pregenAheadRadius, pregenAheadRadius, 'concentric')) {
          state.current = cell
          console.info('[pregen ahead] started ' + cell + ' (radius ' + pregenAheadRadius + '), ' + state.queue.length + ' left')
        } else {
          state.queue.unshift(cell)
        }
        changed = true
      }
    }
  }
  if (changed) pregenAheadSave(server, state)
}

ServerEvents.tick(event => {
  if (event.server.tickCount % 200 !== 0) return
  pregenAheadStep(event.server)
})

ServerEvents.commandRegistry(event => {
  let C = event.commands
  event.register(C.literal('pregenahead').requires(s => s.hasPermission(2))
    .executes(ctx => {
      let server = ctx.source.server
      let state = pregenAheadState(server)
      let api = pregenAheadApi()
      ctx.source.sendSystemMessage(Text.of('Pregen ahead: ' + (api == null ? 'Chunky not installed' :
        'current ' + (state.current || 'none') + (api.isRunning(pregenAheadWorld) ? ' (running)' : '') +
        ', queued ' + state.queue.length + (state.queue.length > 0 ? ' [' + state.queue.slice(0, 6).join(' | ') + ']' : '') +
        ', finished ' + state.done.length)))
      return 1
    })
    .then(C.literal('clear').executes(ctx => {
      let server = ctx.source.server
      let state = pregenAheadState(server)
      let api = pregenAheadApi()
      if (api != null && state.current.length > 0) api.cancelTask(pregenAheadWorld)
      state.queue = []
      state.current = ''
      pregenAheadSave(server, state)
      ctx.source.sendSystemMessage(Text.of('Pregen ahead: queue cleared'))
      return 1
    })))
})
