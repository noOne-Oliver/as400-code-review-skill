# Forward Test Notes

These notes capture common drift patterns when reviewing AS400 code with this skill.

## Drift 1: Checklist Over Findings

Observed risk:

- The review turns into a generic checklist instead of prioritized findings.

Correction:

- Lead with concrete defects from the code.
- Keep checklist-style statements only for `pre-release-gate` mode or when no specific finding is possible.

## Drift 2: Naming Over Runtime Risk

Observed risk:

- The review spends too much space on `TMP1`, `FLAG`, or comment quality while underweighting missing `%FOUND`, initialization, or commit failures.

Correction:

- Rank runtime and data-integrity issues first.
- Mention naming after correctness unless the name itself can cause wrong maintenance behavior.

## Drift 3: Overconfident AS400 Claims

Observed risk:

- The review states DS mismatch, object-lock, or compile-risk conclusions without definitions or operational context.

Correction:

- Move unverified concerns to `Open Risks`.
- Keep the finding level only for defects visible from the code itself.
