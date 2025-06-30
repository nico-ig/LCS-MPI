#!/usr/bin/env python3

import pandas as pd

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Generate LaTeX table from CSV data.")
    parser.add_argument("--input", type=str, help="Path to the input CSV file.", default="efficiency.csv")
    parser.add_argument("--output", type=str, help="Path to save the output LaTeX table.", default="efficiency.tex")
    return parser.parse_args()

def main():
    args = parse_args()
    df = pd.read_csv(args.input)
    pivot = df.pivot(index="Length", columns="Processes", values="Efficiency")
    pivot = pivot[sorted(pivot.columns)]
    pivot.columns = [f"{int(col)}" for col in pivot.columns]
    pivot.columns.name = "N/Processes"
    pivot.index.name = None

    latex_table = pivot.to_latex(float_format="%.3f", escape=False)

    with open(args.output, "w") as f:
        f.write(latex_table)

if __name__ == "__main__":
    main()
