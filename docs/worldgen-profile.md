# Worldgen performance profile (Oct 24, 2026)

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
