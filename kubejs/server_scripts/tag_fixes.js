// Tag entries that point at items a mod never registers. One missing reference makes the whole tag fail to load,
// and every tag that includes it fails too (Oct 25: 21 tags, including minecraft:hoes, minecraft:enchantable/*
// and c:tools, which would break enchanting tools).

ServerEvents.tags('item', event => {
  // Apocalyptic Bosses 3.6 (panascraftrpgmod) lists a hoe it doesn't register in 1.21.1.
  event.remove('minecraft:hoes', 'panascraftrpgmod:the_king_of_the_abyss_hoe')
  // Elytra Slot 9.0.2 (its newest) reads a Deeper and Darker 1.3 config field that 1.4 removed, so
  // the soul elytra's boost errors when worn in the Elytra Slot. Keep it out of that slot; worn in
  // the chest slot its boost works.
  event.remove('elytraslot:elytra', 'deeperdarker:soul_elytra')
})
