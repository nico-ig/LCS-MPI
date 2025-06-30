#!/usr/bin/env python3

import pandas as pd

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Generate LaTeX table from CSV data.")
    parser.add_argument("--input", type=str, help="Path to the input CSV file.", default="global_summary.csv")
    parser.add_argument("--output", type=str, help="Path to save the output LaTeX table.", default="global_summary.tex")
    return parser.parse_args()

def main():
    args = parse_args()
    df = pd.read_csv(args.input)

    ts_mean = df['Ts_mean'][0] * 100
    ts_stdev = df['Ts_stdev'][0] * 100
    tp_mean = df['Tp_mean'][0] * 100
    tp_stdev = df['Tp_stdev'][0] * 100

    table = pd.DataFrame({
        r"Ts (\%)": [f"{ts_mean:.1f}\\% ± {ts_stdev:.1f}\\%"],
        r"Tp (\%)": [f"{tp_mean:.1f}\\% ± {tp_stdev:.1f}\\%"]
    })

    with open(args.output, "w") as f:
        f.write(table.to_latex(index=False, escape=False))

if __name__ == "__main__":
    main()
