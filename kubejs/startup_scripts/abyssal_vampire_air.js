// Breathing in the Abyssal Plain (strata:abyssal_plain): only diving gear and real potions count.
// (The file keeps its first name: it began as the rule that vampires drown here.)
//
// Many items keep a player breathing for free: trinkets that top the air bar up every tick (the
// Aether's Iron Bubble, the Snorkel), armour, augments, charms, pets and familiars that keep
// re-applying a short hidden Water Breathing, a Conduit, and Vampirism, which refills a vampire's
// air at the end of every tick. Down here that would skip the dimension's whole point (pumps,
// airlocks, air tanks), so:
//   * Water Breathing and Conduit Power are refused when they are ambient, hidden, endless or
//     shorter than 30 seconds. A brewed potion or a meal still works; a trinket's pulse does not.
//   * Unless the player wears a diving helmet that has air to give (below) or has Water Breathing,
//     this script keeps the air count itself, after every mod has had its say (lowest priority, end
//     of the tick): it drains underwater like vanilla (1 per tick, 2 damage a second at empty) and
//     refills out of the water, whatever else set the air bar.
//   * With a diving helmet on AND its supply present (air in a Create backtank, oxygen in a
//     Mekanism scuba tank or an Ad Astra suit, a powered MekaSuit breathing unit, a pressurised
//     PneumaticCraft helmet with the scuba upgrade), the air is left to the helmet's own mod. An
//     empty one is no helmet at all: before Nov 17 any listed helmet let a charm or a vampire's
//     refill through.
//   * The cheap diving helmets with no air supply (Hybrid Aquatic's, 7 copper and a pane, and
//     Alex's Caves') gave endless Water Breathing. Here they are a longer breath: 60 seconds, 90
//     for the reinforced one, instead of 15 (Darin, Nov 17). The air bar shows the share left.
// Everywhere else nothing changes. Creative and spectator players are left alone.
// A startup script so the listeners are registered once (server scripts reload).
// KubeJS startup scripts share one scope: every top-level name here starts with "vampAir".
const vampAirDimension = 'strata:abyssal_plain'
const vampAirKey = 'strata_vamp_air'
const vampAirMax = 300
// Helmets that only stretch a breath: ticks of air (300 = the bare 15 seconds).
const vampAirBreath = {
  'hybrid_aquatic:diving_helmet': 1200,
  'hybrid_aquatic:reinforced_diving_helmet': 1800,
  'alexscaves:diving_helmet': 1200
}
const vampAirMaxOf = entity => vampAirBreath[String(entity.headArmorItem.id)] || vampAirMax
// Headgear that brings its own air supply, each with the test its own mod uses before it gives
// air. A test that throws (a mod update renamed something) counts as supplied and is logged once:
// better a loophole than drowning someone in working gear.
const vampAirSlot = Java.loadClass('net.minecraft.world.entity.EquipmentSlot')
const vampAirBroken = {}
const vampAirSupplies = [
  [/^create:.*diving_helmet$/, entity =>
    !Java.loadClass('com.simibubi.create.content.equipment.armor.BacktankUtil').getAllWithAir(entity).isEmpty()],
  [/^mekanism:scuba_mask$/, entity =>
    Java.loadClass('mekanism.common.CommonPlayerTickHandler').isScubaMaskOn(entity, entity.getItemBySlot(vampAirSlot.CHEST))],
  [/^mekanism:mekasuit_helmet$/, entity => {
    const unit = Java.loadClass('mekanism.api.gear.IModuleHelper').INSTANCE.getIfEnabled(entity, vampAirSlot.HEAD,
      Java.loadClass('mekanism.common.registries.MekanismModules').ELECTROLYTIC_BREATHING_UNIT)
    return unit != null && unit.getContainerEnergy(entity.getItemBySlot(vampAirSlot.HEAD)) > 0
  }],
  [/^pneumaticcraft:pneumatic_helmet$/, entity => {
    const armor = Java.loadClass('me.desht.pneumaticcraft.common.pneumatic_armor.CommonArmorHandler').getHandlerForPlayer(entity)
    const scuba = Java.loadClass('me.desht.pneumaticcraft.common.pneumatic_armor.CommonUpgradeHandlers').scubaHandler
    return armor.upgradeUsable(scuba, true) && armor.hasMinPressure(vampAirSlot.HEAD)
  }],
  [/^ad_astra:.*(space_helmet|jet_suit_helmet)$/, entity =>
    Java.loadClass('earth.terrarium.adastra.common.items.armor.SpaceSuitItem').hasOxygen(entity)]
]
const vampAirHasHelmet = entity => {
  const id = String(entity.headArmorItem.id)
  for (let i = 0; i < vampAirSupplies.length; i++) {
    if (!vampAirSupplies[i][0].test(id)) continue
    try {
      return !!vampAirSupplies[i][1](entity)
    } catch (e) {
      if (!vampAirBroken[id]) console.error(`Abyssal air: can't check the air supply of ${id}: ${e}`)
      vampAirBroken[id] = true
      return true
    }
  }
  return false
}

