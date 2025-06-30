#!/bin/bash
echo "Activating Core Performance Boost..."
echo 1 | sudo tee /sys/devices/system/cpu/cpufreq/boost > /dev/null
echo "Core Performance Boost Activated."
./scripts/utils/check_core_boost.sh