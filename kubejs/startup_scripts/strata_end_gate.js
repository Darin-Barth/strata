// The End stays sealed until its portal is opened the intended way (Darin, Nov 17; docs/end-eyes.md).
//
// The eyes are the gate, but the pack is big and a portal block is not the only way into a dimension. An audit
// on Nov 17 found a Weeping Angels catacomb room with a working End portal in it, Oritech's particle accelerator
// making one, a chain that moved pre-filled vanilla frames with AE2 Spatial IO, and a mod's teleport packet.
// Those are closed one by one elsewhere; this is the rule behind them, for the ones nobody has found yet:
//
//   Until the End has been opened, no player can travel to minecraft:the_end by any means, except through an
//   End portal ringed by twelve End Remastered frames (endrem:ancient_portal_frame) that each hold an eye.
//   The first such crossing opens the End for good (server flag strata_end_open); after that every way in
//   works as the mods ship it (/tpa to a friend there, a teleporter, a waystone...).
//
// Ops are let through without opening it. /endgate (ops, server_scripts/strata_end_gate.js) shows, opens or
// closes the flag. A startup script so the listener is registered once; names start with "endGate".
const endGateKey = 'strata_end_open'
const endGateOffsets = [[-1, -2], [0, -2], [1, -2], [-1, 2], [0, 2], [1, 2], [-2, -1], [-2, 0], [-2, 1], [2, -1], [2, 0], [2, 1]]

const endGateIs = (level, BlockPos, x, y, z, name) => String(level.getBlockState(new BlockPos(x, y, z))).indexOf('Block{' + name + '}') === 0

// True if the player stands in a 3x3 End portal whose twelve frames are End Remastered's, each with its eye.
const endGateProperPortal = (player, BlockPos) => {
  const level = player.level
  const px = Math.floor(player.x), py = Math.floor(player.y), pz = Math.floor(player.z)
  let found = null
  for (let dy = -1; dy <= 1 && !found; dy++) {
    for (let dx = -1; dx <= 1 && !found; dx++) {
      for (let dz = -1; dz <= 1 && !found; dz++) {
        if (endGateIs(level, BlockPos, px + dx, py + dy, pz + dz, 'minecraft:end_portal')) found = [px + dx, py + dy, pz + dz]
      }
    }
  }
  if (!found) return false
  let x0 = found[0], y = found[1], z0 = found[2]
  for (let i = 0; i < 3 && endGateIs(level, BlockPos, x0 - 1, y, z0, 'minecraft:end_portal'); i++) x0--
  for (let i = 0; i < 3 && endGateIs(level, BlockPos, x0, y, z0 - 1, 'minecraft:end_portal'); i++) z0--
  const cx = x0 + 1, cz = z0 + 1
  for (let i = 0; i < endGateOffsets.length; i++) {
    let state = String(level.getBlockState(new BlockPos(cx + endGateOffsets[i][0], y, cz + endGateOffsets[i][1])))
    if (state.indexOf('Block{endrem:ancient_portal_frame}') !== 0 || state.indexOf('eye=true') < 0) return false
  }
  return true
}

const endGateSetup = () => {
  const Travel = Java.loadClass('net.neoforged.neoforge.event.entity.EntityTravelToDimensionEvent')
  const ServerPlayer = Java.loadClass('net.minecraft.server.level.ServerPlayer')
  const BlockPos = Java.loadClass('net.minecraft.core.BlockPos')
  const lastTold = {}
  NativeEvents.onEvent(Travel, event => {
    try {
      let player = event.getEntity()
      if (!(player instanceof ServerPlayer)) return
      if (String(event.getDimension().location()) !== 'minecraft:the_end') return
      let server = player.server
      if (server.persistentData.getBoolean(endGateKey)) return
      if (endGateProperPortal(player, BlockPos)) {
        server.persistentData.putBoolean(endGateKey, true)
        console.info(`End gate: opened by ${player.username} through a portal of twelve eyes`)
        server.tell(Text.lightPurple('The twelve eyes are set. The End is open.'))
        return
      }
      if (player.hasPermissions(2)) return
      event.setCanceled(true)
      let name = String(player.username), now = Date.now()
      if (!lastTold[name] || now - lastTold[name] > 5000) {
        lastTold[name] = now
        console.info(`End gate: refused ${name} at ${Math.floor(player.x)} ${Math.floor(player.y)} ${Math.floor(player.z)} in ${player.level.dimension}`)
        player.displayClientMessage(Text.lightPurple('The End is sealed. Its portal has to be opened with the twelve eyes first.').italic(), true)
      }
    } catch (e) {
      console.error(`End gate: ${e}`)
    }
  })
}

endGateSetup()