// One tick for one player. Returns the air value set, or null when the player is left alone.
const vampAirTick = (entity, waterBreathing, drown) => {
  const data = entity.persistentData
  if (String(entity.level.dimension) !== vampAirDimension) {
    // Left the dimension (or died there): forget the count, or the next visit starts with the old one.
    if (data.contains(vampAirKey)) data.remove(vampAirKey)
    return null
  }
  if (entity.isCreative() || entity.isSpectator() || vampAirHasHelmet(entity) || entity.hasEffect(waterBreathing)) {
    if (data.contains(vampAirKey)) data.remove(vampAirKey)
    return null
  }
  // The count runs to the helmet's own maximum; the air bar gets the share left (out of 300).
  let max = vampAirMaxOf(entity)
  // A fresh count starts full: it only starts on arriving, or when a helmet's supply or a potion
  // has just run out, and the air bar then may hold whatever a trinket last wrote (the Iron
  // Bubble pins it at 30, which left a second and a half).
  let air = data.contains(vampAirKey) ? Math.min(max, data.getInt(vampAirKey)) : max
  if (entity.isUnderWater()) {
    air -= 1
    if (air <= -20) {
      air = 0
      entity.attack(drown(), 2)      // KubeJS hides hurt(); attack(source, amount) is its version
    }
  } else {
    air = Math.min(max, air + Math.round(max / 75))
  }
  data.putInt(vampAirKey, air)
  entity.setAirSupply(Math.ceil(air * vampAirMax / max))
  return air
}

// Whether an effect about to be applied is a trinket's pulse rather than a potion.
const vampAirIsPulse = instance => instance.isAmbient() || !instance.isVisible() || !instance.showIcon() ||
  instance.isInfiniteDuration() || instance.getDuration() < 600

const vampAirSetup = () => {
  const priority = Java.loadClass('net.neoforged.bus.api.EventPriority')
  const effects = Java.loadClass('net.minecraft.world.effect.MobEffects')
  const tickPost = Java.loadClass('net.neoforged.neoforge.event.tick.PlayerTickEvent$Post')
  const applicable = Java.loadClass('net.neoforged.neoforge.event.entity.living.MobEffectEvent$Applicable')
  const refuse = Java.loadClass('net.neoforged.neoforge.event.entity.living.MobEffectEvent$Applicable$Result').DO_NOT_APPLY
  const playerClass = Java.loadClass('net.minecraft.world.entity.player.Player')
  const lastTold = {}
  NativeEvents.onEvent(priority.LOWEST, tickPost, event => {
    const player = event.getEntity()
    if (player.level.isClientSide()) return
    try {
      vampAirTick(player, effects.WATER_BREATHING, () => player.level.damageSources().drown())
    } catch (e) {
      console.error(`Abyssal air: ${e}`)
    }
  })
  NativeEvents.onEvent(priority.LOWEST, applicable, event => {
    try {
      let entity = event.getEntity()
      if (!(entity instanceof playerClass) || entity.level.isClientSide()) return
      if (String(entity.level.dimension) !== vampAirDimension) return
      let instance = event.getEffectInstance()
      if (!instance.is(effects.WATER_BREATHING) && !instance.is(effects.CONDUIT_POWER)) return
      if (!vampAirIsPulse(instance) || vampAirHasHelmet(entity)) return
      event.setResult(refuse)
      let name = String(entity.username), now = Date.now()
      if (entity.isUnderWater() && vampAirMaxOf(entity) === vampAirMax && (!lastTold[name] || now - lastTold[name] > 60000)) {
        lastTold[name] = now
        entity.displayClientMessage(Text.aqua('Charms and trinkets can\'t breathe for you down here. Diving gear or a potion can.').italic(), true)
      }
    } catch (e) {
      console.error(`Abyssal air (effect): ${e}`)
    }
  })
}

vampAirSetup()
