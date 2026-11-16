package strata.tweaks.mixin;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.Level;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * A level's sea level is hard-coded to 63 in 1.21.1, whatever the dimension's generator says. The Abyssal
 * Plain's water reaches up to Y 568 and its floor lies between Y 14 and Y 480, so every "only below sea
 * level" spawn rule failed there: no Alex's Caves creature (Deep Ones need Y below -17), no Naturalist
 * anglerfish or isopod, no thrasher, glow squid or cachalot ever spawned. This reports the real water top.
 */
@Mixin(Level.class)
public abstract class LevelSeaLevelMixin {
    private static final ResourceKey<Level> STRATA_ABYSSAL_PLAIN =
            ResourceKey.create(Registries.DIMENSION, ResourceLocation.fromNamespaceAndPath("strata", "abyssal_plain"));
    private static final int STRATA_ABYSSAL_SEA_LEVEL = 568;

    @Shadow
    public abstract ResourceKey<Level> dimension();

    @Inject(method = "getSeaLevel", at = @At("HEAD"), cancellable = true)
    private void strata_tweaks$abyssalSeaLevel(CallbackInfoReturnable<Integer> cir) {
        if (this.dimension() == STRATA_ABYSSAL_PLAIN) cir.setReturnValue(STRATA_ABYSSAL_SEA_LEVEL);
    }
}
