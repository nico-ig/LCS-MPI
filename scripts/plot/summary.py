#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Plot summary data: Mean Time vs Processes")
    parser.add_argument("--input", type=str, required=True, help="Input CSV file path")
    parser.add_argument("--output", type=str, required=True, help="Output plot file path")
    return parser.parse_args()

def main():
    args = parse_args()
    df = pd.read_csv(args.input)

    plt.figure(figsize=(8, 5))
    for length, group in df.groupby("Length"):
        plt.errorbar(
            group["Processes"],
            group["Mean Time"],
            yerr=group["Std Dev"],
            marker='o',
            capsize=3,
            label=f"N = {length}"
        )

    plt.title("Tamanho da Entrada - Tempo Médio vs Número de Processos")
    plt.xlabel("Número de Processos")
    plt.ylabel("Tempo Médio (s)")
    plt.grid(True, linestyle='--')
    plt.legend()
    plt.tight_layout()

    plt.savefig(args.output)

if __name__ == "__main__":
    main()
