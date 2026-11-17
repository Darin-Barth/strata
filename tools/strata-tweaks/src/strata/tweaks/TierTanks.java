package strata.tweaks;

import com.simibubi.create.api.stress.BlockStressValues;
import com.simibubi.create.content.equipment.armor.AllArmorMaterials;
import com.simibubi.create.content.equipment.armor.BacktankBlock;
import com.simibubi.create.content.equipment.armor.BacktankItem;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Supplier;
import net.minecraft.ChatFormatting;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ArmorMaterials;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.neoforge.event.BlockEntityTypeAddBlocksEvent;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

/**
 * Carapace and Abyssal backtanks: Create's backtank, copper or netherite, plated at the smithing table. They
 * hold two and three times the air.
 *
 * Each is a block and an item of Create's own classes ({@code BacktankBlock}, {@code BacktankItem}), set up the
 * way Create sets up its two: the item is worn or carried, a hidden "placeable" block item puts the block
 * down, and the block joins Create's backtank block entity type, so filling on a shaft, the comparator and
 * picking the tank up again are Create's code. Create draws a placed or worn tank from the block the item
 * points at, so our block models (Create's shapes with our texture) show up there too; the spinning cogs and
 * the shaft are Create's parts ({@code mixin/BacktankRendererMixin} picks the netherite ones for our
 * netherite tanks). The capacity is multiplied in {@code mixin/BacktankUtilMixin} (item) and
 * {@code mixin/BacktankBlockEntityMixin} (placed).
 */
public final class TierTanks {
    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(StrataTweaks.MODID);

    public record Tank(int tier, boolean netherite, DeferredBlock<BacktankBlock> block, DeferredItem<BacktankItem> item) {}

    public static final List<Tank> ALL = new ArrayList<>();

    static {
        add("carapace", 2, false);
        add("carapace", 2, true);
        add("abyssal", 3, false);
        add("abyssal", 3, true);
    }

    private TierTanks() {}

    private static ResourceLocation create(String path) {
        return ResourceLocation.fromNamespaceAndPath("create", path);
    }

    private static void add(String tierName, int tier, boolean netherite) {
        String metal = netherite ? "netherite" : "copper";
        String name = tierName + "_" + metal + "_backtank";
        ResourceLocation id = ResourceLocation.fromNamespaceAndPath(StrataTweaks.MODID, name);
        // The block properties Create gives its own tanks: those of a copper or netherite block. (Not copied from
        // Create's tank: our blocks are registered before Create's, and the lookup then returns air.)
        DeferredBlock<BacktankBlock> block = BLOCKS.register(name,
                () -> new BacktankBlock(BlockBehaviour.Properties.ofFullCopy(netherite ? Blocks.NETHERITE_BLOCK : Blocks.COPPER_BLOCK)));
        Supplier<Item> actual = () -> BuiltInRegistries.ITEM.get(id);
        DeferredItem<BacktankItem.BacktankBlockItem> placeable = DivingSuit.ITEMS.register(name + "_placeable",
                () -> new BacktankItem.BacktankBlockItem(block.get(), actual, new Item.Properties()));
        Component air = Component.translatable("tooltip.strata_tweaks.tank." + tier).withStyle(ChatFormatting.AQUA);
        DeferredItem<BacktankItem> item = DivingSuit.ITEMS.register(name, () -> netherite
                ? new BacktankItem.Layered(ArmorMaterials.NETHERITE, new Item.Properties().fireResistant(), create("netherite_diving"), placeable) {
                    @Override
                    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flag) {
                        lines.add(air);
                        super.appendHoverText(stack, context, lines, flag);
                    }
                }
                : new BacktankItem(AllArmorMaterials.COPPER, new Item.Properties(), create("copper_diving"), placeable) {
                    @Override
                    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flag) {
                        lines.add(air);
                        super.appendHoverText(stack, context, lines, flag);
                    }
                });
        ALL.add(new Tank(tier, netherite, block, item));
    }

    /** How many times the usual air this item holds: 1 for anything that is not one of our tanks. */
    public static int multiplier(Item item) {
        for (Tank tank : ALL) {
            if (tank.item.get() == item) return tank.tier;
        }
        return 1;
    }

    /** The same for a placed tank. */
    public static int multiplier(Block block) {
        for (Tank tank : ALL) {
            if (tank.block.get() == block) return tank.tier;
        }
        return 1;
    }

    /** Whether this block is one of our tanks made from the netherite backtank (else null if it is not ours). */
    public static Boolean netherite(Block block) {
        for (Tank tank : ALL) {
            if (tank.block.get() == block) return tank.netherite;
        }
        return null;
    }

    static void addToBlockEntity(BlockEntityTypeAddBlocksEvent event) {
        BlockEntityType<?> backtank = BuiltInRegistries.BLOCK_ENTITY_TYPE.get(create("backtank"));
        if (backtank == null) throw new IllegalStateException("Create's backtank block entity type is missing");
        for (Tank tank : ALL) event.modify(backtank, tank.block.get());
    }

    /** The same stress as Create's tanks (4 per rpm), or ours would fill for free. */
    static void commonSetup(FMLCommonSetupEvent event) {
        event.enqueueWork(() -> {
            for (Tank tank : ALL) BlockStressValues.IMPACTS.register(tank.block.get(), () -> 4.0);
        });
    }
}
