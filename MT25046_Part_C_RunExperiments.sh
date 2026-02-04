#!/bin/bash
# Roll Number: MT25046
# PA02: Master Experiment Runner (Server-Side Profiling with Hybrid CPU Fixes)

PORT=9000
DURATION=5
MESSAGE_SIZES=(1024 4096 16384 65536)
THREAD_COUNTS=(1 2 4 8)
IMPLEMENTATIONS=("A1" "A2" "A3")

CSV="MT25046_Part_C_Results.csv"
NS_SERVER="ns_server"
NS_CLIENT="ns_client"
SERVER_IP="10.0.0.1"
CLIENT_IP="10.0.0.2"

# ------------------------------------------------------------
# Cleanup function (ALWAYS runs on exit)
# ------------------------------------------------------------
cleanup() {
    ip netns del $NS_SERVER 2>/dev/null || true
    ip netns del $NS_CLIENT 2>/dev/null || true
    ip link del veth_server 2>/dev/null || true
}
trap cleanup EXIT

# ------------------------------------------------------------
# Setup Network Namespaces
# ------------------------------------------------------------
ip netns del $NS_SERVER 2>/dev/null || true
ip netns del $NS_CLIENT 2>/dev/null || true
ip link del veth_server 2>/dev/null || true

ip netns add $NS_SERVER
ip netns add $NS_CLIENT
ip link add veth_server type veth peer name veth_client
ip link set veth_server netns $NS_SERVER
ip link set veth_client netns $NS_CLIENT
ip netns exec $NS_SERVER ip addr add $SERVER_IP/24 dev veth_server
ip netns exec $NS_CLIENT ip addr add $CLIENT_IP/24 dev veth_client
ip netns exec $NS_SERVER ip link set veth_server up
ip netns exec $NS_CLIENT ip link set veth_client up
ip netns exec $NS_SERVER ip link set lo up
ip netns exec $NS_CLIENT ip link set lo up

# ------------------------------------------------------------
# Compilation
# ------------------------------------------------------------
make clean >/dev/null 2>&1
make >/dev/null 2>&1 || { echo "Compilation failed"; exit 1; }

# Fresh CSV
rm -f "$CSV"
echo "Impl,MsgSize,Threads,ThroughputGbps,LatencyUs,CPUCycles,L1Misses,LLCMisses,ContextSwitches" > "$CSV"

