// Vampirism coffins in an Ars Nouveau Planarium (Darin, Nov 1). The Planarium turns sleep down with a reason that has
// no message text, the coffin sends that empty message on, and the server kicks the player ("Failed to encode packet
// 'clientbound/minecraft:system_chat'"). So a coffin inside a Planarium refuses sleep itself. Shift + right-click
// (open or close the lid) still works. Planarium dimensions are ars_nouveau:<uuid>.
BlockEvents.rightClicked(event => {
  if (!String(event.block.id).startsWith('vampirism:coffin')) return
  if (!String(event.level.dimension).startsWith('ars_nouveau:')) return
  if (event.player.isShiftKeyDown()) return
  event.player.displayClientMessage(Text.gray("You can't sleep in a coffin inside a Planarium."), true)
  event.cancel()
})
