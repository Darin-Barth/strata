package strata.tweaks.mixin;

import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import strata.tweaks.DivingSuit;

/** A Carapace or Abyssal backtank (TierTanks) holds two or three times the air. */
@Mixin(targets = "com.simibubi.create.content.equipment.armor.BacktankUtil", remap = false)
public abstract class BacktankUtilMixin {
    @Inject(method = "maxAir(Lnet/minecraft/world/item/ItemStack;)I", at = @At("RETURN"), cancellable = true, remap = false)
    private static void strata_tweaks$upgradedTank(ItemStack stack, CallbackInfoReturnable<Integer> cir) {
        int times = DivingSuit.tankMultiplier(stack);
        if (times > 1) cir.setReturnValue(cir.getReturnValue() * times);
    }
}
