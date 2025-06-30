#!/bin/bash

SRC_DIR=$1
REMOTE_DIR=$2
REMOTE_HOST=$3
RESULTS_DIR=$4

if [ -z "$1" -o -z "$2" -o -z "$3" -o -z "$4" ]; then
    echo "Usage: $0 <source_directory> <remote_directory> <remote_host> <results_dir>"
    echo "Example: $0 ./ ./remote_dir user@host ./results"
    exit 1
fi

rsync -a $REMOTE_HOST:$REMOTE_DIR/$RESULTS_DIR/ $SRC_DIR/$RESULTS_DIR/
