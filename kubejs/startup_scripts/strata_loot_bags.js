// Quest loot bags (server_scripts/strata_loot_bags.js): quests give one; opening it rolls a rarity, then
// one item from that rarity's pool. Bigger quests give bigger bags with better odds
// (tools/build_quest_bags.py). Textures in kubejs/assets/strata/textures/item/.
StartupEvents.registry('item', event => {
  ;[
    // id, name, name colour, enchantment glint (the textures also sparkle more by tier)
    ['strata:loot_bag_small', 'Small Loot Bag', 'common', false],
    ['strata:loot_bag', 'Loot Bag', 'uncommon', false],
    ['strata:loot_bag_large', 'Large Loot Bag', 'rare', true],
    ['strata:loot_bag_grand', 'Grand Loot Bag', 'epic', true],
  ].forEach(b => {
    event.create(b[0]).displayName(b[1]).rarity(b[2]).glow(b[3])
      .tooltip(Text.gray('Right-click to open: Common, Uncommon, Rare, Epic or Legendary loot'))
  })
})
