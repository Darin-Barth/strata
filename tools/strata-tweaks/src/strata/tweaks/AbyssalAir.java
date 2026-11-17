package strata.tweaks;

import it.unimi.dsi.fastutil.longs.LongArrayList;
import it.unimi.dsi.fastutil.longs.LongOpenHashSet;
import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;
import net.neoforged.neoforge.fluids.capability.IFluidHandler;

/**
 * Dry rooms in the Abyssal Plain (strata:abyssal_plain) need an oxygen supply.
 *
 * The game's own water already does the physics a base needs there: a room open to the sea at the side or
 * the top floods, and a hole in the floor does not (water never flows up), so a moon pool or a submarine
 * dock under a base works as built. What the game does not ask for is where the air came from: fill a shell
 * with blocks, dig them out, and you have a dry room for nothing. So every two seconds, for each player
 * standing in air there, the connected dry space around them is walked (the nearest 120,000 cells; a bigger
 * space is judged on those and pays for 120,000). It stays dry
 * while a Create: Deep Seas Oxygen Diffuser in or next to it holds oxygen (from an Electrolyzer), which is
 * used up in proportion to the room's size. Without one the player is warned for ten seconds, then the room
 * floods from the floor up, a layer every two seconds (pockets that can't flood, such as a doorway, and anyone
 * who stays on in the last of the air, suffocate instead). The Lifepod is exempt. Ships are not touched: aboard one the world's
 * block at the player's head is water, and Deep Seas keeps the ship's own air.
 */
public final class AbyssalAir {
    private static final ResourceLocation DIMENSION = ResourceLocation.fromNamespaceAndPath("strata", "abyssal_plain");
    private static final ResourceLocation DIFFUSER = ResourceLocation.fromNamespaceAndPath("create_submarine", "oxygene_diffuser");
    private static final ResourceLocation CREATIVE_OXYGENATOR = ResourceLocation.fromNamespaceAndPath("create_submarine", "creative_oxygenator");
    private static final int PERIOD = 40;
    private static final int MAX_CELLS = 120_000;
    private static final int GRACE_CHECKS = 5;
    private static final Map<UUID, Integer> FAILING = new HashMap<>();
    private static Field oxygenTank;
    private static boolean tankBroken;
    private static boolean warned;

    private AbyssalAir() {}

    public static void onPlayerTick(PlayerTickEvent.Post event) {
        if (!(event.getEntity() instanceof ServerPlayer player) || player.tickCount % PERIOD != 0) return;
        if (!StrataTweaks.abyssalRoomsNeedOxygen()) return;
        if (!player.level().dimension().location().equals(DIMENSION) || player.isCreative() || player.isSpectator()) {
            FAILING.remove(player.getUUID());
            return;
        }
        try {
            check(player, (ServerLevel) player.level());
        } catch (RuntimeException e) {
            // Never take the server down over a room check.
            if (!warned) {
                warned = true;
                org.slf4j.LoggerFactory.getLogger("Strata Tweaks").warn("Abyssal room check failed", e);
            }
        }
    }

    private static boolean open(BlockState state, ServerLevel level, BlockPos pos) {
        return state.getFluidState().isEmpty() && !state.isCollisionShapeFullBlock(level, pos);
    }

