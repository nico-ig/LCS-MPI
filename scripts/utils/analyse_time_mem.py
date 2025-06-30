#!/usr/bin/env python3

import os
import argparse
import sys
import csv
import tempfile
import statistics
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".", ".")))
import utils as utils

def parse_args():
    parser = argparse.ArgumentParser(description="Run LCS-MPI experiments to analyze time and memory usage. This script should be run in cluster.")
    parser.add_argument("--config", required=True, help="Path to the YAML configuration file.")
    return parser.parse_args()

def make_usage_script(case, binary, input_files, output_dir):
    script_list = {}
    for length in input_files:
        fileA, fileB = input_files[length]
        with open("./scripts/utils/monitor.sh", "r") as f:
            monitor_script = f.read()
        output_file = os.path.join(output_dir, f"{case['nodes']}_{case['ntasks']}_{length}_{{INDEX}}.out")
        script = monitor_script.replace("{OUTPUT}", output_file)
        script = script.replace("{BINARY}", binary)
        script = script.replace("{FILE_A}", fileA)
        script = script.replace("{FILE_B}", fileB)
        script = script.replace("{NODES}", str(case["nodes"]))
        script = script.replace("{NTASKS}", str(case["ntasks"]))
        script = script.replace("{NTASKS_PER_NODE}", str(case["ntasks_per_node"]))
        script = script.replace("{BIND_TO}", str(case["bind_to"]))
        script = script.replace("{CPU_LIST}", ",".join(str(c) for c in case['cpu_list']))
        script_list[length] = script
    return script_list

def parse_time(lines):
    elapsed_line = next(line.split(": ", 1)[1] for line in lines if "Elapsed (wall clock)" in line)
    elapsed_str = elapsed_line.replace("seconds", "").strip()
    elapsed_sec = float(elapsed_str)
    return elapsed_sec

def parse_memory(lines):
    mem_line = next(line.split(":", 1)[1].strip() for line in lines if "Maximum resident set size" in line)
    mem_kb_str = mem_line.replace("KB", "").strip()
    mem_kb = int(mem_kb_str)
    mem_gb = round(mem_kb / (1024 * 1024), 3)
    return mem_gb

def run_single_script(nodes, ntasks, script, length, i, output_dir, tmp_dir):
    script = script.replace("{INDEX}", str(i))
    job_id = utils.submit_job(script, tmp_dir)
    utils.wait_for_job(job_id, 5)
    output_file = os.path.join(output_dir, f"{nodes}_{ntasks}_{length}_{i}.out")
    with open(output_file, "r") as f:
        result = f.read()
    lines = result.splitlines() 
    elapsed = parse_time(lines)
    mem = parse_memory(lines)
    return elapsed, mem

def run_script_multiple_times(nodes, ntasks, script, length, output_dir, tmp_dir, runs):
    elapsed_list = []
    mem_list = []
    for i in range(runs):
        elapsed, mem = run_single_script(nodes, ntasks, script, length, i, output_dir, tmp_dir)
        elapsed_list.append(elapsed)
        mem_list.append(mem)
    avg_elapsed = statistics.mean(elapsed_list)
    avg_mem = statistics.mean(mem_list)
    return avg_elapsed, avg_mem

def run_usage_scripts(nodes, ntasks, script_list, output_dir, tmp_dir, runs=1):
    usage = {}
    for length, script in script_list.items():
        print(f"> Running usage for length {length}.")
        avg_elapsed, avg_mem = run_script_multiple_times(nodes, ntasks, script, length, output_dir, tmp_dir, runs)
        usage[length] = (avg_elapsed, avg_mem)
    return usage

def save_usage_to_csv(usage, output_path):
    with open(output_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["nodes", "ntasks", "length", "time_seconds", "memory_gb"])
        for (nodes, ntasks), usage_dict in usage.items():
            for length, (time_sec, mem_gb) in usage_dict.items():
                writer.writerow([nodes, ntasks, length, f"{time_sec:.2f}", mem_gb])

def main():
    args = parse_args()
    config = utils.load_config(args.config)
    benchmark_config = config["benchmark"]
    release_config = config["release"]

    tmp_dir = benchmark_config["tmp_dir"]
    output_dir = utils.prepare_directories(config, "usage")
    output_path = os.path.join(output_dir, "usage.csv")

    try:
        utils.compile_release_binary(config)
        input_files = utils.generate_sequence_files(config["experiments"]["length_cases"], benchmark_config["tmp_dir"])
        usage = {}

        for test_case in config["experiments"]["test_cases"]:
            nodes = test_case["nodes"]
            ntasks = test_case["ntasks"]
            print(f"> Running usage for {nodes} nodes and {ntasks} tasks.")
            script_list = make_usage_script(test_case, release_config["binary"], input_files, output_dir)
            usage[(nodes, ntasks)] = run_usage_scripts(nodes, ntasks, script_list, output_dir, tmp_dir)

        save_usage_to_csv(usage, output_path)
    except KeyboardInterrupt:
        print("\n> Analysis interrupted by user.")
        sys.exit(1)
    finally:
        print(f"> Usage saved to {output_path}.")

if __name__ == "__main__":
    main()
