# Worldgen performance profile

**Setup:** Docker test server (itzg `java21`, 8 GB, G1 GC), i5-13600K (20 threads), fresh world. Chunky pregenerated a 600-block radius (5,929 chunks) in the Overworld while Spark's async profiler recorded every thread. The profile was saved to a local file and decoded with `tools/profiling/` (nothing uploaded).

## Results
- **Speed:** 5,929 chunks in 14 min 27 s, about **6.8 chunks/s** on average. The rate swung between 0.3 and 130 chunks/s.
- **CPU was not the limit.** The server used about 2–3 of 20 hardware threads. Idle CPU is 7–10% (Sable's native physics threads sleep and don't spin).

| Thread | CPU during the run | Notes |
| --- | --- | --- |
| Server thread (main) | ~11 min (busy almost the whole run) | **The bottleneck.** 86% of its busy time is `ChunkMap.processUnloads` (unloading and saving chunks), mostly vanilla task-queue churn (`ConcurrentLinkedDeque`, `CompletableFuture`). Mods on this thread: NeoForge 3.4%, Sable 1.9%, Serene Seasons 0.6%. |
| 17 Worker-Main threads (worldgen) | ~1 min each | Mostly idle. |
| G1 GC (concurrent + parallel) | ~14.6 min (~30% of all CPU) | Memory pressure at 8 GB. |

