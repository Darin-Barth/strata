package strata.tweaks;

import com.simibubi.create.content.equipment.armor.DivingBootsItem;
import com.simibubi.create.content.equipment.armor.DivingHelmetItem;
import java.util.List;
import net.minecraft.core.Holder;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;

/**
 * The Carapace and Abyssal diving helmets and boots. They are Create's own classes, so everything Create does
 * for its diving helmet (breathing from a backtank, Aqua Affinity) and boots (walking on the sea floor) holds
 * for them without another line; only the armour material and the texture differ. Create looks the texture up
 * as {@code <namespace>:textures/models/armor/<path>_layer_1.png}, the same file the chestplate uses.
 * Kept apart from {@link DivingSuit} because this class needs Create on the class path.
 */
final class SuitGear {
    private SuitGear() {}

    private static Item.Properties properties(ArmorItem.Type type, int durability, boolean fireproof) {
        Item.Properties properties = new Item.Properties().durability(type.getDurability(durability));
        return fireproof ? properties.fireResistant() : properties;
    }

    static Item helmet(Holder<ArmorMaterial> material, String texture, int tier, int durability, boolean fireproof) {
        return new DivingHelmetItem(material, properties(ArmorItem.Type.HELMET, durability, fireproof),
                ResourceLocation.fromNamespaceAndPath(StrataTweaks.MODID, texture)) {
            @Override
            public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flag) {
                DivingSuit.describe(tier, false, lines);
                super.appendHoverText(stack, context, lines, flag);
            }
        };
    }

    static Item boots(Holder<ArmorMaterial> material, String texture, int tier, int durability, boolean fireproof) {
        return new DivingBootsItem(material, properties(ArmorItem.Type.BOOTS, durability, fireproof),
                ResourceLocation.fromNamespaceAndPath(StrataTweaks.MODID, texture)) {
            @Override
            public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flag) {
                DivingSuit.describe(tier, false, lines);
                super.appendHoverText(stack, context, lines, flag);
            }
        };
    }
}
