#!/usr/bin/env python3

import os
import sys
import csv
import statistics
import argparse
from functools import reduce
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import scripts.utils.utils as utils

def parse_args():
    parser = argparse.ArgumentParser(description="Analyze profiling experiments to extract the pure sequential time.")
    parser.add_argument("--config", required=True, help="Path to the YAML configuration file.")
    return parser.parse_args()

def prepare_dirs(benchmark_config):
    input_dir = benchmark_config["results_dir"] + "/profile"
    output_dir = benchmark_config["analysis_dir"]
    tables_dir = output_dir + "/tables"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)
    return input_dir, output_dir, tables_dir

def split_runs(lines):
    groups = []
    current = []
    for line in lines:
        if  "#PROFILE# start_time,end_time,elapsed_time" in line and len(current) > 0:
            groups.append(current)
            current = []
        else:
            current.append(line)
    groups.append(current)
    return groups

def collect_job_data(filename):
    with open(filename, "r") as file:
        result = file.readlines()
    for run in split_runs(result):
        profile_lines = [line.strip() for line in run]
        profile_lines = [line.split('#PROFILE#')[1].strip() for line in profile_lines]
        times_list = [float(line.split(',')[2]) for line in profile_lines[1:-1]]
        avg_call_time = statistics.mean(times_list)
        total_time = float(profile_lines[-1].split(',')[2])
        total_calls = len(times_list)
        yield total_time, total_calls, avg_call_time

def compute_ts_and_tp(total_time, total_calls, avg_call_time):
    Tp = (avg_call_time * total_calls) / total_time
    Ts = 1 - Tp
    return round(Ts, 3), round(Tp, 3)

def collect_profiling_data(config, input_dir):
    Ts_list = []
    Tp_list = []
    profile_files = [f for f in os.listdir(input_dir) if "mpi_profile" in f]
    for filename in profile_files:
        filename = os.path.join(input_dir, filename)
        for total_time, total_calls, avg_call_time in collect_job_data(filename):
            Ts, Tp = compute_ts_and_tp(total_time, total_calls, avg_call_time)
            Ts_list.append(Ts)
            Tp_list.append(Tp)
    return Ts_list, Tp_list

def compute_values(config, input_dir): 
    Ts_list, Tp_list = collect_profiling_data(config, input_dir)
    Ts_mean, Ts_std = utils.compute_mean_and_std(Ts_list)
    Tp_mean, Tp_std = utils.compute_mean_and_std(Tp_list)
    return Ts_list, Tp_list, Ts_mean, Ts_std, Tp_mean, Tp_std

def write_runs_summary(Ts_list, Tp_list, output_dir):
    output_file = os.path.join(output_dir, "runs_profile_summary.csv")
    with open(output_file, "w", newline="") as runs_file:
        runs_writer = csv.writer(runs_file)
        runs_writer.writerow(["Ts", "Tp"])
        for (Ts, Tp) in zip(Ts_list, Tp_list):
            runs_writer.writerow([Ts, Tp])
    return os.path.basename(output_file)

def write_summary(Ts_mean, Ts_std, Tp_mean, Tp_std, output_dir):
    output_file = os.path.join(output_dir, "profile_summary.csv")
    with open(output_file, "w", newline="") as summary_file:
        summary_writer = csv.writer(summary_file)
        summary_writer.writerow(["Ts_mean", "Ts_stdev", "Tp_mean", "Tp_stdev"])
        summary_writer.writerow([Ts_mean, Ts_std, Tp_mean, Tp_std])
    return os.path.basename(output_file)

def write_amdahl(Ts_mean, Tp_mean, config, output_dir):
    output_file = os.path.join(output_dir, "amdahl.csv")
    with open(output_file, "w", newline="") as amdahl_file:
        amdahl_writer = csv.writer(amdahl_file)
        amdahl_writer.writerow(["Processes", "Speed Up"])
        for processes in config["amdahl"]["processes"]:
            speed_up = round(1 / (Ts_mean + (Tp_mean / processes)), 3)
            amdahl_writer.writerow([processes, speed_up])
        infinity_speed_up = round(1 / Ts_mean, 3)
        amdahl_writer.writerow(["∞", infinity_speed_up])
    return os.path.basename(output_file)

def write_files(Ts_list, Tp_list, Ts_mean, Ts_std, Tp_mean, Tp_std, config, output_dir):
    runs_summary_filename = write_runs_summary(Ts_list, Tp_list, output_dir)
    summary_filename = write_summary(Ts_mean, Ts_std, Tp_mean, Tp_std, output_dir)
    amdahl_filename = write_amdahl(Ts_mean, Tp_mean, config, output_dir)
    return runs_summary_filename, summary_filename, amdahl_filename

def write_summary_table(input_file, output_file):
    utils.run_file(
        "scripts/tables/profile.py",
        ["--input", input_file, "--output", output_file],
        capture_output=False
    )

def write_amdahl_table(input_file, output_file):
    utils.run_file(
        "scripts/tables/amdahl.py",
        ["--input", input_file, "--output", output_file],
        capture_output=False
    )

def write_tables(summary_filename, amdahl_filename, output_dir, tables_dir):
    write_summary_table(
        os.path.join(output_dir, summary_filename),
        os.path.join(tables_dir, summary_filename.replace(".csv", ".tex"))
    )
    write_amdahl_table(
        os.path.join(output_dir, amdahl_filename),
        os.path.join(tables_dir, amdahl_filename.replace(".csv", ".tex"))
    )

def main():
    args = parse_args()
    config = utils.load_config(args.config)
    benchmark_config = config["benchmark"]
    input_dir, output_dir, tables_dir = prepare_dirs(benchmark_config)

    Ts_list, Tp_list, Ts_mean, Ts_std, Tp_mean, Tp_std = compute_values(config, input_dir)
    runs_summary_filename, summary_filename, amdahl_filename = write_files(
        Ts_list, Tp_list, Ts_mean, Ts_std, Tp_mean, Tp_std, config, output_dir
    )
    write_tables(
        summary_filename, amdahl_filename, output_dir, tables_dir
    )

    print("> All profiling experiments analyzed. Summaries written.")

if __name__ == "__main__":
    main()
