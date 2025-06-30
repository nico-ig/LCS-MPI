#!/bin/bash

REMOTE_DIR=$1
REMOTE_HOST=$2
RESULTS_DIR=$3
DONE_MESSAGE=$4
SUBMIT_LOG_FILE=$5
SLEEP_TIME=$6

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ] || [ -z "$5" ] || [ -z "$6" ]; then
    echo "Usage: $0 <remote_directory> <remote_host> <results_dir> <done_message> <submit_log_file> <sleep_time>"
    echo "Example: $0 ./remote_dir user@host results 'All jobs done.' ./submit.log 10"
    exit 1
fi

while true; do
    if ssh "$REMOTE_HOST" "grep -q '$DONE_MESSAGE' '$REMOTE_DIR/$RESULTS_DIR/$SUBMIT_LOG_FILE'" 2>/dev/null ; then
        ssh "$REMOTE_HOST" "cat '$REMOTE_DIR/$RESULTS_DIR/$SUBMIT_LOG_FILE'"
        echo "> Remote jobs completed successfully."
        break
    else
        echo "> Waiting for remote jobs to complete..."
        sleep $SLEEP_TIME
    fi
done
