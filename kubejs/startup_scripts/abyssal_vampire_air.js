// Vampires can drown in the Abyssal Plain (Lopez / Darin, Oct 26: "make sure that in the abyssal
// plain they aren't immune to drowning. Just in that dimension"). Vampirism refills a vampire
// player's air to full at the end of every tick (VampirePlayer.onUpdate on PlayerTickEvent.Post),
// so this runs after it (lowest priority) and keeps the vampire's own air count there instead:
// it drains underwater like vanilla (1 per tick, 2 damage every second at empty) and refills
// quickly out of the water. Water Breathing, Conduit power and a diving helmet still let them
// breathe. Everywhere else vampires keep their benefit.
// A startup script so the listener is registered once (server scripts reload).
// KubeJS startup scripts share one scope: every top-level name here starts with "vampAir".
const vampAirDimension = 'strata:abyssal_plain'
const vampAirKey = 'strata_vamp_air'
const vampAirMax = 300

// One tick for one entity. `isVampire` is passed in so the logic can be tested without Vampirism.
// Returns the air value set, or null when the entity is left alone.
const vampAirTick = (entity, isVampire, waterBreathing, conduit, drown) => {
  if (!isVampire || String(entity.level.dimension) !== vampAirDimension) return null
  const data = entity.persistentData
  let air = data.contains(vampAirKey) ? data.getInt(vampAirKey) : vampAirMax
  const helmet = String(entity.headArmorItem.id)
  const breathing = entity.hasEffect(waterBreathing) || entity.hasEffect(conduit) || helmet.indexOf('diving_helmet') >= 0
  if (entity.isUnderWater() && !breathing) {
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

const vampAirSetup = () => {
  const priority = Java.loadClass('net.neoforged.bus.api.EventPriority')
  const helper = Java.loadClass('de.teamlapen.vampirism.util.Helper')
  const effects = Java.loadClass('net.minecraft.world.effect.MobEffects')
  const tickPost = Java.loadClass('net.neoforged.neoforge.event.tick.PlayerTickEvent$Post')
  NativeEvents.onEvent(priority.LOWEST, tickPost, event => {
    const player = event.getEntity()
    if (player.level.isClientSide()) return
    try {
      vampAirTick(player, helper.isVampire(player), effects.WATER_BREATHING, effects.CONDUIT_POWER,
        () => player.level.damageSources().drown())
    } catch (e) {
      console.error(`Vampire air: ${e}`)
    }
  })
}

vampAirSetup()
