# Roll Number: MT25046
# PA02 Part D: Professional Performance Visualization
import matplotlib.pyplot as plt
import os
import numpy as np

# ---------------------------------------------------------
# Configuration & Directory Setup
# ---------------------------------------------------------
OUTPUT_DIR = "plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

system_info = "System: Linux | CPU: x86_64 (Hybrid) | Threads: 1, 2, 4, 8"
msg_sizes = [1024, 4096, 16384, 65536]
msg_labels = ['1KB', '4KB', '16KB', '64KB']
threads = [1, 2, 4, 8]

# ---------------------------------------------------------
# VERIFIED HARD-CODED VALUES (Extracted from MT25046_Part_C_Results.csv)
# ---------------------------------------------------------

# Plot 1: Throughput (Gbps) vs Message Size (Threads=4)
throughput_A1 = [1.901260, 3.457383, 5.714884, 19.276332]
throughput_A2 = [3.865997, 8.600654, 28.729002, 60.213093]
throughput_A3 = [2.449172, 6.393183, 20.733090, 46.034261]

# Plot 2: Latency (µs) vs Thread Count (Size=1024)
lat_A1 = [4.516687, 4.697866, 4.308725, 4.951955]
lat_A2 = [1.621000, 1.761020, 2.118988, 2.245692]
lat_A3 = [2.461477, 2.839393, 3.344804, 4.710199]

# Plot 3: Cache Misses (Threads=4)
l1_A1 = [327834123, 526405590, 663350646, 1554967920]
l1_A2 = [418249976, 584316360, 2012412754, 3387189605]
l1_A3 = [411337724, 602395615, 1826112322, 2911453937]

llc_A1 = [7343, 9900, 42580, 21787]
llc_A2 = [8776, 11100, 14439, 28453]
llc_A3 = [53415, 7166, 10808, 32452]

# Plot 4: CPU Cycles (Threads=4) for Cycles per Byte
cycles_A1 = [97339949176, 95473420086, 75905887486, 76368539974]
cycles_A2 = [77271359447, 75539964918, 73962976272, 74708748286]
cycles_A3 = [74968731759, 75483646679, 77224511985, 76537571571]

cpb_A1 = [c / s for c, s in zip(cycles_A1, msg_sizes)]
cpb_A2 = [c / s for c, s in zip(cycles_A2, msg_sizes)]
cpb_A3 = [c / s for c, s in zip(cycles_A3, msg_sizes)]

# ---------------------------------------------------------
# Visualization Functions
# ---------------------------------------------------------

def plot_throughput():
    plt.figure(figsize=(10, 6))
    x = np.arange(len(msg_labels))
    width = 0.25
    plt.bar(x - width, throughput_A1, width, label='Two-Copy (A1)', color='#d62728', edgecolor='black')
    plt.bar(x, throughput_A2, width, label='One-Copy (A2)', color='#1f77b4', edgecolor='black')
    plt.bar(x + width, throughput_A3, width, label='Zero-Copy (A3)', color='#2ca02c', edgecolor='black')
    plt.ylabel('Throughput (Gbps)', fontweight='bold')
    plt.xticks(x, msg_labels)
    plt.title(f'Throughput vs Message Size (Threads=4)\n{system_info}')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(OUTPUT_DIR, "throughput_vs_size.png"), dpi=300)
    plt.close()

def plot_latency():
    plt.figure(figsize=(10, 6))
    plt.plot(threads, lat_A1, 'o-', label='A1', color='#d62728', linewidth=2)
    plt.plot(threads, lat_A2, 's-', label='A2', color='#1f77b4', linewidth=2)
    plt.plot(threads, lat_A3, '^-', label='A3', color='#2ca02c', linewidth=2)
    plt.xlabel('Thread Count', fontweight='bold')
    plt.ylabel('Latency (µs)', fontweight='bold')
    plt.title(f'Latency vs Thread Count (Size=1KB)\n{system_info}')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(os.path.join(OUTPUT_DIR, "latency_vs_threads.png"), dpi=300)
    plt.close()

