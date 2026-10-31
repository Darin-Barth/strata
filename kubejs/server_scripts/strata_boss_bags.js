// Boss loot bags: a boss fight is a group event, so everyone who fought gets their own full share.
// Every player who hits a boss (entity tag strata:boss_bags) in the 10 minutes before it dies gets a
// Boss Loot Bag in their inventory when it dies. Each bag holds that player's own roll of the boss's
// loot table, and nothing drops on the floor. The player who lands the killing blow (or else the last
// player to hit it) gets the boss's actual drops, so drops that other mods add at death (affix gear,
// gems) still reach someone; everyone else gets a fresh roll of the loot table with themselves as the
// killer. Loot modifiers (Strata's pet and gate drops) run in both cases. XP orbs drop as usual.
// Bosses killed with no player hits drop normally. Solo kills work the same, just in one bag.
const bossBagLootParams = Java.loadClass('net.minecraft.world.level.storage.loot.LootParams$Builder')
const bossBagParams = Java.loadClass('net.minecraft.world.level.storage.loot.parameters.LootContextParams')
const bossBagParamSets = Java.loadClass('net.minecraft.world.level.storage.loot.parameters.LootContextParamSets')
const bossBagContents = Java.loadClass('net.minecraft.world.item.component.ItemContainerContents')
const bossBagComponents = Java.loadClass('net.minecraft.core.component.DataComponents')
const bossBagTagKey = Java.loadClass('net.minecraft.tags.TagKey')
const bossBagRegistries = Java.loadClass('net.minecraft.core.registries.Registries')
const bossBagRL = Java.loadClass('net.minecraft.resources.ResourceLocation')
const bossBagTypes = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries').ENTITY_TYPE
const bossBagStack = Java.loadClass('net.minecraft.world.item.ItemStack')
const bossBagModelData = Java.loadClass('net.minecraft.world.item.component.CustomModelData')
const bossBagTag = bossBagTagKey.create(bossBagRegistries.ENTITY_TYPE, bossBagRL.parse('strata:boss_bags'))
const bossBagWindowMs = 10 * 60 * 1000
const bossBagMaxStacks = 256
// boss UUID -> { player UUID: time of their last hit }
const bossBagFighters = {}
// Entity type IDs in strata:boss_bags, read from the registry on first use (tags are bound by then).
// KubeJS gives entity.type as an ID string.
let bossBagIds = null

function bossBagEntityType(entity) {
  return bossBagTypes.get(bossBagRL.parse(String(entity.type)))
}

function bossBagIsBoss(entity) {
  if (bossBagIds === null) {
    bossBagIds = {}
    let named = bossBagTypes.getTag(bossBagTag)
    if (named.isPresent()) {
      let it = named.get().iterator()
      while (it.hasNext()) bossBagIds[String(it.next().unwrapKey().get().location())] = true
    }
    console.info(`strata_boss_bags: ${Object.keys(bossBagIds).length} boss types`)
  }
  return bossBagIds[String(entity.type)] === true
}

EntityEvents.afterHurt(event => {
  const boss = event.entity
  if (!bossBagIsBoss(boss)) return
  const attacker = event.source.actual
  if (!attacker || !attacker.isPlayer()) return
  const key = String(boss.uuid)
  if (!bossBagFighters[key]) bossBagFighters[key] = {}
  bossBagFighters[key][String(attacker.uuid)] = Date.now()
})

// A fresh roll of the boss's loot table with `player` as the killer.
function bossBagRoll(boss, player, source) {
  const level = boss.level
  const table = level.server.reloadableRegistries().getLootTable(boss.getLootTable())
  const params = new bossBagLootParams(level)
    .withParameter(bossBagParams.THIS_ENTITY, boss)
    .withParameter(bossBagParams.ORIGIN, boss.position())
    .withParameter(bossBagParams.DAMAGE_SOURCE, source)
    .withOptionalParameter(bossBagParams.ATTACKING_ENTITY, player)
    .withOptionalParameter(bossBagParams.DIRECT_ATTACKING_ENTITY, player)
    .withParameter(bossBagParams.LAST_DAMAGE_PLAYER, player)
    .withLuck(player.getLuck())
    .create(bossBagParamSets.ENTITY)
  const out = []
  const rolled = table.getRandomItems(params)
  for (let i = 0; i < rolled.size(); i++) {
    let stack = rolled.get(i)
    if (!stack.isEmpty()) out.push(stack)
  }
  return out
}

