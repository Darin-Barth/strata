// Boss loot bags (server_scripts/strata_boss_bags.js): every player who hits a boss gets one when it
// dies, holding their own roll of its loot. Stacks to 1 so each bag keeps its own contents. Each boss
// has its own bag texture (kubejs/assets/strata/models/item/boss_bag.json, tools/build_boss_bags.py).
StartupEvents.registry('item', event => {
  event.create('strata:boss_bag').displayName('Boss Loot Bag').maxStackSize(1).rarity('epic')
    .tooltip(Text.gray('Right-click to open'))
})
