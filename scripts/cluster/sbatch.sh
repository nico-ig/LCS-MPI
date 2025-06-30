#!/bin/bash

#SBATCH --distribution=block:block:block
#SBATCH --cpu-freq=3000000:userspace

#SBATCH --job-name={JOB_NAME}
#SBATCH --output={OUTPUT_FILE}
#SBATCH --error={ERROR_FILE}
#SBATCH --nodes={NODES}
#SBATCH --ntasks={NTASKS}
#SBATCH --ntasks-per-node={NTASKS_PER_NODE}
#SBATCH --mem={MEM}

HOST_LIST=$(srun hostname | sort -u | sed 's/$/:{NTASKS_PER_NODE}/' | paste -sd ",")
mpirun --report-bindings --host $HOSTS -n {NTASKS} --map-by ppr:{NTASKS_PER_NODE}:node:PE-LIST={CPU_LIST} --bind-to {BIND_TO} --rank-by core {BINARY} -f {FILE_A} -f {FILE_B}