// Combine identical stacks (a loot table often rolls an item one at a time).
function bossBagMerge(stacks) {
  const out = []
  stacks.forEach(s => {
    let left = s.copy()
    for (let i = 0; i < out.length && !left.isEmpty(); i++) {
      let o = out[i]
      if (bossBagStack.isSameItemSameComponents(o, left) && o.count < o.getMaxStackSize()) {
        let move = Math.min(left.count, o.getMaxStackSize() - o.count)
        o.grow(move)
        left.shrink(move)
      }
    }
    if (!left.isEmpty()) out.push(left)
  })
  return out
}

// bossBagModels (strata_boss_bag_models.js, generated) picks each boss's own bag texture.
function bossBagGive(player, boss, rolled) {
  const bossName = bossBagEntityType(boss).getDescription().getString()
  const model = bossBagModels[String(boss.type)]
  const stacks = bossBagMerge(rolled)
  if (stacks.length === 0) return
  for (let start = 0; start < stacks.length; start += bossBagMaxStacks) {
    let bag = Item.of('strata:boss_bag')
    bag.set(bossBagComponents.CONTAINER, bossBagContents.fromItems(stacks.slice(start, start + bossBagMaxStacks)))
    bag.set(bossBagComponents.CUSTOM_NAME, Text.gold(`${bossName} Loot Bag`).italic(false))
    if (model) bag.set(bossBagComponents.CUSTOM_MODEL_DATA, new bossBagModelData(model))
    player.give(bag)
  }
  player.tell(Text.gold(`Your share of the loot: ${bossName} Loot Bag`).append(Text.gray(' (right-click to open)')))
  player.server.runCommandSilent(`execute as ${player.username} at @s run playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.2`)
}

EntityEvents.drops(event => {
  const boss = event.entity
  if (!bossBagIsBoss(boss)) return
  const key = String(boss.uuid)
  const hits = bossBagFighters[key]
  delete bossBagFighters[key]
  if (!hits) return
  const server = boss.level.server
  const now = Date.now()
  const fighters = []
  server.players.forEach(player => {
    let last = hits[String(player.uuid)]
    if (last && now - last <= bossBagWindowMs) fighters.push({ player: player, last: last })
  })
  if (fighters.length === 0) return

  // The killing blow's player, or the most recent hitter, gets the real drops.
  const killer = event.source.actual
  let main = fighters.find(f => killer && killer.isPlayer() && String(f.player.uuid) === String(killer.uuid))
  if (!main) main = fighters.reduce((a, b) => (b.last > a.last ? b : a))

  const drops = []
  event.drops.forEach(itemEntity => {
    let stack = itemEntity.getItem()
    if (!stack.isEmpty()) drops.push(stack.copy())
  })
  bossBagGive(main.player, boss, drops)
  fighters.forEach(f => {
    if (f === main) return
    try {
      bossBagGive(f.player, boss, bossBagRoll(boss, f.player, event.source))
    } catch (e) {
      console.error(`strata_boss_bags: rolling ${boss.type} loot for ${f.player.username} failed: ${e}`)
    }
  })
  event.cancel()
})

// Opening: the bag's items go into the inventory (anything that doesn't fit drops at your feet).
function bossBagOpen(player, bag) {
  const contents = bag.get(bossBagComponents.CONTAINER)
  if (!contents) return
  const names = []
  const it = contents.nonEmptyItemsCopy().iterator()
  while (it.hasNext()) {
    let stack = it.next()
    names.push(`${stack.count}x ${stack.hoverName.string}`)
    player.give(stack)
  }
  bag.shrink(1)
  player.server.runCommandSilent(`execute as ${player.username} at @s run playsound minecraft:item.bundle.drop_contents player @s`)
  player.tell(Text.gold('You open the bag: ').append(Text.white(names.length > 0 ? names.join(', ') : 'nothing')))
}

ItemEvents.rightClicked('strata:boss_bag', event => {
  bossBagOpen(event.player, event.item)
  event.cancel()
})
