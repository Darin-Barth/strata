// Apotheosis elites and invaders ("bosses") stay rare near spawn and ramp up with distance
// (design doc: "elite mobs rare near spawn, more common far out"). Apotheosis has no distance
// setting, so this thins them out as they join the Overworld: 10% of them are kept at world
// spawn, rising to all of them by 2,000 blocks out. Other dimensions are left alone.
// KubeJS server scripts share one scope: every top-level name here starts with "strataElite".
const strataEliteFullAt = 2000
const strataEliteKeepAtSpawn = 0.1

EntityEvents.spawned(event => {
  const entity = event.entity
  if (!entity.isLiving() || entity.isPlayer()) return
  const data = entity.persistentData
  if (!data.contains('apoth.boss') && !data.contains('apoth.miniboss')) return
  // Joining again after a chunk reload doesn't roll again.
  if (data.getBoolean('strata_elite_rolled')) return
  data.putBoolean('strata_elite_rolled', true)
  const level = entity.level
  if (String(level.dimension.location ? level.dimension.location() : level.dimension) !== 'minecraft:overworld') return
  const spawn = level.getSharedSpawnPos()
  const dist = Math.hypot(entity.x - spawn.x, entity.z - spawn.z)
  const keep = strataEliteKeepAtSpawn + (1 - strataEliteKeepAtSpawn) * Math.min(1, dist / strataEliteFullAt)
  if (Math.random() >= keep) event.cancel()
})
