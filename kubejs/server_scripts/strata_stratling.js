// Legendary Monsters Cloudy Temple crash fix (Nov 6). A Stratling fills its trades from the level's random generator
// whenever it loads; inside a temple being generated that happens on a world-generation thread, and sharing the level's
// random with the server thread crashed the server ("Accessing LegacyRandomSource from multiple threads").
// tools/build_cloudy_temple.py replaces the Stratlings in the temple pieces with markers tagged "strata_stratling";
// when a marker joins the world (server thread), this puts a Stratling in its place, facing the same way.
// KubeJS server scripts share one scope: every top-level name here starts with "stratling".
let stratlingTag = 'strata_stratling'

EntityEvents.spawned('minecraft:marker', event => {
  let m = event.entity
  if (!m.tags.contains(stratlingTag)) return
  let level = m.level
  event.server.scheduleInTicks(1, () => {
    if (m.isRemoved()) return
    let s = level.createEntity('legendary_monsters:stratling')
    let yaw = m.yRot
    s.setPos(m.x, m.y, m.z)
    s.setYaw(yaw)
    s.setYHeadRot(yaw)
    s.setBodyYaw(yaw)
    s.setPersistenceRequired()
    s.spawn()
    m.discard()
  })
})
