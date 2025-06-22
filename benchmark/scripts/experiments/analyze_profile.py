#!/usr/bin/env python3

import os
import csv
import statistics
import argparse
import yaml
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.utils import generate_sequence_file, run_file

def compile_binary(config):
    print("Compiling binary...")
    run_file(
        "./scripts/utils/compile.sh",
        [
            config["makefile_path"],
            "profile"
        ]
    )
    print("Compilation done.")

def run_profile(binary, func):
    result = run_file(
        "./scripts/experiments/collect_profile.sh",
        [binary, func],
        capture_output=True
    ).splitlines()
    total_time, calls, avg_call_time = map(float, result[1].split(","))
    return total_time, int(calls), avg_call_time

def run_experiments(config, raw_writer):
    for pair in config["profile_pairs"]:
        length = pair["length"]
        seed_a, seed_b = pair["seeds"]

        try:
            input_a = generate_sequence_file(length, seed_a)
            input_b = generate_sequence_file(length, seed_b)

            Ts_list = []
            Tp_list = []

            print(f"Running profile for input length {length}...")
            for i in range(config["profile_repeats"]):
                print(f"  Repeat {i+1}/{config['profile_repeats']}...")
                run_file(
                    config["binary"],
                    [
                        "-f", input_a,
                        "-f", input_b,
                        "-t", "1",
                        "-b", str(config["block"]),
                    ],
                    capture_output=True
                )
                try:
                    total_time, calls, avg_call_time = run_profile(
                        config["binary"], config["profile_function"]
                    )

                    raw_writer.writerow([length, i, total_time, calls, avg_call_time])

                    Tp = (avg_call_time * calls) / total_time if total_time else 0
                    Ts = 1 - Tp

                    Ts_list.append(Ts)
                    Tp_list.append(Tp)
                finally:
                    os.remove("gmon.out")

            yield length, Ts_list, Tp_list

        finally:
            os.remove(input_a)
            os.remove(input_b)

def compute_mean_and_std(time_list):
    mean = statistics.mean(time_list)
    stdev = statistics.stdev(time_list)
    return round(mean, 3), round(stdev, 3)

def write_amdahl(Ts_mean, Tp_mean, config, output_dir):
    with open(os.path.join(output_dir, "amdahl.csv"), "w", newline="") as amdahl_file:
        amdahl_writer = csv.writer(amdahl_file)
        amdahl_writer.writerow(["threads", "speed_up"])
        for threads in config["threads"]:
            speed_up = round(1 / (Ts_mean + (Tp_mean / threads)), 3)
            amdahl_writer.writerow([threads, speed_up])
        infinity_speed_up = round(1 / Ts_mean, 3)
        amdahl_writer.writerow(["∞", infinity_speed_up])

def main():
    parser = argparse.ArgumentParser(description="Run profiling experiments to extract the pure sequential time.")
    parser.add_argument("--config", required=True, help="Path to the YAML configuration file.")
    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    output_dir = "results/profile"
    os.makedirs(output_dir, exist_ok=True)

    print("=> Starting profiling experiments...")
    compile_binary(config)

    with open(os.path.join(output_dir, "raw_runs.csv"), "w", newline="") as raw_file, \
        open(os.path.join(output_dir, "length_summary.csv"), "w", newline="") as length_summary_file, \
        open(os.path.join(output_dir, "global_summary.csv"), "w", newline="") as global_summary_file:
        
        raw_writer = csv.writer(raw_file)
        length_summary_writer = csv.writer(length_summary_file)
        global_summary_writer = csv.writer(global_summary_file)

        raw_writer.writerow(["input_length", "rep", "total_time", "calls", "avg_call_time"])
        length_summary_writer.writerow(["input_length", "Ts_mean", "Ts_stdev", "Tp_mean", "Tp_stdev"])
        global_summary_writer.writerow(["Ts_mean", "Ts_stdev", "Tp_mean", "Tp_stdev"])

        all_Ts = []
        all_Tp = []

        for length, Ts_list, Tp_list in run_experiments(config, raw_writer):
            Ts_mean, Ts_std = compute_mean_and_std(Ts_list)
            Tp_mean, Tp_std = compute_mean_and_std(Tp_list)
            length_summary_writer.writerow([length, Ts_mean, Ts_std, Tp_mean, Tp_std])
            all_Ts.extend(Ts_list)
            all_Tp.extend(Tp_list)
            print(f"Completed profiling experiments for length {length}.")

        Ts_mean_all, Ts_std_all = compute_mean_and_std(all_Ts)
        Tp_mean_all, Tp_std_all = compute_mean_and_std(all_Tp)
        global_summary_writer.writerow([Ts_mean_all, Ts_std_all, Tp_mean_all, Tp_std_all])

        write_amdahl(Ts_mean_all, Tp_mean_all, config, output_dir)
        print("=> All profiling experiments completed. Summaries written.")

if __name__ == "__main__":
    main()
