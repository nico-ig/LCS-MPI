#!/usr/bin/env python3

import pandas as pd

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Generate LaTeX table from CSV data.")
    parser.add_argument("--input", type=str, help="Path to the input CSV file.")
    parser.add_argument("--output", type=str, help="Path to save the output LaTeX table.")
    return parser.parse_args()

def format_latex_table(df, output_path):
    df = df.sort_values(by=["Processes", "Length"])

    table_data = {}
    for _, row in df.iterrows():
        processes = int(row["Processes"])
        length = int(row["Length"])
        mean = row["Mean Time"]
        std = row["Std Dev"]
        if processes not in table_data:
            table_data[processes] = {}
        table_data[processes][length] = (mean, std)

    lengths = sorted({l for data in table_data.values() for l in data})
    proc_counts = sorted(table_data.keys())

    lines = []
    lines.append("\\begin{tabular}{rr|" + "c" * len(lengths) + "}")
    lines.append("\\toprule")
    lines.append("\\multicolumn{2}{r|}{} & \\multicolumn{%d}{c}{\\textbf{Tamanho}} \\\\" % len(lengths))
    lines.append("\\cmidrule(lr){3-%d}" % (2 + len(lengths)))
    header = " & ".join([f"\\textbf{{{l:,.0f}}}" for l in lengths])
    lines.append("\\multicolumn{2}{c|}{\\textbf{Threads}} & " + header + " \\\\")
    lines.append("\\midrule")

    for p in proc_counts:
        lines.append(f"\\multirow{{2}}{{*}}{{\\textbf{{{p}}}}}")
        means = [f"{table_data[p][l][0]:.3f}" if l in table_data[p] else "" for l in lengths]
        lines.append(f"& \\textit{{mean}} (s) & " + " & ".join(means) + " \\\\")
        stds = [f"{table_data[p][l][1]:.3f}" if l in table_data[p] else "" for l in lengths]
        lines.append(f"& \\textit{{stdv}} (s) & " + " & ".join(stds) + " \\\\")
        lines.append("\\midrule")

    lines[-1] = "\\bottomrule"
    lines.append("\\end{tabular}")

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

def main():
    args = parse_args()
    df = pd.read_csv(args.input)
    format_latex_table(df, args.output)

if __name__ == "__main__":
    main()
