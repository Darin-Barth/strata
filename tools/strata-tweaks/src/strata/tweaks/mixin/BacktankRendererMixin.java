package strata.tweaks.mixin;

import java.lang.reflect.Field;
import net.minecraft.world.level.block.state.BlockState;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import strata.tweaks.TierTanks;

/**
 * Create picks a backtank's spinning cogs and its shaft by asking whether the block is its netherite tank;
 * everything else gets the copper parts. Our tanks made from a netherite backtank get the netherite parts.
 * (Client only. The part models are Flywheel classes this mod is not compiled against, hence the reflection.)
 */
@Mixin(targets = "com.simibubi.create.content.equipment.armor.BacktankRenderer", remap = false)
public abstract class BacktankRendererMixin {
    private static Object strata_tweaks$part(String field) {
        try {
            Field f = Class.forName("com.simibubi.create.AllPartialModels").getField(field);
            return f.get(null);
        } catch (ReflectiveOperationException e) {
            return null;
        }
    }

    @Inject(method = "getCogsModel", at = @At("HEAD"), cancellable = true, remap = false)
    private static void strata_tweaks$cogs(BlockState state, CallbackInfoReturnable<Object> cir) {
        if (Boolean.TRUE.equals(TierTanks.netherite(state.getBlock()))) {
            Object part = strata_tweaks$part("NETHERITE_BACKTANK_COGS");
            if (part != null) cir.setReturnValue(part);
        }
    }

    @Inject(method = "getShaftModel", at = @At("HEAD"), cancellable = true, remap = false)
    private static void strata_tweaks$shaft(BlockState state, CallbackInfoReturnable<Object> cir) {
        if (Boolean.TRUE.equals(TierTanks.netherite(state.getBlock()))) {
            Object part = strata_tweaks$part("NETHERITE_BACKTANK_SHAFT");
            if (part != null) cir.setReturnValue(part);
        }
    }
}
