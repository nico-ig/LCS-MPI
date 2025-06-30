#!/usr/bin/env python3

import argparse
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import scripts.utils.utils as utils

def parse_args():
    parser = argparse.ArgumentParser(description="Connect to remote host and run experiments.")
    parser.add_argument("--config", required=True, help="Path to the YAML configuration file.")
    return parser.parse_args()

def run_remote_jobs(config, args):
    try:
        print("> Preparing, syncing, and submitting job to remote cluster...")
        
        utils.run_file(
            "./scripts/utils/make_executable.sh",
            [
                "./scripts"
            ]
        )

        print("> Syncing project files to remote host...")
        utils.run_file(
            "./scripts/cluster/sync-project.sh",
            [
                ".",
                config["cluster"]["remote_dir"],
                config["cluster"]["remote_host"],
                config["benchmark"]["results_dir"],
                config["benchmark"]["tmp_dir"],
                config["benchmark"]["analysis_dir"]
            ]
        )

        print("> Connecting to remote host and submitting jobs...")
        utils.run_file(
            "./scripts/cluster/connect-and-submit.sh",
            [
                config["cluster"]["remote_dir"],
                config["cluster"]["remote_host"],
                config["benchmark"]["results_dir"],
                config["benchmark"]["submit_log_file"],
                args.config
            ]
        )

        print("> Waiting for remote jobs to complete...")
        utils.run_file(
            "./scripts/cluster/wait-for-jobs.sh",
            [
                config["cluster"]["remote_dir"],
                config["cluster"]["remote_host"],
                config["benchmark"]["results_dir"],
                config["benchmark"]["done_message"],
                config["benchmark"]["submit_log_file"],
                config["benchmark"]["sleep_time"]
            ]
        )
    
        print("> Syncing results from remote host...")
        utils.run_file(
            "./scripts/cluster/sync-results.sh",
            [
                ".",
                config["cluster"]["remote_dir"],
                config["cluster"]["remote_host"],
                config["benchmark"]["results_dir"]
            ]
        )

    finally:
        print("> Remote job submission completed.")

def run_local_analysis(config, args):
    try:
        print("> Analyzing profiling data locally...")
        utils.run_file(
            "./scripts/experiments/analyse_profile.py",
            [
                "--config", args.config
            ]
        )
        print("> Profiling analysis completed.")
    
        print("> Analyzing experiments data locally...")
        utils.run_file(
            "./scripts/experiments/analyse_experiments.py",
            [
                "--config", args.config
            ]
        )
        print("> Experiments analysis completed.")

    except KeyboardInterrupt:
        print("\n> Analysis interrupted by user.")
        sys.exit(1)

    finally:
        analysis_dir = config["benchmark"]["analysis_dir"]
        print(f"> Analysis results are available in {analysis_dir}.")

def main():
    args = parse_args()
    config = utils.load_config(args.config)
    run_remote_jobs(config, args)
    run_local_analysis(config, args)

if __name__ == "__main__":
    main()
