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
