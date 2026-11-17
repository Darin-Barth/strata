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
//   * Unless the player wears a diving helmet (below) or has Water Breathing, this script keeps
//     the air count itself, after every mod has had its say (lowest priority, end of the tick): it
//     drains underwater like vanilla (1 per tick, 2 damage a second at empty) and refills out of
//     the water, whatever else set the air bar.
//   * With a diving helmet on, the air is left to the helmet's own mod (a Create helmet without
//     air in its backtank still drowns you).
// Everywhere else nothing changes. Creative and spectator players are left alone.
// A startup script so the listeners are registered once (server scripts reload).
// KubeJS startup scripts share one scope: every top-level name here starts with "vampAir".
const vampAirDimension = 'strata:abyssal_plain'
const vampAirKey = 'strata_vamp_air'
const vampAirMax = 300
// Headgear that brings its own air supply: Create's diving helmets (backtank), Mekanism's scuba
// mask and MekaSuit, PneumaticCraft's helmet, Ad Astra's suits, the diving suits of Hybrid Aquatic
// and Alex's Caves.
const vampAirHelmets = /diving_helmet|scuba_mask|mekasuit_helmet|pneumatic_helmet|space_helmet|jet_suit_helmet|diving_suit_helmet/
const vampAirHasHelmet = entity => vampAirHelmets.test(String(entity.headArmorItem.id))

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
  let air = data.contains(vampAirKey) ? data.getInt(vampAirKey) : Math.min(vampAirMax, entity.getAirSupply())
  if (entity.isUnderWater()) {
    air -= 1
    if (air <= -20) {
      air = 0
      entity.attack(drown(), 2)      // KubeJS hides hurt(); attack(source, amount) is its version
    }
  } else {
    air = Math.min(vampAirMax, air + 4)
  }
  data.putInt(vampAirKey, air)
  entity.setAirSupply(air)
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
      if (entity.isUnderWater() && (!lastTold[name] || now - lastTold[name] > 60000)) {
        lastTold[name] = now
        entity.displayClientMessage(Text.aqua('Charms and trinkets can\'t breathe for you down here. Diving gear or a potion can.').italic(), true)
      }
    } catch (e) {
      console.error(`Abyssal air (effect): ${e}`)
    }
  })
}

vampAirSetup()
