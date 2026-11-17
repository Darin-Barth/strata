package strata.tweaks.mixin;

import java.util.Map;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * About one launch in ten the game died while starting with "Duplicate client extensions registration for
 * Block{create:belt}" (Darin's crash of Nov 14, test launches of Nov 16 and 17): the same extension class
 * was registered for the same block twice, and NeoForge treats any second registration as fatal. Nothing is
 * wrong with the second one, it is a copy of the first; so a repeat of the same class is ignored (and
 * logged), and only a registration of a different class for a taken target still stops the game.
 * Client only. The cause of the double registration is not known; no report of it was found.
 */
@Mixin(targets = "net.neoforged.neoforge.client.extensions.common.ClientExtensionsManager", remap = false)
public abstract class ClientExtensionsMixin {
    private static final Logger strata_tweaks$LOG = LogManager.getLogger("Strata Tweaks");

    @Inject(method = "register", at = @At("HEAD"), cancellable = true, remap = false)
    private static void strata_tweaks$sameClassTwice(Object extensions, Map<Object, Object> registered, Object[] targets, CallbackInfo ci) {
        if (targets.length == 0) return;
        boolean repeat = false;
        for (Object target : targets) {
            Object old = registered.get(target);
            if (old == null) continue;
            if (old.getClass() != extensions.getClass()) return;   // a real conflict: NeoForge's own error
            repeat = true;
        }
        if (!repeat) return;
        for (Object target : targets) {
            if (registered.putIfAbsent(target, extensions) != null) {
                strata_tweaks$LOG.warn("Ignored a second registration of {} for {}", extensions.getClass().getName(), target);
            }
        }
        ci.cancel();
    }
}
