# Joining the Strata beta

Strata is a big modpack (about 400 mods). It runs on Minecraft 1.21.1 with NeoForge, and you install it through the free
**Modrinth App**.

## 1. Install
1. Install the Modrinth App from https://modrinth.com/app and sign in with your Microsoft/Minecraft account.
2. Download **Strata-0.2.0.mrpack** from the latest release: https://github.com/Darin-Barth/strata/releases/latest
3. In the Modrinth App: **+ (Create instance) → From file** → pick the `.mrpack` you downloaded. It downloads
   everything; the first time takes a few minutes.

## 2. Give it enough memory
Open the Strata instance → **Settings → Java and memory** → set memory to **10–12 GB** (8 GB minimum).
Less than that and the game stutters or crashes.

In the same screen, under **Java arguments**, add:

```
-XX:+UseZGC -XX:+ZGenerational
```

This switches Java to a garbage collector that doesn't freeze the game for big cleanups, so there's much less stutter
(Distant Horizons recommends it too).

## 3. Join
**Multiplayer → Add Server**, address: **strata.dev-duo.com**. The server has a whitelist; ask Darin if you can't
get in.

The first time you load into the world it takes a minute; that's normal for a pack this size.

## Updating
The server and the pack must be on the **same version**, or you'll be disconnected when joining. When Darin posts a
new version, download the new `.mrpack` from the releases page and import it the same way as a new instance. To keep
your keybinds and settings, copy `options.txt` (and `config/` if you changed mod settings) from the old instance
folder into the new one before launching (instance → **⋮ → Open folder**).

## Good to know
- Open the quest book from the **quest button in your inventory**. Start with the **Welcome to Strata** chapter; it
  explains the rules and where to go next.
- No free teleporting, and flight always costs something (fuel, power, mana or stamina).
- Difficulty steps up after the first Nether trip and again after the Ender Dragon.
- This is a **beta**: some balance rules aren't enforced yet. If something seems broken or too easy, tell Darin.
