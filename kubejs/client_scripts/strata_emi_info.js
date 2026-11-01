// EMI info pages for recipes EMI can't show (Darin, Oct 31). Iron's Spells' Alchemist Cauldron brews
// liquids (250 mB = one bottle), so looking up the bottled ink or elixir in EMI finds no recipe.
// Recipes as in irons_spellbooks/recipe/alchemist_cauldron (Iron's 3.16.3); re-check after an update.
const emiInfoPour = 'Fill the cauldron by right-clicking it with bottles, and take the result out with empty glass bottles (250 mB each).'

const emiInfoPages = {
  'irons_spellbooks:common_ink': [
    'Dissolve a common scroll in an Alchemist Cauldron of water: drop it in, 50% chance to get the ink back.',
    'Wandering traders sell ink too.',
  ],
  'irons_spellbooks:uncommon_ink': ['Alchemist Cauldron: 1000 mB Common Ink + 1 copper ingot = 250 mB Uncommon Ink. Dissolving an uncommon scroll in water also works.', emiInfoPour],
  'irons_spellbooks:rare_ink': ['Alchemist Cauldron: 1000 mB Uncommon Ink + 1 iron ingot = 250 mB Rare Ink. Dissolving a rare scroll in water also works.', emiInfoPour],
  'irons_spellbooks:epic_ink': ['Alchemist Cauldron: 1000 mB Rare Ink + 1 gold ingot = 250 mB Epic Ink. Dissolving an epic scroll in water also works.', emiInfoPour],
  'irons_spellbooks:legendary_ink': ['Alchemist Cauldron: 1000 mB Epic Ink + 1 amethyst shard = 250 mB Legendary Ink. Dissolving a legendary scroll in water also works.', emiInfoPour],
  'irons_spellbooks:greater_healing_potion': ['Alchemist Cauldron: 1000 mB Strong Healing potion (4 bottles) + 1 amethyst shard = 250 mB Greater Healing.', emiInfoPour],
  'irons_spellbooks:oakskin_elixir': ['Alchemist Cauldron: 500 mB Strong Healing potion (2 bottles) + 1 oak log = 250 mB Oakskin Elixir.', emiInfoPour],
  'irons_spellbooks:greater_oakskin_elixir': ['Alchemist Cauldron: 500 mB Oakskin Elixir + 1 amethyst shard = 250 mB Greater Oakskin Elixir.', emiInfoPour],
  'irons_spellbooks:invisibility_elixir': ['Alchemist Cauldron: 1000 mB Long Invisibility potion (4 bottles) + 1 Shriving Stone = 250 mB Invisibility Elixir.', emiInfoPour],
  'irons_spellbooks:greater_invisibility_elixir': ['Alchemist Cauldron: 250 mB Invisibility Elixir + 1 amethyst cluster = 250 mB Greater Invisibility Elixir.', emiInfoPour],
  'irons_spellbooks:evasion_elixir': ['Alchemist Cauldron: 1000 mB Instant Mana III potion (4 bottles) + 1 ender pearl = 250 mB Evasion Elixir.', emiInfoPour],
  'irons_spellbooks:greater_evasion_elixir': ["Alchemist Cauldron: 250 mB Evasion Elixir + 1 dragon's breath = 250 mB Greater Evasion Elixir.", emiInfoPour],
  'irons_spellbooks:ice_venom_vial': ['Alchemist Cauldron: 250 mB water + 1 Icy Fang = 250 mB Ice Venom.', emiInfoPour],
  'irons_spellbooks:timeless_slurry': ['Alchemist Cauldron: 250 mB Mundane potion (1 bottle) + 1 echo shard = 250 mB Timeless Slurry.', emiInfoPour],
  'irons_spellbooks:bloody_vellum': ['Alchemist Cauldron: soak Hogskin in 1000 mB of blood (4 Blood Vials) to get Bloody Vellum.'],
}

RecipeViewerEvents.addInformation('item', event => {
  Object.keys(emiInfoPages).forEach(id => {
    event.add(id, emiInfoPages[id])
  })
})
