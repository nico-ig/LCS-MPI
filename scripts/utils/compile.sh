#!/bin/bash

SRC_DIR="$1"
RULE="${2:-release}"

if [ -z "$SRC_DIR" ]; then
    echo "Usage: $0 <source_directory> <makefile_rule> <TARGET=<target_name>>"
    echo "Example: $0 ../ profile lcs-profile"
    exit 1
fi

make -C $SRC_DIR clean > /dev/null 2>&1
make -C "$SRC_DIR" "$RULE" TARGET="$TARGET" > /dev/null 2>&1
