// Strata balance patch (docs/balance-patch.md, Darin's answers Oct 27). Recipe count changes are
// generated into kubejs/data by tools/build_balance.py; config changes ship in config/. This file
// holds what needs a script.
// KubeJS server scripts share one scope: every top-level name here starts with "strataBalance".

// D2: Theurgy's reformation turned iron and gold sulfur into Ad Astra's desh and ostrum, skipping
// the Moon and Mars. Those four recipes go; desh and ostrum ore you mined still liquefy as usual.
const strataBalanceRemovedRecipes = [
  'theurgy:reformation/alchemical_sulfur_desh_from_alchemical_sulfurs_metals_common',
  'theurgy:reformation/alchemical_sulfur_desh_from_alchemical_niter_metals_common',
  'theurgy:reformation/alchemical_sulfur_ostrum_from_alchemical_sulfurs_metals_rare',
  'theurgy:reformation/alchemical_sulfur_ostrum_from_alchemical_niter_metals_rare',
]

ServerEvents.recipes(event => {
  strataBalanceRemovedRecipes.forEach(id => event.remove({ id: id }))
})

// F1: the Charm of Sinking (Reliquified Artifacts) gives damage reduction per block of water
// above you and immortality on the seabed, which makes the Abyssal Plain harmless (it has 80-500
// blocks of water). It doesn't work there: worn in the Plain, it comes off into your inventory.
const strataBalanceCurios = Java.loadClass('top.theillusivec4.curios.api.CuriosApi')
const strataBalanceCharm = 'artifacts:charm_of_sinking'
const strataBalancePlain = 'strata:abyssal_plain'

PlayerEvents.tick(event => {
  const player = event.player
  if (player.tickCount % 40 !== 0 || String(player.level.dimension) !== strataBalancePlain) return
  strataBalanceUnequipCharm(player)
})

function strataBalanceUnequipCharm(player) {
  try {
    let inventory = strataBalanceCurios.getCuriosInventory(player)
    if (!inventory.isPresent()) return
    let curios = inventory.get().getCurios()
    curios.forEach((slot, handler) => {
      let stacks = handler.getStacks()
      for (let i = 0; i < stacks.getSlots(); i++) {
        let stack = stacks.getStackInSlot(i)
        if (stack.isEmpty() || String(stack.id) !== strataBalanceCharm) continue
        stacks.setStackInSlot(i, Item.empty)
        player.give(stack)
        player.displayClientMessage(Text.aqua('The Charm of Sinking goes quiet this deep. It has no power in the Abyssal Plain.').italic(), true)
      }
    })
  } catch (e) {
    console.warn(`strata_balance: Charm of Sinking check failed: ${e}`)
  }
}
