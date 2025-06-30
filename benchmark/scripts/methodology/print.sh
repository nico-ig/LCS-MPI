#!/bin/bash

VARS_MK="$1"
if [ -z "$VARS_MK" ]; then
  echo "Usage: $0 <vars.mk>"
  exit 1
fi

print_section_title() {
  local title="$1"
  local line_len=$2
  local separator="$3"
  local title_len=${#title}
  local side_len=$(( (line_len - title_len - 2) / 2 ))

  local left_pad=$(printf '%*s' "$side_len" '' | tr ' ' $separator)
  local right_pad=$(printf '%*s' "$side_len" '' | tr ' ' $separator)

  # Balance if length is odd
  if (( (line_len - title_len - 2) % 2 != 0 )); then
    right_pad="${right_pad}$separator"
  fi

  echo "${left_pad} ${title} ${right_pad}"
}

TITLE="Experiment Methodology"
HEADER=$(print_section_title "$TITLE" 95 "=")
LINE=$(printf '%*s' 95 '' | tr ' ' '=')

cat <<EOF

$HEADER

1. System Preparation
   - The system is checked to ensure it is running in rescue mode. If not, rescue mode
     is set as the default, and the user is instructed to reboot to apply the change.
   - Unnecessary systemd services and user processes are stopped prior to benchmarking.
   - CPU frequency is set according to experiment configurations to avoid the effects of
     dynamic frequency scaling.
   - Core Performance Boost and Hyper-Threading are disabled.
   - Thread binding and scheduling strategies are configured according to the experiment
     settings.
  - The binary is cleaned and recompiled before experiments begin to ensure a fresh
     build.

2. Hardware and Software Environment
   - Hardware details (CPU model, core count, cache sizes, memory) and software versions
     (OS, compiler, libraries) are recorded.

3. Input Generation
   - Input sequences are generated for each experiment run using a deterministic script,
     with sizes and seeds specified in the configuration to ensure reproducibility.

4. Experiment Execution
   - Experiments are conducted using various thread counts and block sizes, as defined in
     the configuration.
   - Each configuration is executed multiple times to account for variability.
   - The number of runs per configuration is specified in the experiment setup.
   - Runs are interleaved across thread counts to reduce systematic bias.

5. Metrics Collected
   - Execution time and relevant performance metrics are recorded for each run.
   - The results/profile directory contains data on pure sequential and parallel fractions, 
     including:
      - Average execution time and number of calls for parallel functions (as defined in 
        the configuration),
      - Calculated pure sequential and parallel fractions,
      - Speed-up estimates based on Amdahl's law.

   - The results/experiments directory contains detailed run data, including:
     - Input size,
     - Thread count,
     - Number of repetitions,
     - Execution time,
     - Speed-up,
     - Parallel efficiency,
     - Strong and weak scaling metrics.


6. Restoration
   - After experiments, the following system settings are restored:
     - CPU frequency governor (reset to the default value),
     - Core Performance Boost and Hyper-Threading (re-enabled),
     - System default mode (restored to graphical mode).

7. Additional Information
   - The experiment configuration are specified in the config.yml.

EOF

declare -A info_scripts=(
  ["System Information"]="system_infos.sh $VARS_MK"
  ["CPU Information"]="cpu_info.sh"
  ["CPU Features"]="cpu_features.sh"
  ["Cache Information"]="cache_info.sh"
  ["TLB Information"]="tlb_info.sh"
  ["DRAM Information"]="dram_info.sh"
  ["Active CPU Frequency"]="active_cpu_frequency.sh"
)


for script in "${!info_scripts[@]}"; do
  print_section_title "$script" 95 "-"
  echo
  eval "./scripts/methodology/${info_scripts[$script]}"
  echo
done

echo "$LINE"
