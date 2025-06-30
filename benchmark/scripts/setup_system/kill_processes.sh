#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 process_name1 [process_name2 ...]"
    exit 1
fi

echo "Killing processes..."
for name in "$@"; do
    sudo pkill -f "$name" 2&>/dev/null || true;
done

echo "Processes killed."
echo -n "Listing all active processes: "
ps -eo user,pid,comm | awk 'NR==1{next} {printf "(%s, %s), ", $1, $3}'
echo
