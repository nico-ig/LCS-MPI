#!/bin/bash

echo "CPU,Frequency_MHz"
for cpu_dir in /sys/devices/system/cpu/cpu[0-9]*; do
    if [ -f "$cpu_dir/online" ] && [ "$(cat $cpu_dir/online)" = "0" ]; then
        continue  # skip offline CPUs
    fi
    freq_file="$cpu_dir/cpufreq/scaling_cur_freq"
    cpu_num=$(basename $cpu_dir | sed 's/cpu//')
    if [ -f "$freq_file" ]; then
        freq_khz=$(cat "$freq_file")
        freq_mhz=$(awk "BEGIN {printf \"%.2f\", $freq_khz/1000}")
        echo "$cpu_num,$freq_mhz"
    fi
done | sort -n
