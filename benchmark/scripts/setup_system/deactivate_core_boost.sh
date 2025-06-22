#!/bin/bash

echo "Detivating Core Performance Boost..."
echo 0 | sudo tee /sys/devices/system/cpu/cpufreq/boost > /dev/null
echo "Core Performance Boost deactivated."
./scripts/utils/check_core_boost.sh