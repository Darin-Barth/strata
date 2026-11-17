package strata.tweaks;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.Holder;
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
import net.minecraft.world.item.crafting.Ingredient;
import net.neoforged.neoforge.event.BuildCreativeModeTabContentsEvent;
import net.neoforged.neoforge.event.entity.living.LivingIncomingDamageEvent;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
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
 * A suit is four pieces and its tier is the lowest of the four (Darin, Nov 17: all four are required).
 * Create's copper and netherite diving helmets and boots are tier 1 (Deep Seas only accepted the copper
 * ones); the Carapace and Abyssal helmets and boots are Create's own classes ({@link SuitGear}) with better
 * armour and the tier's look. The mixins in {@code mixin/DiverPressureMixin} and
 * {@code mixin/DeepSeasBacktanksMixin} hand Deep Seas these answers; everything else about pressure is its own.
 *
 * Backtanks: the suit's chestplate takes the slot a backtank would be worn in, so Deep Seas lets the helmet
 * breathe from backtanks carried in the inventory. That list is rebuilt here so it also holds for the new
 * chestplates and for netherite backtanks. The Carapace and Abyssal backtanks, which hold two and three
 * times the air, are in {@link TierTanks}.
 */
public final class DivingSuit {
    public static final DeferredRegister<ArmorMaterial> MATERIALS = DeferredRegister.create(Registries.ARMOR_MATERIAL, StrataTweaks.MODID);
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(StrataTweaks.MODID);
    private static final TagKey<Item> AIR_SOURCES = TagKey.create(Registries.ITEM, ResourceLocation.fromNamespaceAndPath("create", "pressurized_air_sources"));

    public static final DeferredItem<Item> CARAPACE_PLATING = ITEMS.registerSimpleItem("carapace_plating");
    public static final DeferredItem<Item> ABYSSAL_PLATING = ITEMS.registerSimpleItem("abyssal_plating", new Item.Properties().fireResistant());
    // Deep Seas' copper pieces are iron-grade (chest 6, legs 5). Carapace is diamond-grade, Abyssal a step past netherite.
    // (Create's copper helmet and boots: 1 and 2.)
    static final Holder<ArmorMaterial> CARAPACE = material("carapace_diving", 3, 6, 8, 3, 2.0F, 0.0F, CARAPACE_PLATING);
    static final Holder<ArmorMaterial> ABYSSAL = material("abyssal_diving", 4, 7, 9, 3, 3.0F, 0.1F, ABYSSAL_PLATING);
    public static final DeferredItem<Piece> CARAPACE_CHESTPLATE = piece("carapace_diving_chestplate", CARAPACE, ArmorItem.Type.CHESTPLATE, 2, 33, false);
    public static final DeferredItem<Piece> CARAPACE_LEGGINGS = piece("carapace_diving_leggings", CARAPACE, ArmorItem.Type.LEGGINGS, 2, 33, false);
    public static final DeferredItem<Piece> ABYSSAL_CHESTPLATE = piece("abyssal_diving_chestplate", ABYSSAL, ArmorItem.Type.CHESTPLATE, 3, 40, true);
    public static final DeferredItem<Piece> ABYSSAL_LEGGINGS = piece("abyssal_diving_leggings", ABYSSAL, ArmorItem.Type.LEGGINGS, 3, 40, true);
    public static final DeferredItem<Item> CARAPACE_HELMET = ITEMS.register("carapace_diving_helmet", () -> SuitGear.helmet(CARAPACE, "carapace_diving", 2, 33, false));
    public static final DeferredItem<Item> CARAPACE_BOOTS = ITEMS.register("carapace_diving_boots", () -> SuitGear.boots(CARAPACE, "carapace_diving", 2, 33, false));
    public static final DeferredItem<Item> ABYSSAL_HELMET = ITEMS.register("abyssal_diving_helmet", () -> SuitGear.helmet(ABYSSAL, "abyssal_diving", 3, 40, true));
    public static final DeferredItem<Item> ABYSSAL_BOOTS = ITEMS.register("abyssal_diving_boots", () -> SuitGear.boots(ABYSSAL, "abyssal_diving", 3, 40, true));

    private DivingSuit() {}

