package strata.tweaks;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.NonNullList;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ClickType;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.ItemContainerContents;

/**
 * The Omnistrata's six slots as a screen: right-click with it in hand (put away) to open (Darin, Nov 20).
 *
 * The tools live in the held stack's component, so every change is written straight back to that stack on the
 * server; nothing is kept until the screen closes. The hotbar slot holding the Omnistrata is locked while the
 * screen is open (no picking it up, no number-key swap onto it), or the stack being written to could walk off.
 */
public final class OmnistrataMenu extends AbstractContainerMenu {
    public static final int TOOLS_X = 35, TOOLS_Y = 20, INVENTORY_Y = 51, HOTBAR_Y = 109;

    private final Inventory inventory;
    private final int held;
    private final SimpleContainer tools = new SimpleContainer(Omnistrata.SLOTS);

    public OmnistrataMenu(int id, Inventory inventory) {
        super(Omnistrata.MENU.get(), id);
        this.inventory = inventory;
        this.held = inventory.selected;
        NonNullList<ItemStack> stowed = Omnistrata.stowed(inventory.getItem(held));
        for (int i = 0; i < Omnistrata.SLOTS; i++) tools.setItem(i, stowed.get(i).copy());
        tools.addListener(changed -> save());
        for (int i = 0; i < Omnistrata.SLOTS; i++) {
            addSlot(new Slot(tools, i, TOOLS_X + i * 18, TOOLS_Y) {
                @Override
                public boolean mayPlace(ItemStack stack) {
                    return Omnistrata.accepts(stack);
                }

                @Override
                public int getMaxStackSize() {
                    return 1;
                }
            });
        }
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 9; col++) addSlot(new Slot(inventory, 9 + row * 9 + col, 8 + col * 18, INVENTORY_Y + row * 18));
        }
        for (int col = 0; col < 9; col++) {
            boolean locked = col == held;
            addSlot(new Slot(inventory, col, 8 + col * 18, HOTBAR_Y) {
                @Override
                public boolean mayPickup(Player player) {
                    return !locked;
                }

                @Override
                public boolean mayPlace(ItemStack stack) {
                    return !locked;
                }
            });
        }
    }

    private void save() {
        if (inventory.player.level().isClientSide) return;
        ItemStack kit = inventory.getItem(held);
        if (!(kit.getItem() instanceof Omnistrata.KitItem)) return;
        List<ItemStack> list = new ArrayList<>();
        for (int i = 0; i < Omnistrata.SLOTS; i++) list.add(tools.getItem(i).copy());
        kit.set(Omnistrata.KIT.get(), ItemContainerContents.fromItems(list));
        Integer previous = kit.get(Omnistrata.PREV.get());
        if (previous != null && tools.getItem(previous).isEmpty()) kit.remove(Omnistrata.PREV.get());
    }

    @Override
    public boolean stillValid(Player player) {
        return inventory.getItem(held).getItem() instanceof Omnistrata.KitItem;
    }

    @Override
    public void clicked(int slot, int button, ClickType type, Player player) {
        if (type == ClickType.SWAP && button == held) return;
        super.clicked(slot, button, type, player);
    }

    /** Shift-click: a tool in the inventory goes into the first free slot, a stowed tool goes back to the inventory. */
    @Override
    public ItemStack quickMoveStack(Player player, int index) {
        Slot slot = slots.get(index);
        if (!slot.hasItem() || !slot.mayPickup(player)) return ItemStack.EMPTY;
        ItemStack stack = slot.getItem();
        ItemStack before = stack.copy();
        if (index < Omnistrata.SLOTS) {
            if (!moveItemStackTo(stack, Omnistrata.SLOTS, slots.size(), true)) return ItemStack.EMPTY;
        } else {
            if (!Omnistrata.accepts(stack) || !moveItemStackTo(stack, 0, Omnistrata.SLOTS, false)) return ItemStack.EMPTY;
        }
        if (stack.isEmpty()) slot.setByPlayer(ItemStack.EMPTY);
        else slot.setChanged();
        return before;
    }
}
