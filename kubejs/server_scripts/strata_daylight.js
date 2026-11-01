// Longer days: a full day takes 30 real minutes (vanilla: 20), 20 of daylight and 10 of night.
// Daylight runs from mid-sunrise (time 23500) to mid-sunset (12500), night from there back to
// mid-sunrise, so each half of sunrise and sunset sits on its own side.
// doDaylightCycle stays on, so the game still moves the clock one tick per tick (sleeping, Serene
// Seasons and every mod's day counter keep working); this script holds the clock back on some ticks.
// Other dimensions share the Overworld's clock, so this covers them too.
// Serene Seasons' day_duration (config/sereneseasons/seasons.toml) is 36000 to match.
// KubeJS server scripts share one scope: every top-level name here starts with "daylight".
const daylightDayTicks = 20 * 60 * 20      // real ticks of daylight
const daylightNightTicks = 10 * 60 * 20    // real ticks of night
const daylightDawn = 23500                 // daylight starts (mid-sunrise)
const daylightDusk = 12500                 // night starts (mid-sunset)
// Share of ticks to hold back: daylight covers 13000 clock ticks, night 11000.
const daylightHoldDay = 1 - 13000 / daylightDayTicks
const daylightHoldNight = 1 - 11000 / daylightNightTicks
const daylightRules = Java.loadClass('net.minecraft.world.level.GameRules')
const daylightTimePacket = Java.loadClass('net.minecraft.network.protocol.game.ClientboundSetTimePacket')

let daylightLast = -1
let daylightDebt = 0

ServerEvents.tick(event => {
  const server = event.server
  const level = server.overworld()
  if (!level.gameRules.getBoolean(daylightRules.RULE_DAYLIGHT)) { daylightLast = -1; return }
  const time = Number(level.dayTime)
  // Only hold back a normal one-tick step: skip after /time set, sleeping through the night, etc.
  const normal = time === daylightLast + 1
  daylightLast = time
  if (!normal) return
  const t = time % 24000
  const isDay = t >= daylightDawn || t < daylightDusk
  daylightDebt += isDay ? daylightHoldDay : daylightHoldNight
  if (daylightDebt < 1) return
  daylightDebt -= 1
  level.setDayTime(time - 1)
  daylightLast = time - 1
  // Clients move their own clock every tick and only hear the server's once a second; tell them now
  // so the sun doesn't run ahead and jump back.
  server.playerList.broadcastAll(new daylightTimePacket(level.levelData.getGameTime(), time - 1, true))
})
