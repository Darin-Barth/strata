// The Hollow's fog (client only). Heavy fog that makes navigation hard; holding a light clears some
// of it. Punishing without a light source, but never impossible. In the Hollow you see about 12 blocks; holding a light
// (any lantern or torch, the Pale Lantern, glowstone, froglights, end rods, sea lanterns, glow
// sticks...) in either hand pushes the fog back to about 30; low sanity pulls both in (to 6 and 16). It eases between the two instead of
// snapping. Underwater and lava fog are left alone. Visual only, and it works without shaders;
// shader packs that draw their own fog may show less of it.
// A startup script so the listeners are registered once; the guard keeps the client-only event
// classes off the dedicated server. Everything lives in functions: Rhino mishandles `const`
// inside nested blocks (tools/check_kubejs_const.py).
// KubeJS startup scripts share one scope: every top-level name here starts with "hollowFog".
const hollowFogDimension = 'strata:hollow'
// Fog distance without / with a held light, at full sanity and at none: the lower a player's sanity
// (Sanity: Renewed, read on the client), the closer the fog. 12 -> 6 blocks unlit, 30 -> 16 with a light.
const hollowFogDark = 12
const hollowFogDarkInsane = 6
const hollowFogLit = 30
const hollowFogLitInsane = 16
const hollowFogEase = 0.06
const hollowFogLights = ['strata:pale_lantern', 'minecraft:glowstone', 'minecraft:sea_lantern', 'minecraft:end_rod',
  'minecraft:shroomlight', 'minecraft:ochre_froglight', 'minecraft:verdant_froglight', 'minecraft:pearlescent_froglight',
  'minecraft:glow_berries', 'minecraft:jack_o_lantern', 'minecraft:magma_block']
const hollowFogColor = [0.09, 0.085, 0.1]
let hollowFogCurrent = hollowFogLit

const hollowFogIsLight = id => {
  const s = String(id)
  return hollowFogLights.indexOf(s) >= 0 || s.indexOf('lantern') >= 0 || s.indexOf('torch') >= 0 || s.indexOf('glow_stick') >= 0
}

// Sanity as 1 (sane) to 0 (none). The mod stores it the other way round (0 = sane); 1 without the mod.
let hollowFogSanityHolder = null
const hollowFogSanity = entity => {
  if (hollowFogSanityHolder === null || !entity.isPlayer()) return 1
  let raw = Number(hollowFogSanityHolder.get(entity).getSanity())
  return isNaN(raw) ? 1 : Math.max(0, Math.min(1, 1 - raw))
}

const hollowFogInHollow = entity => !!entity && String(entity.level.dimension) === hollowFogDimension
const hollowFogHoldsLight = entity =>
  entity.isLiving() && (hollowFogIsLight(entity.mainHandItem.id) || hollowFogIsLight(entity.offHandItem.id))

// Where the fog should end for this camera entity, or -1 outside the Hollow.
const hollowFogTarget = entity => {
  if (!hollowFogInHollow(entity)) return -1
  if (!entity.isLiving()) return hollowFogDark
  const sane = hollowFogSanity(entity)
  return hollowFogHoldsLight(entity) ? hollowFogLitInsane + (hollowFogLit - hollowFogLitInsane) * sane
    : hollowFogDarkInsane + (hollowFogDark - hollowFogDarkInsane) * sane
}

// Other mods (Distant Horizons, Sodium Extra, Atmospherics) rewrite the fog distance after the RenderFog
// event, so the value is also handed to Strata Tweaks (1.1.0+), which applies it last of all. Without
// that mod the event's own values are all there is.
let hollowFogBridge = null
const hollowFogBridgeSet = far => {
  if (hollowFogBridge !== null) hollowFogBridge.set(far)
}

// Applies the fog to a RenderFog event; returns the far distance used, or -1 when untouched.
const hollowFogApply = (event, entity, inFluid) => {
  const target = hollowFogTarget(entity)
  if (target < 0 || inFluid) {
    hollowFogCurrent = hollowFogLit
    hollowFogBridgeSet(-1)
    return -1
  }
  hollowFogCurrent += (target - hollowFogCurrent) * hollowFogEase
  const far = Math.min(event.getFarPlaneDistance(), hollowFogCurrent)
  event.setNearPlaneDistance(Math.min(event.getNearPlaneDistance(), far * 0.1))
  event.setFarPlaneDistance(far)
  event.setCanceled(true)          // NeoForge only applies fog changes from a cancelled event
  hollowFogBridgeSet(far)
  return far
}

