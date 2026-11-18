package strata.tweaks.mixin;

import java.lang.reflect.Method;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.player.Player;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Xaero's Minimap &amp; World Map - Waystones Compatibility turns a waystone into a map waypoint. It does so for the
 * player who activates one, which is the point, but also for every player online whenever any waystone is
 * renamed or edited: everyone ended up with everyone else's waystones on their map, in whatever dimension they
 * happened to stand in, and a deleted one came back at the next edit (Darin, Nov 17).
 * A waypoint now only goes to a player who has activated that waystone and is in its dimension.
 * Server-side; Waystones is reached by reflection so the build needs neither jar.
 */
@Mixin(targets = "fr.shoqapik.w2w2.W2w2Mod", remap = false)
public abstract class WaystoneWaypointMixin {
    private static Method strata_tweaks$activated;
    private static Method strata_tweaks$dimension;

    @Inject(method = "sendWaypointPacket", at = @At("HEAD"), cancellable = true, remap = false)
    private void strata_tweaks$ownWaystonesOnly(ServerPlayer player, @org.spongepowered.asm.mixin.injection.Coerce Object waystone, CallbackInfo ci) {
        try {
            if (strata_tweaks$activated == null) {
                Class<?> api = Class.forName("net.blay09.mods.waystones.api.Waystone");
                strata_tweaks$dimension = api.getMethod("getDimension");
                strata_tweaks$activated = Class.forName("net.blay09.mods.waystones.core.PlayerWaystoneManager")
                        .getMethod("isWaystoneActivated", Player.class, api);
            }
            ResourceKey<?> dimension = (ResourceKey<?>) strata_tweaks$dimension.invoke(waystone);
            if (!player.level().dimension().equals(dimension)
                    || !Boolean.TRUE.equals(strata_tweaks$activated.invoke(null, player, waystone))) ci.cancel();
        } catch (ReflectiveOperationException e) {
            ci.cancel();
        }
    }
}
