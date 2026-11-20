package strata.tweaks.mixin;

import net.minecraft.world.entity.Mob;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Coerce;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import strata.tweaks.StrataTweaks;

/**
 * Vampirism has no setting for how often a vampire mob's bite infects. A vampire that wants blood and hits a
 * player who is not looking at it drinks, and then calls {@code VampirePlayer.tryInfect}, which always gives
 * Sanguinare Vampiris: every such bite was an infection (Darin, Nov 20: far too often). Here a bite from a mob
 * only infects with the chance in the config ({@code vampireBiteInfectChance}). A vampire player infecting
 * someone on purpose (the Infect action passes a player, not a mob) is left alone.
 */
@Mixin(targets = "de.teamlapen.vampirism.entity.player.vampire.VampirePlayer", remap = false)
public abstract class VampireInfectMixin {
    @Inject(method = "tryInfect", at = @At("HEAD"), cancellable = true, remap = false)
    private void strata_tweaks$mobBiteChance(@Coerce Object vampire, CallbackInfoReturnable<Boolean> cir) {
        if (vampire instanceof Mob mob && mob.getRandom().nextDouble() >= StrataTweaks.vampireBiteInfectChance()) {
            cir.setReturnValue(false);
        }
    }
}
