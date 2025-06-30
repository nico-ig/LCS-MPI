#!/usr/bin/env python3

import pandas as pd

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Generate LaTeX table from CSV data.")
    parser.add_argument("--input", type=str, help="Path to the input CSV file.", default="amdahl.csv")
    parser.add_argument("--output", type=str, help="Path to save the output LaTeX table.", default="amdahl.tex")
    return parser.parse_args()

def main():
    args = parse_args()
    df = pd.read_csv(args.input)
    df["Processes"] = df["Processes"].replace("∞", r"$\infty$")
    latex_table = df.to_latex(index=False, escape=True, float_format="%.3f")
    with open(args.output, "w") as f:
        f.write(latex_table)

if __name__ == "__main__":
    main()
