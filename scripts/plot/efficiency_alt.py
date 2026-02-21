#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Plot speed up from CSV data.")
    parser.add_argument("--input", type=str, required=True, help="Path to the input CSV file.")
    parser.add_argument("--output", type=str, required=True, help="Path to save the output plot.")
    return parser.parse_args()

def main():
    args = parse_args()
    df = pd.read_csv(args.input)

    mean_efficiency = df.groupby(["Processes", "Nodes"])["Efficiency"].mean().reset_index()
    mean_efficiency["Label"] = mean_efficiency.apply(lambda row: f"({row['Processes']}, {row['Nodes']})", axis=1)
    mean_efficiency = mean_efficiency.sort_values(by="Efficiency", ascending=False)
    fig, ax = plt.subplots(figsize=(12, 6))
    x_labels = mean_efficiency["Label"].to_numpy()
    x_pos = range(len(x_labels))

    ax.plot(x_pos, mean_efficiency["Efficiency"].to_numpy(), marker='o', label="Eficiência Média")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(x_labels)

    ax.set_ylim(0, 1.2)
    ax.set_title("Eficiência Média por Número de Processos e Nodos")
    ax.set_xlabel("(Processos, Nodos)")
    ax.set_ylabel("Eficiência Média")
    ax.grid(True, linestyle="--")
    ax.legend()
    plt.tight_layout()
    plt.savefig(args.output)

if __name__ == "__main__":
    main()