    private static Holder<ArmorMaterial> material(String name, int helmet, int legs, int chest, int boots, float toughness, float knockback, DeferredItem<Item> repair) {
        return MATERIALS.register(name, () -> {
            EnumMap<ArmorItem.Type, Integer> defense = new EnumMap<>(ArmorItem.Type.class);
            for (ArmorItem.Type type : ArmorItem.Type.values()) defense.put(type, 3);
            defense.put(ArmorItem.Type.HELMET, helmet);
            defense.put(ArmorItem.Type.BOOTS, boots);
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
            describe(tier, true, lines);
            super.appendHoverText(stack, context, lines, flag);
        }
    }

    /** Tooltip lines of a suit piece. */
    static void describe(int tier, boolean decidesDepth, List<Component> lines) {
        lines.add(Component.translatable("tooltip.strata_tweaks.suit.part." + tier).withStyle(ChatFormatting.GRAY));
        int depth = depthOf(tier, 280);
        lines.add((depth >= NO_LIMIT ? Component.translatable("tooltip.strata_tweaks.suit.no_limit")
                : Component.translatable("tooltip.strata_tweaks.suit.depth", depth)).withStyle(ChatFormatting.AQUA));
        if (tier >= 3 && StrataTweaks.abyssalSuitLaserScale() < 1.0) {
            lines.add(Component.translatable("tooltip.strata_tweaks.suit.laser").withStyle(ChatFormatting.AQUA));
        }
    }

    private static final String ARRIVED = "strata_dim_arrived";
    private static final int ARRIVAL_GRACE = 100;

    /** Remembers when a player changed dimension, for {@link #justArrived}. */
    public static void onChangedDimension(PlayerEvent.PlayerChangedDimensionEvent event) {
        Player player = event.getEntity();
        player.getPersistentData().putLong(ARRIVED, player.level().getGameTime());
    }

    /**
     * True for five seconds after a change of dimension. Deep Seas' pressure is held off for that long
     * ({@code mixin/DiverPressureMixin}): the Abyssal Plain's portal spot is far below what kills, and the
     * pressure check could run before the arrival script had moved the player into their Lifepod.
     */
    public static boolean justArrived(Player player) {
        if (!player.getPersistentData().contains(ARRIVED)) return false;
        long since = player.level().getGameTime() - player.getPersistentData().getLong(ARRIVED);
        return since >= 0 && since < ARRIVAL_GRACE;
    }

    private static final ResourceLocation LEVIATHAN_LASER = ResourceLocation.fromNamespaceAndPath("cataclysm", "deathlaser");

    /**
     * The Leviathan's laser does about 10 damage a hit, three hits a second, and armour hardly counts against
     * it: a diver in the full Abyssal suit was dead in a second (test, Nov 17), and a diver in diving boots
     * walks the sea floor and cannot swim out of the beam. The full Abyssal suit takes a share of it
     * ({@code abyssalSuitLaserScale}), enough to walk out of the beam, not to stand in it.
     */
    public static void onIncomingDamage(LivingIncomingDamageEvent event) {
        if (!(event.getEntity() instanceof Player player)) return;
        if (!event.getSource().typeHolder().unwrapKey().map(key -> key.location().equals(LEVIATHAN_LASER)).orElse(false)) return;
        double scale = StrataTweaks.abyssalSuitLaserScale();
        if (scale < 1.0 && tier(player) >= 3) event.setAmount((float) (event.getAmount() * scale));
    }

    public static void addToTabs(BuildCreativeModeTabContentsEvent event) {
        String tab = event.getTabKey().location().toString();
        if (tab.equals("minecraft:combat")) {
            event.accept(CARAPACE_HELMET.get());
            event.accept(CARAPACE_CHESTPLATE.get());
            event.accept(CARAPACE_LEGGINGS.get());
            event.accept(CARAPACE_BOOTS.get());
            event.accept(ABYSSAL_HELMET.get());
            event.accept(ABYSSAL_CHESTPLATE.get());
            event.accept(ABYSSAL_LEGGINGS.get());
            event.accept(ABYSSAL_BOOTS.get());
            for (TierTanks.Tank tank : TierTanks.ALL) event.accept(tank.item().get());
        } else if (tab.equals("minecraft:ingredients")) {
            event.accept(CARAPACE_PLATING.get());
            event.accept(ABYSSAL_PLATING.get());
        }
    }

    // ---- the suit ----

    private static final int NO_LIMIT = 1_000_000;

    /** The tier of a diving helmet (or boots): 1 for Create's two, 2 and 3 for ours, 0 for anything else. */
    private static int gearTier(ItemStack stack, String kind) {
        ResourceLocation id = BuiltInRegistries.ITEM.getKey(stack.getItem());
        String path = id.getPath();
        if (id.getNamespace().equals("create")) return path.equals("copper_diving_" + kind) || path.equals("netherite_diving_" + kind) ? 1 : 0;
        if (!id.getNamespace().equals(StrataTweaks.MODID)) return 0;
        return path.equals("carapace_diving_" + kind) ? 2 : path.equals("abyssal_diving_" + kind) ? 3 : 0;
    }

    /** 0 for anything that is no suit piece, 1 for Deep Seas' copper chestplate and leggings, 2 and 3 for ours. */
    public static int pieceTier(ItemStack stack) {
        if (stack.getItem() instanceof Piece piece) return piece.tier;
        ResourceLocation id = BuiltInRegistries.ITEM.getKey(stack.getItem());
        return id.getNamespace().equals("create_submarine") && (id.getPath().equals("diving_chestplate") || id.getPath().equals("diving_leggings")) ? 1 : 0;
    }

    /** The tier of the whole suit worn, 0 without a full one. */
    public static int tier(LivingEntity entity) {
        int gear = Math.min(gearTier(entity.getItemBySlot(EquipmentSlot.HEAD), "helmet"), gearTier(entity.getItemBySlot(EquipmentSlot.FEET), "boots"));
        if (gear == 0) return 0;
        return Math.min(gear, Math.min(pieceTier(entity.getItemBySlot(EquipmentSlot.CHEST)), pieceTier(entity.getItemBySlot(EquipmentSlot.LEGS))));
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

    /** How many times the usual air this backtank holds: 1, or the tier of a Carapace or Abyssal one. */
    public static int tankMultiplier(ItemStack stack) {
        return TierTanks.multiplier(stack.getItem());
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
