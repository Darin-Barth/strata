// The Hollow's progression (docs/hollow-progression.md): the Pale Beacon, its safe zone, and the
// Lost Signal story pages. Behaviour: server_scripts/hollow_beacon.js; textures: tools/build_hollow_beacon.py.
StartupEvents.registry('block', event => {
  // Lit: the safe zone is on. Fed one Hollow Ember per in-game day; when it runs out the server
  // swaps it for the dormant block below (same item, no safe zone).
  event.create('strata:pale_beacon').displayName('Pale Beacon').soundType('amethyst').mapColor('color_light_gray')
    .hardness(5).resistance(1200).requiresTool(true).tagBlock(['minecraft:mineable/pickaxe']).lightLevel(1)
  event.create('strata:pale_beacon_dormant').displayName('Pale Beacon').soundType('amethyst').mapColor('color_gray')
    .hardness(5).resistance(1200).requiresTool(true).tagBlock(['minecraft:mineable/pickaxe']).lightLevel(0.2)
    .noItem().noDrops()
})

StartupEvents.registry('item', event => {
  // The Pale Survey's log, found page by page in the Hollow's chests (server_scripts/hollow_beacon.js).
  for (let i = 1; i <= 6; i++) {
    event.create(`strata:pale_survey_page_${i}`).displayName(`Pale Survey Log, Page ${i}`).rarity('uncommon')
      .maxStackSize(1).tooltip(Text.gray('Its text is in the quest book: The Hollow, Lost Signal'))
  }
})
