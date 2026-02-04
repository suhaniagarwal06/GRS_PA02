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
# HARD-CODED VALUES FROM FINAL CSV  (PA02 rule)
# ---------------------------------------------------------

# Throughput vs message size (threads = 4)
throughput_A1 = [23.500089, 32.949083, 25.601345, 22.525410]
throughput_A2 = [19.868088, 25.835550, 22.392252, 21.245714]
throughput_A3 = [20.223489, 25.911797, 23.433695, 21.719602]

# Latency vs thread count (message size = 1024)
lat_A1 = [26.401940, 27.512845, 23.500089, 19.131448]
lat_A2 = [27.267088, 24.877104, 19.868088, 11.971516]
lat_A3 = [28.001805, 25.410531, 20.223489, 15.063669]

# Cache misses vs message size (threads = 4)
cache_A1 = [232203667, 1110799, 2449830, 2474210]
cache_A2 = [145135793, 1827827, 6139592, 2761909]
cache_A3 = [213954337, 1673806, 1283489, 2370526]

# CPU cycles per byte (threads = 4)
cycles_A1 = [70795354570, 52527616098, 41320676611, 38212361855]
cycles_A2 = [61644985394, 42657972807, 34033343386, 35569131277]
cycles_A3 = [61050211481, 46057140796, 37650426650, 36495853396]

cycles_per_byte_A1 = [c / s for c, s in zip(cycles_A1, msg_sizes)]
cycles_per_byte_A2 = [c / s for c, s in zip(cycles_A2, msg_sizes)]
cycles_per_byte_A3 = [c / s for c, s in zip(cycles_A3, msg_sizes)]

# ---------------------------------------------------------
# Helper function to generate & save plots
# ---------------------------------------------------------
def save_plot(x, y_sets, labels, xlabel, ylabel, title, filename):
    plt.figure()
    for y, label in zip(y_sets, labels):
        plt.plot(x, y, marker='o', label=label)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title + "\n" + system_info)
    plt.legend()
    plt.grid()

    plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=300, bbox_inches="tight")
    plt.close()   # IMPORTANT → prevents blocking

# ---------------------------------------------------------
# Generate all four plots automatically
# ---------------------------------------------------------
save_plot(
    msg_sizes,
    [throughput_A1, throughput_A2, throughput_A3],
    ["Two-Copy (A1)", "One-Copy (A2)", "Zero-Copy (A3)"],
    "Message Size (Bytes)",
    "Throughput (Gbps)",
    "Throughput vs Message Size",
    "throughput_vs_size.png",
)

save_plot(
    threads,
    [lat_A1, lat_A2, lat_A3],
    ["Two-Copy (A1)", "One-Copy (A2)", "Zero-Copy (A3)"],
    "Thread Count",
    "Latency (µs)",
    "Latency vs Thread Count",
    "latency_vs_threads.png",
)

save_plot(
    msg_sizes,
    [cache_A1, cache_A2, cache_A3],
    ["Two-Copy (A1)", "One-Copy (A2)", "Zero-Copy (A3)"],
    "Message Size (Bytes)",
    "Cache Misses",
    "Cache Misses vs Message Size",
    "cache_vs_size.png",
)

save_plot(
    msg_sizes,
    [cycles_per_byte_A1, cycles_per_byte_A2, cycles_per_byte_A3],
    ["Two-Copy (A1)", "One-Copy (A2)", "Zero-Copy (A3)"],
    "Message Size (Bytes)",
    "CPU Cycles per Byte",
    "CPU Cycles per Byte vs Message Size",
    "cycles_per_byte.png",
)

print("✅ All 4 plots generated inside ./plots/")

# import matplotlib.pyplot as plt

# # =========================================================
# # System configuration (must appear in plots as per PA02)
# # =========================================================
# system_info = "System: Linux | CPU: x86_64 | Threads tested: 1,2,4,8"

# # =========================================================
# # Common axes
# # =========================================================
# msg_sizes = [1024, 4096, 16384, 65536]
# threads = [1, 2, 4, 8]

# # =========================================================
# # HARD-CODED VALUES FROM FINAL CSV  (NO CSV READING ALLOWED)
# # =========================================================

