package strata.tweaks.mixin;

import net.minecraft.world.entity.MobCategory;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import strata.tweaks.StrataTweaks;

/** Scales the natural hostile mob cap (fewer spawn attempts and fewer mobs to tick). */
@Mixin(value = MobCategory.class, remap = false)
public abstract class MobCategoryMixin {
    @Inject(method = "getMaxInstancesPerChunk", at = @At("RETURN"), cancellable = true, remap = false)
    private void strata_tweaks$scaleMonsterCap(CallbackInfoReturnable<Integer> cir) {
        if ((Object) this != MobCategory.MONSTER) return;
        double scale = StrataTweaks.monsterCapScale();
        if (scale != 1.0) cir.setReturnValue(Math.max(1, (int) Math.round(cir.getReturnValueI() * scale)));
    }
}
