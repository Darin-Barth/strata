package strata.tweaks.mixin;

import java.util.function.Consumer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import strata.tweaks.Omnistrata;

/**
 * A tool taken out of the Omnistrata carries the other tools with it (see {@link Omnistrata}). When it runs out
 * of durability the game shrinks the stack to nothing, kit and all; just before that, the rest of the kit is
 * handed back to the player as the Omnistrata item.
 */
@Mixin(ItemStack.class)
public abstract class ToolBreakMixin {
    @Inject(method = "hurtAndBreak(ILnet/minecraft/server/level/ServerLevel;Lnet/minecraft/world/entity/LivingEntity;Ljava/util/function/Consumer;)V",
            at = @At(value = "INVOKE", target = "Lnet/minecraft/world/item/ItemStack;shrink(I)V"))
    private void strata_tweaks$keepKit(int damage, ServerLevel level, LivingEntity holder, Consumer<Item> onBreak, CallbackInfo ci) {
        Omnistrata.onToolBroke((ItemStack) (Object) this, holder);
    }
}
