// Balance patch F6 (docs/balance-patch.md): Cataclysm and Legendary Monsters cap how
// much one hit can do to their bosses, but Bosses of Mass Destruction and Bosses'Rise don't, so an
// Alex's Caves nuke or a Create Big Cannons shell deleted them. Explosions (and Big Cannons'
// projectile damage) now do at most 10 per hit to those bosses. Swords, bows and spells stay
// uncapped, so getting strong still pays off. A startup script because native listeners in server
// scripts would stack up on every /reload.
// KubeJS scripts share one scope per type: every top-level name here starts with "bossBlastCap".
const bossBlastCapNamespaces = ['bosses_of_mass_destruction', 'block_factorys_bosses']
const bossBlastCapMax = 10
const bossBlastCapTagKey = Java.loadClass('net.minecraft.tags.TagKey')
const bossBlastCapRegistries = Java.loadClass('net.minecraft.core.registries.Registries')
const bossBlastCapRL = Java.loadClass('net.minecraft.resources.ResourceLocation')
const bossBlastCapExplosion = bossBlastCapTagKey.create(bossBlastCapRegistries.DAMAGE_TYPE, bossBlastCapRL.parse('minecraft:is_explosion'))

NativeEvents.onEvent('net.neoforged.neoforge.event.entity.living.LivingDamageEvent$Pre', event => {
  const victim = event.getEntity()
  if (!victim || victim.level.isClientSide() || victim.isPlayer()) return
  if (bossBlastCapNamespaces.indexOf(String(victim.type).split(':')[0]) < 0) return
  const source = event.getSource()
  const key = source.typeHolder().unwrapKey()
  const cannon = key.isPresent() && String(key.get().location()).split(':')[0] === 'createbigcannons'
  if (!cannon && !source.is(bossBlastCapExplosion)) return
  if (event.getNewDamage() > bossBlastCapMax) event.setNewDamage(bossBlastCapMax)
})
