# Formal Methods — TLC Results Analysis and Validation

This area supports the **results analysis and validation** workstream for the project on Automatic Symmetry and View for TLC.

## Status
- CSV files are templates and initially contain headers only.
- No experimental results are fabricated or presented as real.
- Populate them only with measurements from actual TLC runs.
- Confirm the exact method implementation, TLC version, model/specification, and command-line options with the team before interpreting results.

## Contents
- `analysis/data/results.csv`: one row per actual run/configuration.
- `analysis/data/validation_checklist.csv`: expected-vs-actual safety validation cases.
- `analysis/scripts/analyze_results.py`: CSV checks, summary tables, and plots.
- `analysis/docs/validation_protocol.md`: validation procedure and interpretation rules.
- `analysis/reports/analysis_report_template.md`: report outline.

## Quick start
Install dependencies:
```bash
python -m pip install pandas matplotlib
```
Run analysis from the repository root:
```bash
python analysis/scripts/analyze_results.py --input analysis/data/results.csv --output-dir analysis/figures
```

The script preserves missing measurements, keeps timeout/crash/unknown outcomes distinct from completed runs, and writes summaries and plots only when measurements exist.

## Important interpretation notes
- State-count reduction alone does not prove correctness or improved runtime.
- A timeout, crash, or unknown result is not evidence that a safety property holds.
- If the baseline finds a counterexample but the candidate method does not, investigate as a potential soundness issue.
- Keep raw TLC logs, exact commands, and tool/model versions alongside the experiment records.
