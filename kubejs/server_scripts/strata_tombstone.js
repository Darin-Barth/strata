// Corail Tombstone's player teleport commands are ops-only (limited-teleport rule, Darin Oct 27):
// /tbrequestteleport + /tbacceptteleport would be a /tpa, /tbteleportdeath a free trip to your last death.
// The Grave's Key still teleports you to your grave (Darin's call). Its teleport tablets are switched off
// in config/tombstone-server.toml.
// KubeJS server scripts share one scope: every top-level name here starts with "tombstone".
const tombstoneOpsOnly = ['tbrequestteleport', 'tbacceptteleport', 'tbteleportdeath', 'tbteleport']

ServerEvents.command(event => {
  if (tombstoneOpsOnly.indexOf(String(event.commandName)) < 0) return
  const source = event.parseResults.context.source
  if (source.hasPermission(2)) return
  source.sendFailure(Text.red('Teleport commands are turned off on Strata.'))
  event.cancel()
})
