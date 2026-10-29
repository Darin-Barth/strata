// Simple Voice Chat polls its push-to-talk and whisper keys every tick in a world; with either key unbound the
// game logs "Invalid key -1" every tick and stutters. The pack's default layout
// (config/defaultoptions/keybindings.txt) only reaches new installs, so on joining a world this binds either key
// back to the pack default if it's unbound, and saves. A key the player set to something else is left alone.
// (Not at script load: mods register their keys later. Not on the title screen: KubeJS client ticks start in a world.)
// KubeJS client scripts share one scope: every top-level name here starts with "strataVoiceKeys".
const strataVoiceKeysInput = Java.loadClass('com.mojang.blaze3d.platform.InputConstants')
const strataVoiceKeysMapping = Java.loadClass('net.minecraft.client.KeyMapping')
const strataVoiceKeysDefaults = { 'key.push_to_talk': 'key.keyboard.caps.lock', 'key.whisper': 'key.keyboard.right.alt' }

ClientEvents.loggedIn(event => {
  try {
    strataVoiceKeysFix()
  } catch (e) {
    console.error('Voice chat key check failed: ' + e)
  }
})

function strataVoiceKeysFix() {
  const options = Client.options
  const mappings = options.keyMappings
  let changed = 0
  for (let i = 0; i < mappings.length; i++) {
    let m = mappings[i]
    let target = strataVoiceKeysDefaults[String(m.getName())]
    if (!target || !m.isUnbound()) continue
    m.setKey(strataVoiceKeysInput.getKey(target))
    changed++
  }
  if (!changed) return
  strataVoiceKeysMapping.resetMapping()
  options.save()
  console.info('Voice chat: bound ' + changed + ' unbound voice key(s) to the pack defaults')
}
