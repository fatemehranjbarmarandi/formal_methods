# Validation protocol

## Goal
Check that the tested symmetry/view configuration preserves the safety conclusions relevant to the project, and document cases where behavior differs from the baseline.

## Before running
1. Record the exact TLC/TLA+ version, operating system, Java version, hardware, model/spec files, command-line options, and method configuration.
2. Keep the baseline and candidate runs identical except for the option under test.
3. Save raw TLC output/logs and do not overwrite them.
4. Decide a timeout and memory limit before the comparison; use the same limits for comparable runs.

## Test cases
1. **Known-safe model:** baseline and candidate should both complete without a safety violation, assuming the state space is fully explored.
2. **Known-buggy model:** introduce a deliberate, documented safety violation. Baseline and candidate should both report it if the method is intended to preserve that property and the run completes.
3. **Boundary/small model:** use a small instance where states and expected behavior can be inspected manually.
4. **Symmetry assumptions:** verify that the declared symmetry is valid for the model and property; symmetry is not safe merely because it reduces states.
5. **View assumptions:** document what information the view removes/abstracts and why it is irrelevant to the safety property. Check that property-relevant distinctions are not erased.
6. **Failure handling:** classify `timeout`, `unknown`, and `crash` separately; none means the property was proven safe.

## Compare and investigate
- If baseline finds a counterexample but candidate does not, do not claim success. Re-run, inspect configuration/logs, and treat it as a potential soundness issue until explained.
- Inspect counterexamples, not only the final status.
- A lower state count does not by itself establish correctness or faster runtime.
- Record any manual review and rationale in `validation_checklist.csv`.

## Suggested status values
`pass`, `fail`, `needs_investigation`, `not_run`.

## Evidence to retain
Raw logs, model/spec files, exact commands, version information, CSV rows, plots, and notes explaining exclusions or reruns.
