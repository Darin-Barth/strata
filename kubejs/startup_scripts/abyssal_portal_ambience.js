// The Abyssal portal's ambience (client only). BBL Portals plays the Nether portal's whoosh from
// every portal block; near an Abyssal portal (dark prismarine, "molten" texture slot) that whoosh
// is swapped for deep-sea sounds (now and then, never stacked), and each one sheds a few water
// particles: drips, a splash and a bioluminescent glint. Darin, Oct 26: "creepy ocean sounds and
// water like particles". A startup script so the listener is registered once (client scripts
// reload); the guard keeps the client-only event class off the dedicated server.
// KubeJS startup scripts share one scope: every top-level name here starts with "abyssalPortal".
if (Platform.isClientEnvironment()) {
  const abyssalPortalMc = Java.loadClass('net.minecraft.client.Minecraft')
  const abyssalPortalRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')
  const abyssalPortalRL = Java.loadClass('net.minecraft.resources.ResourceLocation')
  const abyssalPortalSoundSource = Java.loadClass('net.minecraft.sounds.SoundSource')
  const abyssalPortalSoundInstance = Java.loadClass('net.minecraft.client.resources.sounds.SoundInstance')
  const abyssalPortalSimpleSound = Java.loadClass('net.minecraft.client.resources.sounds.SimpleSoundInstance')
  const abyssalPortalParticles = Java.loadClass('net.minecraft.core.particles.ParticleTypes')
  const abyssalPortalBlockPos = Java.loadClass('net.minecraft.core.BlockPos')
  // [sound id, weight, volume, lowest pitch, highest pitch]
  const abyssalPortalSounds = [
    ['minecraft:ambient.underwater.loop.additions', 5, 0.7, 0.7, 1.0],
    ['minecraft:ambient.underwater.loop.additions.rare', 3, 0.8, 0.7, 0.9],
    ['minecraft:ambient.underwater.loop.additions.ultra_rare', 2, 0.8, 0.6, 0.8],
    ['minecraft:block.conduit.ambient', 3, 0.6, 0.5, 0.6],
    ['minecraft:entity.elder_guardian.ambient', 1, 0.3, 0.45, 0.55],
  ]
  const abyssalPortalWeights = abyssalPortalSounds.reduce((sum, s) => sum + s[1], 0)
  const abyssalPortalGapMs = 4500
  let abyssalPortalLastSound = 0

  const abyssalPortalPick = () => {
    let r = Math.random() * abyssalPortalWeights
    for (let i = 0; i < abyssalPortalSounds.length; i++) {
      r -= abyssalPortalSounds[i][1]
      if (r <= 0) return abyssalPortalSounds[i]
    }
    return abyssalPortalSounds[0]
  }

  const abyssalPortalDrip = (level, x, y, z) => {
    const P = abyssalPortalParticles
    const rx = () => (Math.random() - 0.5) * 0.9
    level.addParticle(P.FALLING_WATER, x + rx(), y + Math.random() * 0.5, z + rx(), 0, 0, 0)
    if (Math.random() < 0.5) level.addParticle(P.DRIPPING_WATER, x + rx(), y + 0.45, z + rx(), 0, 0, 0)
    if (Math.random() < 0.35) level.addParticle(P.SPLASH, x + rx(), y - 0.3, z + rx(), 0, 0.05, 0)
    if (Math.random() < 0.3) level.addParticle(P.GLOW, x + rx(), y + rx(), z + rx(), rx() * 0.02, 0.01, rx() * 0.02)
  }

  NativeEvents.onEvent('net.neoforged.neoforge.client.event.sound.PlaySoundEvent', event => {
    try {
      const sound = event.getOriginalSound()
      if (!sound || String(sound.getLocation()) !== 'minecraft:block.portal.ambient') return
      const level = abyssalPortalMc.getInstance().level
      if (!level) return
      const x = sound.getX(), y = sound.getY(), z = sound.getZ()
      if (String(level.getBlockState(abyssalPortalBlockPos.containing(x, y, z))).indexOf('texture=molten') < 0) return
      abyssalPortalDrip(level, x, y, z)
      const now = Date.now()
      if (now - abyssalPortalLastSound < abyssalPortalGapMs) {
        event.setSound(null)
        return
      }
      abyssalPortalLastSound = now
      const s = abyssalPortalPick()
      const soundEvent = abyssalPortalRegistries.SOUND_EVENT.get(abyssalPortalRL.parse(s[0]))
      if (!soundEvent) {
        event.setSound(null)
        return
      }
      const pitch = s[3] + Math.random() * (s[4] - s[3])
      event.setSound(new abyssalPortalSimpleSound(soundEvent, abyssalPortalSoundSource.AMBIENT, s[2], pitch,
        abyssalPortalSoundInstance.createUnseededRandom(), x, y, z))
    } catch (e) {
      console.error(`Abyssal portal ambience: ${e}`)
    }
  })
}
