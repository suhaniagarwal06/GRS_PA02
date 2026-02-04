# MT25046 — GRS PA02

**Graduate Systems (CSE638)**
**Assignment:** Analysis of Network I/O Primitives using `perf`

---

# 1. Overview

This assignment experimentally evaluates the **cost of data movement in network I/O** by comparing:

* **Two-copy socket communication (A1)**
* **One-copy optimized communication (A2)**
* **Zero-copy communication using `MSG_ZEROCOPY` (A3)**

All implementations are **multithreaded TCP client–server programs** and are profiled using the **Linux `perf` tool** to study:

* Throughput
* Latency
* CPU cycles
* Cache misses
* Context switches

---

# 2. Repository Structure

```
MT25046_PA02/
│
├── MT25046_Part_A1_Server.c
├── MT25046_Part_A1_Client.c
├── MT25046_Part_A2_Server.c
├── MT25046_Part_A2_Client.c
├── MT25046_Part_A3_Server.c
├── MT25046_Part_A3_Client.c
│
├── MT25046_Part_C_RunExperiments.sh
├── MT25046_Run_All.sh
├── MT25046_Part_D_Plots.py
│
├── MT25046_Part_C_Results.csv
├── Plots
├── Makefile
├── README.md
└── Report.pdf
```

**Naming convention strictly follows PA02 rules.**

---

# 3. Compilation Instructions

Compile all implementations using:

```
make
```

This builds:

* A1 server & client
* A2 server & client
* A3 server & client

Compiler flags:

* `-O2` → realistic performance profiling
* `-pthread` → multithreading support

---

# 4. Running Experiments (Part-C)

Automated experiment script:

```
sudo ./MT25046_Part_C_RunExperiments.sh
```

### The script performs:

* Clean compilation
* Runs **all combinations** of:

  * 4 message sizes → 1KB, 4KB, 16KB, 64KB
  * 4 thread counts → 1, 2, 4, 8
  * 3 implementations → A1, A2, A3
* Collects:

  * Throughput & latency (application level)
  * CPU cycles, cache misses, context switches (`perf stat`)
* Stores results in:

```
MT25046_Part_C_Results.csv
```

### No manual intervention is required.

---

# 5. Plot Generation (Part-D)

Plots are generated using:

```
python3 MT25046_Part_D_Plots.py
```

### Important PA02 compliance:

* **Matplotlib only**
* **Values hard-coded (NO CSV reading)**
* Plots include:

  * Axis labels
  * Legends
  * System configuration
* Four required plots:

  * Throughput vs Message Size
  * Latency vs Thread Count
  * Cache Misses vs Message Size
  * CPU Cycles per Byte

Temporary images are saved in:

```
plots/
```

### Clean removal:

```
make clean
```

removes:

* Binaries
* CSV results
* `plots/` directory

---

# 6. Implementation Details (Part-A)

## A1 — Two-Copy Communication

Uses:

```
send() / recv()
```

Copies occur:

1. User → kernel socket buffer
2. Kernel → NIC / receiver buffer

---

## A2 — One-Copy Optimization

Uses:

```
sendmsg() with pre-registered buffer
```

Eliminates:

* One intermediate kernel copy

Result:

* Reduced CPU overhead
* Lower latency for medium/large messages

---

## A3 — Zero-Copy Communication

Uses:

```
sendmsg() + MSG_ZEROCOPY
```

Kernel behavior:

* Pages are **pinned and directly transmitted**
* Completion notified via **error queue**

Benefits:

* Reduced CPU usage for **large transfers**
* Overhead may hurt **small messages**

---

# 7. Measurements Collected (Part-B)

For each configuration:

* Throughput (Gbps)
* Latency (µs)
* CPU cycles
* Cache misses (LLC)
* Context switches

Total experiments:

```
3 implementations × 4 sizes × 4 threads = 48 runs
```

---

# 8. AI Usage Declaration

AI tools were used for:

* Code debugging and correction
* Performance interpretation guidance
* Plotting script structuring
* Documentation refinement

All generated code was:

* **Reviewed manually**
* **Understood line-by-line**
* **Modified to satisfy PA02 rules**

No blind code submission was performed.

---

# 9. How to Reproduce Results

```
make clean
make
sudo ./MT25046_Part_C_RunExperiments.sh
./MT25046_Run_All.sh
python3 MT25046_Part_D_Plots.py
```

This reproduces:

* CSV measurements
* All four plots

---

# 10. Notes for Evaluation

* Code is **modular, commented, and structured**
* Automation is **fully reproducible**
* Plotting strictly follows **hard-coding requirement**
* Repository is **public as required**

---

# 11. Author

**Roll Number:** MT25046
**Course:** CSE638 — Graduate Systems
**Institute:** IIIT Delhi

---

# End of README