def plot_combined_cache():
    plt.figure(figsize=(10, 6))
    # Using log scale for dual-axis effect in a single plot
    plt.plot(msg_labels, llc_A1, 'o-', color='#d62728', label="A1: LLC Misses")
    plt.plot(msg_labels, l1_A1, 'o:', color='#d62728', label="A1: L1 Misses", alpha=0.5)
    plt.plot(msg_labels, llc_A2, 's-', color='#1f77b4', label="A2: LLC Misses")
    plt.plot(msg_labels, l1_A2, 's:', color='#1f77b4', label="A2: L1 Misses", alpha=0.5)
    plt.plot(msg_labels, llc_A3, '^-', color='#2ca02c', label="A3: LLC Misses")
    plt.plot(msg_labels, l1_A3, '^:', color='#2ca02c', label="A3: L1 Misses", alpha=0.5)
    plt.yscale('log')
    plt.ylabel('Miss Count (Log Scale)', fontweight='bold')
    plt.title(f'Cache Behavior (L1 & LLC) vs Message Size\n{system_info}')
    plt.legend(ncol=2, fontsize='small')
    plt.grid(True, which="both", linestyle='--', alpha=0.4)
    plt.savefig(os.path.join(OUTPUT_DIR, "cache_vs_size.png"), dpi=300)
    plt.close()

def plot_cycles_per_byte():
    plt.figure(figsize=(10, 6))
    plt.plot(msg_labels, cpb_A1, 'o-', label='A1', color='#d62728', linewidth=2)
    plt.plot(msg_labels, cpb_A2, 's-', label='A2', color='#1f77b4', linewidth=2)
    plt.plot(msg_labels, cpb_A3, '^-', label='A3', color='#2ca02c', linewidth=2)
    plt.ylabel('CPU Cycles per Byte', fontweight='bold')
    plt.title(f'CPU Cycles per Byte vs Message Size (Threads=4)\n{system_info}')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(os.path.join(OUTPUT_DIR, "cycles_per_byte.png"), dpi=300)
    plt.close()

if __name__ == "__main__":
    plot_throughput()
    plot_latency()
    plot_combined_cache()
    plot_cycles_per_byte()
    print(f"✅ Professional plots generated in ./{OUTPUT_DIR}/")

# import matplotlib.pyplot as plt
# import os

# # ---------------------------------------------------------
# # Create plots directory
# # ---------------------------------------------------------
# OUTPUT_DIR = "plots"
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# system_info = "System: Linux | CPU: x86_64 | Threads tested: 1,2,4,8"
# msg_sizes = [1024, 4096, 16384, 65536]
# threads = [1, 2, 4, 8]

# # ---------------------------------------------------------
# # UPDATED HARD-CODED VALUES (Verified from Final CSV)
# # ---------------------------------------------------------

# # Throughput vs message size (Threads = 4)
# throughput_A1 = [1.901260, 3.748368, 11.692552, 26.425571]
# throughput_A2 = [3.865997, 8.600654, 28.729002, 60.742976]
# throughput_A3 = [2.449172, 6.393183, 20.733090, 46.034261]

# # Latency vs thread count (Size = 1024)
# lat_A1 = [4.516687, 4.697866, 4.308725, 4.951955]
# lat_A2 = [1.621000, 1.761020, 2.118988, 2.245692]
# lat_A3 = [2.461477, 2.839393, 3.344804, 4.710199]

# # Cache misses (Threads = 4)
# l1_A1 = [327834123, 303741892, 555448142, 800829385]
# l1_A2 = [187391823, 343661239, 800268067, 1093222172]
# l1_A3 = [319721296, 302070647, 706089900, 847447487]

# llc_A1 = [7343, 8578, 42580, 21787]
# llc_A2 = [8776, 11100, 14439, 28453]
# llc_A3 = [53415, 7166, 10808, 32452]

# # CPU cycles (Threads = 4) for Cycles per Byte
# cycles_A1 = [97339949176, 96010110863, 75905887486, 76368539974]
# cycles_A2 = [77271359447, 75424923422, 73962976272, 74708748286]
# cycles_A3 = [74968731759, 75483646679, 77224511985, 76537571571]

