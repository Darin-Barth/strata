// Inventory Pets are found, not crafted (Darin, Oct 27): every recipe that makes a pet is removed,
// and so is the Petrifier (it turns mobs into pets; also off in config/inventorypets-common.toml).
// Pets come from structure chests instead (tools/build_pet_loot.py: common, rare and legendary
// tiers). The pet food nuggets and the Feed Bag keep their recipes. Pets players already have
// keep working; the strong ones are weaker through the config (cooldowns, costlier food).
// Recipe IDs from Inventory Pets 2.2.8; re-check after a mod update that adds pets.
// KubeJS server scripts share one scope: every top-level name here starts with "strataPet".
const strataPetRecipes = [
  'anvil_pet', 'apple_pet', 'april_fool_pet', 'banana_pet', 'bed_pet', 'biome_pet',
  'black_hole_pet', 'blaze_pet', 'brewing_stand_pet', 'cheetah_pet', 'chest_pet', 'chicken_pet',
  'cloud_pet', 'cobblestone_pet', 'cow_pet', 'crafting_table_pet', 'creeper_pet', 'dingot_pet',
  'dirt_pet', 'double_chest_pet', 'dubstep_pet', 'enchanting_table_pet', 'end_portal_pet',
  'ender_chest_pet', 'enderman_pet', 'flying_saddle_pet', 'furnace_pet', 'ghast_pet', 'heart_pet',
  'house_pet', 'illuminati_pet', 'iron_golem_pet', 'juggernaut_pet', 'jukebox_pet', 'lead_pet',
  'loot_pet', 'magma_cube_pet', 'meta_pet_aoe', 'meta_pet_fan', 'meta_pet_legend_100',
  'meta_pet_legend_25', 'meta_pet_legend_50', 'meta_pet_legend_75', 'meta_pet_mob',
  'meta_pet_peaceful', 'meta_pet_special', 'meta_pet_utility', 'meta_pet_youtuber', 'meta_pet_zzz',
  'mickerson_pet', 'moon_pet', 'mooshroom_pet', 'mooshroom_pet_alt', 'nether_portal_pet',
  'ocelot_pet', 'pacman_pet', 'pet_christmas_tree', 'pet_menorah', 'pet_mishumaa_saba',
  'pet_politically_correct', 'petrifier', 'pig_pet', 'pingot_pet', 'pixie_pet', 'pufferfish_pet',
  'purplicious_cow_pet', 'qcm_pet', 'quiver_pet', 'saddle_pet', 'sated_chest_pet',
  'sated_double_chest_pet', 'sheep_pet', 'shield_pet', 'siamese_pet', 'silverfish_pet',
  'slime_pet', 'snow_golem_pet', 'spider_pet', 'spider_pet_alt', 'sponge_pet', 'squid_pet',
  'sun_pet', 'torch_pet', 'wither_pet', 'wolf_pet', 'wolf_pet_alt',
]

ServerEvents.recipes(event => {
  strataPetRecipes.forEach(id => event.remove({ id: 'inventorypets:' + id }))
})