const hollowFogSetup = () => {
  if (Platform.isLoaded('strata_tweaks')) {
    try {
      hollowFogBridge = Java.loadClass('strata.tweaks.ClientFog')
    } catch (e) {
      console.warn('Hollow fog: this Strata Tweaks has no ClientFog (older than 1.1.0)')
    }
  }
  if (Platform.isLoaded('sanity_renewed')) {
    try {
      hollowFogSanityHolder = Java.loadClass('guivnf.sanity_renewed.capability.SanityHolder')
    } catch (e) {
      console.warn(`Hollow fog: no sanity link (${e})`)
    }
  }
  const fogTypeNone = Java.loadClass('net.minecraft.world.level.material.FogType').NONE
  NativeEvents.onEvent('net.neoforged.neoforge.client.event.ViewportEvent$RenderFog', event => {
    try {
      hollowFogApply(event, event.getCamera().getEntity(), event.getType() !== fogTypeNone)
    } catch (e) {
      console.error(`Hollow fog: ${e}`)
    }
  })
  NativeEvents.onEvent('net.neoforged.neoforge.client.event.ViewportEvent$ComputeFogColor', event => {
    try {
      if (hollowFogTarget(event.getCamera().getEntity()) < 0) {
        if (hollowFogBridge !== null) hollowFogBridge.setColor(-1, 0, 0)
        return
      }
      event.setRed(hollowFogColor[0])
      event.setGreen(hollowFogColor[1])
      event.setBlue(hollowFogColor[2])
      // Atmospherics repaints the background after this event: Strata Tweaks puts ours back.
      if (hollowFogBridge !== null) hollowFogBridge.setColor(hollowFogColor[0], hollowFogColor[1], hollowFogColor[2])
    } catch (e) {
      console.error(`Hollow fog colour: ${e}`)
    }
  })
}

// Shader packs draw their own fog and never read the game's fog distance, so the fog above is
// invisible with shaders on. What they do draw is the Darkness effect, so while a shader pack is in
// use the client gives its own player a Darkness effect that exists on this client only (the server
// never hears of it; no icon, no particles). Complementary shows it as a wall of black at about
// 16 blocks. Holding a light fades it out. Ours is the ambient one: infinite while it holds, 22 ticks
// while it fades; a real Darkness from the server (a dread event, a Warden) is left alone.
const hollowFogShaderFadeTicks = 22

const hollowFogShaderTick = (mc, iris, darkness, MobEffectInstance) => {
  const player = mc.player
  if (!player) return
  const want = iris.isShaderPackInUse() && hollowFogInHollow(player) && !hollowFogHoldsLight(player)
  const cur = player.getEffect(darkness)
  const ours = cur !== null && cur.isAmbient()
  if (want) {
    if (cur === null || (ours && !cur.isInfiniteDuration())) {
      player.forceAddEffect(new MobEffectInstance(darkness, -1, 0, true, false, false), null)
    }
  } else if (ours) {
    if (cur.isInfiniteDuration()) {
      player.forceAddEffect(new MobEffectInstance(darkness, hollowFogShaderFadeTicks, 0, true, false, false), null)
    } else if (cur.getDuration() <= 1) {
      player.removeEffectNoUpdate(darkness)   // the client never expires effects by itself
    }
  }
}

const hollowFogShaderSetup = () => {
  const mc = Java.loadClass('net.minecraft.client.Minecraft').getInstance()
  const iris = Java.loadClass('net.irisshaders.iris.api.v0.IrisApi').getInstance()
  const darkness = Java.loadClass('net.minecraft.world.effect.MobEffects').DARKNESS
  const MobEffectInstance = Java.loadClass('net.minecraft.world.effect.MobEffectInstance')
  NativeEvents.onEvent('net.neoforged.neoforge.client.event.ClientTickEvent$Post', event => {
    try {
      hollowFogShaderTick(mc, iris, darkness, MobEffectInstance)
    } catch (e) {
      console.error(`Hollow shader fog: ${e}`)
    }
  })
}

// Distant Horizons runs with "enableVanillaFog = false": after the game sets up its fog, DH pushes the
// fog distance out to infinity so its far terrain shows, which also wiped the fog above (nothing was
// drawn at all). Its ignored-dimension list is meant to lift that in the Hollow but doesn't. So while
// the player is in a dimension with its own fog, ask DH through its API to leave the game's fog alone and
// to stop drawing its far terrain (bright distant land showed straight through the fog);
// an API value overrides the player's config without changing their file, and is cleared on leaving.
const hollowFogDhDimensions = ['strata:hollow', 'strata:abyssal_plain']

const hollowFogDhSetup = () => {
  const mc = Java.loadClass('net.minecraft.client.Minecraft').getInstance()
  const DhApi = Java.loadClass('com.seibel.distanthorizons.api.DhApi')
  let on = false
  NativeEvents.onEvent('net.neoforged.neoforge.client.event.ClientTickEvent$Post', event => {
    try {
      let player = mc.player
      let want = player !== null && hollowFogDhDimensions.indexOf(String(player.level.dimension)) >= 0
      if (want === on) return
      let configs = DhApi.Delayed.configs
      if (configs === null) return          // DH hasn't finished starting
      let vanillaFog = configs.graphics().fog().enableVanillaFog()
      let farTerrain = configs.graphics().renderingEnabled()   // DH's far terrain is drawn beyond any fog
      if (want) {
        vanillaFog.setValue(true)
        farTerrain.setValue(false)
      } else {
        vanillaFog.clearValue()
        farTerrain.clearValue()
      }
      on = want
    } catch (e) {
      console.error(`Hollow fog (Distant Horizons): ${e}`)
    }
  })
}

if (Platform.isClientEnvironment()) {
  hollowFogSetup()
  if (Platform.isLoaded('distanthorizons')) hollowFogDhSetup()
  if (Platform.isLoaded('iris')) hollowFogShaderSetup()
}
