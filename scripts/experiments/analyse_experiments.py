#!/usr/bin/env python3

import os
import sys
import csv
import argparse
from functools import reduce
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import scripts.utils.utils as utils

def parse_args():
    parser = argparse.ArgumentParser(description="Analyze experiments.")
    parser.add_argument("--config", required=True, help="Path to the YAML configuration file.")
    return parser.parse_args()

def prepare_dirs(benchmark_config):
    input_dir = benchmark_config["results_dir"] + "/experiments"
    output_dir = benchmark_config["analysis_dir"]
    graphs_dir = output_dir + "/graphs"
    tables_dir = output_dir + "/tables"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(graphs_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)
    return input_dir, output_dir, graphs_dir, tables_dir

def verify_correctness(input_dir, num_of_lengths):
    score_list = {}
    length_cnt = 0
    experiment_files = [f for f in os.listdir(input_dir) if f.endswith(".out") and "mpi_experiment" not in f]
    for filename in experiment_files:
        with open(os.path.join(input_dir, filename), "r") as file:
            result = file.readlines()
        for line in result:
            line = line.strip()
            if "Score: " not in line:
                continue
            score = int(line.split("Score: ")[1].strip())
            if length_cnt not in score_list:
                score_list[length_cnt] = score
            elif score_list[length_cnt] != score:
                raise ValueError("Inconsistent score found in file: " + filename)
            length_cnt = (length_cnt + 1) % num_of_lengths

def init_files(output_dir):
    with open(os.path.join(output_dir, "experiments_summary.csv"), "w", newline="") as summary_file:
        summary_writer = csv.writer(summary_file)
        summary_writer.writerow(["Nodes", "Processes", "Length", "Mean Time", "Std Dev"])

    with open(os.path.join(output_dir, "speed_up.csv"), "w", newline="") as speed_up_file:
        speed_up_writer = csv.writer(speed_up_file)
        speed_up_writer.writerow(["Nodes", "Processes", "Length", "Speed Up"])

    with open(os.path.join(output_dir, "efficiency.csv"), "w", newline="") as efficiency_file:
        efficiency_writer = csv.writer(efficiency_file)
        efficiency_writer.writerow(["Nodes", "Processes", "Length", "Efficiency"])

def split_runs(lines):
    groups = []
    current = []
    length = 0
    for line in lines:
        if "#RUN# start_time,end_time,elapsed_time" in line and len(current) > 0:
            groups.append([length, current])
        elif  "#RUN# length=" in line and len(current) == 0:
            length = int(line.split("=")[1])
        elif  "#RUN# length=" in line and len(current) > 0:
            length = int(line.split("=")[1])
            current = []
        else:
            current.append(line)
    groups.append([length, current])
    return groups

def collect_job_data(filename):
    with open(filename, "r") as file:
        result = file.readlines() 
    for length, run in split_runs(result):
        experiment_lines = [line.strip() for line in run]
        experiment_lines = [line.split('#RUN#')[1].strip() for line in experiment_lines]
        total_time = float(experiment_lines[-1].split(',')[2])
        yield length, total_time

def collect_experiments_data(config, input_dir):
    experiment_files = [f for f in os.listdir(input_dir) if "mpi_experiment" in f]
    experiment_files = sorted(experiment_files, key=lambda f: (
        int(f.split("nodes_")[1].split("_")[0]),
        int(f.split("ntasks_")[1].split("_")[0])
    ))
    print(experiment_files)
    for filename in experiment_files:
        T_list = {}
        filename = os.path.join(input_dir, filename)
        nodes = int(filename.split("nodes_")[1].split("_")[0])
        processes = int(filename.split("ntasks_")[1].split("_")[0])
        for length, total_time in collect_job_data(filename):
            if length not in T_list:
                T_list[length] = []
            T_list[length].append(total_time)
        yield nodes, processes, T_list

def compute_length_mean_and_std(T_list):
    new_list = {}
    for (length, T_times) in T_list.items():
        T_mean, T_std = utils.compute_mean_and_std(T_times)
        new_list[length] = (T_mean, T_std)
    return new_list

def get_mean_and_seq_times(nodes, processes, T_list, T_seq):
    if (nodes == 1 and processes == 1):
        T_seq = {length: T_mean for (length, (T_mean, _)) in T_list.items()}
    T_mean = {length: T_mean for (length, (T_mean, _)) in T_list.items()}
    return T_mean, T_seq

def compute_values(nodes, processes, T_list, T_seq):
    T_list = compute_length_mean_and_std(T_list)
    T_mean, T_seq = get_mean_and_seq_times(nodes, processes, T_list, T_seq)
    lengths = sorted(T_list.keys())
    speed_up = (lambda length: round(T_seq[length] / T_mean[length], 3))
    efficiency = (lambda length: round(speed_up(length) / processes, 3))
    return T_list, lengths, speed_up, efficiency, T_seq

def write_summary(nodes, processes, T_list, output_dir):
    output_filename = os.path.join(output_dir, "experiments_summary.csv")
    with open(output_filename, "a", newline="") as summary_file:
        summary_writer = csv.writer(summary_file)
        for length, (T_mean, T_std) in T_list.items():
            summary_writer.writerow([nodes, processes, length, T_mean, T_std])
    return os.path.basename(output_filename)

