package strata.tweaks.client;

import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.inventory.Slot;
import strata.tweaks.OmnistrataMenu;

/**
 * The Omnistrata's screen: six tool slots over the player's inventory. The panel is drawn with plain
 * rectangles in the game's own container colours (grey panel, bevelled slots), so it needs no texture file.
 */
public final class OmnistrataScreen extends AbstractContainerScreen<OmnistrataMenu> {
    public OmnistrataScreen(OmnistrataMenu menu, Inventory inventory, Component title) {
        super(menu, inventory, title);
        imageWidth = 176;
        imageHeight = 133;
        inventoryLabelY = imageHeight - 94;
    }

    @Override
    public void render(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
        super.render(graphics, mouseX, mouseY, partialTick);
        renderTooltip(graphics, mouseX, mouseY);
    }

    @Override
    protected void renderBg(GuiGraphics graphics, float partialTick, int mouseX, int mouseY) {
        int x = leftPos, y = topPos, w = imageWidth, h = imageHeight;
        graphics.fill(x + 2, y, x + w - 2, y + h, 0xFF000000);
        graphics.fill(x, y + 2, x + w, y + h - 2, 0xFF000000);
        graphics.fill(x + 1, y + 1, x + w - 1, y + h - 1, 0xFF000000);
        graphics.fill(x + 2, y + 1, x + w - 2, y + h - 1, 0xFFC6C6C6);
        graphics.fill(x + 1, y + 2, x + w - 1, y + h - 2, 0xFFC6C6C6);
        graphics.fill(x + 2, y + 1, x + w - 3, y + 3, 0xFFFFFFFF);
        graphics.fill(x + 1, y + 2, x + 3, y + h - 3, 0xFFFFFFFF);
        graphics.fill(x + 3, y + h - 3, x + w - 2, y + h - 1, 0xFF555555);
        graphics.fill(x + w - 3, y + 3, x + w - 1, y + h - 2, 0xFF555555);
        for (Slot slot : menu.slots) {
            int sx = x + slot.x - 1, sy = y + slot.y - 1;
            graphics.fill(sx, sy, sx + 18, sy + 18, 0xFFFFFFFF);
            graphics.fill(sx, sy, sx + 17, sy + 17, 0xFF373737);
            graphics.fill(sx + 1, sy + 1, sx + 17, sy + 17, 0xFF8B8B8B);
        }
    }
}
