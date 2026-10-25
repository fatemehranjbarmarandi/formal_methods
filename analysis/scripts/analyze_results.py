#!/usr/bin/env python3
"""Validate TLC results CSV and create summary CSVs/plots.

Usage:
  python analysis/scripts/analyze_results.py --input analysis/data/results.csv --output-dir analysis/figures

Only actual measurements should be entered in the input CSV. Missing metrics are
kept missing. Timeout/unknown/crash runs are not treated as completed timings.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd
import matplotlib.pyplot as plt

REQUIRED = [
    "run_id", "model_name", "configuration", "method",
    "elapsed_sec", "states_generated", "distinct_states", "result_status"
]
VALID_STATUSES = {"success", "violation", "timeout", "unknown", "crash"}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="analysis/data/results.csv")
    parser.add_argument("--output-dir", default="analysis/figures")
    args = parser.parse_args()

    source = Path(args.input)
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    if not source.exists():
        print(f"ERROR: CSV not found: {source}", file=sys.stderr)
        return 2

    df = pd.read_csv(source)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        print("ERROR: missing required columns: " + ", ".join(missing), file=sys.stderr)
        return 2
    if df.empty:
        print("CSV has headers but no runs yet. Add actual TLC measurements, then rerun.")
        return 0

    df["result_status"] = df["result_status"].astype("string").str.strip().str.lower()
    unknown_statuses = sorted(set(df["result_status"].dropna()) - VALID_STATUSES)
    if unknown_statuses:
        print("WARNING: unexpected result_status values:", unknown_statuses)

    for col in ["elapsed_sec", "states_generated", "distinct_states"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    status = (
        df.groupby(["model_name", "configuration", "method", "result_status"], dropna=False)
          .size().rename("runs").reset_index()
    )
    status.to_csv(out / "status_summary.csv", index=False)

    completed = df[~df["result_status"].isin(["timeout", "unknown", "crash"])].copy()
    metrics = ["elapsed_sec", "states_generated", "distinct_states"]
    if not completed.empty:
        summary = (
            completed.groupby(["model_name", "configuration", "method"], dropna=False)[metrics]
            .agg(["count", "median", "mean", "min", "max"])
        )
        summary.columns = ["_".join(map(str, c)) for c in summary.columns]
        summary.reset_index().to_csv(out / "completed_run_summary.csv", index=False)

        for metric, title, filename, ylabel in [
            ("distinct_states", "Distinct states by model/configuration/method",
             "distinct_states_comparison.png", "Distinct states"),
            ("elapsed_sec", "Elapsed time by model/configuration/method",
             "runtime_comparison.png", "Elapsed time (seconds)"),
        ]:
            plot_df = completed.dropna(subset=[metric]).copy()
            if plot_df.empty:
                continue
            plot_df["group"] = (
                plot_df["model_name"].astype(str) + " | " +
                plot_df["configuration"].astype(str) + " | " +
                plot_df["method"].astype(str)
            )
            grouped = plot_df.groupby("group")[metric].median().sort_values()
            ax = grouped.plot(kind="bar", figsize=(max(8, len(grouped) * 1.2), 5))
            ax.set_title(title)
            ax.set_ylabel(ylabel)
            ax.set_xlabel("Model | configuration | method")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.savefig(out / filename, dpi=160)
            plt.close()

    total = df.groupby(["model_name", "configuration", "method"], dropna=False).size()
    completed_count = (
        df[~df["result_status"].isin(["timeout", "unknown", "crash"])]
        .groupby(["model_name", "configuration", "method"], dropna=False).size()
    )
    completion = pd.concat(
        [total.rename("total_runs"), completed_count.rename("completed_runs")], axis=1
    ).fillna(0).reset_index()
    completion["completion_rate_pct"] = (
        completion["completed_runs"] / completion["total_runs"] * 100
    )
    completion.to_csv(out / "completion_summary.csv", index=False)

    print(f"Analysis outputs written to: {out.resolve()}")
    print("Remember: plots summarize entered data; they do not validate the method by themselves.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
