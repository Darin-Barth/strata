// Pokémon world: the starter choice opens the first time a player enters pokeworld:pokeworld.
// config/cobblemon/starters.json turns off Cobblemon's on-join prompt (allowStarterOnJoin
// false, which also locks the starter for new players); /openstarterscreen unlocks it and
// opens the screen. Once per player, remembered in persistent data.
const POKEWORLD = 'pokeworld:pokeworld'

PlayerEvents.tick(event => {
  const player = event.player
  if (player.age % 20 !== 0) return
  if (String(player.level.dimension.location()) !== POKEWORLD) return
  if (player.persistentData.getBoolean('strata_starter_offered')) return
  player.persistentData.putBoolean('strata_starter_offered', true)
  event.server.runCommandSilent(`openstarterscreen ${player.username}`)
})
