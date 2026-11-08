// /spawn for every player (Darin, Nov 8): back to the world spawn (the Tavern village) from any
// dimension, with the same 10-second cooldown as /home (its own timer). Server-only.
// KubeJS server scripts share one scope: every top-level name here starts with "spawnCmd".
const spawnCmdCooldownMs = 10 * 1000

ServerEvents.commandRegistry(event => {
  const { commands: Commands } = event

  event.register(Commands.literal('spawn').executes(ctx => {
    const player = ctx.source.player
    if (!player) { ctx.source.sendFailure(Text.of('Only players can use this.')); return 0 }
    const data = player.persistentData
    const now = Date.now()
    const waitMs = data.getLong('strata_spawn_last') + spawnCmdCooldownMs - now
    if (waitMs > 0) {
      player.tell(Text.yellow(`/spawn is on cooldown for ${Math.ceil(waitMs / 1000)} more second(s).`))
      return 0
    }
    const server = ctx.source.server
    const pos = server.overworld().getSharedSpawnPos()
    const x = pos.getX() + 0.5, y = pos.getY(), z = pos.getZ() + 0.5
    server.runCommandSilent(`execute in minecraft:overworld run tp ${player.username} ${x} ${y} ${z}`)
    data.putLong('strata_spawn_last', now)
    player.tell(Text.green('Back at spawn.'))
    return 1
  }))
})
