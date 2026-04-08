# Mixed-Source RPGLE Review Guide

Use this reference when a member combines fixed-format and free-format logic, subroutines, indicators, or transitional syntax.

## Why Mixed-Source Review Needs Special Care

Mixed members often fail at the seam between styles rather than inside one style alone. The risk is not only syntax, but whether state, indicators, and assumptions survive correctly across the fixed/free boundary.

## High-Priority Checks

- Verify that a found/not-found condition established in fixed-format still protects later free-format logic.
- Verify that indicator-driven state is not silently replaced by `%FOUND` or modern conditionals without preserving behavior.
- Verify that arithmetic or movement done in fixed-format is not later interpreted as fully validated in free-format.
- Verify that shared working variables are initialized and understood consistently across both styles.
- Verify that a subroutine called from one style does not depend on hidden state set only in the other style.

## Typical Failure Patterns

- Fixed-format `CHAIN` guarded by `*IN90`, followed by free-format field usage outside the guarded branch
- Legacy indicator state reused in a free-format `if` path without reset or clear ownership
- Fixed-format `MOVE/MOVEL` or `Z-ADD` transforming data that free-format code later treats as canonical
- `/FREE` block added for readability, but release or error handling still lives in a fragile fixed-format path

## Review Strategy

1. Trace the data and indicator state before the style transition.
2. Trace the first free-format statement that assumes the earlier state is safe.
3. Flag the seam if protection, initialization, or release logic does not carry across clearly.

## Output Notes

- Call out the style transition explicitly in the finding.
- Prefer “behavior leaks across the fixed/free boundary” over generic modernization commentary.
