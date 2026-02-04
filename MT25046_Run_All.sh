#!/bin/bash

echo "========================================"
echo " PA02 MASTER RUN SCRIPT STARTED"
echo "========================================"

# ---------- Clean previous outputs ----------
echo "[1/3] Cleaning old outputs..."
make clean >/dev/null 2>&1

# ---------- Run experiments ----------
echo "[2/3] Running experiments (~4–5 minutes)..."
chmod +x MT25046_Part_C_RunExperiments.sh
sudo ./MT25046_Part_C_RunExperiments.sh

if [ $? -ne 0 ]; then
    echo "❌ Experiment script failed."
    exit 1
fi

echo "✔ CSV generated."

# ---------- Generate plots ----------
echo "[3/3] Generating plots (PNG files inside ./plots)..."
python3 MT25046_Part_D_Plots.py

echo "========================================"
echo " PA02 RUN COMPLETE"
echo "========================================"
echo "IMPORTANT:"
echo "- Use PNGs from ./plots ONLY for report screenshots."
echo "- Run 'make clean' BEFORE zipping submission."
