package strata.tweaks;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;
import java.util.Optional;
import net.minecraft.ChatFormatting;
import net.minecraft.core.Holder;
import net.minecraft.core.component.DataComponentPatch;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.TagKey;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.item.crafting.Ingredient;
import net.neoforged.neoforge.event.BuildCreativeModeTabContentsEvent;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

/**
 * Diving suit tiers for the Abyssal Plain (Darin, Nov 17).
 *
 * Create: Deep Seas knows one suit: Create's Copper Diving Helmet and Boots plus its own Diving Chestplate and
 * Leggings hold out to 280 m, anything else to 120 m, and 60 m past the limit kills. The Trench floor is about
 * 550 m down, so the Leviathan could not be fought on foot. Two more tiers, each bought with the boss before:
 *
 *   1  Copper (Deep Seas' own pieces)           280 m   the Plain
 *   2  Carapace (Karkinos Claw)                 420 m   the upper Trench, where the Hullbreaker hunts
 *   3  Abyssal (the Hullbreaker's engine)       no limit: the Trench floor, the Leviathan
 *
 * A tier is the lower of the chestplate's and the leggings'; the helmet and boots are Create's, copper or
 * netherite (Deep Seas only accepted the copper ones). The mixins in {@code mixin/DiverPressureMixin} and
 * {@code mixin/DeepSeasBacktanksMixin} hand Deep Seas these answers; everything else about pressure is its own.
 *
 * Backtanks: the suit's chestplate takes the slot a backtank would be worn in, so Deep Seas lets the helmet
 * breathe from backtanks carried in the inventory. That list is rebuilt here so it also holds for the new
 * chestplates and for netherite backtanks. A backtank upgraded at the smithing table carries
 * {@code strata_tank_tier} (2 or 3) in its custom data and holds that many times the air
 * ({@code mixin/BacktankUtilMixin}, {@code mixin/BacktankBlockEntityMixin}); the tag travels with the tank when
 * it is placed and picked up again, because Create keeps the item's components on the block.
 */
public final class DivingSuit {
    public static final String TANK_TIER = "strata_tank_tier";
    public static final DeferredRegister<ArmorMaterial> MATERIALS = DeferredRegister.create(Registries.ARMOR_MATERIAL, StrataTweaks.MODID);
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(StrataTweaks.MODID);
    private static final TagKey<Item> AIR_SOURCES = TagKey.create(Registries.ITEM, ResourceLocation.fromNamespaceAndPath("create", "pressurized_air_sources"));

    public static final DeferredItem<Item> CARAPACE_PLATING = ITEMS.registerSimpleItem("carapace_plating");
    public static final DeferredItem<Item> ABYSSAL_PLATING = ITEMS.registerSimpleItem("abyssal_plating", new Item.Properties().fireResistant());
    // Deep Seas' copper pieces are iron-grade (chest 6, legs 5). Carapace is diamond-grade, Abyssal a step past netherite.
    private static final Holder<ArmorMaterial> CARAPACE = material("carapace_diving", 6, 8, 2.0F, 0.0F, CARAPACE_PLATING);
    private static final Holder<ArmorMaterial> ABYSSAL = material("abyssal_diving", 7, 9, 3.0F, 0.1F, ABYSSAL_PLATING);
    public static final DeferredItem<Piece> CARAPACE_CHESTPLATE = piece("carapace_diving_chestplate", CARAPACE, ArmorItem.Type.CHESTPLATE, 2, 33, false);
    public static final DeferredItem<Piece> CARAPACE_LEGGINGS = piece("carapace_diving_leggings", CARAPACE, ArmorItem.Type.LEGGINGS, 2, 33, false);
    public static final DeferredItem<Piece> ABYSSAL_CHESTPLATE = piece("abyssal_diving_chestplate", ABYSSAL, ArmorItem.Type.CHESTPLATE, 3, 40, true);
    public static final DeferredItem<Piece> ABYSSAL_LEGGINGS = piece("abyssal_diving_leggings", ABYSSAL, ArmorItem.Type.LEGGINGS, 3, 40, true);

    private DivingSuit() {}

    private static Holder<ArmorMaterial> material(String name, int legs, int chest, float toughness, float knockback, DeferredItem<Item> repair) {
        return MATERIALS.register(name, () -> {
            EnumMap<ArmorItem.Type, Integer> defense = new EnumMap<>(ArmorItem.Type.class);
            for (ArmorItem.Type type : ArmorItem.Type.values()) defense.put(type, 3);
            defense.put(ArmorItem.Type.LEGGINGS, legs);
            defense.put(ArmorItem.Type.CHESTPLATE, chest);
            return new ArmorMaterial(defense, 12, SoundEvents.ARMOR_EQUIP_NETHERITE, () -> Ingredient.of(repair.get()),
                    List.of(new ArmorMaterial.Layer(ResourceLocation.fromNamespaceAndPath(StrataTweaks.MODID, name))), toughness, knockback);
        });
    }

    private static DeferredItem<Piece> piece(String name, Holder<ArmorMaterial> material, ArmorItem.Type type, int tier, int durability, boolean fireproof) {
        return ITEMS.register(name, () -> {
            Item.Properties properties = new Item.Properties().durability(type.getDurability(durability));
            return new Piece(material, type, fireproof ? properties.fireResistant() : properties, tier);
        });
    }

    /** A chestplate or leggings of one of our tiers. */
    public static final class Piece extends ArmorItem {
        public final int tier;

