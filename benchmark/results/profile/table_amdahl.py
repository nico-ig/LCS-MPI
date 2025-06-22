#!/usr/bin/env python3

import pandas as pd

def main():
    df = pd.read_csv("amdahl.csv")
    df["threads"] = df["threads"].replace("∞", r"$\infty$")
    latex_table = df.to_latex(index=False, escape=True, float_format="%.3f")
    with open("amdahl.tex", "w") as f:
        f.write(latex_table)

if __name__ == "__main__":
    main()
