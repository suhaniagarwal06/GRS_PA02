#!/bin/bash

PORT=9000
DURATION=5

MESSAGE_SIZES=(1024 4096 16384 65536)
THREAD_COUNTS=(1 2 4 8)
IMPLEMENTATIONS=("A1" "A2" "A3")

CSV="MT25046_Part_C_Results.csv"

# rm -f "$CSV"
# echo "Impl,MsgSize,Threads,ThroughputGbps,LatencyUs,CPUCycles,CacheMisses,ContextSwitches" >> "$CSV"

make clean >/dev/null 2>&1
make >/dev/null 2>&1 || { echo "Compilation failed"; exit 1; }

rm -f "$CSV"
echo "Impl,MsgSize,Threads,ThroughputGbps,LatencyUs,CPUCycles,CacheMisses,ContextSwitches" >> "$CSV"

run_test() {
    IMPL=$1
    SIZE=$2
    THREADS=$3

    SERVER="./MT25046_Part_${IMPL}_Server"
    CLIENT="./MT25046_Part_${IMPL}_Client"

    $SERVER $PORT $SIZE > server.log 2>&1 &
    SERVER_PID=$!

    while ! grep -q "READY" server.log; do sleep 0.1; done

    PERF_OUT=$(perf stat -e cycles,cache-misses,context-switches \
        $CLIENT 127.0.0.1 $PORT $SIZE $THREADS $DURATION 2>&1)

    kill $SERVER_PID >/dev/null 2>&1
    wait $SERVER_PID 2>/dev/null

    # -------- Take ONLY LAST RESULT line (aggregate)
    RESULT_LINE=$(echo "$PERF_OUT" | grep "^RESULT" | tail -n 1)

    THROUGHPUT=$(echo "$RESULT_LINE" | awk '{print $2}')
    LATENCY=$(echo "$RESULT_LINE" | awk '{print $3}')

    # -------- Robust perf parsing
    CYCLES=$(echo "$PERF_OUT" | grep "cycles" | head -n1 | sed 's/,//g' | awk '{print $1}')
    CACHE=$(echo "$PERF_OUT" | grep "cache-misses" | head -n1 | sed 's/,//g' | awk '{print $1}')
    CTX=$(echo "$PERF_OUT" | grep "context-switches" | head -n1 | sed 's/,//g' | awk '{print $1}')

    # -------- Fallback safety
    THROUGHPUT=${THROUGHPUT:-0}
    LATENCY=${LATENCY:-0}
    CYCLES=${CYCLES:-0}
    CACHE=${CACHE:-0}
    CTX=${CTX:-0}

    echo "$IMPL,$SIZE,$THREADS,$THROUGHPUT,$LATENCY,$CYCLES,$CACHE,$CTX" >> "$CSV"

    echo "Done → $IMPL | Size=$SIZE | Threads=$THREADS"
}

for IMPL in "${IMPLEMENTATIONS[@]}"; do
    for SIZE in "${MESSAGE_SIZES[@]}"; do
        for THREADS in "${THREAD_COUNTS[@]}"; do
            run_test "$IMPL" "$SIZE" "$THREADS"
        done
    done
done

echo "All experiments finished."
