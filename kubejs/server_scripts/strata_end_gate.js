// /endgate for ops: the switch behind startup_scripts/strata_end_gate.js (the End stays sealed until its portal
// is opened with twelve eyes). `/endgate` shows the state, `/endgate open` and `/endgate close` set it.
// KubeJS server scripts share one scope: every top-level name here starts with "endGateCmd".
const endGateCmdKey = 'strata_end_open'

ServerEvents.commandRegistry(event => {
  const { commands: Commands } = event
  const show = ctx => {
    const open = ctx.source.server.persistentData.getBoolean(endGateCmdKey)
    ctx.source.sendSystemMessage(Text.of(open ? 'The End is open.' : 'The End is sealed (no portal of twelve eyes has been crossed yet).'))
    return 1
  }
  const set = (ctx, open) => {
    ctx.source.server.persistentData.putBoolean(endGateCmdKey, open)
    ctx.source.sendSystemMessage(Text.of(open ? 'The End is now open to everyone.' : 'The End is sealed again.'))
    return 1
  }
  event.register(Commands.literal('endgate').requires(source => source.hasPermission(2))
    .executes(show)
    .then(Commands.literal('open').executes(ctx => set(ctx, true)))
    .then(Commands.literal('close').executes(ctx => set(ctx, false))))
})
