#!/usr/bin/env python3

import os
import argparse
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import scripts.utils.utils as utils
import sbatch_builder as builder

def parse_args():
    parser = argparse.ArgumentParser(description="Submit profiling experiments.")
    parser.add_argument("--config", required=True, help="Path to the YAML configuration file.")
    return parser.parse_args()

def main():
    args = parse_args()
    config = utils.load_config(args.config)
    output_dir = utils.prepare_directories(config, 'profile')
    sbatch_template = builder.read_sbatch_template()

    profile_config = config["profile"]
    benchmark_config = config["benchmark"]

    print("> Submitting profiling experiments...")
    try:
        input_files = utils.generate_sequence_files(profile_config["length_cases"], benchmark_config["tmp_dir"])
        all_sbatch_scripts = []
        sbatch_scripts = []
            
        sbatch_scripts = builder.create_sbatch_scripts(
            sbatch_template,
            profile_config["repeats"],
            profile_config["repeats_per_job"],
            len(input_files),
            1,
            1
        )

        job_name = f"profile"
        output_file = os.path.join(output_dir, f"{job_name}")
        error_file = os.path.join(output_dir, f"{job_name}")

        case = {
            "nodes": 1,
            "ntasks": 1,
            "cpu_list": [0],
            "ntasks_per_node": 1,
            "bind_to": "core",
            "memory": profile_config["memory"],
        }

        extra_fields = {
            "MPI_PROFILE_NAME": os.path.join(output_dir, f"{job_name}_mpi_profile_part_<INDEX>.out"),
        }

        sbatch_scripts = builder.format_sbatch_body(sbatch_scripts, input_files, profile_config["binary"], case)
        sbatch_scripts = builder.format_sbatch_header(sbatch_scripts, job_name, output_file, error_file, case, extra_fields)

        utils.submit_and_wait_for_jobs(sbatch_scripts, job_name, profile_config["sleep_time"], benchmark_config["tmp_dir"])
        remove_input_files_script = utils.create_remove_input_files_script(input_files, benchmark_config["tmp_dir"])
        utils.submit_and_wait_for_jobs([remove_input_files_script], "remove_input_files", profile_config["sleep_time"], benchmark_config["tmp_dir"])
       
    finally:
        print("> All experiments jobs submitted.")

if __name__ == "__main__":
    main()
