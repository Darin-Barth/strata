package strata.tweaks.mixin;

import net.minecraft.world.entity.LivingEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * No night vision in the Hollow: it is built on darkness (fog and dread), and a dozen items in the pack
 * give night vision for nothing. (The Abyssal Plain is not on this list: its barrier is water and air, not
 * the dark.) Every
 * source ends up in the game's night vision strength (the potion effect, Vampirism's and Werewolves' own
 * effect instances, the goggles of Artifacts and Reliquified Artifacts, which patch this same method), so
 * this answers last (priority 2000) and says "none" there. Shader packs read the same value through Iris.
 */
@Mixin(targets = "net.minecraft.client.renderer.GameRenderer", priority = 2000)
public abstract class NightVisionMixin {
    @Inject(method = "getNightVisionScale", at = @At("RETURN"), cancellable = true)
    private static void strata_tweaks$noNightVision(LivingEntity entity, float partialTick, CallbackInfoReturnable<Float> cir) {
        if (entity.level().dimension().location().toString().equals("strata:hollow")) cir.setReturnValue(0.0F);
    }
}
