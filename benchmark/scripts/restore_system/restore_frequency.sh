#!/bin/bash

DEFAULT_GOVERNOR_FILE="/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
DEFAULT_GOVERNOR=$(cat "$DEFAULT_GOVERNOR_FILE")

echo "Restoring CPU frequency governor to '$DEFAULT_GOVERNOR'..."
for cpu_dir in /sys/devices/system/cpu/cpu*/cpufreq; do
    cpu=$(basename "$(dirname "$cpu_dir")")
    echo $DEFAULT_GOVERNOR | sudo tee "$cpu_dir/scaling_governor" 2&>/dev/null || true;
done

echo "CPU frequency governor restoration complete."