// The Hollow's fog (client only). Darin, Oct 26: "heavy fog, it should be hard to navigate.
// Holding a lantern helps clear some of the fog"; "pretty punishing if you don't have a light
// source, but don't make it impossible." In the Hollow you see about 10 blocks; holding a light
// (any lantern or torch, the Pale Lantern, glowstone, froglights, end rods, sea lanterns, glow
// sticks...) in either hand pushes the fog back to about 28. It eases between the two instead of
// snapping. Underwater and lava fog are left alone. Visual only, and it works without shaders;
// shader packs that draw their own fog may show less of it.
// A startup script so the listeners are registered once; the guard keeps the client-only event
// classes off the dedicated server. Everything lives in functions: Rhino mishandles `const`
// inside nested blocks (tools/check_kubejs_const.py).
// KubeJS startup scripts share one scope: every top-level name here starts with "hollowFog".
const hollowFogDimension = 'strata:hollow'
const hollowFogDark = 10
const hollowFogLit = 28
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

// Where the fog should end for this camera entity, or -1 outside the Hollow.
const hollowFogTarget = entity => {
  if (!entity || String(entity.level.dimension) !== hollowFogDimension) return -1
  if (!entity.isLiving()) return hollowFogDark
  return hollowFogIsLight(entity.mainHandItem.id) || hollowFogIsLight(entity.offHandItem.id) ? hollowFogLit : hollowFogDark
}

// Applies the fog to a RenderFog event; returns the far distance used, or -1 when untouched.
const hollowFogApply = (event, entity, inFluid) => {
  const target = hollowFogTarget(entity)
  if (target < 0 || inFluid) {
    hollowFogCurrent = hollowFogLit
    return -1
  }
  hollowFogCurrent += (target - hollowFogCurrent) * hollowFogEase
  const far = Math.min(event.getFarPlaneDistance(), hollowFogCurrent)
  event.setNearPlaneDistance(Math.min(event.getNearPlaneDistance(), far * 0.1))
  event.setFarPlaneDistance(far)
  event.setCanceled(true)          // NeoForge only applies fog changes from a cancelled event
  return far
}

const hollowFogSetup = () => {
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
      if (hollowFogTarget(event.getCamera().getEntity()) < 0) return
      event.setRed(hollowFogColor[0])
      event.setGreen(hollowFogColor[1])
      event.setBlue(hollowFogColor[2])
    } catch (e) {
      console.error(`Hollow fog colour: ${e}`)
    }
  })
}

if (Platform.isClientEnvironment()) hollowFogSetup()