    private static void check(ServerPlayer player, ServerLevel level) {
        BlockPos start = BlockPos.containing(player.getX(), player.getEyeY(), player.getZ());
        // Head under water: nothing to judge. The count of failed checks is kept, so bobbing up into the
        // last of a flooding room's air doesn't start the ten seconds of grace again.
        if (!open(level.getBlockState(start), level, start)) return;
        LongOpenHashSet seen = new LongOpenHashSet();
        LongArrayList queue = new LongArrayList();
        List<BlockPos> diffusers = new ArrayList<>();
        BlockPos.MutableBlockPos cell = new BlockPos.MutableBlockPos(), next = new BlockPos.MutableBlockPos();
        seen.add(start.asLong());
        queue.add(start.asLong());
        boolean supplied = false;
        for (int i = 0; i < queue.size(); i++) {
            cell.set(queue.getLong(i));
            for (Direction dir : Direction.values()) {
                next.setWithOffset(cell, dir);
                if (!level.isLoaded(next)) continue;
                BlockState state = level.getBlockState(next);
                ResourceLocation id = BuiltInRegistries.BLOCK.getKey(state.getBlock());
                if (id.getNamespace().equals("strata") && id.getPath().startsWith("lifepod_")) return;      // the Lifepod
                if (id.equals(CREATIVE_OXYGENATOR)) supplied = true;
                if (id.equals(DIFFUSER)) {
                    BlockPos at = next.immutable();
                    if (!diffusers.contains(at)) diffusers.add(at);
                }
                if (!open(state, level, next)) continue;
                // A space bigger than the limit is not walked any further, but it is not let off either:
                // what was walked still has to hold a Diffuser, and it pays for the full limit.
                if (seen.size() >= MAX_CELLS || !seen.add(next.asLong())) continue;
                queue.add(next.asLong());
            }
        }
        // Oxygen used: 2 mB plus 1 per 1,000 cells, every two seconds (a ship's Diffuser uses 100 in that time).
        int need = 2 + seen.size() / 1000;
        for (BlockPos at : diffusers) {
            if (supplied || need <= 0) break;
            need -= drain(level, at, need);
        }
        if (supplied || need <= 0) {
            FAILING.remove(player.getUUID());
            return;
        }
        int failed = FAILING.merge(player.getUUID(), 1, Integer::sum);
        if (failed <= GRACE_CHECKS) {
            player.displayClientMessage(Component.literal(diffusers.isEmpty()
                    ? "No oxygen supply in this room. Without an Oxygen Diffuser the sea takes it."
                    : "The Oxygen Diffuser is empty. The sea is coming in.").withStyle(ChatFormatting.AQUA, ChatFormatting.ITALIC), true);
            return;
        }
        // The sea comes in: the lowest layer that still holds air fills. Where nothing is left to fill
        // (a doorway, a slab, any pocket that can't hold water) the air is spent: it suffocates.
        int minY = Integer.MAX_VALUE;
        for (int i = 0; i < queue.size(); i++) {
            cell.set(queue.getLong(i));
            if (cell.getY() < minY && level.getBlockState(cell).isAir()) minY = cell.getY();
        }
        if (minY != Integer.MAX_VALUE) {
            for (int i = 0; i < queue.size(); i++) {
                cell.set(queue.getLong(i));
                if (cell.getY() == minY && level.getBlockState(cell).isAir()) level.setBlock(cell, Blocks.WATER.defaultBlockState(), 3);
            }
            level.playSound(null, start, SoundEvents.BUCKET_EMPTY, SoundSource.BLOCKS, 1.0F, 0.6F);
            player.displayClientMessage(Component.literal("The room is flooding.").withStyle(ChatFormatting.RED), true);
        }
        if (minY == Integer.MAX_VALUE || failed > GRACE_CHECKS + 8) {
            player.hurt(player.damageSources().drown(), 2.0F);
            player.displayClientMessage(Component.literal("There is no air left here.").withStyle(ChatFormatting.RED), true);
        }
    }

    /** Takes up to {@code amount} mB of oxygen out of the diffuser at {@code pos}; returns what it got. */
    private static int drain(ServerLevel level, BlockPos pos, int amount) {
        BlockEntity be = level.getBlockEntity(pos);
        if (be == null || tankBroken) return 0;
        try {
            if (oxygenTank == null) {
                oxygenTank = be.getClass().getField("oxygenTank");
            }
            Object tank = oxygenTank.get(be);
            if (tank instanceof IFluidHandler handler) {
                int got = handler.drain(amount, IFluidHandler.FluidAction.EXECUTE).getAmount();
                if (got > 0) be.setChanged();
                return got;
            }
        } catch (ReflectiveOperationException | RuntimeException e) {
            tankBroken = true;
        }
        return 0;
    }
}
