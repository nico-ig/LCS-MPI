#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import argparse
import math
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser(description="Plot speed up from CSV data.")
    parser.add_argument("--input", type=str, required=True, help="Path to the input CSV file.")
    parser.add_argument("--output", type=str, required=True, help="Path to save the output plot.")
    return parser.parse_args()

def main():
    args = parse_args()
    df = pd.read_csv(args.input)

    df = df.sort_values(by=["Processes", "Nodes", "Length"]).reset_index(drop=True)
    df["Label"] = df.apply(lambda row: f"({row['Processes']}, {row['Nodes']})", axis=1)

    fig, ax = plt.subplots(figsize=(12, 6))
    lengths = sorted(df["Length"].unique())

    x = np.arange(len(df["Label"].unique()))

    for i, length in enumerate(lengths):
        group = df[df["Length"] == length]
        ax.errorbar(
            x,
            group["Mean Time"],
            yerr=group["Std Dev"],
            marker='o',
            linestyle='-',
            capsize=3,
            label=f"N = {length}"
        )

    ax.set_xticks(x)
    ax.set_xticklabels(df["Label"].unique())
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.title("Tempo Médio (s) por Número de Processos e Nodos")
    plt.xlabel("(Processos, Nodos)")
    plt.ylabel("Tempo Médio (s)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(args.output)

if __name__ == "__main__":
    main()