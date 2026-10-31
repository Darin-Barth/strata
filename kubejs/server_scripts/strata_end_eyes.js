// Seeker's Compasses (docs/end-eyes.md): a crafted compass for each place that always holds an End
// portal eye. It's a vanilla compass with custom data: right-click it and its needle points at the nearest
// such place (a lodestone target). It never shows coordinates, only a rough distance. What each compass
// finds: kubejs/data/strata/tags/worldgen/structure/seeker/<key>.json (tools/build_end_eyes.py).
// Explorer's Compass can't find these places (config/explorerscompass-common.toml): exploring is free,
// a Seeker's Compass is the paid shortcut. Boss lairs use Cataclysm's own eyes (Flame, Mech, Monstrous).
// KubeJS server scripts share one scope: every top-level name here starts with "strataSeek".
const strataSeekTagKey = Java.loadClass('net.minecraft.tags.TagKey')
const strataSeekRegistries = Java.loadClass('net.minecraft.core.registries.Registries')
const strataSeekId = Java.loadClass('net.minecraft.resources.ResourceLocation')
const strataSeekComponents = Java.loadClass('net.minecraft.core.component.DataComponents')
const strataSeekTracker = Java.loadClass('net.minecraft.world.item.component.LodestoneTracker')
const strataSeekGlobalPos = Java.loadClass('net.minecraft.core.GlobalPos')
const strataSeekOptional = Java.loadClass('java.util.Optional')
const strataSeekLevel = Java.loadClass('net.minecraft.world.level.Level')
const strataSeekRandomSpread = Java.loadClass('net.minecraft.world.level.levelgen.structure.placement.RandomSpreadStructurePlacement')
const strataSeekResult = Java.loadClass('net.minecraft.world.level.levelgen.structure.StructureCheckResult')

// The search works like vanilla /locate (rings of possible structure spots, nearest ring first) but runs a
// few milliseconds per tick: checking unexplored land means planning its terrain, which froze the server for
// seconds when done in one go. It gives up past strataSeekMaxBlocks.
const strataSeekMaxBlocks = 8000
const strataSeekBudgetMs = 10
const strataSeekJobs = []

// key: [place, eye it holds, name colour, corner item (x4), side item (x3)]; compass in the middle,
// Eye of Ender bottom centre
const strataSeekers = {
  old: ["Pharaoh's Tomb", 'Old Eye', 'gold', 'minecraft:gold_ingot', 'minecraft:sandstone'],
  evil: ['Jungle Temple', 'Evil Eye', 'green', 'minecraft:emerald', 'minecraft:mossy_cobblestone'],
  lost: ['Foundry', 'Lost Eye', 'red', 'minecraft:iron_ingot', 'minecraft:blast_furnace'],
  black: ['Pirate Ship', 'Black Eye', 'dark_gray', 'minecraft:gold_ingot', '#minecraft:boats'],
  cold: ['Frostbitten Temple', 'Cold Eye', 'aqua', 'minecraft:blue_ice', 'minecraft:snow_block'],
  guardian: ['Ocean Monument', 'Guardian Eye', 'dark_aqua', 'minecraft:lapis_block', 'minecraft:dried_kelp_block'],
}

