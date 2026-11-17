package strata.tweaks.mixin;

import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.contents.TranslatableContents;
import net.minecraft.world.entity.player.Player;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

/**
 * Inventory Pets switches the Loot Pet's mining bonus off while FTB Ultimine is installed (the pack keeps that
 * default) and tells the holder so in chat on every single ore they break. The bonus stays off; the line goes
 * (Darin, Nov 17). Its other message from the same place, about enchanted tools, is left alone.
 */
@Mixin(targets = "com.inventorypets.events.HarvestHandler", remap = false)
public abstract class LootPetMessageMixin {
    @Redirect(method = "notifyHarvest", remap = false,
            at = @At(value = "INVOKE", target = "Lnet/minecraft/world/entity/player/Player;sendSystemMessage(Lnet/minecraft/network/chat/Component;)V"))
    private static void strata_tweaks$noUltimineLine(Player player, Component message) {
        if (message.getContents() instanceof TranslatableContents text && "item.loot.ftbultimine".equals(text.getKey())) return;
        player.sendSystemMessage(message);
    }
}
