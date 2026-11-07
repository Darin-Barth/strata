// Forsaken Relics 1.0.1 crash workaround (Darin, Nov 1). Crimson Blade's Bleed curse hurts every cursed mob once a
// second while it walks its list of cursed mobs. A mob that dies from it changes that list (its death handler removes
// it, and Hemorrhage curses the mobs around it), and the next step of the walk crashes the server
// (ConcurrentModificationException in CrimsonBladeItem.tickCurses; 5 crashes Oct 30 - Nov 1). Bleed damage is
// indirect magic from the blade's owner, or plain magic with no attacker when the owner isn't in that dimension, on game
// ticks divisible by 20. Only a killing hit changes the list, so this script cancels such a hit when it would kill and
// deals it one tick later, outside that loop. Other magic damage that would kill on those ticks lands one tick late too.
// Re-check after a Forsaken Relics update.
// Tested Nov 7 (six bleeding husks set to 1 health): crash reproduced without this; with it no crash, and they die.
// KubeJS names: the damage type ID is source.getType() (getMsgId() is hidden; the first version of this script failed
// on it for every hit), the game clock is level.levelData.gameTime (getGameTime() is hidden), and event.cancel() ends
// the handler, so the replay is scheduled before it.
// KubeJS server scripts share one scope: every top-level name here starts with "crimsonBlade".
let crimsonBladeReplaying = false

EntityEvents.beforeHurt(event => {
  if (crimsonBladeReplaying) return
  let source = event.source
  let type = String(source.getType())
  if (type !== 'indirectMagic' && type !== 'magic') return
  let attacker = source.actual
  if (type === 'indirectMagic' && (!attacker || !attacker.isPlayer() || source.immediate !== attacker)) return
  if (type === 'magic' && attacker) return
  let target = event.entity
  if (event.damage < target.health) return
  if (Number(target.level.levelData.gameTime) % 20 !== 0) return
  let amount = event.damage
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
  event.cancel() // last: cancel() ends the handler
})
