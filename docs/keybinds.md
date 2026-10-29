# Strata keybinds

Strata ships a default key layout (`config/defaultoptions/keybindings.txt`, applied by the Default Options mod) so
that no two keys you use in normal play fire at once. It only applies to **new installs** and to keys you have never
set. Default Options never overwrites a key that is already in your `options.txt`. If your keys differ from this
layout, open **Options > Controls > Key Binds** and press **Reset All** (or reset single keys) to switch to it.

"Alt+X" means hold Alt, then press X. The general rule: when a mod's default key is already taken, its key is the
**same letter with Alt** (or Ctrl or Shift).

## Cheat sheet

**Can't remember a key?** Press **Alt+Q** for Keybind Atlas: a map of your keyboard and mouse with every binding, its mod, search, and rebinding on the map.

**Movement and vanilla**: unchanged (WASD, Space, Shift, Ctrl sprint, E, Q, F, T, /, 1-9, Tab, F1-F3, F5, L, P).

**Voice chat (Simple Voice Chat)**
| Key | Action |
|---|---|
| V | Voice chat menu |
| G | Group management |
| N | Disable voice chat |
| H | Hide voice chat icons |
| F4 | Mute microphone |
| Caps Lock | Push to talk (voice chat) |
| Right Alt | Whisper (voice chat). Keep both voice keys bound to some key: with no key set, the game logs an error every tick and stutters. |