# cpb_A1 = [c / s for c, s in zip(cycles_A1, msg_sizes)]
# cpb_A2 = [c / s for c, s in zip(cycles_A2, msg_sizes)]
# cpb_A3 = [c / s for c, s in zip(cycles_A3, msg_sizes)]

# # ---------------------------------------------------------
# # Plotting Logic
# # ---------------------------------------------------------

# def save_plot(x, y_sets, labels, xlabel, ylabel, title, filename, styles=None):
#     plt.figure(figsize=(10, 6))
#     for i, (y, label) in enumerate(zip(y_sets, labels)):
#         style = styles[i] if styles else '-'
#         plt.plot(x, y, marker='o', label=label, linestyle=style)
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     plt.title(title + "\n" + system_info)
#     plt.legend()
#     plt.grid(True, linestyle='--', alpha=0.6)
#     plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=300, bbox_inches="tight")
#     plt.close()

# # Combined Cache Plot (L1 Dotted, LLC Solid)
# plt.figure(figsize=(10, 6))
# colors = ['#1f77b4', '#ff7f0e', '#2ca02c'] # Blue, Orange, Green
# plt.plot(msg_sizes, llc_A1, marker='o', color=colors[0], linestyle='-', label="A1: LLC Misses")
# plt.plot(msg_sizes, l1_A1, marker='s', color=colors[0], linestyle=':', label="A1: L1 Misses")
# plt.plot(msg_sizes, llc_A2, marker='o', color=colors[1], linestyle='-', label="A2: LLC Misses")
# plt.plot(msg_sizes, l1_A2, marker='s', color=colors[1], linestyle=':', label="A2: L1 Misses")
# plt.plot(msg_sizes, llc_A3, marker='o', color=colors[2], linestyle='-', label="A3: LLC Misses")
# plt.plot(msg_sizes, l1_A3, marker='s', color=colors[2], linestyle=':', label="A3: L1 Misses")
# plt.yscale('log') # Use log scale because L1 is much higher than LLC
# plt.xlabel("Message Size (Bytes)")
# plt.ylabel("Cache Misses (Log Scale)")
# plt.title("L1 & LLC Misses vs Message Size (Threads=4)\n" + system_info)
# plt.legend(ncol=2)
# plt.grid(True, which="both", linestyle='--', alpha=0.5)
# plt.savefig(os.path.join(OUTPUT_DIR, "combined_cache_misses.png"), dpi=300)
# plt.close()

# # Generate other required plots
# save_plot(msg_sizes, [throughput_A1, throughput_A2, throughput_A3], 
#           ["A1", "A2", "A3"], "Message Size (Bytes)", "Throughput (Gbps)", "Throughput vs Size", "throughput_vs_size.png")
# save_plot(threads, [lat_A1, lat_A2, lat_A3], 
#           ["A1", "A2", "A3"], "Threads", "Latency (µs)", "Latency vs Threads", "latency_vs_threads.png")
# save_plot(msg_sizes, [cpb_A1, cpb_A2, cpb_A3], 
#           ["A1", "A2", "A3"], "Message Size (Bytes)", "Cycles/Byte", "CPU Cycles per Byte", "cycles_per_byte.png")

# print("✅ Plots updated with combined cache data and verified CSV values.")
# import matplotlib.pyplot as plt
# import os

# # ---------------------------------------------------------
# # Create plots directory (generated during assignment run)
# # ---------------------------------------------------------
# OUTPUT_DIR = "plots"
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# # ---------------------------------------------------------
# # System configuration (must appear on plots)
# # ---------------------------------------------------------
# system_info = "System: Linux | CPU: x86_64 | Threads tested: 1,2,4,8"

# # ---------------------------------------------------------
# # Common axes
# # ---------------------------------------------------------
# msg_sizes = [1024, 4096, 16384, 65536]
# threads = [1, 2, 4, 8]

# # ---------------------------------------------------------
# # HARD-CODED VALUES FROM NEW CSV DATA (PA02 rule)
# # ---------------------------------------------------------

