#!/bin/bash

if [ $# -ne 1 ]; then
cat <<EOF
Usage: $0 <places_type>
Example places types: cores, threads, sockets
Example: $0 cores
EOF
    exit 1
fi

export OMP_PLACES="$1"
echo "Set OMP_PLACES to '$OMP_PLACES'."
