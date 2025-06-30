#!/bin/bash

FREQ="$1"
if [ -z "$FREQ" ]; then
cat <<EOF
Usage: $0 <frequency_in_kHz>
Example: $0 1400000
EOF
    exit 1
fi

echo "Setting CPU frequency to $FREQ kHz..."

for cpu_dir in /sys/devices/system/cpu/cpu*/cpufreq; do
    cpu=$(basename "$(dirname "$cpu_dir")")
    avail_freqs=$(cat "$cpu_dir/scaling_available_frequencies" 2>/dev/null)
    if [ -n "$avail_freqs" ]; then
        echo userspace | sudo tee "$cpu_dir/scaling_governor" > /dev/null
        echo $FREQ | sudo tee "$cpu_dir/scaling_setspeed" > /dev/null
    fi
done

echo "CPU frequency setting complete."
