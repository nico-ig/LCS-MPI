#!/bin/bash
# Check if Core Performance Boost is ACTIVE
if [ -f /sys/devices/system/cpu/cpufreq/boost ]; then  # AMD/Intel alternative
    boost=$(cat /sys/devices/system/cpu/cpufreq/boost)
    if [ "$boost" -eq 0 ]; then
        core_boost="False"
    else
        core_boost="True"
    fi
fi

echo "Core Boost: $core_boost"

# Get and format CPU lists
online_cpus=$(lscpu | grep -i "on-line" | awk -F': ' '{print $2}' | xargs)
offline_cpus=$(lscpu | grep -i "off-line" | awk -F': ' '{print $2}' | xargs)

# Check if Hyper-Threading is ACTIVE
if [ -f /sys/devices/system/cpu/smt/active ]; then
    smt_active=$(cat /sys/devices/system/cpu/smt/active)
    if [ "$smt_active" -eq 1 ]; then
        hyperthreading="True"
    else
        hyperthreading="False"
    fi
fi

cat <<EOF
Hyper Threading: $hyperthreading
Online CPUs: ${online_cpus:-None}
Offline CPUs: ${offline_cpus:-None}
EOF
