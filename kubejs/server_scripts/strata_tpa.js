// /tpa and /tpahere for every player (Darin, Oct 31: friends wanted it). /tpa <player> asks to go to
// them, /tpahere <player> asks them to come to you; the other player answers with /tpaccept or
// /tpdeny (or clicks the chat buttons). Works across dimensions. A request lasts 60 seconds, each
// player can have one open request to them at a time, and a player who has just teleported
// waits 10 seconds (the same as /home) before they can be teleported by /tpa again.
// Requests are kept in memory only: a restart clears them.
// KubeJS server scripts share one scope: every top-level name here starts with "tpa".
const tpaExpireMs = 60 * 1000
const tpaCooldownMs = 10 * 1000
const tpaEntityArgument = Java.loadClass('net.minecraft.commands.arguments.EntityArgument')

// target username -> { from: username, here: boolean, at: ms }
const tpaRequests = {}

const tpaDimensionOf = player => { const d = player.level.dimension; return String(d && d.location ? d.location() : d) }

// A clickable chat button; plain text if the click wrapper isn't there.
const tpaButton = (text, command, color) => {
  let t = Text.of(text).color(color)
  try { t = t.clickRunCommand(command).hover(Text.of(command)) } catch (e) { }
  return t
}

const tpaAsk = (ctx, here) => {
  const player = ctx.source.player
  if (!player) { ctx.source.sendFailure(Text.of('Only players can use this.')); return 0 }
  const target = tpaEntityArgument.getPlayer(ctx, 'player')
  if (String(target.username) === String(player.username)) {
    player.tell(Text.red("You can't send a request to yourself."))
    return 0
  }
  tpaRequests[String(target.username)] = { from: String(player.username), here: here, at: Date.now() }
  player.tell(Text.green(`Request sent to ${target.username}. It expires in 60 seconds.`))
  const ask = here ? `${player.username} wants you to teleport to them. ` : `${player.username} wants to teleport to you. `
  target.tell(Text.yellow(ask)
    .append(tpaButton('[Accept]', '/tpaccept', 0x55FF55))
    .append(Text.of(' '))
    .append(tpaButton('[Deny]', '/tpdeny', 0xFF5555)))
  return 1
}

// The request to this player, or null (expired requests are dropped).
const tpaTake = player => {
  const name = String(player.username)
  const req = tpaRequests[name]
  delete tpaRequests[name]
  if (!req || Date.now() - req.at > tpaExpireMs) {
    player.tell(Text.red('You have no teleport request (they expire after 60 seconds).'))
    return null
  }
  return req
}

ServerEvents.commandRegistry(event => {
  const { commands: Commands } = event

  event.register(Commands.literal('tpa')
    .then(Commands.argument('player', tpaEntityArgument.player()).executes(ctx => tpaAsk(ctx, false))))
  event.register(Commands.literal('tpahere')
    .then(Commands.argument('player', tpaEntityArgument.player()).executes(ctx => tpaAsk(ctx, true))))

  event.register(Commands.literal('tpaccept').executes(ctx => {
    const player = ctx.source.player
    if (!player) { ctx.source.sendFailure(Text.of('Only players can use this.')); return 0 }
    const req = tpaTake(player)
    if (!req) return 0
    const other = ctx.source.server.playerList.getPlayerByName(req.from)
    if (!other) { player.tell(Text.red(`${req.from} isn't online any more.`)); return 0 }
    const mover = req.here ? player : other
    const dest = req.here ? other : player
    const now = Date.now()
    const waitMs = mover.persistentData.getLong('strata_tpa_last') + tpaCooldownMs - now
    if (waitMs > 0) {
      player.tell(Text.yellow(`${mover.username} has to wait ${Math.ceil(waitMs / 1000)} more second(s) before teleporting again.`))
      return 0
    }
    ctx.source.server.runCommandSilent(`execute in ${tpaDimensionOf(dest)} run tp ${mover.username} ${dest.x} ${dest.y} ${dest.z} ${dest.yaw} ${dest.pitch}`)
    mover.persistentData.putLong('strata_tpa_last', now)
    other.tell(Text.green(`${player.username} accepted your request.`))
    mover.tell(Text.green(`Teleported to ${dest.username}.`))
    if (!req.here) player.tell(Text.green(`${mover.username} is here.`))
    return 1
  }))

  event.register(Commands.literal('tpdeny').executes(ctx => {
    const player = ctx.source.player
    if (!player) { ctx.source.sendFailure(Text.of('Only players can use this.')); return 0 }
    const req = tpaTake(player)
    if (!req) return 0
    player.tell(Text.gray('Request denied.'))
    const other = ctx.source.server.playerList.getPlayerByName(req.from)
    if (other) other.tell(Text.gray(`${player.username} denied your teleport request.`))
    return 1
  }))
})
