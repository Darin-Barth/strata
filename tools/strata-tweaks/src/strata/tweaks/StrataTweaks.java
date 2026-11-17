package strata.tweaks;

import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.config.ModConfig;
import net.neoforged.neoforge.common.ModConfigSpec;
import net.neoforged.neoforge.common.NeoForge;

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
    public static final ModConfigSpec.BooleanValue ABYSSAL_ROOMS_NEED_OXYGEN = BUILDER
            .comment("In the Abyssal Plain, a dry room a player stands in must have a Create: Deep Seas Oxygen Diffuser",
                    "holding oxygen, or it floods (see AbyssalAir). The Lifepod and ships are exempt.")
            .define("abyssalRoomsNeedOxygen", true);
    public static final ModConfigSpec.BooleanValue ABYSSAL_DIFFUSERS_PUSH_WATER = BUILDER
            .comment("In the Abyssal Plain, an Oxygen Diffuser holding oxygen pushes the water out of a closed room,",
                    "from the ceiling down (nothing else can dry a room there). Does nothing in a space open to the sea.")
            .define("abyssalDiffusersPushWater", true);
    public static final ModConfigSpec.IntValue SUIT_DEPTH_CARAPACE = BUILDER
            .comment("How deep the Carapace Diving Suit (tier 2) holds out, in metres of water. Deep Seas' Copper Diving Suit",
                    "holds to 280 m; 60 m past a suit's limit kills. 0 = no limit.")
            .defineInRange("divingSuitDepthCarapace", 420, 0, 100000);
    public static final ModConfigSpec.IntValue SUIT_DEPTH_ABYSSAL = BUILDER
            .comment("The same for the Abyssal Diving Suit (tier 3). 0 = no limit.")
            .defineInRange("divingSuitDepthAbyssal", 0, 0, 100000);
    public static final ModConfigSpec SPEC = BUILDER.build();

    public StrataTweaks(IEventBus modBus, ModContainer container) {
        container.registerConfig(ModConfig.Type.COMMON, SPEC);
        DivingSuit.MATERIALS.register(modBus);
        TierTanks.BLOCKS.register(modBus);
        DivingSuit.ITEMS.register(modBus);
        modBus.addListener(TierTanks::addToBlockEntity);
        modBus.addListener(TierTanks::commonSetup);
        modBus.addListener(DivingSuit::addToTabs);
        NeoForge.EVENT_BUS.addListener(AbyssalAir::onPlayerTick);
    }

    public static boolean skipModStructureFixers() {
        return !SPEC.isLoaded() || SKIP_MOD_STRUCTURE_FIXERS.getAsBoolean();
    }

    public static boolean abyssalRoomsNeedOxygen() {
        return !SPEC.isLoaded() || ABYSSAL_ROOMS_NEED_OXYGEN.getAsBoolean();
    }

    public static boolean abyssalDiffusersPushWater() {
        return !SPEC.isLoaded() || ABYSSAL_DIFFUSERS_PUSH_WATER.getAsBoolean();
    }

    public static int suitDepthCarapace() {
        return SPEC.isLoaded() ? SUIT_DEPTH_CARAPACE.get() : 420;
    }

    public static int suitDepthAbyssal() {
        return SPEC.isLoaded() ? SUIT_DEPTH_ABYSSAL.get() : 0;
    }

    public static double monsterCapScale() {
        return SPEC.isLoaded() ? MONSTER_CAP_SCALE.get() : 1.0;
    }
}
