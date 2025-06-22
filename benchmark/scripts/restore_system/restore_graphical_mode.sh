#!/bin/bash

echo "Restoring default system mode to graphical.target..."
sudo systemctl set-default graphical.target
echo "You can reboot your system with:"
echo "    sudo reboot"