        Piece(Holder<ArmorMaterial> material, Type type, Properties properties, int tier) {
            super(material, type, properties);
            this.tier = tier;
        }

        @Override
        public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flag) {
            lines.add(Component.translatable("tooltip.strata_tweaks.suit.part." + tier).withStyle(ChatFormatting.GRAY));
            int depth = depthOf(tier, 280);
            lines.add((depth >= NO_LIMIT ? Component.translatable("tooltip.strata_tweaks.suit.no_limit")
                    : Component.translatable("tooltip.strata_tweaks.suit.depth", depth)).withStyle(ChatFormatting.AQUA));
            super.appendHoverText(stack, context, lines, flag);
        }
    }

    public static void addToTabs(BuildCreativeModeTabContentsEvent event) {
        String tab = event.getTabKey().location().toString();
        if (tab.equals("minecraft:combat")) {
            event.accept(CARAPACE_CHESTPLATE.get());
            event.accept(CARAPACE_LEGGINGS.get());
            event.accept(ABYSSAL_CHESTPLATE.get());
            event.accept(ABYSSAL_LEGGINGS.get());
        } else if (tab.equals("minecraft:ingredients")) {
            event.accept(CARAPACE_PLATING.get());
            event.accept(ABYSSAL_PLATING.get());
        }
    }

    // ---- the suit ----

    private static final int NO_LIMIT = 1_000_000;

    private static boolean createPiece(ItemStack stack, String copper, String netherite) {
        ResourceLocation id = BuiltInRegistries.ITEM.getKey(stack.getItem());
        return id.getNamespace().equals("create") && (id.getPath().equals(copper) || id.getPath().equals(netherite));
    }

    /** 0 for anything that is no suit piece, 1 for Deep Seas' copper chestplate and leggings, 2 and 3 for ours. */
    public static int pieceTier(ItemStack stack) {
        if (stack.getItem() instanceof Piece piece) return piece.tier;
        ResourceLocation id = BuiltInRegistries.ITEM.getKey(stack.getItem());
        return id.getNamespace().equals("create_submarine") && (id.getPath().equals("diving_chestplate") || id.getPath().equals("diving_leggings")) ? 1 : 0;
    }

    /** The tier of the whole suit worn, 0 without a full one. */
    public static int tier(LivingEntity entity) {
        if (!createPiece(entity.getItemBySlot(EquipmentSlot.HEAD), "copper_diving_helmet", "netherite_diving_helmet")
                || !createPiece(entity.getItemBySlot(EquipmentSlot.FEET), "copper_diving_boots", "netherite_diving_boots")) return 0;
        return Math.min(pieceTier(entity.getItemBySlot(EquipmentSlot.CHEST)), pieceTier(entity.getItemBySlot(EquipmentSlot.LEGS)));
    }

    private static int depthOf(int tier, int copper) {
        if (tier <= 1) return copper;
        int depth = tier == 2 ? StrataTweaks.suitDepthCarapace() : StrataTweaks.suitDepthAbyssal();
        return depth <= 0 ? NO_LIMIT : depth;
    }

    /** How deep the suit the player wears holds out, in metres of water; {@code copper} is Deep Seas' own figure. */
    public static int depthLimit(LivingEntity entity, int copper) {
        return depthOf(tier(entity), copper);
    }

    /** Backtanks the helmet may breathe from although none is worn: any carried, while a suit chestplate is on. */
    public static List<ItemStack> carriedBacktanks(LivingEntity entity) {
        if (!(entity instanceof Player player) || pieceTier(player.getItemBySlot(EquipmentSlot.CHEST)) < 1) return List.of();
        List<ItemStack> tanks = new ArrayList<>();
        for (ItemStack stack : player.getInventory().items) {
            if (stack.is(AIR_SOURCES)) tanks.add(stack);
        }
        if (player.getOffhandItem().is(AIR_SOURCES)) tanks.add(player.getOffhandItem());
        return tanks;
    }

    // ---- backtanks ----

    private static int tankMultiplier(CustomData data) {
        if (data == null || !data.contains(TANK_TIER)) return 1;
        @SuppressWarnings("deprecation")
        int tier = data.getUnsafe().getInt(TANK_TIER);
        return tier == 2 || tier == 3 ? tier : 1;
    }

    /** How many times the usual air this backtank holds: 1, or the tier a smithing upgrade gave it. */
    public static int tankMultiplier(ItemStack stack) {
        return tankMultiplier(stack.get(DataComponents.CUSTOM_DATA));
    }

    /** The same for a placed backtank, from the item components Create keeps on the block. */
    public static int tankMultiplier(DataComponentPatch patch) {
        if (patch == null) return 1;
        Optional<? extends CustomData> data = patch.get(DataComponents.CUSTOM_DATA);
        return data == null || data.isEmpty() ? 1 : tankMultiplier(data.get());
    }

    private static Method createMaxAir;

    /** Create's {@code BacktankUtil.maxAir(int)}: this mod is built without Create on the class path. */
    public static int createMaxAir(int capacityLevel) {
        try {
            if (createMaxAir == null) {
                createMaxAir = Class.forName("com.simibubi.create.content.equipment.armor.BacktankUtil").getMethod("maxAir", int.class);
            }
            return (Integer) createMaxAir.invoke(null, capacityLevel);
        } catch (ReflectiveOperationException e) {
            throw new IllegalStateException(e);
        }
    }
}
