#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv("efficiency.csv")

    plt.figure(figsize=(8, 5))
    for input_len, group in df.groupby("input_length"):
        plt.errorbar(
            group["threads"], group["efficiency"],
            marker='o', label=f"N = {input_len}"
        )

    plt.title("Eficiência por Número de Threads")
    plt.xlabel("Threads")
    plt.ylabel("Eficiência")
    plt.grid(True, linestyle='--')
    plt.legend()
    plt.tight_layout()

    plt.savefig("efficiency.pgf")

if __name__ == "__main__":
    main()
