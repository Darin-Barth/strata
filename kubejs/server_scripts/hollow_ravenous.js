// The Ravenous in the Hollow. Its own spawn check wants open sky in a #minecraft:is_overworld
// biome, and Hollow biomes are never tagged that (Overworld mobs would leak in), so its natural
// spawns never fire there. This spawns it instead: rarely, out of sight, under open sky, not in
// a player's first minutes after arriving. The Ravenous (one at a time near a player) and its
// Screechers (up to three). It eats blocks by default (Darin, Oct 26: kept, real bite); it's
// confined to the Hollow by In Control! (config/incontrol/spawn.json).
// KubeJS server scripts share one scope: every top-level name here starts with "hollowRav".
const hollowRavHeightmap = Java.loadClass('net.minecraft.world.level.levelgen.Heightmap$Types')
const hollowRavBlockPos = Java.loadClass('net.minecraft.core.BlockPos')
const hollowRavDimension = 'strata:hollow'
const hollowRavEveryTicks = 1200
const hollowRavQuietMs = 3 * 60 * 1000
// [entity, chance per player per check, how many may already be near, "near" radius]
const hollowRavKinds = [
  ['the_ravenous:the_ravenous', 0.04, 0, 256],
  ['the_ravenous:the_screecher', 0.12, 2, 96],
]
let hollowRavTicks = 0

const hollowRavCount = (player, type, radius) => {
  const around = player.level.getEntities(player, player.boundingBox.inflate(radius))
  let n = 0
  for (let i = 0; i < around.size(); i++) if (String(around.get(i).type) === type) n++
  return n
}

const hollowRavSpawn = (player, type) => {
  const level = player.level
  for (let attempt = 0; attempt < 6; attempt++) {
    const angle = Math.random() * Math.PI * 2
    const dist = 48 + Math.random() * 24
    const x = Math.floor(player.x + Math.cos(angle) * dist)
    const z = Math.floor(player.z + Math.sin(angle) * dist)
    if (!level.isLoaded(new hollowRavBlockPos(x, 64, z))) continue
    const y = level.getHeight(hollowRavHeightmap.MOTION_BLOCKING_NO_LEAVES, x, z)
    const pos = new hollowRavBlockPos(x, y, z)
    if (!level.canSeeSky(pos)) continue
    if (!level.getBlockState(pos.below()).getFluidState().isEmpty()) continue
    player.server.runCommandSilent(`execute in ${hollowRavDimension} run summon ${type} ${x + 0.5} ${y} ${z + 0.5}`)
    return true
  }
  return false
}

ServerEvents.tick(event => {
  hollowRavTicks++
  if (hollowRavTicks < hollowRavEveryTicks) return
  hollowRavTicks = 0
  event.server.players.forEach(player => {
    const d = player.level.dimension
    if (String(d && d.location ? d.location() : d) !== hollowRavDimension) return
    if (player.isSpectator() || player.isCreative()) return
    const arrived = player.persistentData.getLong('strata_hollow_arrived')
    if (arrived > 0 && Date.now() - arrived < hollowRavQuietMs) return
    for (let i = 0; i < hollowRavKinds.length; i++) {
      const k = hollowRavKinds[i]
      if (Math.random() >= k[1]) continue
      if (hollowRavCount(player, k[0], k[3]) > k[2]) continue
      hollowRavSpawn(player, k[0])
    }
  })
})
