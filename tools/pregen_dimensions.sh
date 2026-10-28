#!/usr/bin/env bash
# Pregenerate the non-Overworld dimensions on strata-world, two at a time (one Chunky task per dimension;
# each dimension has its own scheduler thread). Run WITHOUT C2ME. Usage: tools/pregen_dimensions.sh <spawn x> <spawn z>
set -u
r(){ docker exec strata-world rcon-cli "$*" 2>&1 | sed 's/\x1b\[[0-9;]*m//g'; }
SX="$1"; SZ="$2"
QUEUE=("minecraft:the_nether $((SX / 8)) $((SZ / 8)) 1250" "minecraft:the_end 0 0 2000" "aether:the_aether $SX $SZ 1000" "pokeworld:pokeworld $SX $SZ 2000" "twilightforest:twilight_forest $SX $SZ 1500" "strata:abyssal_plain $SX $SZ 1000" "strata:hollow $SX $SZ 1000")
r "sable paused true" >/dev/null
start_task(){ set -- $1; r "chunky world $1" >/dev/null; r "chunky center $2 $3" >/dev/null; r "chunky shape circle" >/dev/null; r "chunky radius $4" >/dev/null; r "chunky start" >/dev/null; r "chunky confirm" >/dev/null; echo "$(date +%H:%M) started $1 r=$4"; }
running=0; i=0; t0=$(date -u +%Y-%m-%dT%H:%M:%SZ)
while [ $i -lt ${#QUEUE[@]} ] && [ $running -lt 2 ]; do start_task "${QUEUE[$i]}"; i=$((i+1)); running=$((running+1)); done
done_count=0
while [ $done_count -lt ${#QUEUE[@]} ]; do
  sleep 20
  docker inspect -f '{{.State.Status}}' strata-world | grep -q running || { echo "SERVER DOWN"; exit 1; }
  n=$(docker logs --since "$t0" strata-world 2>&1 | grep -c "\[Chunky\] Task finished for")
  while [ $n -gt $done_count ]; do
    done_count=$((done_count+1)); echo "$(date +%H:%M) $(docker logs --since "$t0" strata-world 2>&1 | grep '\[Chunky\] Task finished for' | sed -n "${done_count}p" | grep -oE 'for [a-z_:]+\. Processed: [0-9]+ chunks.*')"
    if [ $i -lt ${#QUEUE[@]} ]; then start_task "${QUEUE[$i]}"; i=$((i+1)); fi
  done
done
echo "$(date +%H:%M) ALL DIMENSIONS DONE"
