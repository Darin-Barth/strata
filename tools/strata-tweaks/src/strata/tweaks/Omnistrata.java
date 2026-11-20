package strata.tweaks;

import com.mojang.serialization.Codec;
import io.netty.buffer.ByteBuf;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.NonNullList;
import net.minecraft.core.component.DataComponentType;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.TickTask;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.TagKey;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.SimpleMenuProvider;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.SlotAccess;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.flag.FeatureFlags;
import net.minecraft.world.inventory.ClickAction;
import net.minecraft.world.inventory.MenuType;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.ItemContainerContents;
import net.minecraft.world.level.Level;
import net.neoforged.neoforge.event.BuildCreativeModeTabContentsEvent;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.neoforged.neoforge.network.handling.IPayloadContext;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

/**
 * The Omnistrata: one hotbar slot for six tools (Darin, Nov 19).
 *
 * The slot always holds a real item. Put away, it is the Omnistrata item with the tools in its
 * {@link #KIT} component. With a tool out, the slot holds that tool itself, and the tool carries the other five
 * in the same component (plus {@link #OUT}, the slot it came from). So the tool in hand is the genuine article:
 * its enchantments, durability, right-click behaviour and every other mod's test for "is this a wrench" work
 * without a line of ours. The client's wheel (client/OmnistrataClient) only asks the server to swap.
 *
 * A tool that breaks while out would take the kit with it: mixin/ToolBreakMixin hands the rest back as the
 * Omnistrata item ({@link #onToolBroke}).
 */
public final class Omnistrata {
    public static final int SLOTS = 6;
    /** Payload values besides a slot number. */
    public static final int PUT_AWAY = -1, PREVIOUS = -2;

    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(StrataTweaks.MODID);
    public static final DeferredRegister<DataComponentType<?>> COMPONENTS =
            DeferredRegister.create(Registries.DATA_COMPONENT_TYPE, StrataTweaks.MODID);

    /** The tools stowed in this stack, by slot. On the Omnistrata item and on a tool that is out. */
    public static final DeferredHolder<DataComponentType<?>, DataComponentType<ItemContainerContents>> KIT =
            COMPONENTS.register("omnistrata_kit", () -> DataComponentType.<ItemContainerContents>builder()
                    .persistent(ItemContainerContents.CODEC).networkSynchronized(ItemContainerContents.STREAM_CODEC)
                    .cacheEncoding().build());
    /** On a tool that is out: the slot it goes back to. */
    public static final DeferredHolder<DataComponentType<?>, DataComponentType<Integer>> OUT =
            COMPONENTS.register("omnistrata_out", () -> DataComponentType.<Integer>builder()
                    .persistent(Codec.intRange(0, SLOTS - 1)).networkSynchronized(ByteBufCodecs.VAR_INT).build());
    /** The slot that was out before this one, for the quick tap. */
    public static final DeferredHolder<DataComponentType<?>, DataComponentType<Integer>> PREV =
            COMPONENTS.register("omnistrata_prev", () -> DataComponentType.<Integer>builder()
                    .persistent(Codec.intRange(0, SLOTS - 1)).networkSynchronized(ByteBufCodecs.VAR_INT).build());

    public static final DeferredRegister<MenuType<?>> MENUS = DeferredRegister.create(Registries.MENU, StrataTweaks.MODID);
    public static final DeferredHolder<MenuType<?>, MenuType<OmnistrataMenu>> MENU =
            MENUS.register("omnistrata", () -> new MenuType<>(OmnistrataMenu::new, FeatureFlags.DEFAULT_FLAGS));

    public static final DeferredItem<Item> ITEM = ITEMS.register("omnistrata", () -> new KitItem(new Item.Properties().stacksTo(1)));

    /** What may go in: tools only. Extend it from kubejs/data (strata_tweaks/tags/item/omnistrata_tools.json). */
    public static final TagKey<Item> TOOLS =
            TagKey.create(Registries.ITEM, ResourceLocation.fromNamespaceAndPath(StrataTweaks.MODID, "omnistrata_tools"));

    private Omnistrata() {}

    /** The Omnistrata, put away or with a tool out. */
    public static boolean isKit(ItemStack stack) {
        return !stack.isEmpty() && (stack.getItem() instanceof KitItem || stack.has(KIT.get()));
    }

    public static boolean isOut(ItemStack stack) {
        return !stack.isEmpty() && !(stack.getItem() instanceof KitItem) && stack.has(KIT.get());
    }

    public static boolean accepts(ItemStack stack) {
        return !stack.isEmpty() && stack.getCount() == 1 && stack.getMaxStackSize() == 1 && !isKit(stack) && stack.is(TOOLS);
    }

    /** The six slots as the player sees them: a tool that is out sits in its own slot. */
    public static NonNullList<ItemStack> view(ItemStack held) {
        NonNullList<ItemStack> slots = stowed(held);
        if (isOut(held)) slots.set(outSlot(held), held);
        return slots;
    }

