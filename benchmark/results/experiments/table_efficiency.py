#!/usr/bin/env python3

import pandas as pd

def main():
    df = pd.read_csv("efficiency.csv")
    pivot = df.pivot(index="input_length", columns="threads", values="efficiency")
    pivot = pivot[sorted(pivot.columns)]
    pivot.columns = [f"{int(col)}" for col in pivot.columns]
    pivot.columns.name = "N/Threads"
    pivot.index.name = None

    latex_table = pivot.to_latex(float_format="%.3f", escape=False)

    with open("efficiency.tex", "w") as f:
        f.write(latex_table)

if __name__ == "__main__":
    main()