# ------------------------------------------------------------
# Test runner (Server-Side Profiling)
# ------------------------------------------------------------
run_test() {
    > server.log
    IMPL=$1
    SIZE=$2
    THREADS=$3

    SERVER="$(pwd)/MT25046_Part_${IMPL}_Server"
    CLIENT="$(pwd)/MT25046_Part_${IMPL}_Client"

    # 1. Start Server in its namespace
    ip netns exec $NS_SERVER $SERVER $PORT $SIZE > server.log 2>&1 &
    SERVER_PID=$!

    # 2. Wait for Server READY
    for i in {1..50}; do
        grep -q "READY" server.log && break
        sleep 0.1
    done

    if ! grep -q "READY" server.log; then
        echo "Server failed → $IMPL size=$SIZE threads=$THREADS"
        kill $SERVER_PID 2>/dev/null
        return
    fi

    # 3. Start PERF on the SERVER PID in the server namespace
    # We use taskset -c 0 for hybrid CPU stability.
    # We run perf in the background to capture the server while the client runs.
    ip netns exec $NS_SERVER taskset -c 0 perf stat -e cpu_core/cycles/,cpu_core/L1-dcache-load-misses/,cpu_core/LLC-load-misses/,context-switches -p $SERVER_PID > perf_server.out 2>&1 &
    PERF_PID=$!

    # 4. Start CLIENT in its namespace to generate load
    # We capture the RESULT from the client output (throughput/latency)
    CLIENT_OUT=$(ip netns exec $NS_CLIENT timeout $((DURATION + 5)) $CLIENT $SERVER_IP $PORT $SIZE $THREADS $DURATION 2>&1)

    # 5. Stop Perf and Server
    # Sending SIGINT to perf allows it to finish and write its statistics output.
    kill -INT $PERF_PID 2>/dev/null
    wait $PERF_PID 2>/dev/null
    kill -9 $SERVER_PID 2>/dev/null
    wait $SERVER_PID 2>/dev/null

    # 6. Parse Data
    RESULT_LINE=$(echo "$CLIENT_OUT" | grep "^RESULT" | tail -n 1)
    THROUGHPUT=$(echo "$RESULT_LINE" | awk '{print $2}')
    LATENCY=$(echo "$RESULT_LINE" | awk '{print $3}')

    # Parse Perf metrics from the server's perf output file
    extract_perf() {
        echo "$(cat perf_server.out)" | tr -d ',' | awk -v key="$1" '$0 ~ key {print $1; exit}'
    }

    CYCLES=$(extract_perf "cpu_core/cycles/")
    L1=$(extract_perf "cpu_core/L1-dcache-load-misses/")
    LLC=$(extract_perf "cpu_core/LLC-load-misses/")
    CTX=$(extract_perf "context-switches")

    # Fallback to generic names
    [[ -z "$CYCLES" ]] && CYCLES=$(extract_perf "cycles")
    [[ -z "$L1" ]]     && L1=$(extract_perf "L1-dcache-load-misses")
    [[ -z "$LLC" ]]    && LLC=$(extract_perf "LLC-load-misses")

    # Clean non-numeric values
    [[ ! "$CYCLES" =~ ^[0-9]+$ ]] && CYCLES=0
    [[ ! "$L1" =~ ^[0-9]+$ ]]     && L1=0
    [[ ! "$LLC" =~ ^[0-9]+$ ]]    && LLC=0
    [[ ! "$CTX" =~ ^[0-9]+$ ]]    && CTX=0

    echo "$IMPL,$SIZE,$THREADS,${THROUGHPUT:-0},${LATENCY:-0},$CYCLES,$L1,$LLC,$CTX" >> "$CSV"
    echo "Done → $IMPL | Size=$SIZE | Threads=$THREADS | Server Cycles=$CYCLES"
    rm -f perf_server.out
}

# ------------------------------------------------------------
# Main Loop
# ------------------------------------------------------------
for IMPL in "${IMPLEMENTATIONS[@]}"; do
    for SIZE in "${MESSAGE_SIZES[@]}"; do
        for THREADS in "${THREAD_COUNTS[@]}"; do
            run_test "$IMPL" "$SIZE" "$THREADS"
        done
    done
done

echo "All experiments finished."

# #!/bin/bash
# # Roll Number: MT25046
# # PA02: Master Experiment Runner with Hybrid CPU Fixes

# PORT=9000
# DURATION=5

# MESSAGE_SIZES=(1024 4096 16384 65536)
# THREAD_COUNTS=(1 2 4 8)
# IMPLEMENTATIONS=("A1" "A2" "A3")

# CSV="MT25046_Part_C_Results.csv"

# NS_SERVER="ns_server"
# NS_CLIENT="ns_client"

# SERVER_IP="10.0.0.1"
# CLIENT_IP="10.0.0.2"

# # ------------------------------------------------------------
# # Cleanup function (ALWAYS runs on exit)
# # ------------------------------------------------------------
# cleanup() {
#     ip netns del $NS_SERVER 2>/dev/null || true
#     ip netns del $NS_CLIENT 2>/dev/null || true
#     ip link del veth_server 2>/dev/null || true
# }
# trap cleanup EXIT

# # ------------------------------------------------------------
# # Remove old namespaces if present
# # ------------------------------------------------------------
# ip netns del $NS_SERVER 2>/dev/null || true
# ip netns del $NS_CLIENT 2>/dev/null || true
# ip link del veth_server 2>/dev/null || true

# # ------------------------------------------------------------
# # Create namespaces and veth pair
# # ------------------------------------------------------------
# ip netns add $NS_SERVER
# ip netns add $NS_CLIENT

