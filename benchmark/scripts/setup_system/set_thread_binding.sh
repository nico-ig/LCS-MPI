#!/bin/bash

if [ $# -ne 1 ]; then
cat <<EOF
Usage: $0 <binding_type>
Example binding types: close, spread, master, true, false
Example: $0 close
EOF
    exit 1
fi

export OMP_PROC_BIND="$1"
echo "Set OMP_PROC_BIND to '$OMP_PROC_BIND'."