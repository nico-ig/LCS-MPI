#!/bin/bash

CMD="python3 scripts/cluster/entry.py --config scripts/configs.yml"

if pgrep -f "python3 scripts/cluster/entry.py --config scripts/configs.yml" > /dev/null; then
    echo "Still running."
    exit 1
else
    echo "Not running."
    exit 0
fi

