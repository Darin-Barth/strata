package strata.tweaks.mixin;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import strata.tweaks.ClientFog;

/** Client only. Runs after the other mods' fog changes (higher priority = applied later = runs last). */
@Mixin(targets = "net.minecraft.client.renderer.FogRenderer", priority = 2000)
public abstract class FogRendererMixin {
    @Inject(method = "setupFog", at = @At("TAIL"))
    private static void strata$fog(CallbackInfo ci) {
        ClientFog.apply();
    }

    @Shadow private static float fogRed;
    @Shadow private static float fogGreen;
    @Shadow private static float fogBlue;

    /** Both the cleared background and the colour the terrain and sky fade to (Atmospherics replaces them). */
    @Inject(method = "setupColor", at = @At("TAIL"))
    private static void strata$fogColor(CallbackInfo ci) {
        float[] c = ClientFog.color();
        if (c == null) return;
        fogRed = c[0];
        fogGreen = c[1];
        fogBlue = c[2];
        ClientFog.applyColor();
    }
}
