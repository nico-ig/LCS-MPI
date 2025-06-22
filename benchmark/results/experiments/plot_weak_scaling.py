#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv("weak_scaling.csv")

    df = df.sort_values(by="threads")

    x_labels = [f"({n}, {t})" for n, t in zip(df["input_length"], df["threads"])]
    x_positions = range(len(df))

    plt.figure(figsize=(8, 4))

    plt.errorbar(
        x_positions,
        df["T_mean"],
        yerr=df["T_stdev"],
        marker='o',
        capsize=3,
        label="Escalabilidade Fraca"
    )

    plt.title("Escalabilidade Fraca - Tempo Médio vs Threads")
    plt.xlabel("N, Threads")
    plt.ylabel("Tempo Médio (s)")
    plt.xticks(ticks=x_positions, labels=x_labels, rotation=0, ha='center')
    plt.grid(True, linestyle='--')
    plt.legend()
    plt.tight_layout()

    plt.savefig("weak_scaling.pgf")

if __name__ == "__main__":
    main()