    public static int outSlot(ItemStack held) {
        if (!isOut(held)) return -1;
        Integer slot = held.get(OUT.get());
        return slot == null ? 0 : slot;
    }

    public static int previousSlot(ItemStack held) {
        Integer slot = held.get(PREV.get());
        return slot == null ? -1 : slot;
    }

    static NonNullList<ItemStack> stowed(ItemStack held) {
        NonNullList<ItemStack> slots = NonNullList.withSize(SLOTS, ItemStack.EMPTY);
        ItemContainerContents contents = held.get(KIT.get());
        if (contents != null) contents.copyInto(slots);
        return slots;
    }

    /** The tool without the kit it was carrying. */
    private static ItemStack bare(ItemStack tool) {
        ItemStack copy = tool.copy();
        copy.remove(KIT.get());
        copy.remove(OUT.get());
        copy.remove(PREV.get());
        return copy;
    }

    private static ItemStack putAway(NonNullList<ItemStack> slots, int previous) {
        ItemStack kit = new ItemStack(ITEM.get());
        kit.set(KIT.get(), ItemContainerContents.fromItems(slots));
        if (previous >= 0) kit.set(PREV.get(), previous);
        return kit;
    }

    /** What the hand holds after choosing {@code want} (a slot, PUT_AWAY or PREVIOUS); null for no change. */
    public static ItemStack choose(ItemStack held, int want) {
        if (!isKit(held)) return null;
        int out = outSlot(held);
        if (want == PREVIOUS) {
            want = previousSlot(held);
            if (want < 0 && out < 0) {
                NonNullList<ItemStack> all = stowed(held);
                for (int i = SLOTS - 1; i >= 0; i--) if (!all.get(i).isEmpty()) want = i;
            }
            if (want < 0) return null;
        }
        if (want < PUT_AWAY || want >= SLOTS || want == out) return null;
        NonNullList<ItemStack> slots = stowed(held);
        if (out >= 0) slots.set(out, bare(held));
        if (want == PUT_AWAY) return out < 0 ? null : putAway(slots, out);
        ItemStack tool = slots.get(want);
        if (tool.isEmpty()) return null;
        slots.set(want, ItemStack.EMPTY);
        tool = bare(tool);
        tool.set(KIT.get(), ItemContainerContents.fromItems(slots));
        tool.set(OUT.get(), want);
        if (out >= 0) tool.set(PREV.get(), out);
        else if (previousSlot(held) >= 0 && previousSlot(held) != want) tool.set(PREV.get(), previousSlot(held));
        return tool;
    }

    // ---- the swap request ------------------------------------------------------------------------------------

    public record Select(int slot) implements CustomPacketPayload {
        public static final Type<Select> TYPE =
                new Type<>(ResourceLocation.fromNamespaceAndPath(StrataTweaks.MODID, "omnistrata_select"));
        public static final StreamCodec<ByteBuf, Select> CODEC = ByteBufCodecs.VAR_INT.map(v -> new Select(v - 2), s -> s.slot() + 2);

        @Override
        public Type<Select> type() {
            return TYPE;
        }
    }

    static void registerPayloads(RegisterPayloadHandlersEvent event) {
        event.registrar("1").playToServer(Select.TYPE, Select.CODEC, Omnistrata::onSelect);
    }

    private static void onSelect(Select message, IPayloadContext context) {
        if (!(context.player() instanceof ServerPlayer player) || player.isSpectator()) return;
        ItemStack next = choose(player.getMainHandItem(), message.slot());
        if (next == null) return;
        player.setItemInHand(InteractionHand.MAIN_HAND, next);
        player.level().playSound(null, player.blockPosition(), SoundEvents.ARMOR_EQUIP_LEATHER.value(), SoundSource.PLAYERS, 0.6f, 1.3f);
    }

    /** A tool broke while out: the other tools come back as the Omnistrata, into the same hand if it is free. */
    public static void onToolBroke(ItemStack tool, LivingEntity holder) {
        if (!isOut(tool) || holder == null) return;
        ItemStack kit = putAway(stowed(tool), -1);
        if (!(holder instanceof ServerPlayer player)) {
            holder.spawnAtLocation(kit);
            return;
        }
        player.server.tell(new TickTask(player.server.getTickCount(), () -> {
            if (player.getMainHandItem().isEmpty()) player.setItemInHand(InteractionHand.MAIN_HAND, kit);
            else player.getInventory().placeItemBackInInventory(kit);
        }));
    }

    static void addToTabs(BuildCreativeModeTabContentsEvent event) {
        if (event.getTabKey().location().toString().equals("minecraft:tools_and_utilities")) event.accept(ITEM.get());
    }

