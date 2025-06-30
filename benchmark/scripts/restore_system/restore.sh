#!/bin/bash

# Usage:
#   ./restore.sh

echo "=> Restoring system after benchmarking..."

./scripts/restore_system/restore_frequency.sh
./scripts/restore_system/activate_core_boost.sh
./scripts/restore_system/activate_hyper_threading.sh
./scripts/restore_system/restore_graphical_mode.sh

echo "=> System restored."