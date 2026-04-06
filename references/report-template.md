# Report Template

Use this structure to keep review output consistent.

Rules:

- Findings come first.
- Each finding should fit on 2-3 short lines.
- Prefer concrete runtime impact over generic “best practice” language.
- If no confirmed findings exist, state that explicitly and use `Open Risks` for anything unverified.

## Example

### Findings

- `critical` [ORD010.RPGLE:45] Numeric `VARX` is declared without initialization and is used in amount calculation.
  Impact: the value can be undefined and produce incorrect totals.
  Fix: initialize `VARX` with `INZ(0)` or assign a guaranteed value before first use.

- `medium` [ORD010.RPGLE:88] `CHAIN` result is used without a `%FOUND` check.
  Impact: downstream fields may be read from an unfound record path.
  Fix: gate field access behind `%FOUND(file)` and add the not-found branch.

### Open Risks

- Record format and DDS field widths were not provided, so DS alignment checks are partial.

### Release Gate

- `blocked` because transaction failure handling has not been demonstrated for the commit path.

### Summary

- 2 findings total: 1 critical, 1 medium.
- Highest risk theme: unsafe initialization and missing file-status checks.
