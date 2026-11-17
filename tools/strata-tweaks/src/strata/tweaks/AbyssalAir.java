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
import net.minecraft.tags.FluidTags;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.LiquidBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.chunk.LevelChunk;
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
 *
 * Getting the water out is the Diffuser's job too (nothing else can: water sources re-form faster than a Create
 * Hose Pulley drains them, and sponges are refused in this dimension). A Diffuser that holds oxygen pushes the
 * water out of the space it stands in, from the ceiling down, a layer every two seconds, down to its own level:
 * the water it can reach going sideways and up, never below itself, the way trapped air would spread. That only
 * works in a closed space: if that water reaches the open sea (more than 120,000 cells, or the edge of loaded
 * land) the oxygen has nowhere to stay and nothing happens. A hole in the floor is below the Diffuser, so a moon
 * pool stays a pool. Waterlogged blocks around the dried cells are dried too, or they would pour back in.
 */
public final class AbyssalAir {
    private static final ResourceLocation DIMENSION = ResourceLocation.fromNamespaceAndPath("strata", "abyssal_plain");
    private static final ResourceLocation DIFFUSER = ResourceLocation.fromNamespaceAndPath("create_submarine", "oxygene_diffuser");
    private static final ResourceLocation CREATIVE_OXYGENATOR = ResourceLocation.fromNamespaceAndPath("create_submarine", "creative_oxygenator");
    private static final int PERIOD = 40;
    private static final int MAX_CELLS = 120_000;
    private static final int GRACE_CHECKS = 5;
    private static final int PURGE_MAX = MAX_CELLS;
    private static final int PURGE_REACH = 12;
    private static final int PURGE_RETRY = 600;
    private static final int REST_CELLS = 16_000;
    private static final Map<UUID, int[]> RESTING = new HashMap<>();
    private static final Map<Long, Long> OPEN_UNTIL = new HashMap<>();
    private static final Map<UUID, Integer> FAILING = new HashMap<>();
    private static final boolean TIMING = Boolean.getBoolean("strata.tweaks.airTiming");
    private static Field oxygenTank;
    private static boolean tankBroken;
    private static boolean warned;

    private AbyssalAir() {}

