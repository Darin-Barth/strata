// /sethome and /home for every player (Darin, Oct 25, 2026): one home each, any dimension,
// 10-second cooldown after each /home. The home lives in the player's KubeJS persistent data,
// so it survives logouts, deaths and server restarts.
// KubeJS server scripts share one scope: every top-level name here starts with "home".
const homeCooldownMs = 10 * 1000

const homeDimensionOf = player => { const d = player.level.dimension; return String(d && d.location ? d.location() : d) }

ServerEvents.commandRegistry(event => {
  const { commands: Commands } = event

  event.register(Commands.literal('sethome').executes(ctx => {
    const player = ctx.source.player
    if (!player) { ctx.source.sendFailure(Text.of('Only players can use this.')); return 0 }
    const data = player.persistentData
    data.putString('strata_home_dim', homeDimensionOf(player))
    data.putDouble('strata_home_x', player.x)
    data.putDouble('strata_home_y', player.y)
    data.putDouble('strata_home_z', player.z)
    data.putFloat('strata_home_yaw', player.yaw)
    data.putFloat('strata_home_pitch', player.pitch)
    player.tell(Text.green(`Home set at ${Math.floor(player.x)}, ${Math.floor(player.y)}, ${Math.floor(player.z)}.`))
    return 1
  }))

  event.register(Commands.literal('home').executes(ctx => {
    const player = ctx.source.player
    if (!player) { ctx.source.sendFailure(Text.of('Only players can use this.')); return 0 }
    const data = player.persistentData
    if (!data.contains('strata_home_dim')) {
      player.tell(Text.red('You have no home yet. Use /sethome first.'))
      return 0
    }
    const now = Date.now()
    const waitMs = data.getLong('strata_home_last') + homeCooldownMs - now
    if (waitMs > 0) {
      player.tell(Text.yellow(`/home is on cooldown for ${Math.ceil(waitMs / 1000)} more second(s).`))
      return 0
    }
    const x = data.getDouble('strata_home_x'), y = data.getDouble('strata_home_y'), z = data.getDouble('strata_home_z')
    const yaw = data.getFloat('strata_home_yaw'), pitch = data.getFloat('strata_home_pitch')
    ctx.source.server.runCommandSilent(`execute in ${data.getString('strata_home_dim')} run tp ${player.username} ${x} ${y} ${z} ${yaw} ${pitch}`)
    data.putLong('strata_home_last', now)
    player.tell(Text.green('Welcome home.'))
    return 1
  }))
})
