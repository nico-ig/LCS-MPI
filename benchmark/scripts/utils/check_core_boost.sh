#!/bin/bash
# Check if Core Performance Boost is ACTIVE
if [ -f /sys/devices/system/cpu/cpufreq/boost ]; then
    boost=$(cat /sys/devices/system/cpu/cpufreq/boost)
    if [ "$boost" -eq 1 ]; then
        core_boost="Active"
    else
        core_boost="Inactive"
    fi
fi

echo "Core Boost: $core_boost"