    public static void onPlayerTick(PlayerTickEvent.Post event) {
        if (!(event.getEntity() instanceof ServerPlayer player) || player.tickCount % PERIOD != 0) return;
        if (!StrataTweaks.abyssalRoomsNeedOxygen()) return;
        if (!player.level().dimension().location().equals(DIMENSION) || player.isSpectator()) {
            FAILING.remove(player.getUUID());
            RESTING.remove(player.getUUID());
            return;
        }
        try {
            long began = TIMING ? System.nanoTime() : 0L;
            // A big room that was fine is walked less often (it costs about a millisecond per 3,000 cells): the
            // next checks are skipped and paid for in one go. Anything wrong is looked at every time.
            int[] rest = RESTING.get(player.getUUID());
            if (rest != null && rest[0]-- > 0) return;
            boolean purging = StrataTweaks.abyssalDiffusersPushWater() && purge(player, (ServerLevel) player.level());
            if (player.isCreative()) FAILING.remove(player.getUUID());
            else check(player, (ServerLevel) player.level(), purging);
            // -Dstrata.tweaks.airTiming=true: how long each check took, for measuring this rule on a server.
            if (TIMING) org.slf4j.LoggerFactory.getLogger("Strata Tweaks").info("Abyssal room check: {} us", (System.nanoTime() - began) / 1000);
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

    private static void check(ServerPlayer player, ServerLevel level, boolean purging) {
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
        // Oxygen used: 2 mB plus 1 per 1,000 cells, every two seconds (a ship's Diffuser uses 100 in that time),
        // for this check and, when there is enough, for the ones a big room skips after it.
        int skips = seen.size() / REST_CELLS;
        int base = 2 + seen.size() / 1000;
        int need = base * (1 + skips);
        for (BlockPos at : diffusers) {
            if (supplied || need <= 0) break;
            need -= drain(level, at, need);
        }
        // A Diffuser that is still pushing the water out nearby counts: the air above it is its own.
        if (supplied || purging || need <= base * skips) {
            FAILING.remove(player.getUUID());
            if (skips > 0 && !purging && (supplied || need <= 0)) RESTING.put(player.getUUID(), new int[] {skips});
            else RESTING.remove(player.getUUID());
            return;
        }
        RESTING.remove(player.getUUID());
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

    private static boolean wet(BlockState state, ServerLevel level, BlockPos pos) {
        return state.getFluidState().is(FluidTags.WATER) && state.getCollisionShape(level, pos).isEmpty();
    }

    /** Diffusers near the player that hold oxygen push the water out of a closed space; true if one did. */
    private static boolean purge(ServerPlayer player, ServerLevel level) {
        BlockPos at = player.blockPosition();
        List<BlockPos> found = new ArrayList<>();
        for (int cx = (at.getX() - PURGE_REACH) >> 4; cx <= (at.getX() + PURGE_REACH) >> 4; cx++) {
            for (int cz = (at.getZ() - PURGE_REACH) >> 4; cz <= (at.getZ() + PURGE_REACH) >> 4; cz++) {
                LevelChunk chunk = level.getChunkSource().getChunkNow(cx, cz);
                if (chunk == null) continue;
                for (BlockPos pos : chunk.getBlockEntities().keySet()) {
                    if (Math.abs(pos.getX() - at.getX()) > PURGE_REACH || Math.abs(pos.getY() - at.getY()) > PURGE_REACH
                            || Math.abs(pos.getZ() - at.getZ()) > PURGE_REACH) continue;
                    if (BuiltInRegistries.BLOCK.getKey(chunk.getBlockState(pos).getBlock()).equals(DIFFUSER)) found.add(pos.immutable());
                }
            }
        }
        boolean any = false;
        long now = level.getGameTime();
        for (BlockPos pos : found) {
            Long wait = OPEN_UNTIL.get(pos.asLong());
            if (wait != null && wait > now) continue;
            if (stored(level, pos) <= 0) continue;
            int result = purgeFrom(level, pos);
            if (result > 0) {
                any = true;
                level.playSound(null, pos, SoundEvents.BUBBLE_COLUMN_UPWARDS_AMBIENT, SoundSource.BLOCKS, 1.0F, 1.0F);
                player.displayClientMessage(Component.literal("The Oxygen Diffuser is pushing the water out.").withStyle(ChatFormatting.AQUA), true);
            } else if (result < 0) {
                OPEN_UNTIL.put(pos.asLong(), now + PURGE_RETRY);
                if (OPEN_UNTIL.size() > 4096) OPEN_UNTIL.values().removeIf(until -> until <= now);
                player.displayClientMessage(Component.literal("This space is open to the sea. The oxygen has nowhere to stay.")
                        .withStyle(ChatFormatting.AQUA, ChatFormatting.ITALIC), true);
            }
        }
        return any;
    }

    /** One step for one Diffuser: cells dried (0 = nothing to do), or -1 when its water reaches the open sea. */
    private static int purgeFrom(ServerLevel level, BlockPos diffuser) {
        int floor = diffuser.getY();
        LongOpenHashSet seen = new LongOpenHashSet();
        LongArrayList queue = new LongArrayList();
        BlockPos.MutableBlockPos cell = new BlockPos.MutableBlockPos(), next = new BlockPos.MutableBlockPos();
        for (Direction dir : Direction.values()) {
            if (dir == Direction.DOWN) continue;
            next.setWithOffset(diffuser, dir);
            if (wet(level.getBlockState(next), level, next) && seen.add(next.asLong())) queue.add(next.asLong());
        }
        for (int i = 0; i < queue.size(); i++) {
            cell.set(queue.getLong(i));
            for (Direction dir : Direction.values()) {
                next.setWithOffset(cell, dir);
                if (next.getY() < floor) continue;                  // trapped air never spreads below its source
                if (!level.isLoaded(next)) return -1;
                if (!wet(level.getBlockState(next), level, next) || seen.contains(next.asLong())) continue;
                if (seen.size() >= PURGE_MAX) return -1;
                seen.add(next.asLong());
                queue.add(next.asLong());
            }
        }
        if (queue.isEmpty()) return 0;
        int top = Integer.MIN_VALUE, count = 0;
        for (int i = 0; i < queue.size(); i++) {
            int y = BlockPos.getY(queue.getLong(i));
            if (y > top) {
                top = y;
                count = 0;
            }
            if (y == top) count++;
        }
        // 1 mB of oxygen for every 20 cells of water pushed out.
        if (drain(level, diffuser, Math.max(1, (count + 19) / 20)) <= 0) return 0;
        for (int i = 0; i < queue.size(); i++) {
            cell.set(queue.getLong(i));
            if (cell.getY() != top) continue;
            level.setBlock(cell, Blocks.AIR.defaultBlockState(), 3);
            for (Direction dir : Direction.values()) {
                next.setWithOffset(cell, dir);
                BlockState state = level.getBlockState(next);
                if (state.hasProperty(BlockStateProperties.WATERLOGGED) && state.getValue(BlockStateProperties.WATERLOGGED)
                        && !(state.getBlock() instanceof LiquidBlock) && !state.getCollisionShape(level, next).isEmpty()) {
                    level.setBlock(next, state.setValue(BlockStateProperties.WATERLOGGED, false), 3);
                }
            }
        }
        return count;
    }

    /** Oxygen in the diffuser at {@code pos}, in mB. */
    private static int stored(ServerLevel level, BlockPos pos) {
        BlockEntity be = level.getBlockEntity(pos);
        if (be == null || tankBroken) return 0;
        try {
            if (oxygenTank == null) oxygenTank = be.getClass().getField("oxygenTank");
            return oxygenTank.get(be) instanceof IFluidHandler handler ? handler.getFluidInTank(0).getAmount() : 0;
        } catch (ReflectiveOperationException | RuntimeException e) {
            tankBroken = true;
            return 0;
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
