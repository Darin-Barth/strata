// Teammates can't hurt each other (Darin, Oct 25, 2026). Damage between two players in the same
// FTB Teams party is cancelled: melee, arrows and other projectiles, spells, anything whose damage
// source traces back to a teammate. Players in different teams can still fight (Vampirism factions).
// Solo players each have their own player team, so they aren't protected from each other.
// KubeJS server scripts share one scope: every top-level name here starts with "teamProtect".
const teamProtectApi = Java.loadClass('dev.ftb.mods.ftbteams.api.FTBTeamsAPI')

EntityEvents.beforeHurt(event => {
  const victim = event.entity
  if (!victim || !victim.isPlayer()) return
  const attacker = event.source.actual
  if (!attacker || !attacker.isPlayer() || attacker === victim) return
  if (teamProtectApi.api().getManager().arePlayersInSameTeam(attacker.getUUID(), victim.getUUID())) {
    event.cancel()
  }
})