# # Throughput vs message size (extracted where threads = 4)
# throughput_A1 = [1.901260, 3.457383, 5.714884, 19.276332]
# throughput_A2 = [3.865997, 8.600654, 28.729002, 60.213093]
# throughput_A3 = [2.449172, 6.393183, 20.733090, 46.034261]

# # Latency vs thread count (extracted where message size = 1024)
# lat_A1 = [4.516687, 4.697866, 4.308725, 4.951955]
# lat_A2 = [1.621000, 1.761020, 2.118988, 2.245692]
# lat_A3 = [2.461477, 2.839393, 3.344804, 4.710199]

# # Cache misses (Threads = 4)
# l1_A1 = [327834123, 303741892, 555448142, 800829385]
# l1_A2 = [187391823, 343661239, 800268067, 1093222172]
# l1_A3 = [319721296, 302070647, 706089900, 847447487]

# llc_A1 = [7343, 8578, 42580, 21787]
# llc_A2 = [8776, 11100, 14439, 28453]
# llc_A3 = [53415, 7166, 10808, 32452]

# # CPU cycles (extracted where threads = 4) to calculate cycles per byte
# cycles_A1 = [97339949176, 95473420086, 75905887486, 76368539974]
# cycles_A2 = [77271359447, 75539964918, 73962976272, 74708748286]
# cycles_A3 = [74968731759, 75483646679, 77224511985, 76537571571]

# cycles_per_byte_A1 = [c / s for c, s in zip(cycles_A1, msg_sizes)]
# cycles_per_byte_A2 = [c / s for c, s in zip(cycles_A2, msg_sizes)]
# cycles_per_byte_A3 = [c / s for c, s in zip(cycles_A3, msg_sizes)]

# # ---------------------------------------------------------
# # Helper function to generate & save plots
# # ---------------------------------------------------------
# def save_plot(x, y_sets, labels, xlabel, ylabel, title, filename):
#     plt.figure(figsize=(10, 6))
#     for y, label in zip(y_sets, labels):
#         plt.plot(x, y, marker='o', linestyle='-', linewidth=2, label=label)

#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     plt.title(title + "\n" + system_info)
#     plt.legend()
#     plt.grid(True, linestyle='--', alpha=0.7)

#     plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=300, bbox_inches="tight")
#     plt.close()

# # ---------------------------------------------------------
# # Generate all four plots automatically
# # ---------------------------------------------------------

# # Plot 1: Throughput vs Message Size
# save_plot(
#     msg_sizes,
#     [throughput_A1, throughput_A2, throughput_A3],
#     ["Two-Copy (A1)", "One-Copy (A2)", "Zero-Copy (A3)"],
#     "Message Size (Bytes)",
#     "Throughput (Gbps)",
#     "Throughput vs Message Size (Threads=4)",
#     "throughput_vs_size.png",
# )

# # Plot 2: Latency vs Thread Count
# save_plot(
#     threads,
#     [lat_A1, lat_A2, lat_A3],
#     ["Two-Copy (A1)", "One-Copy (A2)", "Zero-Copy (A3)"],
#     "Thread Count",
#     "Latency (µs)",
#     "Latency vs Thread Count (Size=1024)",
#     "latency_vs_threads.png",
# )

# # Plot 3: Cache Misses vs Message Size
# save_plot(
#     msg_sizes,
#     [cache_A1, cache_A2, cache_A3],
#     ["Two-Copy (A1)", "One-Copy (A2)", "Zero-Copy (A3)"],
#     "Message Size (Bytes)",
#     "LLC Cache Misses",
#     "LLC Misses vs Message Size (Threads=4)",
#     "cache_vs_size.png",
# )

# # Plot 4: CPU Cycles per Byte
# save_plot(
#     msg_sizes,
#     [cycles_per_byte_A1, cycles_per_byte_A2, cycles_per_byte_A3],
#     ["Two-Copy (A1)", "One-Copy (A2)", "Zero-Copy (A3)"],
#     "Message Size (Bytes)",
#     "CPU Cycles per Byte",
#     "CPU Cycles per Byte vs Message Size (Threads=4)",
#     "cycles_per_byte.png",
# )

# print(f"✅ All 4 plots generated inside ./{OUTPUT_DIR}/")