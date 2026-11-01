// Sleeping bag key (Darin, Oct 31): the key (startup/client strata_sleeping_bag.js) lays the Comforts sleeping
// bag from the player's Curios "sleeping_bag" slot just in front of them (a block can't go where they stand), facing where they look, and sleeps in it, the
// same as placing it by hand (Comforts' autoUse). When they wake (or it was the wrong time to sleep) the bag is
// packed back into the slot. Comforts' own rules still apply: night only, monsters nearby, the Hollow's beds.
// KubeJS server scripts share one scope: every top-level name here starts with "sleepingBag".
const sleepingBagCurios = Java.loadClass('top.theillusivec4.curios.api.CuriosApi')
const sleepingBagHand = Java.loadClass('net.minecraft.world.InteractionHand')
const sleepingBagDir = Java.loadClass('net.minecraft.core.Direction')
const sleepingBagHit = Java.loadClass('net.minecraft.world.phys.BlockHitResult')
const sleepingBagVec = Java.loadClass('net.minecraft.world.phys.Vec3')
const sleepingBagPos = Java.loadClass('net.minecraft.core.BlockPos')
const sleepingBagSlot = 'sleeping_bag'

// The slot's item handler, or null.
const sleepingBagStacks = player => {
  const inv = sleepingBagCurios.getCuriosInventory(player).orElse(null)
  if (!inv) return null
  const handler = inv.getStacksHandler(sleepingBagSlot).orElse(null)
  return handler ? handler.getStacks() : null
}

const sleepingBagDimensionOf = player => { const d = player.level.dimension; return String(d && d.location ? d.location() : d) }

NetworkEvents.dataReceived('strata_sleeping_bag', event => {
  const player = event.player
  if (!player || player.isSleeping() || player.isSpectator()) return
  const data = player.persistentData
  if (data.contains('strata_bag_item')) return
  const stacks = sleepingBagStacks(player)
  const bag = stacks ? stacks.getStackInSlot(0) : null
  if (!bag || bag.isEmpty()) {
    player.displayClientMessage(Text.gray('Put a sleeping bag in your Sleeping Bag slot first.'), true)
    return
  }
  if (!player.onGround()) {
    player.displayClientMessage(Text.gray('You need solid ground to lay out your sleeping bag.'), true)
    return
  }
  // Use the bag on the top of the block in front of the player, from the main hand (Comforts reads the item
  // from the hand), then put back whatever the player was holding.
  const spot = player.blockPosition().relative(player.getDirection())
  const below = spot.below()
  const held = player.mainHandItem.copy()
  const id = String(bag.id)
  player.setItemInHand(sleepingBagHand.MAIN_HAND, bag.copy())
  const hit = new sleepingBagHit(new sleepingBagVec(below.x + 0.5, below.y + 1.0, below.z + 0.5), sleepingBagDir.UP, below, false)
  player.gameMode.useItemOn(player, player.level, player.mainHandItem, sleepingBagHand.MAIN_HAND, hit)
  const placed = player.mainHandItem.isEmpty()
  player.setItemInHand(sleepingBagHand.MAIN_HAND, held)
  if (!placed) {
    player.displayClientMessage(Text.gray('No room to lay out your sleeping bag here: it needs two clear blocks of flat ground in front of you.'), true)
    return
  }
  stacks.setStackInSlot(0, Item.empty)
  data.putString('strata_bag_item', id)
  data.putString('strata_bag_dim', sleepingBagDimensionOf(player))
  data.putLong('strata_bag_pos', spot.asLong())
  data.putInt('strata_bag_wait', 2)
})

// Pack the bag up once the player is out of it (checked every half second; the first check waits a second, so
// Comforts has time to put them to sleep).
PlayerEvents.tick(event => {
  const player = event.player
  if (player.tickCount % 10 !== 0) return
  const data = player.persistentData
  if (!data.contains('strata_bag_item') || player.isSleeping()) return
  const wait = data.getInt('strata_bag_wait')
  if (wait > 0) { data.putInt('strata_bag_wait', wait - 1); return }
  if (data.getString('strata_bag_dim') !== sleepingBagDimensionOf(player)) return
  const id = data.getString('strata_bag_item')
  const pos = sleepingBagPos.of(data.getLong('strata_bag_pos'))
  data.remove('strata_bag_item')
  data.remove('strata_bag_dim')
  data.remove('strata_bag_pos')
  data.remove('strata_bag_wait')
  const block = player.level.getBlock(pos)
  // Broken or moved meanwhile: the player already has the dropped bag.
  if (!String(block.id).startsWith('comforts:sleeping_bag')) return
  const props = block.properties
  const facing = sleepingBagDir.valueOf(String(props.get('facing')).toUpperCase())
  const other = String(props.get('part')) === 'foot' ? pos.relative(facing) : pos.relative(facing.getOpposite())
  if (String(player.level.getBlock(other).id) === String(block.id)) player.level.getBlock(other).set('minecraft:air')
  block.set('minecraft:air')
  const stacks = sleepingBagStacks(player)
  if (stacks && stacks.getStackInSlot(0).isEmpty()) stacks.setStackInSlot(0, Item.of(id))
  else player.give(Item.of(id))
})
