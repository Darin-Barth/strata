package strata.tweaks.mixin;

import net.minecraft.world.entity.player.Player;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Constant;
import org.spongepowered.asm.mixin.injection.ModifyConstant;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Whispering Spirits ray-traces 100 blocks along every player's view every tick, in every dimension, to see
 * whether they look at a spirit; with the pack's water-collision mixins each trace was slow and it lagged the
 * server (removed in 1.2.1). Spirits only exist in the Hollow, so the check runs only there, twice a second and over 32 blocks
 * (at every 5th tick and 100 blocks it still took 1.5% of the server thread per player, spark Nov 15).
 */
@Mixin(targets = "net.locallupo.whisperingspirits.procedures.PlayerLookAtSpiritProcedure", remap = false)
public abstract class WhisperingSpiritsMixin {
    @Inject(method = "onPlayerTick", at = @At("HEAD"), cancellable = true, remap = false)
    private static void strata_tweaks$hollowOnly(PlayerTickEvent.Post event, CallbackInfo ci) {
        Player player = event.getEntity();
        if (player.tickCount % 10 != 0 || !"strata:hollow".equals(player.level().dimension().location().toString())) ci.cancel();
    }

    /** The trace length: 100 blocks is far beyond what the Hollow's fog lets anyone see. */
    @ModifyConstant(method = "execute(Lnet/neoforged/bus/api/Event;Lnet/minecraft/world/level/LevelAccessor;Lnet/minecraft/world/entity/Entity;)V", constant = @Constant(intValue = 100), remap = false)
    private static int strata_tweaks$range(int blocks) {
        return 32;
    }
}
