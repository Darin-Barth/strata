// Sleeping bag key (Darin, Oct 31): a Comforts sleeping bag in its own Curios slot is laid out and slept in with
// one key. The slot is kubejs/data/strata/curios; the key is sent to server_scripts/strata_sleeping_bag.js by
// client_scripts/strata_sleeping_bag.js. Its default (Alt+S) is in config/defaultoptions/keybindings.txt.
if (Platform.isClientEnvironment()) {
  KeyBindEvents.registry(event => {
    let key = event.register('sleeping_bag')
    try { key.category('key.categories.inventory') } catch (e) { console.warn('Sleeping bag key category: ' + e) }
  })
}
