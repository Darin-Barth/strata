#!/usr/bin/env bash
# Boot the real Strata world (container strata-world, data in server/) from a pack copy served on :8080,
# set the spawn, and start Chunky. Usage: tools/start_pregen.sh <pack-dir>
# just `docker start strata-world` and run `chunky continue` over rcon.
set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"; D="$REPO/server"; PACK="$1"
SEED=-6609605124472974960; SX=416; SY=70; SZ=16; RADIUS=5000
r(){ docker exec strata-world rcon-cli "$*" 2>&1 | sed 's/\x1b\[[0-9;]*m//g'; }
mkdir -p "$D"
(cd "$PACK" && "$HOME/go/bin/packwiz.exe" refresh >/dev/null && exec "$HOME/go/bin/packwiz.exe" serve --port 8080) > "$D/../build/serve-pregen.log" 2>&1 &
SERVE=$!
for i in $(seq 1 120); do curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/pack.toml | grep -q 200 && break; sleep 1; done
MSYS_NO_PATHCONV=1 docker run -d --name strata-world -p 25565:25565 -e EULA=TRUE -e TYPE=NEOFORGE -e VERSION=1.21.1 -e NEOFORGE_VERSION=21.1.264 \
  -e PACKWIZ_URL=http://host.docker.internal:8080/pack.toml -e MEMORY=12G -e SEED="$SEED" -e MOTD="Strata" \
  -e JVM_XX_OPTS="-XX:+UseZGC -XX:+ZGenerational" -e SYNC_CHUNK_WRITES=false -v "$D:/data" itzg/minecraft-server:java21 >/dev/null
start=$(date +%s); ok=0
for i in $(seq 1 200); do
  st=$(docker inspect -f '{{.State.Status}}' strata-world)
  docker logs strata-world 2>&1 | grep -qE 'Done \([0-9.]+s\)! For help' && { ok=1; break; }
  [ "$st" != running ] && { echo "CONTAINER $st"; docker logs strata-world 2>&1 | grep -E "^\s+- |requires|Caused by" | head -15; break; }
  sleep 5
done
kill $SERVE 2>/dev/null
[ $ok = 1 ] || exit 2
echo "booted in $(( $(date +%s) - start ))s; $(r seed)"
r "setworldspawn $SX $SY $SZ"
r "chunky world minecraft:overworld"; r "chunky center $SX $SZ"; r "chunky shape circle"; r "chunky radius $RADIUS"
r "chunky start"; r "chunky confirm"
sleep 20; docker logs --tail 3 strata-world 2>&1 | grep Chunky | tail -1
