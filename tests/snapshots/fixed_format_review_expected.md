### Findings

- `critical` [ORDUPD.RPGLE:9] `DIV` uses `OHQTY` without a visible zero check before dividing `AMT`.
  Impact: a zero quantity can trigger arithmetic failure or produce invalid average values in the update path.
  Fix: guard the divide with an explicit zero check before executing `DIV`.

- `critical` [ORDUPD.RPGLE:10] `UPDATE ORDHDR` executes even when `*IN90` signals that the `CHAIN` did not find a record.
  Impact: the member can attempt an unsafe update using stale record state or an invalid access path.
  Fix: move `UPDATE ORDHDR` inside the found-record branch or add an explicit not-found exit path.

- `medium` [ORDUPD.RPGLE:7] `*IN90` protects `Z-ADD` but does not protect the later arithmetic and update flow.
  Impact: the member appears partially guarded, which makes the not-found path easy to misread and maintain incorrectly.
  Fix: keep the full business path, including divide and update, inside the same found-record branch.

### Open Risks

- DDS definitions and record-level lock behavior were not provided, so external format and concurrency checks are partial.

### Summary

- 3 findings total: 2 critical, 1 medium.
- Highest risk theme: fixed-format indicator leakage and unsafe arithmetic/update flow.
