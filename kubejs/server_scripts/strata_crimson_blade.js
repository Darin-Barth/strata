// Forsaken Relics 1.0.1 crash workaround (Darin, Nov 1). Crimson Blade's Bleed curse hurts every cursed mob once a
// second while it walks its list of cursed mobs. A mob that dies from it changes that list (its death handler removes
// it, and Hemorrhage curses the mobs around it), and the next step of the walk crashes the server
// (ConcurrentModificationException in CrimsonBladeItem.tickCurses; 5 crashes Oct 30 - Nov 1). Bleed damage is
// indirect magic with the player as both attacker and direct source, on game ticks divisible by 20: this script cancels
// it and deals the same damage one tick later, outside that loop. Re-check after a Forsaken Relics update.
// KubeJS server scripts share one scope: every top-level name here starts with "crimsonBlade".
let crimsonBladeReplaying = false

EntityEvents.beforeHurt(event => {
  if (crimsonBladeReplaying) return
  const source = event.source
  if (String(source.getMsgId()) !== 'indirectMagic') return
  const attacker = source.actual
  if (!attacker || !attacker.isPlayer() || source.immediate !== attacker) return
  const target = event.entity
  if (Number(target.level.getGameTime()) % 20 !== 0) return
  const amount = event.damage
  event.cancel()
  event.server.scheduleInTicks(1, () => {
    if (!target.isAlive()) return
    crimsonBladeReplaying = true
    try {
      target.invulnerableTime = 0
      target.attack(source, amount)
    } finally {
      crimsonBladeReplaying = false
    }
  })
})
