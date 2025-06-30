#!/bin/bash

echo "Deactivating Hyper-Threading..."
echo off | sudo tee /sys/devices/system/cpu/smt/control > /dev/null
echo "Hyper-Threading deactivated."
./scripts/utils/check_hyper_threading.sh