# ip link add veth_server type veth peer name veth_client
# ip link set veth_server netns $NS_SERVER
# ip link set veth_client netns $NS_CLIENT

# ip netns exec $NS_SERVER ip addr add $SERVER_IP/24 dev veth_server
# ip netns exec $NS_CLIENT ip addr add $CLIENT_IP/24 dev veth_client

# ip netns exec $NS_SERVER ip link set veth_server up
# ip netns exec $NS_CLIENT ip link set veth_client up
# ip netns exec $NS_SERVER ip link set lo up
# ip netns exec $NS_CLIENT ip link set lo up

# # ------------------------------------------------------------
# # Compile fresh
# # ------------------------------------------------------------
# make clean >/dev/null 2>&1
# make >/dev/null 2>&1 || { echo "Compilation failed"; exit 1; }

# # ------------------------------------------------------------
# # Fresh CSV
# # ------------------------------------------------------------
# rm -f "$CSV"
# echo "Impl,MsgSize,Threads,ThroughputGbps,LatencyUs,CPUCycles,L1Misses,LLCMisses,ContextSwitches" > "$CSV"

# # ------------------------------------------------------------
# # Test runner
# # ------------------------------------------------------------
# run_test() {
#     > server.log

#     IMPL=$1
#     SIZE=$2
#     THREADS=$3

#     SERVER="$(pwd)/MT25046_Part_${IMPL}_Server"
#     CLIENT="$(pwd)/MT25046_Part_${IMPL}_Client"

#     # Start server
#     ip netns exec $NS_SERVER $SERVER $PORT $SIZE > server.log 2>&1 &
#     SERVER_PID=$!

#     # Wait for READY (max 5 sec)
#     for i in {1..50}; do
#         grep -q "READY" server.log && break
#         sleep 0.1
#     done

#     if ! grep -q "READY" server.log; then
#         echo "Server failed → $IMPL size=$SIZE threads=$THREADS"
#         kill $SERVER_PID 2>/dev/null
#         return
#     fi

#     # UPDATE: taskset -c 0 pins to a P-core. Targeting cpu_core/ PMUs directly.
#     # We capture stderr (2>&1) because perf outputs stats there.
#     PERF_OUT=$(ip netns exec $NS_CLIENT timeout 15 \
#         taskset -c 0 perf stat -e cpu_core/cycles/,cpu_core/L1-dcache-load-misses/,cpu_core/LLC-load-misses/,context-switches -- \
#         $CLIENT $SERVER_IP $PORT $SIZE $THREADS $DURATION 2>&1)

#     kill $SERVER_PID >/dev/null 2>&1
#     wait $SERVER_PID 2>/dev/null

#     # Extract RESULT
#     RESULT_LINE=$(echo "$PERF_OUT" | grep "^RESULT" | tail -n 1)
#     THROUGHPUT=$(echo "$RESULT_LINE" | awk '{print $2}')
#     LATENCY=$(echo "$RESULT_LINE" | awk '{print $3}')

#     # Perf parsing
#     # tr -d ',' is essential to handle large numbers (e.g., 1,234,567)
#     extract_perf() {
#         echo "$PERF_OUT" \
#         | tr -d ',' \
#         | awk -v key="$1" '$0 ~ key {print $1; exit}'
#     }

#     # Specifically look for the cpu_core strings in the perf output
#     CYCLES=$(extract_perf "cpu_core/cycles/")
#     L1=$(extract_perf "cpu_core/L1-dcache-load-misses/")
#     LLC=$(extract_perf "cpu_core/LLC-load-misses/")
#     CTX=$(extract_perf "context-switches")

#     # Fallback: if cpu_core strings are not found, try generic names
#     [[ -z "$CYCLES" ]] && CYCLES=$(extract_perf "cycles")
#     [[ -z "$L1" ]]     && L1=$(extract_perf "L1-dcache-load-misses")
#     [[ -z "$LLC" ]]    && LLC=$(extract_perf "LLC-load-misses")

