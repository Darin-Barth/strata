// Friends can't hurt each other (Darin, Oct 25, 2026). Damage between two players is cancelled when
// they are in the same FTB Teams party OR either team lists the other player as an ally. Allies keep
// separate teams, so their FTB Quests progress stays separate. Covers melee, arrows and other
// projectiles, spells: anything whose damage source traces back to the other player. Everyone else
// can still fight (Vampirism factions).
// KubeJS server scripts share one scope: every top-level name here starts with "teamProtect".
const teamProtectApi = Java.loadClass('dev.ftb.mods.ftbteams.api.FTBTeamsAPI')

const teamProtectFriendly = (attacker, victim) => {
  const manager = teamProtectApi.api().getManager()
  if (manager.arePlayersInSameTeam(attacker.getUUID(), victim.getUUID())) return true
  // FTB Teams allies are one-way (a team adds players as allies), so either direction counts.
  const allied = (player, other) => {
    const team = manager.getTeamForPlayerID(player.getUUID()).orElse(null)
    return team != null && team.getRankForPlayer(other.getUUID()).isAllyOrBetter()
  }
  return allied(victim, attacker) || allied(attacker, victim)
}

EntityEvents.beforeHurt(event => {
  const victim = event.entity
  if (!victim || !victim.isPlayer()) return
  const attacker = event.source.actual
  if (!attacker || !attacker.isPlayer() || attacker === victim) return
  if (teamProtectFriendly(attacker, victim)) event.cancel()
})
