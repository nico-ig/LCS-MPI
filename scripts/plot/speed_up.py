#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import argparse
import math

def parse_args():
    parser = argparse.ArgumentParser(description="Plot speed up from CSV data.")
    parser.add_argument("--input", type=str, required=True, help="Path to the input CSV file.")
    parser.add_argument("--output", type=str, required=True, help="Path to save the output plot.")
    return parser.parse_args()

def main():
    args = parse_args()
    df = pd.read_csv(args.input)

    df = df.sort_values(by=["Processes", "Nodes"]).reset_index(drop=True)
    df = df[~df[["Processes", "Nodes"]].apply(tuple, axis=1).isin({(6, 1), (12, 2)})]
    df["Label"] = df.apply(lambda row: f"({row['Processes']}, {row['Nodes']})", axis=1)

    fig, ax = plt.subplots(figsize=(12, 6))
    lengths = sorted(df["Length"].unique())

    for i, length in enumerate(lengths):
        group = df[df["Length"] == length]
        ax.plot(
            group["Label"].to_numpy(), 
            group["Speed Up"].to_numpy(), 
            marker='o', label=f"N = {length}"          
        )
        ax.set_ylim(0, 2.5)

    plt.title("Speed Up por Número de Processos e Nodos")
    plt.xlabel("(Processos, Nodos)")
    plt.ylabel("Speed Up")
    plt.grid(True, linestyle='--')
    plt.legend()
    plt.tight_layout()

    plt.savefig(args.output)

if __name__ == "__main__":
    main()