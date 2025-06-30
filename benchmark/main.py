#!/usr/bin/env python3

import yaml
import subprocess
import os
import argparse
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from scripts.utils.utils import generate_sequence_file, run_file

def main():
    parser = argparse.ArgumentParser(description="Run parallel LCS experiments.")
    parser.add_argument("--config", required=True, help="Path to the YAML configuration file.")
    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    try:
        print("> Starting benchmark...")
        run_file(
            "./scripts/make_executable.sh",
            [
                "./"
            ]
        )

        run_file(
            "./scripts/setup_system/setup.sh",
            [
                " ".join(map(str, config["services"])) if config["services"] else "",
                " ".join(map(str, config["processes"])) if config["processes"] else "",
                config["thread_binding"],
                config["scheduler"],
                str(config["frequency"]),
                config["thread_placement"],
                str(config["ensure_rescue_mode"])
            ]
        )

        run_file(
            "./scripts/methodology/print.sh",
            [
                config["makefile_variables_path"]
            ]
        )

        run_file(
            "./scripts/experiments/analyze_profile.py",
            ["--config", args.config]
        )

        run_file(
            "./scripts/experiments/run.py",
            ["--config", args.config]
        )
        
        run_file("./scripts/restore_system/restore.sh")
    finally:
        print("> Benchmark completed successfully.")

if __name__ == "__main__":
    main()
