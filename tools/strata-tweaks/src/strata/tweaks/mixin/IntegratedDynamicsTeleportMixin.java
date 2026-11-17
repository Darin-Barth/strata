package strata.tweaks.mixin;

import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.level.Level;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Integrated Dynamics' "teleport me" packet takes a dimension and a position from the client and moves the
 * player there, without asking whether that player may. The mod only sends it from an op's screen, but a
 * modified client can send it for anyone: a free teleport to any dimension (End gate audit, Nov 17).
 * The server now ignores it from anyone who is not an op.
 */
@Mixin(targets = "org.cyclops.integrateddynamics.network.packet.PlayerTeleportPacket", remap = false)
public abstract class IntegratedDynamicsTeleportMixin {
    @Inject(method = "actionServer", at = @At("HEAD"), cancellable = true, remap = false)
    private void strata_tweaks$opsOnly(Level level, ServerPlayer player, CallbackInfo ci) {
        if (!player.hasPermissions(2)) ci.cancel();
    }
}