#     # Replace invalid, empty, or "<not counted>" with 0 for safety
#     [[ ! "$CYCLES" =~ ^[0-9]+$ ]] && CYCLES=0
#     [[ ! "$L1" =~ ^[0-9]+$ ]]     && L1=0
#     [[ ! "$LLC" =~ ^[0-9]+$ ]]    && LLC=0
#     [[ ! "$CTX" =~ ^[0-9]+$ ]]    && CTX=0

#     echo "$IMPL,$SIZE,$THREADS,${THROUGHPUT:-0},${LATENCY:-0},$CYCLES,$L1,$LLC,$CTX" >> "$CSV"

#     echo "Done → $IMPL | Size=$SIZE | Threads=$THREADS | L1Misses=$L1 | LLCMisses=$LLC"
# }

# # ------------------------------------------------------------
# # Run all experiments
# # ------------------------------------------------------------
# for IMPL in "${IMPLEMENTATIONS[@]}"; do
#     for SIZE in "${MESSAGE_SIZES[@]}"; do
#         for THREADS in "${THREAD_COUNTS[@]}"; do
#             run_test "$IMPL" "$SIZE" "$THREADS"
#         done
#     done
# done

# echo "All experiments finished."


# #!/bin/bash

# PORT=9000
# DURATION=5

# MESSAGE_SIZES=(1024 4096 16384 65536)
# THREAD_COUNTS=(1 2 4 8)
# IMPLEMENTATIONS=("A1" "A2" "A3")

# CSV="MT25046_Part_C_Results.csv"

# NS_SERVER="ns_server"
# NS_CLIENT="ns_client"

# SERVER_IP="10.0.0.1"
# CLIENT_IP="10.0.0.2"

# # ------------------------------------------------------------
# # Cleanup old namespaces if present
# # ------------------------------------------------------------
# sudo ip netns del $NS_SERVER 2>/dev/null
# sudo ip netns del $NS_CLIENT 2>/dev/null

# # ------------------------------------------------------------
# # Create namespaces
# # ------------------------------------------------------------
# sudo ip netns add $NS_SERVER
# sudo ip netns add $NS_CLIENT

# # ------------------------------------------------------------
# # Create veth pair
# # ------------------------------------------------------------
# sudo ip link add veth_server type veth peer name veth_client

# # Move to namespaces
# sudo ip link set veth_server netns $NS_SERVER
# sudo ip link set veth_client netns $NS_CLIENT

# # ------------------------------------------------------------
# # Configure IP addresses
# # ------------------------------------------------------------
# sudo ip netns exec $NS_SERVER ip addr add $SERVER_IP/24 dev veth_server
# sudo ip netns exec $NS_CLIENT ip addr add $CLIENT_IP/24 dev veth_client

# # Bring interfaces up
# sudo ip netns exec $NS_SERVER ip link set veth_server up
# sudo ip netns exec $NS_CLIENT ip link set veth_client up

# # Bring loopback up
# sudo ip netns exec $NS_SERVER ip link set lo up
# sudo ip netns exec $NS_CLIENT ip link set lo up

# # ------------------------------------------------------------
# # Compile fresh
# # ------------------------------------------------------------
# make clean >/dev/null 2>&1
# make >/dev/null 2>&1 || { echo "Compilation failed"; exit 1; }

# # ------------------------------------------------------------
# # Fresh CSV with header
# # ------------------------------------------------------------
# rm -f "$CSV"
# echo "Impl,MsgSize,Threads,ThroughputGbps,LatencyUs,CPUCycles,CacheMisses,ContextSwitches" > "$CSV"

# run_test() {
#     IMPL=$1
#     SIZE=$2
#     THREADS=$3

#     SERVER="./MT25046_Part_${IMPL}_Server"
#     CLIENT="./MT25046_Part_${IMPL}_Client"

