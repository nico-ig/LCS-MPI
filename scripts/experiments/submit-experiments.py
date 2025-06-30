#!/usr/bin/env python3

import os
import argparse
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import scripts.utils.utils as utils
import sbatch_builder as builder

def parse_args():
    parser = argparse.ArgumentParser(description="Submit experiments.")
    parser.add_argument("--config", required=True, help="Path to the YAML configuration file.")
    return parser.parse_args()

def main():
    args = parse_args()
    config = utils.load_config(args.config)
    output_dir = utils.prepare_directories(config, 'experiments')
    sbatch_template = builder.read_sbatch_template()

    release_config = config["release"]
    benchmark_config = config["benchmark"]
    experiments_config = config["experiments"]

    print("> Submitting experiments...")
    try:
        input_files = utils.generate_sequence_files(experiments_config["length_cases"], benchmark_config["tmp_dir"])
        all_sbatch_scripts = []
        for case in experiments_config["test_cases"]:
            sbatch_scripts = []
            
            repeats_per_job = utils.get_repeats_per_job(case["nodes"], case["ntasks"], case["repeats_per_job"])

            sbatch_scripts = builder.create_sbatch_scripts(
                sbatch_template,
                release_config["repeats"],
                repeats_per_job,
                len(input_files),
                case["nodes"],
                case["ntasks"]
            )

            job_name = f"experiment_nodes_{case['nodes']}_ntasks_{case['ntasks']}"
            output_file = os.path.join(output_dir, f"{job_name}")
            error_file = os.path.join(output_dir, f"{job_name}")

            extra_fields = {
                "MPI_PROFILE_NAME": os.path.join(output_dir, f"{job_name}_mpi_experiment_part_<INDEX>.out"),
            }

            sbatch_scripts = builder.format_sbatch_body(sbatch_scripts, input_files, release_config["binary"], case)
            sbatch_scripts = builder.format_sbatch_header(sbatch_scripts, job_name, output_file, error_file, case, extra_fields)

            for script in sbatch_scripts:
                utils.submit_and_wait_for_jobs([script], job_name, release_config["sleep_time"], benchmark_config["tmp_dir"])
        
        remove_input_files_script = utils.create_remove_input_files_script(input_files, benchmark_config["tmp_dir"])
        utils.submit_and_wait_for_jobs([remove_input_files_script], "remove_input_files", release_config["sleep_time"], benchmark_config["tmp_dir"])
        
    finally:
        print("> All experiments jobs submitted.")

if __name__ == "__main__":
    main()
