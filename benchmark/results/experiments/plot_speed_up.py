#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv("speed_up.csv")

    plt.figure(figsize=(8, 5))
    for input_len, group in df.groupby("input_length"):
        plt.errorbar(
            group["threads"], group["speed_up"],
            marker='o', label=f"N = {input_len}"
        )

    plt.title("Speed Up por Número de Threads")
    plt.xlabel("Threads")
    plt.ylabel("Speed Up")
    plt.grid(True, linestyle='--')
    plt.legend()
    plt.tight_layout()

    plt.savefig("speed_up.pgf")

if __name__ == "__main__":
    main()
