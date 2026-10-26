// The Hollow: scary but fair (Darin, Oct 25: "I really don't want BS mobs that just kill you
// without any chance of survival"). One hit from a horror mob can take at most 40% of a player's
// max health (after armor), and horror mobs can't hurt a player in the first 10 seconds after
// arriving in the Hollow. Bosses keep their designed damage. Applies wherever the hit happens, so
// a horror mob that follows someone through a portal is capped too. A startup script because
// native listeners registered in server scripts would stack up on every /reload.
// KubeJS scripts share one scope per type: every top-level name here starts with "hollowCap".
const hollowCapEntityType = Java.loadClass('net.minecraft.world.entity.EntityType')
const hollowCapNamespaces = ['cave_dweller', 'weeping_angels', 'whispering_spirits', 'the_ravenous',
  'grim_and_bleak', 'graveyard', 'mutantmonsters', 'sanity_renewed']
const hollowCapBosses = ['graveyard:lich', 'grim_and_bleak:gate_guardian']
const hollowCapFraction = 0.4
const hollowCapGraceMs = 10 * 1000

NativeEvents.onEvent('net.neoforged.neoforge.event.entity.living.LivingDamageEvent$Pre', event => {
  const victim = event.getEntity()
  if (!victim || victim.level.isClientSide() || !victim.isPlayer()) return
  const attacker = event.getSource().getEntity()
  if (!attacker) return
  const id = String(hollowCapEntityType.getKey(attacker.getType()))
  if (hollowCapBosses.indexOf(id) >= 0) return
  if (hollowCapNamespaces.indexOf(id.split(':')[0]) < 0) return
  const arrived = victim.persistentData.getLong('strata_hollow_arrived')
  if (arrived > 0 && Date.now() - arrived < hollowCapGraceMs) {
    event.setNewDamage(0)
    return
  }
  const cap = victim.getMaxHealth() * hollowCapFraction
  if (event.getNewDamage() > cap) event.setNewDamage(cap)
})
