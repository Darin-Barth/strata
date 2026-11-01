// The sleeping bag key (startup_scripts/strata_sleeping_bag.js) asks the server to lay out the bag in the
// player's sleeping bag slot (server_scripts/strata_sleeping_bag.js).
KeyBindEvents.pressed('sleeping_bag', event => {
  if (!Client.screen) event.player.sendData('strata_sleeping_bag', {})
})
