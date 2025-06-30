#!/bin/bash

SERVICES="$1"
PROCESSES="$2"
THREAD_BINDING="$3"
SCHEDULER="$4"
FREQ="$5"
THREAD_PLACEMENT="$6"
SKIP_RESCUE_MODE="$7"

if [ $# -lt 5 ]; then
    cat <<EOF
Usage: $0 "service1 service2" "proc1 proc2" "thread_binding" "scheduler" "freq" [skip]
  "service1 service2" : Space-separated list of systemd services to stop
  "proc1 proc2"       : Space-separated list of process names to kill
  "thread_binding"    : Thread binding type (e.g., close, spread, master)
  "scheduler"         : Thread scheduler to use (e.g., dynamic, static)
  "freq"              : CPU frequency in kHz (e.g., 1400000)
  "places"            : Thread placement (e.g., cores, threads, sockets)
  [skip]              : Optional, use 'skip' to skip rescue mode check

Example:
    $0 "service1 service2" "proc1 proc2" "close" 1400000 "cores"
    $0 "service1 service2" "proc1 proc2" "close" 1400000 "cores" skip
EOF
    exit 1
fi

echo "=> Setting up system for benchmarking..."

if [ "$SKIP_RESCUE_MODE" == "skip" ]; then
    echo "Skipping ensure rescue mode check."
else
    ./scripts/setup_system/ensure_rescue_mode.sh

    if [ $? != 0 ]; then
        exit 1
    fi
fi

./scripts/setup_system/set_frequency.sh $FREQ
./scripts/setup_system/deactivate_core_boost.sh
./scripts/setup_system/deactivate_hyper_threading.sh
./scripts/setup_system/stop_systemd_services.sh $SERVICES
./scripts/setup_system/kill_processes.sh $PROCESSES
./scripts/setup_system/set_thread_binding.sh "$THREAD_BINDING"
./scripts/setup_system/set_scheduler.sh $SCHEDULER
./scripts/setup_system/set_thread_places.sh $THREAD_PLACEMENT

echo "=> System setup complete."
