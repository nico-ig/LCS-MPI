#!/bin/bash

current_target=$(systemctl get-default)

if [ "$current_target" != "rescue.target" ]; then
    echo "Rescue mode: False."
    echo "Setting default system mode to rescue mode..."
    sudo systemctl set-default rescue.target
    echo "You should reboot your system to enter rescue mode:"
    echo "    sudo reboot"
    exit 1
else
    echo "Rescue mode: True"
fi