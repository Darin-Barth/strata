// Panascraft RPG 3.6 infinite loot fix (Darin, Nov 6). When an Echo King or Sculk Sentinel dies, the mod runs
// "setblock ~ ~ ~ chest{LootTable:...} destroy" where it died (MiniBossDefeated + BossDefeated procedures: totems,
// enchanted golden apples, diamond apples, echo shards...), and Lootr turns that chest into a per-player Lootr chest.
// Both mobs only come from the mob spawners in the Silence Death dungeon (silencedeath_dungeonv3: two of each; no
// natural spawns, no other structure), so that dungeon handed out unlimited reward chests (found Nov 6). One tick
// after either dies, this removes the chest its death placed. Their own drops (diamond apples, sculk catalysts) stay,
// and the dungeon's own Lootr chests and the Silence Death boss's reward are untouched. The setblock's "destroy" still
// breaks the block the mob died on. Re-check after a Panascraft update (which mobs call those procedures, and whether
// any spawner or natural spawn adds a chest-dropping mob).
// KubeJS server scripts share one scope: every top-level name here starts with "spawnerChests".
let spawnerChestsMobs = ['panascraftrpgmod:echo_king', 'panascraftrpgmod:sculk_sentinel']
let spawnerChestsBlocks = ['minecraft:chest', 'lootr:lootr_chest']

EntityEvents.death(event => {
  let entity = event.entity
  if (spawnerChestsMobs.indexOf(String(entity.type)) < 0) return
  let level = entity.level
  let x = Math.floor(entity.x)
  let y = Math.floor(entity.y)
  let z = Math.floor(entity.z)
  event.server.scheduleInTicks(1, () => {
    let block = level.getBlock(x, y, z)
    if (spawnerChestsBlocks.indexOf(String(block.id)) < 0) return
    block.set('minecraft:air')
  })
})