def write_speed_up(nodes, processes, lengths, speed_up, output_dir):
    output_filename = os.path.join(output_dir, "speed_up.csv")
    with open(output_filename, "a", newline="") as speed_up_file:
        speed_up_writer = csv.writer(speed_up_file)
        for length in lengths:
            speed_up_writer.writerow([nodes, processes, length, speed_up(length)])
    return os.path.basename(output_filename)

def write_efficiency(nodes, processes, lengths, efficiency, output_dir):
    output_filename = os.path.join(output_dir, "efficiency.csv")
    with open(output_filename, "a", newline="") as efficiency_file:
        efficiency_writer = csv.writer(efficiency_file)
        for length in lengths:
            efficiency_writer.writerow([nodes, processes, length, efficiency(length)])
    return os.path.basename(output_filename)

def write_files(nodes, processes, T_list, lengths, speed_up, efficiency, output_dir):
    summary_filename = write_summary(nodes, processes, T_list, output_dir)
    speed_up_filename = write_speed_up(nodes, processes, lengths, speed_up, output_dir)
    efficiency_filename = write_efficiency(nodes, processes, lengths, efficiency, output_dir)
    return summary_filename, speed_up_filename, efficiency_filename

def plot_experiment_summary(input_file, output_file):
    utils.run_file(
        "scripts/plot/summary.py",
        ["--input", input_file, "--output", output_file],
        capture_output=False
    )
    
def plot_speed_up(input_file, output_file):
    utils.run_file(
        "scripts/plot/speed_up.py",
        ["--input", input_file, "--output", output_file],
        capture_output=False
    )

def plot_efficiency(input_file, output_file):
    utils.run_file(
        "scripts/plot/efficiency.py",
        ["--input", input_file, "--output", output_file],
        capture_output=False
    )

def plot_weak_scaling(input_file, output_file):
    utils.run_file(
        "scripts/plot/weak_scaling.py",
        ["--input", input_file, "--output", output_file],
        capture_output=False
    )

def plot_strong_scaling(input_file, output_file):
    utils.run_file(
        "scripts/plot/strong_scaling.py",
        ["--input", input_file, "--output", output_file],
        capture_output=False
    )

def plot_files(summary_filename, speed_up_filename, efficiency_filename, output_dir, graphs_dir):
    plot_experiment_summary(
        os.path.join(output_dir, summary_filename),
        os.path.join(graphs_dir, summary_filename.replace(".csv", ".pgf"))
    )
    plot_speed_up(
        os.path.join(output_dir, speed_up_filename),
        os.path.join(graphs_dir, speed_up_filename.replace(".csv", ".pgf")),
    )
    plot_efficiency(
        os.path.join(output_dir, efficiency_filename),
        os.path.join(graphs_dir, efficiency_filename.replace(".csv", ".pgf"))
    )
    plot_weak_scaling(
        os.path.join(output_dir, summary_filename),
        os.path.join(graphs_dir, "weak_scaling.pdf")
    )
    plot_strong_scaling(
        os.path.join(output_dir, summary_filename),
        os.path.join(graphs_dir, "strong_scaling.pdf")
    )

def write_summary_table(input_file, output_file):
    utils.run_file(
        "scripts/tables/summary.py",
        ["--input", input_file, "--output", output_file],
        capture_output=False
    )

def write_speed_up_table(input_file, output_file):
    utils.run_file(
        "scripts/tables/speed_up.py",
        ["--input", input_file, "--output", output_file],
        capture_output=False
    )

def write_efficiency_table(input_file, output_file):
    utils.run_file(
        "scripts/tables/efficiency.py",
        ["--input", input_file, "--output", output_file],
        capture_output=False
    )

def write_tables(summary_filename, speed_up_filename, efficiency_filename, output_dir, tables_dir):
    write_summary_table(
        os.path.join(output_dir, summary_filename),
        os.path.join(tables_dir, summary_filename.replace(".csv", ".tex"))
    )
    write_speed_up_table(
        os.path.join(output_dir, speed_up_filename),
        os.path.join(tables_dir, speed_up_filename.replace(".csv", ".tex"))
    )
    write_efficiency_table(
        os.path.join(output_dir, efficiency_filename),
        os.path.join(tables_dir, efficiency_filename.replace(".csv", ".tex"))
    )

def main():
    args = parse_args()
    config = utils.load_config(args.config)
    benchmark_config = config["benchmark"]
    experiments_config = config["experiments"]

    input_dir, output_dir, graphs_dir, tables_dir = prepare_dirs(benchmark_config)
    verify_correctness(input_dir, len(experiments_config["length_cases"]))
    init_files(output_dir)

    T_seq = 0
    for nodes, processes, T_list in collect_experiments_data(config, input_dir):
        T_list, lengths, speed_up, efficiency, T_seq = compute_values(nodes, processes, T_list, T_seq)
        summary_filename, speed_up_filename, efficiency_filename = write_files(
            nodes, processes, T_list, lengths, speed_up, efficiency, output_dir
        )
        plot_files(
            summary_filename, speed_up_filename, efficiency_filename, output_dir, graphs_dir
        )
        write_tables(
            summary_filename, speed_up_filename, efficiency_filename, output_dir, tables_dir
        )

    print("> All experiments analyzed.")

if __name__ == "__main__":
    main()
