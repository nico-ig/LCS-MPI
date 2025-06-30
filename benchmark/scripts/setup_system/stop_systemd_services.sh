#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 service1 [service2 ...]"
    exit 1
fi

echo "Stopping services..."

for service in "$@"; do
    sudo systemctl stop "$service" 2&>/dev/null || true;
done

echo "Services stopped."

echo -n "Listing all active systemd services: "
systemctl list-units --type=service --state=running --no-pager --no-legend | awk '{print $1}' | paste -sd,