package strata.tweaks.mixin;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;
import strata.tweaks.ElytraCompat;

/** See ElytraCompat: the Soul Elytra's per-tick cooldown display. */
@Mixin(targets = "com.illusivesoulworks.elytraslot.common.integration.deeperdarker.DeeperDarkerPlugin", remap = false)
public abstract class ElytraSlotTickMixin {
    @Redirect(method = "tick", remap = false,
            at = @At(value = "FIELD", target = "Lcom/kyanite/deeperdarker/DeeperDarkerConfig;soulElytraCooldown:I", remap = false))
    private static int strata_tweaks$cooldown() {
        return ElytraCompat.cooldown();
    }
}
