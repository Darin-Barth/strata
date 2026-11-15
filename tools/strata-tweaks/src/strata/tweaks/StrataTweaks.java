package strata.tweaks;

import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.config.ModConfig;
import net.neoforged.neoforge.common.ModConfigSpec;

/** Strata's own small server fixes (see tools/strata-tweaks/README.md). */
@Mod(StrataTweaks.MODID)
public final class StrataTweaks {
    public static final String MODID = "strata_tweaks";

    private static final ModConfigSpec.Builder BUILDER = new ModConfigSpec.Builder();
    public static final ModConfigSpec.BooleanValue SKIP_MOD_STRUCTURE_FIXERS = BUILDER
            .comment("Skip Steam 'n' Rails' and Brewin' and Chewin' extra data-fixer passes when a structure template",
                    "(a saved building piece) is read. Those passes tripled the cost of reading templates, which runs",
                    "on the main thread and froze the server for seconds while players explored.")
            .define("skipModStructureFixers", true);
    public static final ModConfigSpec.DoubleValue MONSTER_CAP_SCALE = BUILDER
            .comment("Multiplier for the natural hostile mob cap (vanilla 70 per player area). 1.0 = vanilla.")
            .defineInRange("monsterCapScale", 0.8, 0.1, 2.0);
    public static final ModConfigSpec SPEC = BUILDER.build();

    public StrataTweaks(ModContainer container) {
        container.registerConfig(ModConfig.Type.COMMON, SPEC);
    }

    public static boolean skipModStructureFixers() {
        return !SPEC.isLoaded() || SKIP_MOD_STRUCTURE_FIXERS.getAsBoolean();
    }

    public static double monsterCapScale() {
        return SPEC.isLoaded() ? MONSTER_CAP_SCALE.get() : 1.0;
    }
}
