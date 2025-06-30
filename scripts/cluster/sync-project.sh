#!/bin/bash

SRC_DIR=$1
REMOTE_DIR=$2
REMOTE_HOST=$3
RESULTS_DIR=$4
TMP_DIR=$5
ANALYSIS_DIR=$6

if [ -z "$1" -o -z "$2" -o -z "$3" -o -z "$4" -o -z "$5" -o -z "$6" ]; then
    echo "Usage: $0 <source_directory> <remote_directory> <remote_host> <results_dir> <tmp_dir> <analysis_dir>"
    echo "Example: $0 ./ ./remote_dir user@host results tmp analysis"
    exit 1
fi

rsync -a --delete --exclude='$RESULTS_DIR' --exclude='$TMP_DIR' --exclude='$ANALYSIS_DIR' $SRC_DIR $REMOTE_HOST:$REMOTE_DIR