function strataSeekSnbt(s) {
  return '"' + s.replace(/\\/g, '\\\\').replace(/"/g, '\\"') + '"'
}

function strataSeekStack(key) {
  const s = strataSeekers[key]
  const name = JSON.stringify({ text: "Seeker's Compass: " + s[0], color: s[2], italic: false })
  const lore = [
    JSON.stringify({ text: 'Finds the nearest ' + s[0] + ' (it holds the ' + s[1] + ')', color: 'gray', italic: false }),
    JSON.stringify({ text: 'Right-click to point the needle', color: 'dark_gray', italic: false }),
  ]
  return Item.of('minecraft:compass[custom_data={strata_seeker:"' + key + '"},item_name=' + strataSeekSnbt(name) +
    ',lore=[' + lore.map(strataSeekSnbt).join(',') + '],enchantment_glint_override=true]')
}

// A search job: every random-spread placement of the compass's structures, walked ring by ring around `from`
function strataSeekJob(level, key, from, done) {
  const tag = strataSeekTagKey.create(strataSeekRegistries.STRUCTURE, strataSeekId.parse('strata:seeker/' + key))
  const holders = level.registryAccess().registryOrThrow(strataSeekRegistries.STRUCTURE).getTag(tag)
  const state = level.getChunkSource().getGeneratorState()
  const entries = []
  if (holders.isPresent()) {
    let it = holders.get().iterator()
    while (it.hasNext()) {
      let holder = it.next()
      let placements = state.getPlacementsForStructure(holder).iterator()
      while (placements.hasNext()) {
        let p = placements.next()
        if (p instanceof strataSeekRandomSpread) entries.push({ placement: p, structure: holder.value(), rings: Math.floor(strataSeekMaxBlocks / (p.spacing() * 16)) })
      }
    }
  }
  return { level: level, state: state, seed: state.getLevelSeed(), cx: from.x >> 4, cz: from.z >> 4, entries: entries,
    ring: 0, cells: null, next: 0, best: null, bestDist: 0, done: done }
}

// The cells of one ring for every placement that still reaches that far, or null when none does
function strataSeekRing(job) {
  const cells = []
  job.entries.forEach(e => {
    if (job.ring > e.rings) return
    let r = job.ring
    let s = e.placement.spacing()
    for (let dx = -r; dx <= r; dx++) {
      for (let dz = -r; dz <= r; dz++) {
        if (Math.abs(dx) != r && Math.abs(dz) != r) continue
        cells.push({ e: e, x: job.cx + s * dx, z: job.cz + s * dz })
      }
    }
  })
  return cells.length ? cells : null
}

// Is there a structure start at this cell? Returns its locate position or null.
// CHUNK_LOAD_NEEDED means unexplored land where the structure fits. Vanilla /locate then generates the chunk's
// structure layer to be sure, which plans every structure of every mod there (up to 11 s in this pack).
// Instead this asks the placement whether the world generator would put this structure set there
// (frequency and exclusion zones: the same check chunk generation makes).
function strataSeekCell(job, cell) {
  const level = job.level
  const cp = cell.e.placement.getPotentialStructureChunk(job.seed, cell.x, cell.z)
  const res = level.structureManager().checkStructurePresence(cp, cell.e.structure, cell.e.placement, false)
  if (res == strataSeekResult.START_NOT_PRESENT) return null
  if (res == strataSeekResult.CHUNK_LOAD_NEEDED && !cell.e.placement.isStructureChunk(job.state, cp.x, cp.z)) return null
  return cell.e.placement.getLocatePos(cp)
}

// Could the next ring of any placement still hold something nearer than the best find?
// (A ring k cell lies at least (k - 1) spacings away: the structure can sit anywhere in its cell.)
function strataSeekMayBeCloser(job) {
  const best = Math.sqrt(job.bestDist)
  return job.entries.some(e => job.ring <= e.rings && Math.max(0, job.ring - 1) * e.placement.spacing() * 16 < best)
}

// Work on a job for up to the time budget. True when it's finished (job.best is the answer or null).
function strataSeekStep(job) {
  const stop = Date.now() + strataSeekBudgetMs
  while (Date.now() < stop) {
    if (!job.cells || job.next >= job.cells.length) {
      if (job.best && !strataSeekMayBeCloser(job)) return true
      job.cells = strataSeekRing(job)
      job.next = 0
      job.ring++
      if (!job.cells) return true // past the search distance
    }
    let cell = job.cells[job.next++]
    let pos = strataSeekCell(job, cell)
    if (pos) {
      let dx = pos.x - job.cx * 16
      let dz = pos.z - job.cz * 16
      let d = dx * dx + dz * dz
      if (!job.best || d < job.bestDist) { job.best = pos; job.bestDist = d }
    }
  }
  return false
}

// One spot can cost far more than the budget (planning a big structure in unexplored land takes 0.1-2 s),
// so after a slow step the search rests one tick per 50 ms it took, and the server catches up.
let strataSeekRest = 0

ServerEvents.tick(event => {
  if (!strataSeekJobs.length) return
  if (strataSeekRest > 0) { strataSeekRest--; return }
  const job = strataSeekJobs[0]
  const t0 = Date.now()
  let finished = true
  try {
    finished = strataSeekStep(job)
  } catch (e) {
    console.error('Seeker\'s Compass search failed: ' + e)
    job.best = null
  }
  strataSeekRest = Math.min(40, Math.floor((Date.now() - t0) / 50))
  if (!finished) return
  strataSeekJobs.shift()
  job.done(job.best)
})

ServerEvents.recipes(event => {
  Object.keys(strataSeekers).forEach(key => {
    let s = strataSeekers[key]
    event.shaped(strataSeekStack(key), ['ABA', 'BCB', 'ADA'],
      { A: s[3], B: s[4], C: 'minecraft:compass', D: 'minecraft:ender_eye' }).id('strata:seekers_compass/' + key)
  })
})

ItemEvents.rightClicked('minecraft:compass', event => strataSeekUse(event.player, event.item, event.level, event.server))

// Start a search for a Seeker's Compass (any other compass is left alone)
function strataSeekUse(player, stack, level, server) {
  const data = stack.get(strataSeekComponents.CUSTOM_DATA)
  if (!data) return
  const key = String(data.copyTag().getString('strata_seeker'))
  const seeker = strataSeekers[key]
  if (!seeker) return
  if (player.cooldowns.isOnCooldown(stack.item)) return
  player.cooldowns.addCooldown(stack.item, 60)
  if (String(level.dimension) != 'minecraft:overworld') {
    player.displayClientMessage(Text.red('The needle spins: a Seeker\'s Compass only works in the Overworld.'), true)
    return
  }
  const uuid = String(player.uuid)
  if (strataSeekJobs.some(j => j.uuid == uuid)) return
  player.displayClientMessage(Text.gray('The needle trembles, searching for the ' + seeker[0] + '...'), true)
  const job = strataSeekJob(level, key, player.blockPosition(), pos => strataSeekDone(server, player, key, pos))
  job.uuid = uuid
  strataSeekJobs.push(job)
}

// Point every compass of this kind the player carries at `pos` (they may have moved it while it searched)
function strataSeekDone(server, player, key, pos) {
  if (player.hasDisconnected()) return
  const seeker = strataSeekers[key]
  if (!pos) {
    player.displayClientMessage(Text.red('The needle spins: no ' + seeker[0] + ' within ' + strataSeekMaxBlocks + ' blocks. Travel further and try again.'), true)
    return
  }
  const inv = player.getInventory()
  for (let i = 0; i < inv.getContainerSize(); i++) {
    let s = inv.getItem(i)
    let data = s.get(strataSeekComponents.CUSTOM_DATA)
    if (!data || String(data.copyTag().getString('strata_seeker')) != key) continue
    s.set(strataSeekComponents.LODESTONE_TRACKER,
      new strataSeekTracker(strataSeekOptional.of(strataSeekGlobalPos.of(strataSeekLevel.OVERWORLD, pos)), false))
  }
  const dx = pos.x - player.x
  const dz = pos.z - player.z
  const dist = Math.max(100, Math.round(Math.sqrt(dx * dx + dz * dz) / 100) * 100)
  player.displayClientMessage(Text.gold('The needle swings toward the nearest ' + seeker[0] + ', about ' + dist + ' blocks away.'), true)
  server.runCommandSilent('playsound minecraft:item.lodestone_compass.lock player ' + player.getGameProfile().getName())
}
