// The Hollow (strata:hollow), the horror dimension: recipe, arrival tracking, beds, Grim & Bleak's
// own realm portal, and Hollow Ember drops. Design: docs/hollow-design.md.
// KubeJS server scripts share one scope: every top-level name here starts with "hollow".
const hollowDimensionId = 'strata:hollow'
const hollowHorrorNamespaces = ['cave_dweller', 'weeping_angels', 'whispering_spirits', 'the_ravenous',
  'grim_and_bleak', 'graveyard', 'mutantmonsters', 'sanity_renewed']
const hollowBosses = ['graveyard:lich', 'grim_and_bleak:gate_guardian']
const hollowDimensionOf = entity => { const d = entity.level.dimension; return String(d && d.location ? d.location() : d) }
const hollowIn = entity => hollowDimensionOf(entity) === hollowDimensionId

ServerEvents.recipes(event => {
  // The Pale Lantern lights a resin-brick portal frame. The Creaking Heart needs Silk Touch and
  // ends that Pale Garden's resin supply; the soul lantern means a Nether trip first.
  event.shaped('strata:pale_lantern', [
    ' R ',
    'RHR',
    ' L ',
  ], {
    R: 'minecraft:resin_clump',
    H: 'minecraft:creaking_heart',
    L: 'minecraft:soul_lantern',
  }).id('strata:pale_lantern')
})

// Arrival time (for the damage-cap grace period, startup_scripts/hollow_damage_cap.js) and
// the dread events' quiet start (hollow_dread.js). Cleared on leaving.
PlayerEvents.tick(event => {
  const player = event.player
  if (player.age % 10 !== 0) return
  const data = player.persistentData
  if (hollowIn(player)) {
    if (!data.getBoolean('strata_hollow_inside')) {
      data.putBoolean('strata_hollow_inside', true)
      data.putLong('strata_hollow_arrived', Date.now())
    }
  } else if (data.getBoolean('strata_hollow_inside')) {
    data.putBoolean('strata_hollow_inside', false)
    data.putLong('strata_hollow_arrived', 0)
  }
})

BlockEvents.rightClicked(event => {
  const player = event.player
  if (!player) return
  // No sleeping in the Hollow (it's always night there anyway).
  if (hollowIn(player) && event.block.id.endsWith('_bed')) {
    player.displayClientMessage(Text.darkGray("You can't sleep here. Something is watching you.").italic(), true)
    event.cancel()
    return
  }
  // Grim & Bleak's Soulsrealm biomes live in the Hollow now; its own chiseled-deepslate portal
  // (lit with the Compass of pain) stays closed.
  if (player.mainHandItem.id === 'grim_and_bleak:soulsrealm' || player.offHandItem.id === 'grim_and_bleak:soulsrealm') {
    player.displayClientMessage(Text.darkGray('The compass points nowhere. Limbo has been swallowed by the Hollow.').italic(), true)
    event.cancel()
  }
})

// TorchMaster's Mega Torch stops every natural spawn in a 64-block radius, which would switch the
// Hollow off around a base (Darin, Oct 26). The Pale Beacon is the Hollow's own safe zone.
BlockEvents.placed('torchmaster:megatorch', event => {
  if (!event.player || !hollowIn(event.player)) return
  event.player.displayClientMessage(Text.darkGray('The flame gutters out. Light alone won\'t hold the Hollow back.').italic(), true)
  event.cancel()
})

// Hollow Ember: dropped by horror mobs killed by a player in the Hollow (and found in its chests,
// kubejs/data/strata/loot_modifiers/hollow_ember).
EntityEvents.death(event => {
  const entity = event.entity
  const player = event.source.player
  if (!player || !hollowIn(entity)) return
  const id = String(entity.type)
  if (hollowHorrorNamespaces.indexOf(id.split(':')[0]) < 0) return
  let count = 0
  if (hollowBosses.indexOf(id) >= 0) count = 3 + Math.floor(Math.random() * 3)
  else if (id.startsWith('mutantmonsters:')) count = Math.random() < 0.5 ? 1 + Math.floor(Math.random() * 2) : 0
  else count = Math.random() < 0.15 ? 1 : 0
  if (count <= 0) return
  event.server.runCommandSilent(`execute in ${hollowDimensionId} run summon minecraft:item ${entity.x} ${entity.y + 0.5} ${entity.z} {Item:{id:"strata:hollow_ember",count:${count}}}`)
})
