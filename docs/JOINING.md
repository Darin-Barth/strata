# Joining a Strata server

Strata is a big modpack (about 400 mods). It runs on Minecraft 1.21.1 with NeoForge, and you install it through the free
**Modrinth App**.

## 1. Install
1. Install the Modrinth App from https://modrinth.com/app and sign in with your Microsoft/Minecraft account.
2. Download the newest **Strata-<version>.mrpack** from the latest release: https://github.com/Darin-Barth/strata/releases/latest
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

## On a Mac
The game crashes about a second after you press Play ("java quit unexpectedly") because Drippy's early loading window
doesn't work on macOS. Turn the early window off once:

1. Press Play once and let it crash, so the config file gets created.
2. Strata instance → **⋮ → Open folder** → `config` → open `fml.toml` in TextEdit.
3. Change `earlyWindowControl = true` to `earlyWindowControl = false`, save, and press Play again.

You'll see a plain window for a few seconds instead of the Strata splash, then the normal loading screen. Pack updates
don't touch this file. On memory: give Java about half your Mac's RAM (8 GB on a 16 GB Mac); 8 GB-RAM Macs can't run the pack.

## 3. Join
**Multiplayer → Add Server** with the address the server admin gives you. Servers usually have a whitelist; ask the admin if you can't
get in.

The first time you load into the world it takes a minute; that's normal for a pack this size.

## Updating
The server and the pack must be on the **same version**, or you'll be disconnected when joining. When a
new version, download the new `.mrpack` from the releases page and import it the same way as a new instance. To keep
your keybinds and settings, copy `options.txt` (and `config/` if you changed mod settings) from the old instance
folder into the new one before launching (instance → **⋮ → Open folder**).

## Good to know
- Open the quest book from the **quest button in your inventory**. Start with the **Welcome to Strata** chapter; it
  explains the rules and where to go next.
- Teleporting is limited: one `/home` each (`/sethome` to set it), waystones cost XP, and there's no /back, /rtp or /tpa.
  Flight takes real effort to get or costs something to run (fuel, power, mana or stamina).
- Difficulty is per player: press **Ctrl+T** to pick your Apotheosis World Tier once you unlock more.
- If something seems broken or too easy, tell the server admin: fixes ship as small updates.
