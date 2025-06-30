#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Usage: $0 <binary> <function_name>"
    exit 1
fi

BINARY="$1"
FUNC="$2"

echo "total_time,calls,avg_call_time_ms"
PROFILE=$(gprof "$BINARY" gmon.out --no-static --flat-profile -b)
total_time=$(echo "$PROFILE" | tail -n 1 | awk '{print $2}')
calls=$(echo "$PROFILE" | grep "$FUNC" | awk '{print $4}')
avg_call_time=$(echo "$PROFILE" | grep "$FUNC" | awk '{print $6}')

echo "$total_time,$calls,$avg_call_time"
