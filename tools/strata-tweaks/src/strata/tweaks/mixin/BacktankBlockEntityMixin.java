package strata.tweaks.mixin;

import net.minecraft.core.component.DataComponentPatch;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;
import strata.tweaks.DivingSuit;

/** The placed backtank fills to the same two or three times the air as the upgraded item (see BacktankUtilMixin). */
@Mixin(targets = "com.simibubi.create.content.equipment.armor.BacktankBlockEntity", remap = false)
public abstract class BacktankBlockEntityMixin {
    @Shadow(remap = false) private DataComponentPatch componentPatch;

    @Redirect(method = {"tick", "getComparatorOutput", "read"},
            at = @At(value = "INVOKE", target = "Lcom/simibubi/create/content/equipment/armor/BacktankUtil;maxAir(I)I"), remap = false)
    private int strata_tweaks$upgradedTank(int capacityLevel) {
        return DivingSuit.createMaxAir(capacityLevel) * DivingSuit.tankMultiplier(componentPatch);
    }
}
