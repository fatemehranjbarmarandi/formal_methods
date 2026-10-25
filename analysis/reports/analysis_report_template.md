# Results analysis and validation report

## 1. Objective
State the research questions and the exact symmetry/view method being evaluated.

## 2. Experimental environment
- TLC/TLA+ version:
- Java version:
- OS / hardware:
- Model and specification versions:
- Commands and configuration:
- Timeout / memory limit:

## 3. Data collection
Explain the unit of a run, how the CSV was populated, how failures were handled, and where raw logs are stored.

## 4. Quantitative results
Report per-model/per-configuration results. Distinguish generated states, distinct states, and any other metrics actually emitted by the selected TLC version.

## 5. Runtime and state-space comparison
Discuss state reduction and runtime separately. Include preprocessing/overhead where measurable. Do not treat timeouts as completed runtime measurements.

## 6. Safety validation
Summarize known-safe and deliberately buggy models, baseline/candidate outcomes, counterexample review, and any discrepancies.

## 7. Research-question answers
- RQ1 — state-space reduction:
- RQ2 — runtime impact:
- RQ3 — safety-violation detection:
- RQ4 — limitations / conditions where behavior may be lost:

## 8. Limitations and threats to validity
Discuss model coverage, configuration choices, runtime variability, tool/version differences, timeout handling, and assumptions behind symmetry/view.

## 9. Conclusion
Give conclusions supported by actual measurements only.

## Appendix
List exact commands, software versions, raw log locations, and validation checklist.
