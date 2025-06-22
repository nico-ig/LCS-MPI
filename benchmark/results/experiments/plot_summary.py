#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv("summary.csv")
    plt.figure(figsize=(8, 5))
    for input_len, group in df.groupby("input_length"):
        plt.errorbar(
            group["threads"],
            group["T_mean"],
            yerr=group["T_stdev"],
            marker='o',
            capsize=3,
            label=f"N = {input_len}"
        )

    plt.title("Tamanho da Entrada - Tempo Médio vs Threads")
    plt.xlabel("Threads")
    plt.ylabel("Tempo Médio (s)")
    plt.grid(True, linestyle='--')
    plt.legend()
    plt.tight_layout()

    plt.savefig("summary.pgf")

if __name__ == "__main__":
    main()