# # ---- Throughput vs Message Size (threads = 4) ----
# throughput_A1 = [23.500089, 32.949083, 25.601345, 22.525410]
# throughput_A2 = [19.868088, 25.835550, 22.392252, 21.245714]
# throughput_A3 = [20.223489, 25.911797, 23.433695, 21.719602]

# # ---- Latency vs Thread Count (message size = 1024) ----
# lat_A1 = [26.401940, 27.512845, 23.500089, 19.131448]
# lat_A2 = [27.267088, 24.877104, 19.868088, 11.971516]
# lat_A3 = [28.001805, 25.410531, 20.223489, 15.063669]

# # ---- Cache Misses vs Message Size (threads = 4) ----
# cache_A1 = [232203667, 1110799, 2449830, 2474210]
# cache_A2 = [145135793, 1827827, 6139592, 2761909]
# cache_A3 = [213954337, 1673806, 1283489, 2370526]

# # ---- CPU Cycles per Byte (threads = 4) ----
# cycles_A1 = [70795354570, 52527616098, 41320676611, 38212361855]
# cycles_A2 = [61644985394, 42657972807, 34033343386, 35569131277]
# cycles_A3 = [61050211481, 46057140796, 37650426650, 36495853396]

# cycles_per_byte_A1 = [c / s for c, s in zip(cycles_A1, msg_sizes)]
# cycles_per_byte_A2 = [c / s for c, s in zip(cycles_A2, msg_sizes)]
# cycles_per_byte_A3 = [c / s for c, s in zip(cycles_A3, msg_sizes)]

# # =========================================================
# # Plot 1 — Throughput vs Message Size
# # =========================================================
# plt.figure()
# plt.plot(msg_sizes, throughput_A1, marker='o', label="Two-Copy (A1)")
# plt.plot(msg_sizes, throughput_A2, marker='o', label="One-Copy (A2)")
# plt.plot(msg_sizes, throughput_A3, marker='o', label="Zero-Copy (A3)")
# plt.xlabel("Message Size (Bytes)")
# plt.ylabel("Throughput (Gbps)")
# plt.title("Throughput vs Message Size\n" + system_info)
# plt.legend()
# plt.grid()
# plt.show()

# # =========================================================
# # Plot 2 — Latency vs Thread Count
# # =========================================================
# plt.figure()
# plt.plot(threads, lat_A1, marker='o', label="Two-Copy (A1)")
# plt.plot(threads, lat_A2, marker='o', label="One-Copy (A2)")
# plt.plot(threads, lat_A3, marker='o', label="Zero-Copy (A3)")
# plt.xlabel("Thread Count")
# plt.ylabel("Latency (µs)")
# plt.title("Latency vs Thread Count\n" + system_info)
# plt.legend()
# plt.grid()
# plt.show()

# # =========================================================
# # Plot 3 — Cache Misses vs Message Size
# # =========================================================
# plt.figure()
# plt.plot(msg_sizes, cache_A1, marker='o', label="Two-Copy (A1)")
# plt.plot(msg_sizes, cache_A2, marker='o', label="One-Copy (A2)")
# plt.plot(msg_sizes, cache_A3, marker='o', label="Zero-Copy (A3)")
# plt.xlabel("Message Size (Bytes)")
# plt.ylabel("Cache Misses")
# plt.title("Cache Misses vs Message Size\n" + system_info)
# plt.legend()
# plt.grid()
# plt.show()

# # =========================================================
# # Plot 4 — CPU Cycles per Byte Transferred
# # =========================================================
# plt.figure()
# plt.plot(msg_sizes, cycles_per_byte_A1, marker='o', label="Two-Copy (A1)")
# plt.plot(msg_sizes, cycles_per_byte_A2, marker='o', label="One-Copy (A2)")
# plt.plot(msg_sizes, cycles_per_byte_A3, marker='o', label="Zero-Copy (A3)")
# plt.xlabel("Message Size (Bytes)")
# plt.ylabel("CPU Cycles per Byte")
# plt.title("CPU Cycles per Byte vs Message Size\n" + system_info)
# plt.legend()
# plt.grid()
# plt.show()
