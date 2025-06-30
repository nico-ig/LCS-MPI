#!/bin/bash
#SBATCH --cpu-freq=3000000:userspace
#SBATCH --distribution=block:block:block
#SBATCH --mem=4G
#SBATCH --output={OUTPUT}
#SBATCH --nodes={NODES}
#SBATCH --ntasks={NTASKS}
#SBATCH --ntasks-per-node={NTASKS_PER_NODE}

TIME=0
MAX_RSS=0
mpirun -n {NTASKS} --map-by ppr:{NTASKS_PER_NODE}:node:PE-LIST={CPU_LIST} --bind-to {BIND_TO} --rank-by core {BINARY} -f {FILE_A} -f {FILE_B} &
PID=$!
while ! ps -p $PID > /dev/null; do sleep 0.1; done
while ps -p $PID > /dev/null; do
    RSS=$(ps -p $PID -o rss= | awk '{print $1}')
    if [[ "$RSS" =~ ^[0-9]+$ ]]; then
        if [ "$RSS" -gt "$MAX_RSS" ]; then
            MAX_RSS=$RSS
        fi
    fi
    TIME=$(echo "$TIME + 0.5" | bc)
    sleep 0.5
done
wait $PID
echo "Elapsed (wall clock) time: $TIME seconds"
echo "Maximum resident set size: $MAX_RSS KB"