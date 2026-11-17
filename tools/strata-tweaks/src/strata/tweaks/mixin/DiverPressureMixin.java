package strata.tweaks.mixin;

import net.minecraft.server.level.ServerPlayer;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Constant;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.ModifyConstant;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import strata.tweaks.DivingSuit;

/**
 * Create: Deep Seas' diver pressure: 120 m without its Copper Diving Suit, 280 m with it. The suit test and the
 * 280 are replaced by {@link DivingSuit}'s: netherite helmets and boots count, and the Carapace and Abyssal
 * tiers go deeper. Re-check after a Deep Seas update (the 280 is a literal in {@code onPlayerTick}).
 */
@Mixin(targets = "com.maxenonyme.createsubmarine.submarine.system.DiverPressure", remap = false)
public abstract class DiverPressureMixin {
    @Inject(method = "wearsCopperSuit", at = @At("HEAD"), cancellable = true, remap = false)
    private static void strata_tweaks$anySuit(ServerPlayer player, CallbackInfoReturnable<Boolean> cir) {
        cir.setReturnValue(DivingSuit.tier(player) >= 1);
    }

    /** No pressure in the first seconds after arriving in a dimension (see DivingSuit.justArrived). */
    @Inject(method = "onPlayerTick", at = @At("HEAD"), cancellable = true, remap = false)
    private static void strata_tweaks$arrivalGrace(PlayerTickEvent.Post event, CallbackInfo ci) {
        if (DivingSuit.justArrived(event.getEntity())) ci.cancel();
    }

    @ModifyConstant(method = "onPlayerTick", constant = @Constant(intValue = 280), remap = false)
    private static int strata_tweaks$suitDepth(int copper, PlayerTickEvent.Post event) {
        return DivingSuit.depthLimit(event.getEntity(), copper);
    }
}
