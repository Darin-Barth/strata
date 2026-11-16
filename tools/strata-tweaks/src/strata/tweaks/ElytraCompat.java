package strata.tweaks;

import net.neoforged.neoforge.common.ModConfigSpec;

/**
 * Elytra Slot 9.0.2 (its last 1.21.1 build) reads Deeper and Darker's Soul Elytra cooldown as a static int
 * field; Deeper and Darker 1.4 turned it into a config value on DeeperDarkerConfig.CONFIG, so every boost
 * with a Soul Elytra in the elytra slot threw NoSuchFieldError on the server. The mixins send that read here.
 */
public final class ElytraCompat {
    private static ModConfigSpec.IntValue value;
    private static boolean broken;

    private ElytraCompat() {}

    public static int cooldown() {
        if (value == null && !broken) {
            try {
                Class<?> cfg = Class.forName("com.kyanite.deeperdarker.DeeperDarkerConfig", true, ElytraCompat.class.getClassLoader());
                value = (ModConfigSpec.IntValue) cfg.getField("soulElytraCooldown").get(cfg.getField("CONFIG").get(null));
            } catch (Throwable t) {
                broken = true;
            }
        }
        return value != null ? value.getAsInt() : 600;
    }
}
