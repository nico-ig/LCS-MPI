#!/bin/bash

SRC_DIR="$1"
RULE="${2:-release}"

if [ -z "$SRC_DIR" ]; then
    echo "Usage: $0 <source_directory> <makefile_rule>"
    echo "Example: $0 /path/to/source release"
    exit 1
fi

make -C "$SRC_DIR" clean > /dev/null 2>&1
make -C "$SRC_DIR" "$RULE" > /dev/null 2>&1