    /** Tooltip lines for the Omnistrata in either form. */
    public static void describe(ItemStack stack, List<Component> lines) {
        NonNullList<ItemStack> slots = view(stack);
        int out = outSlot(stack);
        List<Component> names = new ArrayList<>();
        for (int i = 0; i < SLOTS; i++) {
            if (slots.get(i).isEmpty()) continue;
            names.add(Component.literal(i == out ? " > " : "   ").append(slots.get(i).getHoverName())
                    .withStyle(i == out ? ChatFormatting.GOLD : ChatFormatting.GRAY));
        }
        if (stack.getItem() instanceof KitItem) {
            lines.add(Component.translatable("item.strata_tweaks.omnistrata.count", names.size(), SLOTS).withStyle(ChatFormatting.GRAY));
        } else {
            lines.add(Component.translatable("item.strata_tweaks.omnistrata.carried").withStyle(ChatFormatting.DARK_AQUA));
        }
        lines.addAll(names);
        lines.add(Component.translatable("item.strata_tweaks.omnistrata.hint.wheel").withStyle(ChatFormatting.DARK_GRAY));
        if (stack.getItem() instanceof KitItem) {
            lines.add(Component.translatable("item.strata_tweaks.omnistrata.hint.load").withStyle(ChatFormatting.DARK_GRAY));
        }
    }

    /** The item when no tool is out. Tools go in and out the way a bundle works: right-click in the inventory. */
    public static final class KitItem extends Item {
        KitItem(Properties properties) {
            super(properties);
        }

        private static boolean add(ItemStack kit, ItemStack tool) {
            if (!accepts(tool)) return false;
            NonNullList<ItemStack> slots = stowed(kit);
            for (int i = 0; i < SLOTS; i++) {
                if (slots.get(i).isEmpty()) {
                    slots.set(i, tool.copy());
                    kit.set(KIT.get(), ItemContainerContents.fromItems(slots));
                    return true;
                }
            }
            return false;
        }

        private static ItemStack takeLast(ItemStack kit) {
            NonNullList<ItemStack> slots = stowed(kit);
            for (int i = SLOTS - 1; i >= 0; i--) {
                if (!slots.get(i).isEmpty()) {
                    ItemStack tool = slots.get(i);
                    slots.set(i, ItemStack.EMPTY);
                    kit.set(KIT.get(), ItemContainerContents.fromItems(slots));
                    Integer prev = kit.get(PREV.get());
                    if (prev != null && prev == i) kit.remove(PREV.get());
                    return tool;
                }
            }
            return ItemStack.EMPTY;
        }

        private static void sound(Player player, boolean in) {
            player.playSound(in ? SoundEvents.BUNDLE_INSERT : SoundEvents.BUNDLE_REMOVE_ONE, 0.8f, 0.9f + player.level().getRandom().nextFloat() * 0.2f);
        }

        /** Right-click with it in the main hand: the six slots open as a screen. */
        @Override
        public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
            ItemStack kit = player.getItemInHand(hand);
            if (hand != InteractionHand.MAIN_HAND) return InteractionResultHolder.pass(kit);
            if (!level.isClientSide) {
                player.openMenu(new SimpleMenuProvider((id, inventory, opener) -> new OmnistrataMenu(id, inventory), kit.getHoverName()));
            }
            return InteractionResultHolder.sidedSuccess(kit, level.isClientSide);
        }

        /** Holding the Omnistrata on the cursor, right-click a tool to stow it or an empty slot to take one out. */
        @Override
        public boolean overrideStackedOnOther(ItemStack kit, Slot slot, ClickAction action, Player player) {
            if (action != ClickAction.SECONDARY || kit.getCount() != 1) return false;
            ItemStack other = slot.getItem();
            if (other.isEmpty()) {
                ItemStack tool = takeLast(kit);
                if (tool.isEmpty()) return false;
                ItemStack left = slot.safeInsert(tool);
                if (!left.isEmpty()) add(kit, left);
                else sound(player, false);
                return true;
            }
            if (!accepts(other) || !slot.mayPickup(player)) return false;
            if (add(kit, other)) {
                slot.set(ItemStack.EMPTY);
                sound(player, true);
            }
            return true;
        }

        /** Right-click the Omnistrata with a tool on the cursor to stow it, or with an empty cursor to take one out. */
        @Override
        public boolean overrideOtherStackedOnMe(ItemStack kit, ItemStack other, Slot slot, ClickAction action, Player player, SlotAccess cursor) {
            if (action != ClickAction.SECONDARY || kit.getCount() != 1 || !slot.allowModification(player)) return false;
            if (other.isEmpty()) {
                ItemStack tool = takeLast(kit);
                if (tool.isEmpty()) return false;
                cursor.set(tool);
                sound(player, false);
                return true;
            }
            if (!accepts(other)) return false;
            if (add(kit, other)) {
                cursor.set(ItemStack.EMPTY);
                sound(player, true);
            }
            return true;
        }

        @Override
        public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flag) {
            describe(stack, lines);
        }
    }
}
