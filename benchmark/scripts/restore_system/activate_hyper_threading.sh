#!/bin/bash

echo "Activating Hyper-Threading..."
echo on | sudo tee /sys/devices/system/cpu/smt/control > /dev/null
echo "Hyper-Threading activated."
./scripts/utils/check_hyper_threading.sh