#!/usr/bin/env python3

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Remove odd blocks from a file.")
    parser.add_argument("-i", "--input", help="The name of the file to process.")
    parser.add_argument("-o", "--output", help="The name of the output file.", type=str)
    return parser.parse_args()

def remove_odd_blocks(input_file, output_file):
    with open(input_file, "r") as file:
        lines = file.readlines()
    groups = []
    current = []
    for line in lines:
        if "start_time,end_time,elapsed_time" in line:
            if len(current) > 0:
                groups.append("\n".join(current))
            current = []
        if line.strip():
            current.append(line.strip())
    if len(current) > 0:
        groups.append("\n".join(current))
    groups = [group for i, group in enumerate(groups) if i % 2 == 0]
    with open(output_file, "w") as file:
        file.write("\n".join(groups))
        file.write("\n")

if __name__ == "__main__":
    args = parse_args()
    remove_odd_blocks(args.input, args.output)