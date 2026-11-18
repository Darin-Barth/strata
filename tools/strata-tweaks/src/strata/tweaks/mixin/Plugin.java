package strata.tweaks.mixin;

import java.util.List;
import java.util.Set;
import net.neoforged.fml.loading.LoadingModList;
import org.objectweb.asm.tree.ClassNode;
import org.spongepowered.asm.mixin.extensibility.IMixinConfigPlugin;
import org.spongepowered.asm.mixin.extensibility.IMixinInfo;

/** Applies each mod-specific mixin only when that mod is installed. */
public final class Plugin implements IMixinConfigPlugin {
    private static boolean loaded(String modId) {
        return LoadingModList.get().getModFileById(modId) != null;
    }

    @Override
    public boolean shouldApplyMixin(String targetClassName, String mixinClassName) {
        if (mixinClassName.endsWith(".RailwaysFixersMixin")) return loaded("railways");
        if (mixinClassName.endsWith(".BrewinFixersMixin")) return loaded("brewinandchewin");
        if (mixinClassName.contains(".ElytraSlot")) return loaded("elytraslot") && loaded("deeperdarker");
        if (mixinClassName.endsWith(".WhisperingSpiritsMixin")) return loaded("whispering_spirits");
        if (mixinClassName.endsWith(".ShoulderSurfingPickMixin")) return loaded("shouldersurfing");
        if (mixinClassName.endsWith(".DiverPressureMixin") || mixinClassName.endsWith(".DeepSeasBacktanksMixin")) return loaded("create_submarine");
        if (mixinClassName.contains(".Backtank")) return loaded("create");
        if (mixinClassName.endsWith(".LootPetMessageMixin")) return loaded("inventorypets");
        if (mixinClassName.endsWith(".IntegratedDynamicsTeleportMixin")) return loaded("integrateddynamics");
        if (mixinClassName.endsWith(".WaystoneWaypointMixin")) return loaded("w2w2") && loaded("waystones");
        return true;
    }

    @Override public void onLoad(String mixinPackage) {}
    @Override public String getRefMapperConfig() { return null; }
    @Override public void acceptTargets(Set<String> myTargets, Set<String> otherTargets) {}
    @Override public List<String> getMixins() { return null; }
    @Override public void preApply(String targetClassName, ClassNode targetClass, String mixinClassName, IMixinInfo mixinInfo) {}
    @Override public void postApply(String targetClassName, ClassNode targetClass, String mixinClassName, IMixinInfo mixinInfo) {}
}
