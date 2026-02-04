import matplotlib.pyplot as plt
import os

# ---------------------------------------------------------
# Create plots directory (generated during assignment run)
# ---------------------------------------------------------
OUTPUT_DIR = "plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------
# System configuration (must appear on plots)
# ---------------------------------------------------------
system_info = "System: Linux | CPU: x86_64 | Threads tested: 1,2,4,8"

# ---------------------------------------------------------
# Common axes
# ---------------------------------------------------------
msg_sizes = [1024, 4096, 16384, 65536]
threads = [1, 2, 4, 8]

# ---------------------------------------------------------
# HARD-CODED VALUES FROM NEW CSV DATA (PA02 rule)
# ---------------------------------------------------------

# Throughput vs message size (extracted where threads = 4)
throughput_A1 = [1.901260, 3.457383, 5.714884, 19.276332]
throughput_A2 = [3.865997, 8.600654, 28.729002, 60.213093]
throughput_A3 = [2.449172, 6.393183, 20.733090, 46.034261]

# Latency vs thread count (extracted where message size = 1024)
lat_A1 = [4.516687, 4.697866, 4.308725, 4.951955]
lat_A2 = [1.621000, 1.761020, 2.118988, 2.245692]
lat_A3 = [2.461477, 2.839393, 3.344804, 4.710199]

# Cache misses vs message size (LLCMisses used; extracted where threads = 4)
cache_A1 = [7343, 9900, 42580, 21787]
cache_A2 = [8776, 11100, 14439, 28453]
cache_A3 = [53415, 7166, 10808, 32452]

# CPU cycles (extracted where threads = 4) to calculate cycles per byte
cycles_A1 = [97339949176, 95473420086, 75905887486, 76368539974]
cycles_A2 = [77271359447, 75539964918, 73962976272, 74708748286]
cycles_A3 = [74968731759, 75483646679, 77224511985, 76537571571]

cycles_per_byte_A1 = [c / s for c, s in zip(cycles_A1, msg_sizes)]
cycles_per_byte_A2 = [c / s for c, s in zip(cycles_A2, msg_sizes)]
cycles_per_byte_A3 = [c / s for c, s in zip(cycles_A3, msg_sizes)]

# ---------------------------------------------------------
# Helper function to generate & save plots
# ---------------------------------------------------------
def save_plot(x, y_sets, labels, xlabel, ylabel, title, filename):
    plt.figure(figsize=(10, 6))
    for y, label in zip(y_sets, labels):
        plt.plot(x, y, marker='o', linestyle='-', linewidth=2, label=label)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title + "\n" + system_info)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=300, bbox_inches="tight")
    plt.close()

# ---------------------------------------------------------
# Generate all four plots automatically
# ---------------------------------------------------------

# Plot 1: Throughput vs Message Size
save_plot(
    msg_sizes,
    [throughput_A1, throughput_A2, throughput_A3],
    ["Two-Copy (A1)", "One-Copy (A2)", "Zero-Copy (A3)"],
    "Message Size (Bytes)",
    "Throughput (Gbps)",
    "Throughput vs Message Size (Threads=4)",
    "throughput_vs_size.png",
)

# Plot 2: Latency vs Thread Count
save_plot(
    threads,
    [lat_A1, lat_A2, lat_A3],
    ["Two-Copy (A1)", "One-Copy (A2)", "Zero-Copy (A3)"],
    "Thread Count",
    "Latency (µs)",
    "Latency vs Thread Count (Size=1024)",
    "latency_vs_threads.png",
)

# Plot 3: Cache Misses vs Message Size
save_plot(
    msg_sizes,
    [cache_A1, cache_A2, cache_A3],
    ["Two-Copy (A1)", "One-Copy (A2)", "Zero-Copy (A3)"],
    "Message Size (Bytes)",
    "LLC Cache Misses",
    "LLC Misses vs Message Size (Threads=4)",
    "cache_vs_size.png",
)

# Plot 4: CPU Cycles per Byte
save_plot(
    msg_sizes,
    [cycles_per_byte_A1, cycles_per_byte_A2, cycles_per_byte_A3],
    ["Two-Copy (A1)", "One-Copy (A2)", "Zero-Copy (A3)"],
    "Message Size (Bytes)",
    "CPU Cycles per Byte",
    "CPU Cycles per Byte vs Message Size (Threads=4)",
    "cycles_per_byte.png",
)

print(f"✅ All 4 plots generated inside ./{OUTPUT_DIR}/")