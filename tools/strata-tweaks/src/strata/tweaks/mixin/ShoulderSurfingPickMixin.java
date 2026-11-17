package strata.tweaks.mixin;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyVariable;

/**
 * Shoulder Surfing's crosshair on Sable ships (airships, submarines).
 *
 * In the over-the-shoulder view Shoulder Surfing ray-traces every frame: first for a block, then for entities
 * up to the distance of that block. When the block belongs to a Sable sub-level, the hit position comes back
 * in the ship's own storage coordinates, tens of millions of blocks away, so the entity search box becomes
 * absurdly large. Sable refuses it and logs an error with a full stack trace, every frame: 34,000 traces and
 * a 250 MB client log in twenty minutes of standing in a ship (Nov 16). An absurd distance is cut back to an
 * ordinary reach here, so the search stays small and nothing is logged.
 */
@Mixin(targets = "com.github.exopandora.shouldersurfing.client.world.phys.ObjectPicker", remap = false)
public abstract class ShoulderSurfingPickMixin {
    @ModifyVariable(method = "pickEntities", at = @At("HEAD"), argsOnly = true, ordinal = 0, remap = false)
    private double strata_tweaks$saneRange(double range) {
        return range > 1024.0 || range != range ? 64.0 : range;
    }
}
