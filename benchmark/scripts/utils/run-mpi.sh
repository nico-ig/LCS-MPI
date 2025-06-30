#!/bin/bash

SRC_DIR="$1"

if [ -z "$SRC_DIR" ]; then
    echo "Usage: $0 <source_directory>"
    echo "Example: $0 /path/to/source"
    exit 1
fi

BIN_PATH=$(make -s -C "$SRC_DIR" print-binpath)
REMOTE_DIR=$(make -s -C "$SRC_DIR" print-remotedir)
REMOTE_HOST=$(make -s -C "$SRC_DIR" print-remotehost)
HOST_FILE=$(make -s -C "$SRC_DIR" print-hostfile)
NUMPROCESS=$(make -s -C "$SRC_DIR" print-numprocess)

MPI_CMD="mpirun --verbose --hostfile $REMOTE_DIR/$HOST_FILE -np $NUMPROCESS"
RUN_BIN="$BIN_PATH -f $REMOTE_DIR/fileA.in -f $REMOTE_DIR/fileB.in"
REMOTE_CMD="$MPI_CMD $RUN_BIN"

echo "Running mpi on $REMOTE_HOST"
ssh "$REMOTE_HOST" "$REMOTE_CMD"