#     # Start server inside namespace
#     sudo ip netns exec $NS_SERVER $SERVER $PORT $SIZE > server.log 2>&1 &
#     SERVER_PID=$!

#     # Wait until server ready
#     while ! grep -q "READY" server.log; do sleep 0.1; done

#     # Run client with perf inside client namespace
#     PERF_OUT=$(sudo ip netns exec $NS_CLIENT perf stat -e cycles,cache-misses,context-switches \
#         $CLIENT $SERVER_IP $PORT $SIZE $THREADS $DURATION 2>&1)

#     # Stop server
#     sudo kill $SERVER_PID >/dev/null 2>&1
#     wait $SERVER_PID 2>/dev/null

#     # Extract RESULT line
#     RESULT_LINE=$(echo "$PERF_OUT" | grep "^RESULT" | tail -n 1)

#     THROUGHPUT=$(echo "$RESULT_LINE" | awk '{print $2}')
#     LATENCY=$(echo "$RESULT_LINE" | awk '{print $3}')

#     # Parse perf values safely
#     CYCLES=$(echo "$PERF_OUT" | grep "cycles" | head -n1 | sed 's/,//g' | awk '{print $1}')
#     CACHE=$(echo "$PERF_OUT" | grep "cache-misses" | head -n1 | sed 's/,//g' | awk '{print $1}')
#     CTX=$(echo "$PERF_OUT" | grep "context-switches" | head -n1 | sed 's/,//g' | awk '{print $1}')

#     # Replace unsupported values with 0
#     [[ "$CYCLES" == "<not"* ]] && CYCLES=0
#     [[ "$CACHE" == "<not"* ]] && CACHE=0
#     [[ "$CTX" == "<not"* ]] && CTX=0

#     echo "$IMPL,$SIZE,$THREADS,$THROUGHPUT,$LATENCY,$CYCLES,$CACHE,$CTX" >> "$CSV"

#     echo "Done → $IMPL | Size=$SIZE | Threads=$THREADS"
# }

# # ------------------------------------------------------------
# # Run all experiments
# # ------------------------------------------------------------
# for IMPL in "${IMPLEMENTATIONS[@]}"; do
#     for SIZE in "${MESSAGE_SIZES[@]}"; do
#         for THREADS in "${THREAD_COUNTS[@]}"; do
#             run_test "$IMPL" "$SIZE" "$THREADS"
#         done
#     done
# done

# echo "All experiments finished."

# # ------------------------------------------------------------
# # Cleanup namespaces after experiment
# # ------------------------------------------------------------
# sudo ip netns del $NS_SERVER
# sudo ip netns del $NS_CLIENT

# #!/bin/bash

# PORT=9000
# DURATION=5

# MESSAGE_SIZES=(1024 4096 16384 65536)
# THREAD_COUNTS=(1 2 4 8)
# IMPLEMENTATIONS=("A1" "A2" "A3")

# CSV="MT25046_Part_C_Results.csv"

# NS_SERVER="ns_server"
# NS_CLIENT="ns_client"

# SERVER_IP="10.0.0.1"
# CLIENT_IP="10.0.0.2"

# # ------------------------------------------------------------
# # Ensure namespaces always cleaned on exit
# # ------------------------------------------------------------
# cleanup() {
#     sudo ip netns del $NS_SERVER 2>/dev/null
#     sudo ip netns del $NS_CLIENT 2>/dev/null
# }
# trap cleanup EXIT


# # ------------------------------------------------------------
# # Cleanup old namespaces if present
# # ------------------------------------------------------------
# sudo ip netns del $NS_SERVER 2>/dev/null
# sudo ip netns del $NS_CLIENT 2>/dev/null

# # ------------------------------------------------------------
# # Create namespaces
# # ------------------------------------------------------------
# sudo ip netns add $NS_SERVER
# sudo ip netns add $NS_CLIENT

# # ------------------------------------------------------------
# # Create veth pair
# # ------------------------------------------------------------
# sudo ip link add veth_server type veth peer name veth_client

