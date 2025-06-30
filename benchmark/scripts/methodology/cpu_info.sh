#!/bin/bash

cpuid_output=$(cpuid -1 2>/dev/null)
if [ -z "$cpuid_output" ]; then
    echo "Error: Could not retrieve CPUID information"
    exit 1
fi

# Basic CPU info
vendor=$(grep -m1 -oP 'vendor_id\s*=\s*"\K[^"]+' <<< "$cpuid_output" || echo "N/A")
brand=$(grep -m1 -oP 'brand\s*=\s*"\K[^"]+' <<< "$cpuid_output" | head -1 | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' || echo "N/A")
uarch=$(grep -m1 -oP '\(uarch synth\)\s*=\s*\K[^\n]+' <<< "$cpuid_output" | head -1 | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' || echo "N/A")
family=$(grep -m1 -oP 'family\s*=\s*0x[0-9a-fA-F]+\s*\(\K\d+' <<< "$cpuid_output" || echo "N/A")
model=$(grep -m1 -oP 'model\s*=\s*0x[0-9a-fA-F]+\s*\(\K\d+' <<< "$cpuid_output" || echo "N/A")
stepping=$(grep -m1 -oP 'stepping id\s*=\s*0x[0-9a-fA-F]+\s*\(\K\d+' <<< "$cpuid_output" || echo "N/A")

# Core/thread info
threads=$(grep -m1 -oP 'number of threads\s*=\s*0x[0-9a-fA-F]+\s*\(\K\d+' <<< "$cpuid_output" || echo "1")
tpc=$(grep -m1 -oP 'threads per core\s*=\s*0x[0-9a-fA-F]+\s*\(\K\d+' <<< "$cpuid_output" || echo "1")
physical_cores=$((threads / tpc))

# CPU frequency info
if [ -f /proc/cpuinfo ]; then
    min_freq=$(awk -F: '/cpu MHz/ {print $2}' /proc/cpuinfo | awk '{print $1}' | sort -n | head -1)
    max_freq=$(awk -F: '/cpu MHz/ {print $2}' /proc/cpuinfo | awk '{print $1}' | sort -n | tail -1)
    avg_freq=$(awk -F: '/cpu MHz/ {sum+=$2; n++} END {if(n>0) printf "%.2f", sum/n; else print "N/A"}' /proc/cpuinfo)
else
    min_freq="N/A"
    max_freq="N/A"
    avg_freq="N/A"
fi

# Print key-value pairs
cat <<EOF
Vendor: $vendor
Brand: $brand
Microarchitecture: $uarch
Family: $family
Model: $model
Stepping: $stepping
Physical Cores: $physical_cores
Threads Per Core: $tpc
CPU Min: $min_freq MHz
CPU Max: $max_freq MHz
CPU Avg: $avg_freq MHz
EOF
