// Portal ambience (client only). Each of our BBL Portals portals has its own texture slot
// (pokeworld_portal.js), so the block's "texture" property tells them apart. Near one, that world's
// sounds play (spaced out, never stacked) and the portal sheds a few particles of its own:
//   default (Alph Stone, Pokémon world): bell chimes, a low hum, wind through ruins, Unown;
//     glyph and sparkle particles.
//   nether (resin bricks, the Hollow): whispers, creaking, a slow heartbeat, cave noises, and
//     stretches of total silence; ash, pale petals and smoke.
//   molten (dark prismarine, Abyssal Plain): deep-sea calls and the Conduit's thrum; drips,
//     splashes and glow sparkles.
// The script finds the portal blocks around the player itself (every two seconds, through the
// chunk sections' palettes) and runs sounds and particles on the client tick. Until Nov 16 it
// swapped the Nether whoosh BBL plays from portal blocks instead, but the game only plays that
// about once a minute per portal and from 16 blocks at most, so the ambience was all but silent
// unless you stood in the portal. The whoosh itself is muted near our portals.
// A startup script so the listener is registered once (client scripts reload);
// the guard keeps the client-only event class off the dedicated server. Sounds or particles
// missing from the client's registries are skipped.
// KubeJS startup scripts share one scope: every top-level name here starts with "portalAmb".
// Everything lives inside a function: Rhino rejects `const` inside a bare if-block with
// "redeclaration of var" (0.4.0/0.4.1 clients hit this; the server never runs the block).
// Also no `const` inside any nested block anywhere (Rhino reuses the first value or throws):
// tools/check_kubejs_const.py checks every script.
const portalAmbSetup = () => {
  const portalAmbMc = Java.loadClass('net.minecraft.client.Minecraft')
  const portalAmbRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')
  const portalAmbRL = Java.loadClass('net.minecraft.resources.ResourceLocation')
  const portalAmbSoundSource = Java.loadClass('net.minecraft.sounds.SoundSource')
  const portalAmbSoundInstance = Java.loadClass('net.minecraft.client.resources.sounds.SoundInstance')
  const portalAmbSimpleSound = Java.loadClass('net.minecraft.client.resources.sounds.SimpleSoundInstance')
  const portalAmbBlockPos = Java.loadClass('net.minecraft.core.BlockPos')

  const portalAmbParticle = id => {
    try {
      return portalAmbRegistries.PARTICLE_TYPE.get(portalAmbRL.parse(id))
    } catch (e) {
      return null
    }
  }
  const portalAmbR = () => (Math.random() - 0.5) * 0.9
  const portalAmbAdd = (level, id, x, y, z, vx, vy, vz) => {
    const p = portalAmbParticle(id)
    if (p) level.addParticle(p, x, y, z, vx, vy, vz)
  }

  // Per texture slot: sounds as [id, weight, volume, lowest pitch, highest pitch], the shortest
  // gap between two sounds (ms), the chance a sound is followed by silence and how long, and the
  // particles one whoosh turns into.
  const portalAmbStyles = {
    default: {
      sounds: [
        ['minecraft:block.amethyst_block.chime', 4, 0.7, 0.8, 1.2],
        ['minecraft:block.bell.use', 2, 0.15, 1.7, 2.0],
        ['minecraft:block.beacon.ambient', 2, 0.4, 0.7, 0.8],
        ['minecraft:block.sand.idle', 3, 0.6, 0.9, 1.1],
        ['minecraft:block.dry_grass.ambient', 2, 0.5, 0.9, 1.1],
        ['cobblemon:pokemon.unown.ambient', 1, 0.35, 0.9, 1.1],
      ],
      gapMs: 5000, silenceChance: 0, silenceMs: [0, 0],
      particles: (level, x, y, z) => {
        portalAmbAdd(level, 'minecraft:enchant', x + portalAmbR(), y + portalAmbR(), z + portalAmbR(), portalAmbR() * 2, Math.random(), portalAmbR() * 2)
        portalAmbAdd(level, 'minecraft:enchant', x + portalAmbR(), y + portalAmbR(), z + portalAmbR(), portalAmbR() * 2, Math.random(), portalAmbR() * 2)
        if (Math.random() < 0.4) portalAmbAdd(level, 'minecraft:end_rod', x + portalAmbR(), y + portalAmbR(), z + portalAmbR(), 0, 0.01, 0)
      },
    },
    nether: {
      sounds: [
        ['minecraft:ambient.soul_sand_valley.additions', 2, 0.5, 0.8, 1.0],
        ['minecraft:entity.vex.ambient', 2, 0.25, 0.5, 0.6],
        ['minecraft:entity.creaking.ambient', 2, 0.5, 0.6, 0.8],
        ['minecraft:block.creaking_heart.idle', 2, 0.6, 0.7, 0.9],
        ['minecraft:entity.warden.heartbeat', 2, 0.6, 0.7, 0.75],
        ['minecraft:ambient.cave', 3, 0.6, 0.8, 1.0],
      ],
      gapMs: 6000, silenceChance: 0.3, silenceMs: [20000, 45000],
      particles: (level, x, y, z) => {
        portalAmbAdd(level, 'minecraft:white_ash', x + portalAmbR(), y + portalAmbR(), z + portalAmbR(), 0, -0.02, 0)
        portalAmbAdd(level, 'minecraft:ash', x + portalAmbR(), y + portalAmbR(), z + portalAmbR(), 0, -0.02, 0)
        if (Math.random() < 0.3) portalAmbAdd(level, 'minecraft:pale_oak_leaves', x + portalAmbR(), y + 0.4, z + portalAmbR(), 0, 0, 0)
        if (Math.random() < 0.4) portalAmbAdd(level, 'minecraft:smoke', x + portalAmbR(), y + portalAmbR(), z + portalAmbR(), 0, 0.01, 0)
      },
    },
    molten: {
      sounds: [
        ['minecraft:ambient.underwater.loop.additions', 5, 0.7, 0.7, 1.0],
        ['minecraft:ambient.underwater.loop.additions.rare', 3, 0.8, 0.7, 0.9],
        ['minecraft:ambient.underwater.loop.additions.ultra_rare', 2, 0.8, 0.6, 0.8],
        ['minecraft:block.conduit.ambient', 3, 0.6, 0.5, 0.6],
        ['minecraft:entity.elder_guardian.ambient', 1, 0.3, 0.45, 0.55],
      ],
      gapMs: 4500, silenceChance: 0, silenceMs: [0, 0],
      particles: (level, x, y, z) => {
        portalAmbAdd(level, 'minecraft:falling_water', x + portalAmbR(), y + Math.random() * 0.5, z + portalAmbR(), 0, 0, 0)
        if (Math.random() < 0.5) portalAmbAdd(level, 'minecraft:dripping_water', x + portalAmbR(), y + 0.45, z + portalAmbR(), 0, 0, 0)
        if (Math.random() < 0.35) portalAmbAdd(level, 'minecraft:splash', x + portalAmbR(), y - 0.3, z + portalAmbR(), 0, 0.05, 0)
        if (Math.random() < 0.3) portalAmbAdd(level, 'minecraft:glow', x + portalAmbR(), y + portalAmbR(), z + portalAmbR(), portalAmbR() * 0.02, 0.01, portalAmbR() * 0.02)
      },
    },
  }
  // When each style may next make a sound.
  const portalAmbNext = { default: 0, nether: 0, molten: 0 }

  const portalAmbPick = sounds => {
    let r = Math.random() * sounds.reduce((sum, s) => sum + s[1], 0)
    for (let i = 0; i < sounds.length; i++) {
      r -= sounds[i][1]
      if (r <= 0) return sounds[i]
    }
    return sounds[0]
  }

  // Portal blocks near the player: [{x, y, z, style}], refreshed every two seconds.
  let portalAmbFound = []
  let portalAmbTick = 0
  const portalAmbRange = 28          // how far a portal is heard and sheds particles
  const portalAmbIsPortal = state => String(state.getBlock().builtInRegistryHolder().key().location()) === 'portals:custom_portal'
  const portalAmbScan = (level, player) => {
    const found = []
    const pcx = Math.floor(player.x) >> 4, pcz = Math.floor(player.z) >> 4
    const minSection = level.getMinSection(), maxSection = level.getMaxSection()
    const psy = Math.floor(player.y) >> 4
    for (let cx = pcx - 2; cx <= pcx + 2; cx++) for (let cz = pcz - 2; cz <= pcz + 2; cz++) {
      if (!level.hasChunk(cx, cz)) continue
      let chunk = level.getChunk(cx, cz)
      for (let sy = Math.max(minSection, psy - 2); sy <= Math.min(maxSection - 1, psy + 2); sy++) {
        let section = chunk.getSection(sy - minSection)
        // The palette check is one call; only a section that holds a portal is read block by block.
        if (section.hasOnlyAir() || !section.maybeHas(portalAmbIsPortal)) continue
        for (let x = 0; x < 16; x++) for (let y = 0; y < 16; y++) for (let z = 0; z < 16; z++) {
          let state = section.getBlockState(x, y, z)
          if (!portalAmbIsPortal(state)) continue
          let m = String(state).match(/texture=([a-z]+)/)
          if (m && portalAmbStyles[m[1]]) found.push({ x: cx * 16 + x + 0.5, y: sy * 16 + y + 0.5, z: cz * 16 + z + 0.5, style: m[1] })
        }
      }
    }
    return found
  }

  NativeEvents.onEvent('net.neoforged.neoforge.client.event.ClientTickEvent$Post', event => {
    try {
      let mc = portalAmbMc.getInstance()
      let level = mc.level, player = mc.player
      if (!level || !player || mc.isPaused()) return
      portalAmbTick++
      if (portalAmbTick % 40 === 1) portalAmbFound = portalAmbScan(level, player)
      if (portalAmbFound.length === 0) return
      let now = Date.now()
      let nearest = {}
      for (let i = 0; i < portalAmbFound.length; i++) {
        let b = portalAmbFound[i]
        let dx = b.x - player.x, dy = b.y - player.getEyeY(), dz = b.z - player.z
        let d = Math.sqrt(dx * dx + dy * dy + dz * dz)
        if (d > portalAmbRange) continue
        if (Math.random() < 0.06) portalAmbStyles[b.style].particles(level, b.x, b.y, b.z)
        if (!nearest[b.style] || d < nearest[b.style].d) nearest[b.style] = { d: d, dx: dx, dy: dy, dz: dz }
      }
      for (let name in nearest) {
        if (now < portalAmbNext[name]) continue
        let style = portalAmbStyles[name], n = nearest[name]
        portalAmbNext[name] = now + style.gapMs
        if (Math.random() < style.silenceChance) {
          portalAmbNext[name] = now + style.silenceMs[0] + Math.random() * (style.silenceMs[1] - style.silenceMs[0])
          continue
        }
        let s = portalAmbPick(style.sounds)
        let soundEvent = portalAmbRegistries.SOUND_EVENT.get(portalAmbRL.parse(s[0]))
        if (!soundEvent) continue
        let pitch = s[3] + Math.random() * (s[4] - s[3])
        // A sound fades to nothing 16 blocks out. Played from half way along the line to the
        // portal, it carries the full range and still comes from the portal's direction.
        mc.getSoundManager().play(new portalAmbSimpleSound(soundEvent, portalAmbSoundSource.BLOCKS, s[2], pitch,
          portalAmbSoundInstance.createUnseededRandom(), player.x + n.dx * 0.5, player.getEyeY() + n.dy * 0.5, player.z + n.dz * 0.5))
      }
    } catch (e) {
      console.error(`Portal ambience: ${e}`)
    }
  })

  // BBL Portals plays the Nether portal's whoosh from its portal blocks: not from ours.
  NativeEvents.onEvent('net.neoforged.neoforge.client.event.sound.PlaySoundEvent', event => {
    try {
      let sound = event.getOriginalSound()
      if (!sound || String(sound.getLocation()) !== 'minecraft:block.portal.ambient') return
      let level = portalAmbMc.getInstance().level
      if (!level) return
      let state = String(level.getBlockState(portalAmbBlockPos.containing(sound.getX(), sound.getY(), sound.getZ())))
      if (state.indexOf('portals:custom_portal') < 0) return
      let m = state.match(/texture=([a-z]+)/)
      if (m && portalAmbStyles[m[1]]) event.setSound(null)
    } catch (e) {
      console.error(`Portal ambience: ${e}`)
    }
  })
}

if (Platform.isClientEnvironment()) portalAmbSetup()
