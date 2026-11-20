package strata.tweaks.mixin;

import net.minecraft.world.entity.MobCategory;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import strata.tweaks.StrataTweaks;

/**
 * Scales the natural hostile mob cap (fewer spawn attempts and fewer mobs to tick), and Vampirism's own cap for
 * vampires: they spawn in a category of their own ("vampirism:vampire", 30 per player area), on top of the
 * hostile cap, and were a third of everything hostile around players (Darin, Nov 20).
 */
@Mixin(value = MobCategory.class, remap = false)
public abstract class MobCategoryMixin {
    @Inject(method = "getMaxInstancesPerChunk", at = @At("RETURN"), cancellable = true, remap = false)
    private void strata_tweaks$scaleMonsterCap(CallbackInfoReturnable<Integer> cir) {
        double scale;
        if ((Object) this == MobCategory.MONSTER) scale = StrataTweaks.monsterCapScale();
        else if ("vampirism:vampire".equals(((MobCategory) (Object) this).getName())) scale = StrataTweaks.vampireCapScale();
        else return;
        if (scale != 1.0) cir.setReturnValue(Math.max(scale > 0 ? 1 : 0, (int) Math.round(cir.getReturnValueI() * scale)));
    }
}
