#!/usr/bin/env python3

import argparse
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import scripts.utils.utils as utils

def parse_args():
    parser = argparse.ArgumentParser(description="Run parallel LCS experiments.")
    parser.add_argument("--config", required=True, help="Path to the YAML configuration file.")
    return parser.parse_args()

def main():
    args = parse_args()
    config = utils.load_config(args.config)

    try:
        utils.compile_profile_binary(config)
        utils.compile_release_binary(config)

        print("> Creating jobs...")

        utils.run_file(
            "./scripts/experiments/submit-profile.py",
            [
                "--config", args.config
            ]
        )

        utils.run_file(
            "./scripts/experiments/submit-experiments.py",
            [
                "--config", args.config
            ]
        )

    finally:
        print("> Jobs created successfully.")
        print(config["benchmark"]["done_message"])

if __name__ == "__main__":
    main()
