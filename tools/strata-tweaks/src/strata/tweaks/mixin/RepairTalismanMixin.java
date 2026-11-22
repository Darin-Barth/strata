package strata.tweaks.mixin;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import net.minecraft.core.NonNullList;
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
import strata.tweaks.Omnistrata;

/**
 * Forsaken Relics' Repair Talisman mends anything with a durability bar. An Inventory Pet's bar is its hunger,
 * so the talisman fed every pet for free and the "must be fed" cost that makes the pets fair was gone
 * (Darin, Nov 17). The talisman keeps repairing tools and armour; it skips Inventory Pets' items and anything
 * in the item tag strata_tweaks:repair_talisman_skips (empty, for later cases).
 * Every repair path of the talisman (pulse, lifeline, containers, aura, soul mending) asks this one method.
 *
 * The tools stowed in an Omnistrata sit in a component of the stack that carries them, where the talisman's
 * regular pulse never looks (Darin, Nov 21: it should mend them too). The pulse hands {@code repair} the stacks
 * it found on the player; copies of the stowed tools join that list and are written back once it is done.
 */
@Mixin(targets = "com.forsakenrelics.RepairTalismanItem", remap = false)
public abstract class RepairTalismanMixin {
    private static final TagKey<Item> strata_tweaks$SKIPS =
            TagKey.create(Registries.ITEM, ResourceLocation.fromNamespaceAndPath("strata_tweaks", "repair_talisman_skips"));
    private static final ThreadLocal<List<Object[]>> strata_tweaks$KITS = ThreadLocal.withInitial(ArrayList::new);

    @Inject(method = "repairable", at = @At("HEAD"), cancellable = true, remap = false)
    private static void strata_tweaks$notPets(ItemStack stack, CallbackInfoReturnable<Boolean> cir) {
        if (stack.isEmpty()) return;
        if ("inventorypets".equals(BuiltInRegistries.ITEM.getKey(stack.getItem()).getNamespace()) || stack.is(strata_tweaks$SKIPS)) {
            cir.setReturnValue(false);
        }
    }

    @Inject(method = "repair", at = @At("HEAD"), remap = false)
    private static void strata_tweaks$addStowed(Collection<ItemStack> stacks, int amount, int items, boolean triage, CallbackInfoReturnable<?> cir) {
        List<Object[]> kits = strata_tweaks$KITS.get();
        kits.clear();
        try {
            for (ItemStack stack : new ArrayList<>(stacks)) {
                if (!Omnistrata.isKit(stack)) continue;
                NonNullList<ItemStack> stowed = Omnistrata.stowedCopies(stack);
                int[] before = new int[stowed.size()];
                for (int i = 0; i < before.length; i++) before[i] = stowed.get(i).getDamageValue();
                stacks.addAll(stowed.stream().filter(tool -> !tool.isEmpty()).toList());
                kits.add(new Object[] {stack, stowed, before});
            }
        } catch (UnsupportedOperationException fixedList) {
            kits.clear();
        }
    }

    @Inject(method = "repair", at = @At("RETURN"), remap = false)
    private static void strata_tweaks$saveStowed(Collection<ItemStack> stacks, int amount, int items, boolean triage, CallbackInfoReturnable<?> cir) {
        List<Object[]> kits = strata_tweaks$KITS.get();
        for (Object[] kit : kits) {
            @SuppressWarnings("unchecked")
            NonNullList<ItemStack> stowed = (NonNullList<ItemStack>) kit[1];
            int[] before = (int[]) kit[2];
            boolean changed = false;
            for (int i = 0; i < before.length; i++) changed |= stowed.get(i).getDamageValue() != before[i];
            if (changed) Omnistrata.writeStowed((ItemStack) kit[0], stowed);
        }
        kits.clear();
    }
}
