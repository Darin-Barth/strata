package strata.tweaks.mixin;

import net.minecraft.nbt.CompoundTag;
import net.minecraft.util.datafix.DataFixTypes;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import strata.tweaks.StrataTweaks;

/** Steam 'n' Rails runs its own data fixer over everything vanilla upgrades; skip it for structure templates. */
@Mixin(targets = "com.railwayteam.railways.base.datafixerapi.DataFixesInternalsImpl", remap = false)
public abstract class RailwaysFixersMixin {
    @Inject(method = "updateWithAllFixers", at = @At("HEAD"), cancellable = true, remap = false)
    private void strata_tweaks$skipStructures(DataFixTypes type, CompoundTag tag, CallbackInfoReturnable<CompoundTag> cir) {
        if (type == DataFixTypes.STRUCTURE && StrataTweaks.skipModStructureFixers()) cir.setReturnValue(tag);
    }
}
