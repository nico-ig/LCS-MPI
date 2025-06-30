#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Plot speed up from CSV data.")
    parser.add_argument("--input", type=str, help="Path to the input CSV file.")
    parser.add_argument("--output", type=str, help="Path to save the output plot.")
    return parser.parse_args()

def main():
    args = parse_args()
    df = pd.read_csv(args.input)

    plt.figure(figsize=(8, 5))
    for length, group in df.groupby("Length"):
        plt.plot(
            group["Processes"].to_numpy(), group["Speed Up"].to_numpy(),
            marker='o', label=f"N = {length}"
        )

    plt.title("Speed Up por Número de Processos")
    plt.xlabel("Processos")
    plt.ylabel("Speed Up")
    plt.grid(True, linestyle='--')
    plt.legend()
    plt.tight_layout()

    plt.savefig(args.output)

if __name__ == "__main__":
    main()
