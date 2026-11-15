package strata.tweaks.mixin;

import com.mojang.serialization.Dynamic;
import net.minecraft.util.datafix.DataFixTypes;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import strata.tweaks.StrataTweaks;

/** Brewin' and Chewin' runs its own data fixer over everything vanilla upgrades; skip it for structure templates. */
@Mixin(targets = "umpaz.brewinandchewin.common.utility.dfu.BnCDataFixer", remap = false)
public abstract class BrewinFixersMixin {
    @Inject(method = "updateWithFixers", at = @At("HEAD"), cancellable = true, remap = false)
    private <T> void strata_tweaks$skipStructures(DataFixTypes type, Dynamic<T> data, CallbackInfoReturnable<Dynamic<T>> cir) {
        if (type == DataFixTypes.STRUCTURE && StrataTweaks.skipModStructureFixers()) cir.setReturnValue(data);
    }
}
