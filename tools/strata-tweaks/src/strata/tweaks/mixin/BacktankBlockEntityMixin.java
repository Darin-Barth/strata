package strata.tweaks.mixin;

import net.minecraft.network.chat.Component;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.Redirect;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import strata.tweaks.DivingSuit;
import strata.tweaks.TierTanks;

/** A placed Carapace or Abyssal backtank fills to two or three times the air and carries its own name. */
@Mixin(targets = "com.simibubi.create.content.equipment.armor.BacktankBlockEntity", remap = false)
public abstract class BacktankBlockEntityMixin {
    @Redirect(method = {"tick", "getComparatorOutput", "read"},
            at = @At(value = "INVOKE", target = "Lcom/simibubi/create/content/equipment/armor/BacktankUtil;maxAir(I)I"), remap = false)
    private int strata_tweaks$upgradedTank(int capacityLevel) {
        return DivingSuit.createMaxAir(capacityLevel) * TierTanks.multiplier(((BlockEntity) (Object) this).getBlockState().getBlock());
    }

    /** Create names anything that is not its netherite tank "Copper Backtank". */
    @Inject(method = "getDefaultName", at = @At("HEAD"), cancellable = true, remap = false)
    private static void strata_tweaks$ownName(BlockState state, CallbackInfoReturnable<Component> cir) {
        if (TierTanks.multiplier(state.getBlock()) > 1) cir.setReturnValue(state.getBlock().getName());
    }
}
