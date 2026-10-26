// Items taken out of play for the limited-teleport and no-cheap-flight rules (Darin, Oct 26;
// docs/gate-map.md section 5). "Super easy or cheap = I don't like it."
// - Draconic Evolution dislocators: cheap saved-spot and to-a-player (/tpa) teleports, and the
//   advanced one's unlimited waypoints. All four recipes removed.
// - Iron's Spells Recall (free warp to spawn): disabled in
//   config/irons_spellbooks_spell_config/irons_spellbooks/recall.json.
// - Artifacts' Helium Flamingo and Forsaken Relics' Wind Staff: cheap recharging flight, taken
//   out of every loot table (LootJS runs after other mods' loot modifiers, which is how Forsaken
//   Relics adds its relics to chests).
// Copies already in someone's inventory keep working; nothing is deleted from players.
// KubeJS server scripts share one scope: every top-level name here starts with "strataRemoved".
const strataRemovedRecipes = [
  'draconicevolution:tools/dislocator',
  'draconicevolution:tools/player_dislocator_unbound',
  'draconicevolution:tools/p2p_dislocator_unbound',
  'draconicevolution:tools/advanced_dislocator',
]
const strataRemovedLoot = ['artifacts:helium_flamingo', 'forsaken_relics:wind_staff']

ServerEvents.recipes(event => {
  strataRemovedRecipes.forEach(id => event.remove({ id: id }))
})

LootJS.modifiers(event => {
  event.addTableModifier(/.*/).removeLoot(strataRemovedLoot)
})
