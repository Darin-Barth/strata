// Pokémon world: the starter choice opens the first time a player enters pokeworld:pokeworld.
// config/cobblemon/starters.json turns off Cobblemon's on-join prompt (allowStarterOnJoin
// false, which also locks the starter for new players); /openstarterscreen unlocks it and
// opens the screen. Once per player, remembered in persistent data.
// Same helper as pokeworld_spawns.js (each script file has its own scope).
const starterDimensionId = level => { const d = level.dimension; return String(d && d.location ? d.location() : d) }

PlayerEvents.tick(event => {
  const player = event.player
  if (player.tickCount % 20 !== 0) return
  if (starterDimensionId(player.level) !== 'pokeworld:pokeworld') return
  if (player.persistentData.getBoolean('strata_starter_offered')) return
  player.persistentData.putBoolean('strata_starter_offered', true)
  event.server.runCommandSilent(`openstarterscreen ${player.username}`)
})