**Worldgen work by mod** (worker threads; a mod counts if it's anywhere on the stack):

| Share | Mod | What |
| --- | --- | --- |
| 24% | Lithostitched (Tectonic's library) | Terrain shape: density functions and splines (most of the 37% `fillFromNoise`) |
| 7% | Quark + Zeta | Quark's worldgen features |
| 5% | Biolith | Biome placement |
| 4.4% | Streams Reflowing | Rivers |
| 3.9% | TerraBlender | Surface rules |
| 2.7% | Integrated API (IDAS) | Structures |
| ≤2% each | Mowzie's Mobs, ModernFix, AE2 (meteorites), Steam 'n' Rails, Excessive Utilities, YUNG's Cave Biomes | |

By step: noise fill (terrain shape) 37%, feature decoration 19%, the rest is aquifers, biomes and surface.

## What it means
- Slimming worldgen mods (Tectonic, Quark features) would barely speed up pregeneration, because the worker threads already wait on the main thread.
- The levers are the **main thread's chunk unload/save** and **memory cleanup**:
  1. More heap and/or generational ZGC for the server (30% of CPU went to G1). Re-measure the rate afterwards.
  2. Possibly a chunk-system replacement (for example Moonrise, the Paper chunk system port). This is untested here and would need a compatibility check with Sable/Create and the worldgen mods.
- The same main-thread behavior is what singleplayer players feel as freezes when flying into new terrain. On treehouse, pregeneration moves it to before launch.
- **Treehouse estimate:** at roughly 5–7 chunks/s, a 5,000-block radius (about 390k chunks) is 15–20+ hours in the Overworld alone, before any fixes. Plan for a multi-night pregen, or a smaller first radius.

## Run 2: 12 GB + generational ZGC (same seed, same region, same profiler)
| | Run 1: 8 GB, G1 | Run 2: 12 GB, ZGC generational |
| --- | --- | --- |
| Time for 5,929 chunks | 14 min 27 s | **12 min 02 s** (17% faster) |
| Average rate | 6.8 chunks/s | **8.2 chunks/s** |
| GC CPU | ~14.6 min (~30% of all CPU) | **~2.3 min** (~8%) |
| Main server thread CPU | ~11 min | ~9.5 min (still the bottleneck) |
| Worst server stall | 5.9 s | 3.5 s |
| Container memory | ~10.6 GiB | ~14.3 GiB (of the 15.5 GiB Docker VM, tight) |

**Takeaways**
- ZGC removes most of the memory-cleanup cost and shortens stalls. That matters more for how play *feels* (fewer freezes) than for pregen speed.
- Pregeneration is still limited by the main thread's chunk unload/save, so expect only modest speed-ups from memory settings.
- ZGC needs headroom: with a 12 GB heap the process used ~14.3 GiB. Treehouse (32 GB) is fine; size the Docker/host memory accordingly.

**Recommended settings** (ship in the pack docs / server compose):
- Treehouse server: `MEMORY=12G`, `JVM_XX_OPTS=-XX:+UseZGC -XX:+ZGenerational`.
- Singleplayer clients: 10 GB + the same two flags.
- Multiplayer clients (no local worldgen): 8 GB + the same flags. Confirm in a multiplayer test.

## Runs 3–5: other fixes (same seed, region and profiler; all with 12 GB + generational ZGC)
| Run | Change | Time for 5,929 chunks | Stalls | Notes |
| --- | --- | --- | --- | --- |
| 2 | (baseline: 12 GB + ZGC) | 12 min 02 s | 1 (3.5 s) | |
| 3 | `sync-chunk-writes=false` | **11 min 34 s** | 0 | Safe server setting (itzg `SYNC_CHUNK_WRITES=false`). Small win |
| 4 | + Moonrise + Moonrise Compats | **didn't start** | n/a | Mixin conflict with Cobblemon on `Entity.collide` (Moonrise's collision rewrite). Not usable while Cobblemon is in |
| 5 | + C2ME (pregen-only idea) | **2 min 11 s** (~5× faster) | 0 | Clipped structures: 67 "setBlock in a far chunk" warnings from Integrated Cobblemon's flying and dark gyms (none in normal runs). Ars Nouveau light blocks 138 vs ~5. Otherwise within normal variation |

**Same-seed world comparison:** two normal runs already differ in about 70% of chunk surface heightmaps (trees and mod features aren't deterministic), so C2ME's 76% is within normal variation. Structure counts match. The only C2ME-specific damage found is the clipped Integrated Cobblemon gyms and the extra Ars light blocks.

**Conclusions**
- Treehouse: 12 GB + generational ZGC + `sync-chunk-writes=false`. About 20% faster than run 1, with far fewer stalls.
- C2ME is ~5× faster for pregeneration but alters structures. Only consider it pregen-only, and only after the Integrated Cobblemon gyms move to the Pokémon world (they'd then generate there, not in the Overworld pregen). Never leave it installed for play.
- Pregenerating on the faster desktop and copying the world to treehouse is the other practical lever.

**Side finding (fixed):** both normal worlds still had ~170 Quark variant chests even with Quark's `Replace Worldgen Chests = false`. They come from Artifacts' campsites (`useModdedChests`, now set false in `config/artifacts/general.toml`) and from IDAS structures (no setting found). Lootr can't convert these, so their loot isn't per-player. Verify the Artifacts change in the next server test.

## C2ME for the final Overworld pregen

The Integrated Cobblemon gyms now generate in the Pokémon world (and Nether/End), so C2ME (`c2me-neoforge` 0.4.0-alpha.0.123) was re-tested as a **pregen-only** tool on the final seed `-1678324137078475659`, same 900×900-block area around spawn (3,481 chunks):

| | Normal | C2ME |
|---|---|---|
| Time | 5 min 7 s | **57 s** (5.4×) |
| "setBlock in a far chunk" warnings | n/a | **0** |
| Mean height step inside chunks / across chunk borders | 1.430 / 1.424 | 1.435 / 1.443 |
| Steps ≥ 8 blocks inside / across borders | 5.32% / 5.46% | 5.31% / 5.57% |
| Tavern village building blocks identical (same block, same spot) | | **99.83%** (the rest are Create's natural limestone/scoria/zinc patches) |
| Ars Nouveau light blocks | 330 | 331 |
| Structure starts | 269 | 272 (one extra Better Archeology fossil) |

Tree, leaf and ore positions differ, as they do between two normal runs. Maps side by side: `docs/images/c2me-pregen-compare.png`. Why it's faster: the vanilla chunk scheduler (`ChunkMap.tick`) runs on the main thread and was 66% of a maxed-out server thread, while the 19 worldgen workers used about 2 cores; C2ME spreads the work (13 cores in use, ~50 chunks/s vs ~11).

**Used for:** the Overworld pregen only (resumed with C2ME at 2.7%; the first 10,500 chunks were generated normally). The Nether (1,250-block radius) was generated without it. **The End, Aether and Pokémon world are generated without C2ME** (Cobblemon gyms live in the Pokémon world, Nether and End), and C2ME is removed before anyone plays. Never ship it in the pack.
