#!/bin/bash

# Verifica dependências básicas
if [ ! -f /proc/cpuinfo ]; then
    echo "Error: /proc/cpuinfo not found"
    exit 1
fi

if ! command -v lscpu &>/dev/null; then
    echo "Error: lscpu is not available"
    exit 1
fi

# Basic CPU info
vendor=$(grep -m1 "vendor_id" /proc/cpuinfo | awk -F: '{print $2}' | xargs)
brand=$(grep -m1 "model name" /proc/cpuinfo | awk -F: '{print $2}' | xargs)
uarch=$(lscpu | awk -F: '/Architecture/ {print $2}' | xargs)
family=$(grep -m1 "cpu family" /proc/cpuinfo | awk -F: '{print $2}' | xargs)
model=$(grep -m1 "^model[^_]" /proc/cpuinfo | awk -F: '{print $2}' | xargs)
stepping=$(grep -m1 "stepping" /proc/cpuinfo | awk -F: '{print $2}' | xargs)

# Core/thread info
threads=$(grep -c ^processor /proc/cpuinfo)
cores_per_socket=$(lscpu | awk -F: '/Core\(s\) per socket/ {print $2}' | xargs)
sockets=$(lscpu | awk -F: '/Socket\(s\)/ {print $2}' | xargs)

if [[ "$cores_per_socket" =~ ^[0-9]+$ && "$sockets" =~ ^[0-9]+$ ]]; then
    physical_cores=$((cores_per_socket * sockets))
else
    physical_cores="N/A"
fi

if [[ "$physical_cores" != "N/A" && "$threads" =~ ^[0-9]+$ ]]; then
    tpc=$((threads / physical_cores))
else
    tpc="N/A"
fi

# Frequência da CPU
min_freq=$(lscpu | awk -F: '/CPU min MHz/ {print $2}' | xargs)
max_freq=$(lscpu | awk -F: '/CPU max MHz/ {print $2}' | xargs)

if [[ -z "$min_freq" || -z "$max_freq" ]]; then
    # fallback: usar /proc/cpuinfo
    min_freq=$(awk -F: '/cpu MHz/ {print $2}' /proc/cpuinfo | awk '{print $1}' | sort -n | head -1)
    max_freq=$(awk -F: '/cpu MHz/ {print $2}' /proc/cpuinfo | awk '{print $1}' | sort -n | tail -1)
fi

avg_freq=$(awk -F: '/cpu MHz/ {sum+=$2; n++} END {if(n>0) printf "%.2f", sum/n; else print "N/A"}' /proc/cpuinfo)

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