**Combat and movement**
| Key | Action |
|---|---|
| R | Combat Roll |
| Mouse 5 | Ping Wheel |
| ` (backtick, hold) | FTB Ultimine |

**Maps (Xaero) and claims**
| Key | Action |
|---|---|
| M | World map |
| Y | Minimap settings |
| Alt+Y (hold) | Enlarge minimap |
| U | Waypoint list |
| Alt+U | New waypoint |
| Numpad + | Quick waypoint |
| Shift+M | FTB Chunks map (land claims) |

**Inventory, bags and storage**
| Key | Action |
|---|---|
| B | Sophisticated Backpack |
| Alt+F | Field Guide (creature and plant journal) |
| Alt+B | Occultism satchel |
| Alt+E | Occultism ender satchel |
| Shift+N | Occultism storage accessor |
| Alt+J | Tom's Storage terminal |
| Alt+G | Curios slots |
| I | Aether accessories |
| Alt+H | Accessories screen |
| J | Ars Elemental curio pouch |

**Magic**
| Key | Action |
|---|---|
| X (hold) | Iron's Spells: cast selected spell |
| C (hold) | Iron's Spells: spell wheel |
| Alt + scroll | Iron's Spells: pick spell on the spell bar |
| C | Ars Nouveau: open spell book (book in hand) |
| X / Z | Ars Nouveau: next / previous spell slot (book in hand) |
| Alt+C | Ars Nouveau: selection HUD |

**Vampirism, Werewolves, Bloodlines** (the mods' own keys, plus Alt)
| Key | Action |
|---|---|
| Alt+V | Suck blood (vampire) / Bite (werewolf) |
| Alt+R | Use actions |
| Alt+1 / 2 / 3 | Quick actions 1-3 |
| Alt+P | Vampirism menu (skills) |
| Alt+N | Switch vision |
| Ctrl+V | Bloodlines: devour soul |

**Cobblemon** (Cobblemon's own keys, plus Alt)
| Key | Action |
|---|---|
| Alt+T | Throw / send out selected Pokémon |
| Alt+M | Summary |
| Alt+O | Hide party overlay |
| Up / Down arrows | Change selected party slot |

**Building and tools**
| Key | Action |
|---|---|
| Alt+I | Quark variant selector (stairs, slabs, walls of a held block) |
| Shift+K | Quark rotation lock |
| Z (hold) + 1-3 | Quark hotbar swapper |
| Ctrl+I (hold) | Effortless Building radial menu |
| Ctrl+Z / Ctrl+Y | Effortless Building undo / redo |
| Numpad - | Effortless Building modifier settings |
| Shift+V | Easy Villagers: pick up villager |
| Shift+P | Draconic Evolution: place item |

**Relics and gear HUDs**
| Key | Action |
|---|---|
| Mouse 4 (hold) + scroll | Relics: active abilities list |
| Ctrl+G | Forsaken Relics: switch relic mode |
| Alt+K | Forsaken Relics: relic screen |
| Shift+G (hold) | Oritech implant controls |
| Ctrl+H | Mekanism HUD on/off |
| Shift+H | Neo Vitae: edit HUD layout |
| Ctrl+K | Skill trees (Pufferfish's Skills: Combat, Mining, Fishing, Iron's magic) |
| Alt+L | Apotheosis World Tier screen |

**Graphics and camera**
| Key | Action |
|---|---|
| K | Shaders on/off (Iris) |
| O | Shader pack screen |
| Shift+O | Reload shaders |
| Ctrl+U | Shoulder Surfing: swap shoulder |
| Home / End | Shoulder Surfing: camera in / out |
| F6 / F8 / F10 | Atmospherics menu / Almanac dungeon configs / KubeJS KubeDex |

**Only while holding or wearing the item** (these share keys on purpose; they don't fire without the item): Mekanism
suit modes (V/G/J/B, N item mode), jetpacks, Ad Astra suit flight, Cataclysm / Legendary Monsters / Deep Aether armor
abilities, Building Wands, Building Gadgets, Mechanical Trowel, Create Thrusters tools, Pneumaticcraft armor,
Twilight Forest Traveller's gear, Ice and Fire dragon riding, Vampirism crossbow ammo (C).

## Keys changed from the mods' defaults

Each change keeps two actions from firing from one key in normal play.

| Action | Mod default | Strata | Clashes with on the default |
|---|---|---|---|
| Iron's Spells cast | V | X | Voice chat menu, Vampirism suck, Werewolves bite, Ars HUD, satchels |
| Iron's Spells spell wheel | R | C | Combat Roll |
| Ars Nouveau selection HUD | V | Alt+C | Voice chat menu |
| Vampirism suck blood | V | Alt+V | Voice chat menu |
| Werewolves bite | V | Alt+V | Voice chat menu (shares Alt+V with suck: a player is never both) |
| Vampirism use actions | R | Alt+R | Combat Roll |
| Vampirism menu | P | Alt+P | Social Interactions, Draconic place item |
| Vampirism switch vision | N | Alt+N | Disable voice chat, Occultism storage accessor |
| Bloodlines devour soul | V | Ctrl+V | Voice chat menu, Vampirism suck |
| Cobblemon throw | R | Alt+T | Combat Roll |
| Cobblemon summary | M | Alt+M | Xaero world map |
| Cobblemon hide party | O | Alt+O | Iris shader pack screen |
| Curios slots | G | Alt+G | Voice chat group |
| Accessories screen | H | Alt+H | Voice chat hide icons, Mekanism HUD |
| Occultism satchel | B | Alt+B | Backpack |
| Occultism ender satchel | V | Alt+E | Voice chat menu |
| Occultism storage accessor | N | Shift+N | Disable voice chat |
| Tom's Storage terminal | B | Alt+J | Backpack (Ctrl+B also fired while sprinting) |
| Xaero new waypoint | B | Alt+U | Backpack |
| Xaero enlarge minimap | Z | Alt+Y | Quark hotbar swapper |
| FTB Chunks map | M | Shift+M | Xaero world map |
| Mute microphone | M | F4 | Xaero world map (Ctrl+M also fired while sprinting) |
| Mekanism HUD | H | Ctrl+H | Voice chat hide icons |
| Neo Vitae edit HUD | H | Shift+H | Voice chat hide icons |
| Oritech implant controls | G | Shift+G | Voice chat group |
| Forsaken Relics mode | G | Ctrl+G | Voice chat group (fires while a relic is worn) |
| Forsaken Relics screen | K | Alt+K | Iris shader toggle |
| Relics active abilities | Left Alt | Mouse 4 | Iron's Alt + scroll spell picking, and every Alt key above |
| Quark variant selector | R | Alt+I | Combat Roll (Ctrl+R also fired while sprinting) |
| Apotheosis World Tier screen | Ctrl+T | Alt+L | Chat while sprinting |
| Quark rotation lock | K | Shift+K | Iris shader toggle |
| Iris reload shaders | R | Shift+O | Combat Roll (a roll would reload shaders) |
| Effortless Building radial | Left Alt | Ctrl+I | Create toolbox, Iron's spell bar, every Alt key above (Ctrl+E also fired while sprinting) |
| Effortless Building undo / redo | Z / Y | Ctrl+Z / Ctrl+Y | Quark hotbar swapper / Xaero minimap settings |
| Effortless Building modifiers | Numpad + | Numpad - | Xaero quick waypoint |
| Draconic Evolution place item | P | Shift+P | Social Interactions |
| Easy Villagers pick up | V | Shift+V | Voice chat menu |
| Shoulder Surfing swap shoulder | U | Ctrl+U | Xaero waypoint list |
| Shoulder Surfing camera in / out | Up / Down | Home / End | Cobblemon party slot |
| Atmospherics menu | B | F6 | Backpack |
| Almanac dungeon configs | K | F8 | Iris shader toggle |
| KubeJS KubeDex | K | F10 | Iris shader toggle |

**Unbound** (each duplicates another mod's key):
- Easy Villagers "cycle trades" (C): Trade Cycling does the same thing on the same key in the villager screen, so
  trades would cycle twice per press.
- Bosses'Rise (Block Factory's Bosses) "dodge roll" (Z): Combat Roll (R) is the pack's dodge.

**Kept on purpose**
- Simple Voice Chat keeps all its defaults except mute (V, G, N, H). Combat Roll keeps R. Xaero keeps M, Y, U,
  Numpad +. Sophisticated Backpacks keeps B. Iris keeps K and O. Quark's hotbar swapper keeps Z.
- Shift, Ctrl and Alt still work as modifiers for Create, AE2, Jade, Mekanism, Iron's Spells, etc.
- Werewolves' leap stays on Ctrl: it only works in werewolf form and is meant to pair with sprinting.
- Keys inside one screen only (FTB Quests editor, Ponder, EMI, crafting tweaks) and keys that need a held or worn
  item (see the list above) share keys freely.

## Things to know
- **Sprinting holds Ctrl**, and a held Ctrl turns your next key into a Ctrl+key combo. So no Ctrl combo sits on a key you press while running (E, T, R, B, M, 1-9, Q, F): Ctrl+E opened the build wheel instead of your inventory. The Ctrl combos left (Ctrl+K skills, Ctrl+H, Ctrl+G, Ctrl+U, Ctrl+Z/Y) are on keys you don't press mid-run. (Effortless Building ignores an Alt modifier, so its wheel is Ctrl+I.)
- **Holding a modifier claims the key.** With Shift held, V picks up a villager instead of opening the voice menu;
  with Alt held, 1-3 run Vampirism actions instead of switching hotbar slots (Vampirism's own default). If a key "does
  nothing", check you're not holding Shift, Ctrl or Alt.
- **Alt near a Create toolbox** briefly opens the toolbox menu (Create's default). Deep Aether's Slider Eye slam is
  also on Alt.
- **X and C with an Ars spell book in hand**: X/Z also flip the Ars spell slot, and C also opens the Ars book. If you
  mix both magic mods, rebind one of them.
- **No mouse side buttons?** Rebind Relics abilities (Mouse 4) and Ping Wheel (Mouse 5).