# # Move to namespaces
# sudo ip link set veth_server netns $NS_SERVER
# sudo ip link set veth_client netns $NS_CLIENT

# # ------------------------------------------------------------
# # Configure IP addresses
# # ------------------------------------------------------------
# sudo ip netns exec $NS_SERVER ip addr add $SERVER_IP/24 dev veth_server
# sudo ip netns exec $NS_CLIENT ip addr add $CLIENT_IP/24 dev veth_client

# # Bring interfaces up
# sudo ip netns exec $NS_SERVER ip link set veth_server up
# sudo ip netns exec $NS_CLIENT ip link set veth_client up

# # Bring loopback up
# sudo ip netns exec $NS_SERVER ip link set lo up
# sudo ip netns exec $NS_CLIENT ip link set lo up

# # ------------------------------------------------------------
# # Compile fresh
# # ------------------------------------------------------------
# make clean >/dev/null 2>&1
# make >/dev/null 2>&1 || { echo "Compilation failed"; exit 1; }

# # ------------------------------------------------------------
# # Fresh CSV with header
# # ------------------------------------------------------------
# rm -f "$CSV"
# echo "Impl,MsgSize,Threads,ThroughputGbps,LatencyUs,CPUCycles,CacheMisses,ContextSwitches" > "$CSV"

# run_test() {
#     IMPL=$1
#     SIZE=$2
#     THREADS=$3

#     SERVER="$(pwd)/MT25046_Part_${IMPL}_Server"
#     CLIENT="$(pwd)/MT25046_Part_${IMPL}_Client"


#     # Start server inside namespace
#     sudo ip netns exec $NS_SERVER $SERVER $PORT $SIZE > server.log 2>&1 &
#     SERVER_PID=$!

#     # Wait until server ready
#     # ---- Wait for server READY with timeout (max 5 sec)
#     for i in {1..50}; do
#         if grep -q "READY" server.log; then
#             break
#         fi
#         sleep 0.1
#     done

#     # ---- If still not ready → fail safely
#     grep -q "READY" server.log || { echo "Server failed to start"; exit 1; }


#     # Run client with perf inside client namespace
#     PERF_OUT=$(sudo ip netns exec $NS_CLIENT perf stat -e cycles,cache-misses,context-switches \
#         $CLIENT $SERVER_IP $PORT $SIZE $THREADS $DURATION 2>&1)

#     # Stop server
#     sudo kill $SERVER_PID >/dev/null 2>&1
#     wait $SERVER_PID 2>/dev/null

#     # Extract RESULT line
#     RESULT_LINE=$(echo "$PERF_OUT" | grep "^RESULT" | tail -n 1)

#     THROUGHPUT=$(echo "$RESULT_LINE" | awk '{print $2}')
#     LATENCY=$(echo "$RESULT_LINE" | awk '{print $3}')

#     # ---- Safety if RESULT line missing
#     if [[ -z "$THROUGHPUT" || -z "$LATENCY" ]]; then
#         echo "Measurement failed for $IMPL size=$SIZE threads=$THREADS"
#         THROUGHPUT=0
#         LATENCY=0
#     fi


#     # Parse perf values safely
#     CYCLES=$(echo "$PERF_OUT" | grep "cycles" | head -n1 | sed 's/,//g' | awk '{print $1}')
#     CACHE=$(echo "$PERF_OUT" | grep "cache-misses" | head -n1 | sed 's/,//g' | awk '{print $1}')
#     CTX=$(echo "$PERF_OUT" | grep "context-switches" | head -n1 | sed 's/,//g' | awk '{print $1}')

#     # Replace unsupported values with 0
#     [[ "$CYCLES" == "<not"* ]] && CYCLES=0
#     [[ "$CACHE" == "<not"* ]] && CACHE=0
#     [[ "$CTX" == "<not"* ]] && CTX=0

#     echo "$IMPL,$SIZE,$THREADS,$THROUGHPUT,$LATENCY,$CYCLES,$CACHE,$CTX" >> "$CSV"

