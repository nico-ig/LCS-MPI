#!/bin/bash

REMOTE_DIR="$1"
REMOTE_HOST="$2"
RESULTS_DIR="$3"
SUBMIT_LOG_FILE="$4"
CONFIG="$5"

if [ -z "$1" -o -z "$2" -o -z "$3" -o -z "$4" -o -z "$5" ]; then
    echo "Usage: $0 <remote_directory> <remote_host> <results_dir> <submit_log_file> <config>"
    echo "Example: $0 ./remote_dir user@host results ./submit.log config.yml"
    exit 1
fi

ssh "$REMOTE_HOST" "
    cd $REMOTE_DIR
    rm -rf $RESULTS_DIR 2>/dev/null
    mkdir $RESULTS_DIR
    ./scripts/utils/make_executable.sh ./scripts
    nohup ./scripts/cluster/submit-jobs.py --config $CONFIG > $RESULTS_DIR/$SUBMIT_LOG_FILE 2>&1 &
"