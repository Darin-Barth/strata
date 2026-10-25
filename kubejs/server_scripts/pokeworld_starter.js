// Pokémon world: the starter choice opens when a player who has no starter yet is in
// pokeworld:pokeworld. config/cobblemon/starters.json turns off Cobblemon's on-join prompt
// (allowStarterOnJoin false, which also locks the starter for new players); /openstarterscreen
// unlocks it and opens the screen. It opens at most once per login, so closing it without
// choosing brings it back on the next visit after logging in again; Cobblemon's own
// "starter selected" flag stops it for good once a starter is picked.
// KubeJS server scripts share one scope and pokeworld_spawns.js already declares 'Cobblemon'.
const CobblemonMain = Java.loadClass('com.cobblemon.mod.common.Cobblemon')
const starterOfferedThisLogin = new Set()

// Same helper as pokeworld_spawns.js (each script file has its own scope).
const starterDimensionId = level => { const d = level.dimension; return String(d && d.location ? d.location() : d) }

PlayerEvents.loggedOut(event => {
  starterOfferedThisLogin.delete(String(event.player.uuid))
})

PlayerEvents.tick(event => {
  const player = event.player
  if (player.tickCount % 20 !== 0) return
  if (starterDimensionId(player.level) !== 'pokeworld:pokeworld') return
  const uuid = String(player.uuid)
  if (starterOfferedThisLogin.has(uuid)) return
  starterOfferedThisLogin.add(uuid)
  if (CobblemonMain.INSTANCE.getPlayerDataManager().getGenericData(player).getStarterSelected()) return
  event.server.runCommandSilent(`openstarterscreen ${player.username}`)
})