#     echo "Done → $IMPL | Size=$SIZE | Threads=$THREADS"
# }

# # ------------------------------------------------------------
# # Run all experiments
# # ------------------------------------------------------------
# for IMPL in "${IMPLEMENTATIONS[@]}"; do
#     for SIZE in "${MESSAGE_SIZES[@]}"; do
#         for THREADS in "${THREAD_COUNTS[@]}"; do
#             run_test "$IMPL" "$SIZE" "$THREADS"
#         done
#     done
# done

# echo "All experiments finished."

# # ------------------------------------------------------------
# # Cleanup namespaces after experiment
# # ------------------------------------------------------------
# sudo ip netns del $NS_SERVER
# sudo ip netns del $NS_CLIENT


# #!/bin/bash

# PORT=9000
# DURATION=5

# MESSAGE_SIZES=(1024 4096 16384 65536)
# THREAD_COUNTS=(1 2 4 8)
# IMPLEMENTATIONS=("A1" "A2" "A3")

# CSV="MT25046_Part_C_Results.csv"

# # rm -f "$CSV"
# # echo "Impl,MsgSize,Threads,ThroughputGbps,LatencyUs,CPUCycles,CacheMisses,ContextSwitches" >> "$CSV"

# make clean >/dev/null 2>&1
# make >/dev/null 2>&1 || { echo "Compilation failed"; exit 1; }

# rm -f "$CSV"
# echo "Impl,MsgSize,Threads,ThroughputGbps,LatencyUs,CPUCycles,CacheMisses,ContextSwitches" >> "$CSV"

# run_test() {
#     IMPL=$1
#     SIZE=$2
#     THREADS=$3

#     SERVER="./MT25046_Part_${IMPL}_Server"
#     CLIENT="./MT25046_Part_${IMPL}_Client"

#     $SERVER $PORT $SIZE > server.log 2>&1 &
#     SERVER_PID=$!

#     while ! grep -q "READY" server.log; do sleep 0.1; done

#     PERF_OUT=$(perf stat -e cycles,cache-misses,context-switches \
#         $CLIENT 127.0.0.1 $PORT $SIZE $THREADS $DURATION 2>&1)

#     kill $SERVER_PID >/dev/null 2>&1
#     wait $SERVER_PID 2>/dev/null

#     # -------- Take ONLY LAST RESULT line (aggregate)
#     RESULT_LINE=$(echo "$PERF_OUT" | grep "^RESULT" | tail -n 1)

#     THROUGHPUT=$(echo "$RESULT_LINE" | awk '{print $2}')
#     LATENCY=$(echo "$RESULT_LINE" | awk '{print $3}')

#     # -------- Robust perf parsing
#     CYCLES=$(echo "$PERF_OUT" | grep "cycles" | head -n1 | sed 's/,//g' | awk '{print $1}')
#     CACHE=$(echo "$PERF_OUT" | grep "cache-misses" | head -n1 | sed 's/,//g' | awk '{print $1}')
#     CTX=$(echo "$PERF_OUT" | grep "context-switches" | head -n1 | sed 's/,//g' | awk '{print $1}')

#     # -------- Fallback safety
#     THROUGHPUT=${THROUGHPUT:-0}
#     LATENCY=${LATENCY:-0}
#     CYCLES=${CYCLES:-0}
#     CACHE=${CACHE:-0}
#     CTX=${CTX:-0}

#     echo "$IMPL,$SIZE,$THREADS,$THROUGHPUT,$LATENCY,$CYCLES,$CACHE,$CTX" >> "$CSV"

#     echo "Done → $IMPL | Size=$SIZE | Threads=$THREADS"
# }

# for IMPL in "${IMPLEMENTATIONS[@]}"; do
#     for SIZE in "${MESSAGE_SIZES[@]}"; do
#         for THREADS in "${THREAD_COUNTS[@]}"; do
#             run_test "$IMPL" "$SIZE" "$THREADS"
#         done
#     done
# done

# echo "All experiments finished."
