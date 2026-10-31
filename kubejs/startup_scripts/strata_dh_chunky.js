// Distant Horizons 3.3.3 + Chunky on a NeoForge server crash on boot: on the first chunk load DH binds to
// Chunky's API (ChunkyProvider.get()), but Chunky only registers that API once the server has started,
// after the spawn area and force-loaded chunks are loaded ("Chunky is not loaded").
// DH marks the binding as done before it calls Chunky, so trying it once when a level loads (DH has set up
// its Chunky hook by then; no chunk is loaded yet) makes DH skip it for good. The only loss: DH doesn't
// refresh LODs live from Chunky's progress events during a Chunky pregen run.
// Remove this once a DH update fixes the order (check: boot a server with both and no crash).
let strataDhChunkyDone = false

NativeEvents.onEvent('net.neoforged.neoforge.event.level.LevelEvent$Load', event => {
  if (strataDhChunkyDone || event.level.isClientSide()) return
  strataDhChunkyDone = true
  strataDhChunkySkip()
})

function strataDhChunkySkip() {
  let chunky = null
  try {
    let injector = Java.loadClass('com.seibel.distanthorizons.core.dependencyInjection.ModAccessorInjector')
    chunky = injector.INSTANCE.get(Java.loadClass('com.seibel.distanthorizons.core.wrapperInterfaces.modAccessor.IChunkyAccessor'))
  } catch (e) {
    console.info('Distant Horizons not found, nothing to do (' + e + ')')
    return
  }
  if (!chunky) {
    console.info('Distant Horizons: no Chunky on this side, nothing to do')
    return
  }
  try {
    chunky.tryRunFirstTimeSetup()
    console.info('Distant Horizons is bound to Chunky')
  } catch (e) {
    console.info('Distant Horizons: Chunky binding skipped before boot (Chunky starts later), so DH cannot crash the boot')
  }
}
