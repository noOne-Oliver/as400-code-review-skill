# Review Playbook

Use this playbook to choose the shortest correct review path.

## Mode Selection

### Code Review

Use when the user asks to review a source member, patch, or local change.

Focus:

- concrete code defects
- incorrect status handling
- initialization and DS issues
- naming problems that can mislead maintenance

### Pre-Release Gate

Use when the user asks about上线, deploy readiness, production checks, or release blockers.

Focus:

- must-fix issues before release
- transaction and rollback paths
- object locks and operational risk
- checklist-driven deployment readiness

### Focused Audit

Use when the user wants one narrow class of issues.

Examples:

- variable initialization only
- naming review only
- file I/O safety only
- commit control only

## Default Review Order

1. Identify source style: fixed-format, free-format, or mixed
2. Declarations and initialization
3. File access and status handling
4. Arithmetic and data conversion risks
5. Commit, rollback, and locking behavior
6. Naming and maintainability

## Style-Specific Routing

- If the member is fixed-format or mixed, read `fixed-format-rpgle.md` before finalizing findings.
- If the member relies on indicators, opcodes, or subroutines for control flow, review those paths before naming or style comments.

## Evidence Rules

- Cite the exact operation or declaration that triggered the finding.
- Prefer the smallest reliable fix.
- If context is missing, downgrade to `Open Risks` unless the defect is obvious from the code alone.
