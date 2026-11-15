// Excelsius Propulsion Leggings fall immunity (Darin, Nov 14). Cataclysm: Spellbooks' tooltip says "Any fall damage
// that would be taken is nullified", but the mod never implements it: its only fall handler is the Cursium Mage Boots'
// 70% reduction, and nothing checks the leggings (checked in 1.1.14 and 1.1.15). This cancels fall damage for anyone
// wearing them. Re-check after a Cataclysm: Spellbooks update; drop this script (leave a stub) once the mod does it.
// KubeJS names: the damage type ID is source.getType() (getMsgId() is hidden), and event.cancel() ends the handler.
// KubeJS server scripts share one scope: every top-level name here starts with "excelsiusLegs".
const excelsiusLegsSlot = Java.loadClass('net.minecraft.world.entity.EquipmentSlot').LEGS

EntityEvents.beforeHurt(event => {
  if (String(event.source.getType()) !== 'fall') return
  let entity = event.entity
  if (!entity || !entity.isLiving()) return
  if (String(entity.getItemBySlot(excelsiusLegsSlot).id) !== 'cataclysm_spellbooks:excelsius_leggings') return
  event.cancel() // last: cancel() ends the handler
})
