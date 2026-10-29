// No terrain damage from mobs: creeper explosions (vanilla and any modded creeper) still hurt
// players and mobs but break no blocks. Endermen can't pick up blocks at all: the block tag
// minecraft:enderman_holdable is emptied in kubejs/data/minecraft/tags/block/enderman_holdable.json.
LevelEvents.afterExplosion(event => {
  const exploder = event.exploder
  if (exploder && String(exploder.type).indexOf('creeper') >= 0) event.removeAllAffectedBlocks()
})
