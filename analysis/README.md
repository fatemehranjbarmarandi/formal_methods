# TLC results analysis workflow

## Files
- `data/results.csv`: one row per run and configuration. Do not enter guessed or illustrative measurements as real results.
- `data/validation_checklist.csv`: records expected vs. actual outcomes for safe, buggy, and boundary models.
- `scripts/analyze_results.py`: produces summaries and plots from recorded measurements.
- `docs/validation_protocol.md`: repeatable validation procedure.
- `reports/analysis_report_template.md`: report structure.

## Record consistently
Use the same TLC version, model/specification, environment, timeout, and memory limit for baseline/candidate comparisons except for the method option being tested. Save the exact command and raw log path in `notes` or the team's experiment log. Check which state counters the exact TLC version reports before mapping them into CSV columns.

Suggested `result_status` values: `success`, `violation`, `timeout`, `unknown`, `crash`. A timeout/crash/unknown is not a proof of safety. Leave unmeasured numeric cells blank, not zero.

## Run analysis
From the repository root:
```bash
python -m pip install -r requirements.txt
python analysis/scripts/analyze_results.py --input analysis/data/results.csv --output-dir analysis/figures
```

The script creates status, completed-run, and completion summaries; it creates median distinct-state and runtime plots when suitable numeric data exists. It excludes timeout, unknown, and crash runs from completed-run metrics. It does not infer correctness from state counts.

## Reduction formulas
For comparable completed runs, state reduction (%) = `(baseline distinct states - candidate distinct states) / baseline distinct states * 100`. Runtime improvement (%) = `(baseline elapsed seconds - candidate elapsed seconds) / baseline elapsed seconds * 100`. Do not treat a timeout as a completed runtime measurement; report it separately.
