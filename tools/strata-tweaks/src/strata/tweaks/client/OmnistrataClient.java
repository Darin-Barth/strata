package strata.tweaks.client;

import com.mojang.blaze3d.platform.InputConstants;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.Options;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.core.NonNullList;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.client.IItemDecorator;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.RegisterItemDecorationsEvent;
import net.neoforged.neoforge.client.event.RegisterKeyMappingsEvent;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.entity.player.ItemTooltipEvent;
import net.neoforged.neoforge.network.PacketDistributor;
import strata.tweaks.Omnistrata;

/**
 * The Omnistrata's key and wheel. Hold the key with the Omnistrata (or one of its tools) in hand: the six tools
 * appear around the crosshair; point at one and let go. A quick tap goes back to the tool used before; the
 * scroll wheel steps through them; letting go in the middle puts the tool away. Walking keeps working while
 * the wheel is up.
 */
public final class OmnistrataClient {
    private static final KeyMapping KEY = new KeyMapping("key.strata_tweaks.omnistrata", InputConstants.Type.KEYSYM,
            InputConstants.KEY_V, "key.categories.strata_tweaks");
    private static boolean wasDown;

    private OmnistrataClient() {}

    public static void init(IEventBus modBus) {
        modBus.addListener((RegisterKeyMappingsEvent event) -> event.register(KEY));
        modBus.addListener(OmnistrataClient::registerMark);
        NeoForge.EVENT_BUS.addListener(OmnistrataClient::onTick);
        NeoForge.EVENT_BUS.addListener(OmnistrataClient::onTooltip);
    }

    private static final ResourceLocation MARK =
            ResourceLocation.fromNamespaceAndPath("strata_tweaks", "textures/gui/omnistrata_mark.png");

    /**
     * A tool that is out looks like any other pickaxe, so it gets a small tool case in the bottom right corner of
     * its slot (Darin's sketch, Nov 20). A decorator is tied to an item, and any one-per-stack item can be the
     * tool, so every such item gets the same decorator; it draws only on a stack that carries the kit. The mark
     * moves up two pixels when the durability bar is showing, so the bar stays readable.
     */
    private static void registerMark(RegisterItemDecorationsEvent event) {
        IItemDecorator mark = (graphics, font, stack, x, y) -> {
            if (!Omnistrata.isOut(stack)) return false;
            graphics.pose().pushPose();
            graphics.pose().translate(0f, 0f, 200f);
            graphics.blit(MARK, x + 8, y + (stack.isBarVisible() ? 6 : 8), 0f, 0f, 8, 8, 8, 8);
            graphics.pose().popPose();
            return true;
        };
        for (Item item : BuiltInRegistries.ITEM) {
            if (item.getDefaultMaxStackSize() == 1 && item != Omnistrata.ITEM.get()) event.register(item, mark);
        }
    }

    private static void onTick(ClientTickEvent.Post event) {
        Minecraft mc = Minecraft.getInstance();
        boolean down = KEY.isDown();
        if (down && !wasDown && mc.player != null && mc.screen == null && Omnistrata.isKit(mc.player.getMainHandItem())) {
            mc.setScreen(new Wheel());
        }
        wasDown = down;
    }

    /** A tool that is out is some other mod's item, so its tooltip gets the kit's lines here. */
    private static void onTooltip(ItemTooltipEvent event) {
        if (Omnistrata.isOut(event.getItemStack())) Omnistrata.describe(event.getItemStack(), event.getToolTip());
    }

    private static boolean held(KeyMapping key) {
        InputConstants.Key bound = key.getKey();
        return bound.getType() == InputConstants.Type.KEYSYM && bound.getValue() > 0
                && InputConstants.isKeyDown(Minecraft.getInstance().getWindow().getWindow(), bound.getValue());
    }

    private static final class Wheel extends Screen {
        private static final int RADIUS = 46, DEAD = 16, TAP_MS = 220;
        private final long opened = System.currentTimeMillis();
        private int scrolled = -1;
        private double scrollX, scrollY;
        private boolean done;

        Wheel() {
            super(Component.translatable("item.strata_tweaks.omnistrata"));
        }

        @Override
        public boolean isPauseScreen() {
            return false;
        }

