#!/usr/bin/env python3

import pandas as pd

def main():
    df = pd.read_csv("global_summary.csv")

    # Convert to percentages
    ts_mean = df['Ts_mean'][0] * 100
    ts_stdev = df['Ts_stdev'][0] * 100
    tp_mean = df['Tp_mean'][0] * 100
    tp_stdev = df['Tp_stdev'][0] * 100

    # Create a LaTeX-friendly DataFrame
    table = pd.DataFrame({
        "Ts (\%)": [f"{ts_mean:.1f}\\% ± {ts_stdev:.1f}\\%"],
        "Tp (\%)": [f"{tp_mean:.1f}\\% ± {tp_stdev:.1f}\\%"]
    })

    with open("global_summary.tex", "w") as f:
        f.write(table.to_latex(index=False, escape=False))

if __name__ == "__main__":
    main()
