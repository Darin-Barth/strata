// The Hollow and the Abyssal Plain: scary but fair: no mob should kill a player
// without a chance of survival. One hit from a horror mob can take at most 40% of a player's
// max health (after armor), and horror mobs can't hurt a player in the first 10 seconds after
// arriving in the Hollow. Bosses keep their designed damage. Applies wherever the hit happens, so
// a horror mob that follows someone through a portal is capped too. A startup script because
// native listeners registered in server scripts would stack up on every /reload.
// KubeJS scripts share one scope per type: every top-level name here starts with "hollowCap".
const hollowCapNamespaces = ['cave_dweller', 'weeping_angels', 'whispering_spirits', 'the_ravenous',
  'grim_and_bleak', 'graveyard', 'mutantmonsters', 'sanity_renewed',
  // the Abyssal Plain's deep-sea creatures
  'hybrid_aquatic', 'alexscaves']
const hollowCapBosses = ['graveyard:lich', 'grim_and_bleak:gate_guardian']
const hollowCapFraction = 0.4
const hollowCapGraceMs = 10 * 1000
// Horror damage that comes without an attacker: a Weeping Angel's neck snap, Grim & Bleak's
// smite around a dying Gate Guardian (500 damage, 15 blocks), its decay and possession.
// Capped (not graced) in the Hollow.
const hollowCapSourcelessTypes = ['weeping_angels:snapped_neck', 'weeping_angels:punch_stone',
  'grim_and_bleak:godly_power', 'grim_and_bleak:decayy', 'grim_and_bleak:posession']

NativeEvents.onEvent('net.neoforged.neoforge.event.entity.living.LivingDamageEvent$Pre', event => {
  const victim = event.getEntity()
  if (!victim || victim.level.isClientSide() || !victim.isPlayer()) return
  // KubeJS wraps DamageSource: the attacker is `.actual` (getEntity() isn't visible to scripts).
  const attacker = event.getSource().actual
  if (!attacker) {
    let key = event.getSource().typeHolder().unwrapKey()
    if (!key.isPresent() || hollowCapSourcelessTypes.indexOf(String(key.get().location())) < 0) return
    if (String(victim.level.dimension) !== 'strata:hollow') return
    let cap = victim.getMaxHealth() * hollowCapFraction
    if (event.getNewDamage() > cap) event.setNewDamage(cap)
    return
  }
  const id = String(attacker.type)
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
