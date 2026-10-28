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
| 4.4% | Streams Reflowing | Rivers |
| 3.9% | TerraBlender | Surface rules |
| 2.7% | Integrated API (IDAS) | Structures |
| ≤2% each | Mowzie's Mobs, ModernFix, AE2 (meteorites), Steam 'n' Rails, Excessive Utilities, YUNG's Cave Biomes | |

By step: noise fill (terrain shape) 37%, feature decoration 19%, the rest is aquifers, biomes and surface.

## What it means
- Slimming worldgen mods (Tectonic, Quark features) would barely speed up pregeneration, because the worker threads already wait on the main thread.
- The levers are the **main thread's chunk unload/save** and **memory cleanup**:
  1. More heap and generational ZGC for the server (30% of CPU went to G1 in run 1). Run 2 measures it.
  2. Server settings that lighten chunk saving (run 3).
- The same main-thread behavior is what singleplayer players feel as freezes when flying into new terrain. On treehouse, pregeneration moves it to before launch.
- **Treehouse estimate:** at roughly 5–7 chunks/s (run 1 settings), a 5,000-block radius (about 390k chunks) is 15–20+ hours in the Overworld alone. Plan for a multi-night pregen, or a smaller first radius.

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

## Run 3: chunk writes (same seed, region and profiler; 12 GB + generational ZGC)
| Run | Change | Time for 5,929 chunks | Stalls | Notes |
| --- | --- | --- | --- | --- |
| 2 | (baseline: 12 GB + ZGC) | 12 min 02 s | 1 (3.5 s) | |
| 3 | `sync-chunk-writes=false` | **11 min 34 s** | 0 | Safe server setting (itzg `SYNC_CHUNK_WRITES=false`). Small win |

**Conclusions**
- Treehouse: 12 GB + generational ZGC + `sync-chunk-writes=false`. About 20% faster than run 1, with far fewer stalls.
- Pregenerating on the faster desktop and copying the world to treehouse is the other practical lever.
- Two normal runs on the same seed differ in about 70% of chunk surface heightmaps (trees and mod features aren't deterministic); structure counts match.

**Variant chests:** Quark's `Replace Worldgen Chests = false` is set, but worlds still hold about 170 Quark variant chests. They come from Artifacts' campsites (`useModdedChests = false` in `config/artifacts/general.toml` turns those off) and from IDAS structures (no setting found). Lootr can't convert these, so their loot isn't per-player. The Artifacts setting needs a check in the next server test.

## Final pregen

The final seed is `-1678324137078475659`. The Nether pregen radius is 1,250 blocks.