        @Override
        public void renderBackground(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {}

        private NonNullList<ItemStack> slots() {
            return Omnistrata.view(minecraft.player.getMainHandItem());
        }

        /** The slot pointed at, PUT_AWAY for the middle. */
        private int pointed(double mouseX, double mouseY, NonNullList<ItemStack> slots) {
            if (scrolled >= 0 && Math.abs(mouseX - scrollX) < 4 && Math.abs(mouseY - scrollY) < 4) return scrolled;
            scrolled = -1;
            double dx = mouseX - width / 2.0, dy = mouseY - height / 2.0;
            if (dx * dx + dy * dy < DEAD * DEAD) return Omnistrata.PUT_AWAY;
            double turn = Math.toDegrees(Math.atan2(dy, dx)) + 90 + 30;
            int slot = (int) Math.floor(((turn % 360) + 360) % 360 / 60.0) % Omnistrata.SLOTS;
            return slots.get(slot).isEmpty() ? Omnistrata.PUT_AWAY : slot;
        }

        @Override
        public void render(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
            if (minecraft.player == null) return;
            NonNullList<ItemStack> slots = slots();
            int cx = width / 2, cy = height / 2;
            int pointed = pointed(mouseX, mouseY, slots);
            int out = Omnistrata.outSlot(minecraft.player.getMainHandItem());
            for (int i = 0; i < Omnistrata.SLOTS; i++) {
                double angle = Math.toRadians(-90 + i * 60);
                int x = cx + (int) Math.round(Math.cos(angle) * RADIUS), y = cy + (int) Math.round(Math.sin(angle) * RADIUS);
                boolean hot = i == pointed;
                graphics.fill(x - 13, y - 13, x + 13, y + 13, hot ? 0xE0FFFFFF : i == out ? 0xC0D9A441 : 0x90000000);
                graphics.fill(x - 12, y - 12, x + 12, y + 12, hot ? 0xC0303030 : 0xA0101010);
                ItemStack stack = slots.get(i);
                if (!stack.isEmpty()) {
                    graphics.renderItem(stack, x - 8, y - 8);
                    graphics.renderItemDecorations(font, stack, x - 8, y - 8);
                }
            }
            Component label;
            if (pointed >= 0) label = slots.get(pointed).getHoverName();
            else if (slots.stream().allMatch(ItemStack::isEmpty)) label = Component.translatable("item.strata_tweaks.omnistrata.empty");
            else label = Component.translatable(out >= 0 ? "item.strata_tweaks.omnistrata.put_away" : "item.strata_tweaks.omnistrata.pick");
            graphics.drawCenteredString(font, label, cx, cy + RADIUS + 22, 0xFFFFFF);
        }

        @Override
        public boolean mouseScrolled(double mouseX, double mouseY, double scrollXAmount, double scrollYAmount) {
            NonNullList<ItemStack> slots = slots();
            int from = scrolled >= 0 ? scrolled : Math.max(pointed(mouseX, mouseY, slots), Omnistrata.outSlot(minecraft.player.getMainHandItem()));
            int step = scrollYAmount < 0 ? 1 : -1;
            for (int n = 1; n <= Omnistrata.SLOTS; n++) {
                int slot = Math.floorMod(from + step * n, Omnistrata.SLOTS);
                if (!slots.get(slot).isEmpty()) {
                    scrolled = slot;
                    scrollX = mouseX;
                    scrollY = mouseY;
                    break;
                }
            }
            return true;
        }

        @Override
        public void tick() {
            Options options = minecraft.options;
            for (KeyMapping key : new KeyMapping[] {options.keyUp, options.keyDown, options.keyLeft, options.keyRight,
                    options.keyJump, options.keySprint, options.keyShift}) {
                key.setDown(held(key));
            }
            if (KEY.getKey().getType() == InputConstants.Type.KEYSYM && !held(KEY)) finish();
        }

        @Override
        public boolean mouseReleased(double mouseX, double mouseY, int button) {
            if (KEY.getKey().getType() == InputConstants.Type.MOUSE && KEY.getKey().getValue() == button) finish();
            return true;
        }

        private void finish() {
            if (done) return;
            done = true;
            if (minecraft.player != null) {
                double mouseX = minecraft.mouseHandler.xpos() * width / minecraft.getWindow().getScreenWidth();
                double mouseY = minecraft.mouseHandler.ypos() * height / minecraft.getWindow().getScreenHeight();
                int want = pointed(mouseX, mouseY, slots());
                boolean tap = System.currentTimeMillis() - opened < TAP_MS && want == Omnistrata.PUT_AWAY && scrolled < 0;
                PacketDistributor.sendToServer(new Omnistrata.Select(tap ? Omnistrata.PREVIOUS : want));
            }
            onClose();
        }
    }
}
