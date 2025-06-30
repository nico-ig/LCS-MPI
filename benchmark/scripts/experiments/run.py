#!/usr/bin/env python3

import os
import csv
import statistics
import argparse
import yaml
import sys
import re
import time
from collections import defaultdict
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.utils import generate_sequence_file, run_file

def compile_binary(config):
    print("Compiling binary...")
    run_file(
        "./scripts/utils/compile.sh",
        [
            config["makefile_path"],
            "release"
        ]
    )
    print("Compilation done.")

def run_experiment(input_a, input_b, threads, config):
    start = time.perf_counter()
    result = run_file(
        config["binary"],
        [
            "-f", input_a,
            "-f", input_b,
            "-t", str(threads),
            "-b", str(config["block"]),
        ],
        capture_output=True
    )
    total_time = time.perf_counter() - start
    score = re.search(r"Score:\s*(\d+)", result).group(1)
    return round(total_time, 3), int(score)

def run_experiments(config, raw_writer):
    for pair in sorted(config["experiment_pairs"], key=lambda p: p["length"]):
        length = pair["length"]
        seed_a, seed_b = pair["seeds"]

        try:
            score_list = []
            thread_list = defaultdict(list)

            input_a = generate_sequence_file(length, seed_a)
            input_b = generate_sequence_file(length, seed_b)

            print(f"Running experiments for input length {length}...")
            for i in range(1, config["repeats"] + 1):
                print(f"  Repeat {i+1}/{config['repeats']}...")
                for threads in config["threads"]:
                    print(f"    Threads: {threads}: Started...", end="", flush=True)
                    total_time, score = run_experiment(input_a, input_b, threads, config)
                    raw_writer.writerow([length, threads, i, total_time, score])
                    thread_list[threads].append(total_time)
                    score_list.append(score)
                    print(f", Finished.")

        finally:
            os.remove(input_a)
            os.remove(input_b)
        
        if not all(score == score_list[0] for score in score_list):
            print(f"Scores are different for length {length}: {score_list}")
            exit(1)
        
        for threads in sorted(thread_list):
            yield length, threads, thread_list[threads]

def main():
    parser = argparse.ArgumentParser(description="Run profiling experiments to extract the pure sequential time.")
    parser.add_argument("--config", required=True, help="Path to the YAML configuration file.")
    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    output_dir = "results/experiments"
    os.makedirs(output_dir, exist_ok=True)

    print("=> Starting experiments...")
    compile_binary(config)

    with open(os.path.join(output_dir, "raw_runs.csv"), "w", newline="") as raw_file, \
        open(os.path.join(output_dir, "summary.csv"), "w", newline="") as summary_file, \
        open(os.path.join(output_dir, "strong_scaling.csv"), "w", newline="") as strong_scaling_file, \
        open(os.path.join(output_dir, "weak_scaling.csv"), "w", newline="") as weak_scaling_file, \
        open(os.path.join(output_dir, "speed_up.csv"), "w", newline="") as speed_up_file, \
        open(os.path.join(output_dir, "efficiency.csv"), "w", newline="") as efficiency_file:
        
        raw_writer = csv.writer(raw_file)
        summary_writer = csv.writer(summary_file)
        strong_scaling_writer = csv.writer(strong_scaling_file)
        weak_scaling_writer = csv.writer(weak_scaling_file)
        speed_up_writer = csv.writer(speed_up_file)
        efficiency_writer = csv.writer(efficiency_file)

        raw_writer.writerow(["input_length", "threads", "rep", "total_time", "score"])
        summary_writer.writerow(["input_length", "threads", "T_mean", "T_stdev"])
        strong_scaling_writer.writerow(["input_length", "threads", "T_mean", "T_stdev"])
        weak_scaling_writer.writerow(["input_length", "threads", "T_mean", "T_stdev"])
        speed_up_writer.writerow(["input_length", "threads", "speed_up"])
        efficiency_writer.writerow(["input_length", "threads", "efficiency"])

        seen_lengths = set()
        prev_threads = 0

        for length, threads, T_list in run_experiments(config, raw_writer):
            T_mean = round(statistics.mean(T_list), 3)
            T_std = round(statistics.stdev(T_list), 3)

            if threads == 1:
                T_seq = T_mean

            if length == config["strong_scaling_length"]:
                strong_scaling_writer.writerow([length, threads, T_mean, T_std])

            if length not in seen_lengths and threads > prev_threads:
                weak_scaling_writer.writerow([length, threads, T_mean, T_std])
                seen_lengths.add(length)
                prev_threads = threads

            summary_writer.writerow([length, threads, T_mean, T_std])

            speed_up = round(T_seq / T_mean, 3)
            efficiency = round(speed_up / threads, 3)

            speed_up_writer.writerow([length, threads, speed_up])
            efficiency_writer.writerow([length, threads, efficiency])
            print(f"Completed experiments for [length {length}, threads {threads}].")
        
        print("=> All experiments completed. Summaries written.")

if __name__ == "__main__":
    main()
