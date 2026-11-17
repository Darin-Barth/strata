package strata.tweaks.mixin;

import java.util.List;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import strata.tweaks.DivingSuit;

/**
 * Deep Seas lets a diver in its Diving Chestplate breathe from Copper Backtanks carried in the inventory. The
 * same has to hold for the Carapace and Abyssal chestplates, and for netherite backtanks.
 */
@Mixin(targets = "com.maxenonyme.createsubmarine.submarine.item.DivingSuitItem", remap = false)
public abstract class DeepSeasBacktanksMixin {
    @Inject(method = "carriedBacktanks", at = @At("HEAD"), cancellable = true, remap = false)
    private static void strata_tweaks$anyChestplate(LivingEntity entity, CallbackInfoReturnable<List<ItemStack>> cir) {
        cir.setReturnValue(DivingSuit.carriedBacktanks(entity));
    }
}
