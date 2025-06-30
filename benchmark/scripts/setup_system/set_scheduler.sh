#!/bin/bash

if [ $# -ne 1 ]; then
cat <<EOF
Usage: $0 <schedule_type>
Example schedule types: static, dynamic, guided, auto
You can also specify chunk size, e.g.: dynamic,4
Example: $0 dynamic,4
EOF
    exit 1
fi

export OMP_SCHEDULE="$1"
echo "Set OMP_SCHEDULE to '$OMP_SCHEDULE'."