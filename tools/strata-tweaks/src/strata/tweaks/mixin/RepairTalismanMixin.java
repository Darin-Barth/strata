package strata.tweaks.mixin;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Forsaken Relics' Repair Talisman mends anything with a durability bar. An Inventory Pet's bar is its hunger,
 * so the talisman fed every pet for free and the "must be fed" cost that makes the pets fair was gone
 * (Darin, Nov 17). The talisman keeps repairing tools and armour; it skips Inventory Pets' items and anything
 * in the item tag strata_tweaks:repair_talisman_skips (empty, for later cases).
 * Every repair path of the talisman (pulse, lifeline, containers, aura, soul mending) asks this one method.
 */
@Mixin(targets = "com.forsakenrelics.RepairTalismanItem", remap = false)
public abstract class RepairTalismanMixin {
    private static final TagKey<Item> strata_tweaks$SKIPS =
            TagKey.create(Registries.ITEM, ResourceLocation.fromNamespaceAndPath("strata_tweaks", "repair_talisman_skips"));

    @Inject(method = "repairable", at = @At("HEAD"), cancellable = true, remap = false)
    private static void strata_tweaks$notPets(ItemStack stack, CallbackInfoReturnable<Boolean> cir) {
        if (stack.isEmpty()) return;
        if ("inventorypets".equals(BuiltInRegistries.ITEM.getKey(stack.getItem()).getNamespace()) || stack.is(strata_tweaks$SKIPS)) {
            cir.setReturnValue(false);
        }
    }
}
