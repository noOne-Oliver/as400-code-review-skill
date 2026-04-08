# Golden Findings

Use these examples to calibrate severity, wording, and fix recommendations. Prefer this style over generic checklist output.

## Example 1: Uninitialized Numeric In Critical Path

```text
critical [ORDPAY.RPGLE:42] Packed numeric `payAmt` is declared without `INZ` and is read before a guaranteed assignment.
Impact: payment calculations can use undefined data and write incorrect amounts to the order record.
Fix: initialize `payAmt` with `INZ(0)` or move the first assignment above every read path.
```

Why this is strong:

- Identifies the exact variable and where it matters.
- Explains concrete business impact.
- Recommends the smallest safe fix.

## Example 2: CHAIN Without Found Handling

```text
critical [ORDQRY.RPGLE:88] `CHAIN` to `ORDHDR` is followed by field access without a `%FOUND(ORDHDR)` guard.
Impact: the program can use stale or invalid field values on the not-found path and return incorrect results.
Fix: gate field access behind `%FOUND(ORDHDR)` and add an explicit not-found branch.
```

Why this is strong:

- Ties the finding to a specific file operation.
- Describes the incorrect runtime behavior instead of saying “best practice”.

## Example 3: Weak Naming With Real Maintenance Risk

```text
medium [CUSUPD.RPGLE:31] Variable `FLAG1` controls customer eligibility but its name does not indicate meaning or legal values.
Impact: later maintenance can apply the wrong branch logic or mis-handle status transitions.
Fix: rename it to a business-meaningful name such as `isEligible` or `custStatusFlg`, and document allowed values if it is not boolean.
```

Why this is strong:

- Keeps naming findings below correctness issues.
- Only escalates because the ambiguous name can drive wrong future changes.

## Example 4: Release Blocker On Commit Path

```text
critical [SETLJOB.RPGLE:120] Commit logic is present, but no rollback or failure-path behavior is visible for update errors.
Impact: partial settlement updates may persist without a verified recovery path.
Fix: add and test rollback handling for failed update or post-update validation paths before release.
```

Why this is strong:

- Appropriate for pre-release review.
- Explains why the issue blocks deployment rather than treating all COMMIT usage as equally risky.

## Example 5: Fixed-Format Indicator Leakage

```text
critical [ORDUPD.RPGLE:10] `UPDATE ORDHDR` runs outside the `*IN90 = *OFF` found-record branch after `CHAIN`.
Impact: the member can update with stale record state or on an invalid not-found path.
Fix: keep the entire update flow inside the found-record branch or exit immediately on indicator 90.
```

Why this is strong:

- It captures a fixed-format bug that a free-format-only review would often miss.
- It explains the indicator behavior in business terms rather than only citing legacy syntax.

## Example 6: Mixed-Source Guard Lost At Style Boundary

```text
critical [ORDMIX.RPGLE:8] Free-format logic reads `OHSTAT` after a fixed-format `CHAIN` without carrying the `*IN90` not-found guard across the style boundary.
Impact: the member can read stale or invalid record data when the order is not found.
Fix: keep the free-format branch inside an explicit found-record guard or exit immediately on `*IN90`.
```

Why this is strong:

- It catches a defect that exists at the seam between styles, not inside either style alone.
- It focuses on behavior leakage across the transition rather than generic modernization commentary.
