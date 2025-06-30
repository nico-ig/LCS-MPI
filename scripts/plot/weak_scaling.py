#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Plot weak scaling data.")
    parser.add_argument("--input", type=str, required=True, help="Input CSV file path")
    parser.add_argument("--output", type=str, required=True, help="Output plot file path")
    return parser.parse_args()

def main():
    args = parse_args()
    df = pd.read_csv(args.input)

    df = df.sort_values(by=["Processes", "Length"])

    x_labels = [f"({length}, {procs})" for length, procs in zip(df["Length"], df["Processes"])]
    x_positions = range(len(df))

    plt.figure(figsize=(8, 4))
    plt.errorbar(
        x_positions,
        df["Mean Time"],
        yerr=df["Std Dev"],
        marker='o',
        capsize=3,
        label="Escalabilidade Fraca"
    )

    plt.title("Escalabilidade Fraca - Tempo Médio vs Processos")
    plt.xlabel("Tamanho da entrada e número de processos")
    plt.ylabel("Tempo Médio (s)")
    plt.xticks(ticks=x_positions, labels=x_labels, rotation=0, ha='center')
    plt.grid(True, linestyle='--')
    plt.legend()
    plt.tight_layout()

    plt.savefig(args.output)

if __name__ == "__main__":
    main()
