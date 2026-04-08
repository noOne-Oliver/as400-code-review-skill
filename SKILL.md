---
name: as400-code-review
description: Review IBM i / AS400 RPG and RPGLE code for correctness, production risk, and maintainability. Use when Codex needs to audit AS400 source before merge or release, find bugs in variable initialization and file I/O, verify naming and status-handling rules, apply AS400-specific quality gates, or produce a prioritized review report with must-fix findings and deployment checks.
---

# AS400 Code Review

Use this skill for review, not generation. The primary goal is to surface concrete defects and release risks in AS400 / RPG code with a report that a developer or release owner can act on immediately.

Prioritize in this order:

1. Runtime and data-integrity bugs
2. Incorrect or unverifiable file and field usage
3. Transaction, locking, and release-readiness risks
4. Maintainability and naming issues

## Review Modes

Classify the task before reviewing:

- `code-review`: review one or more source members and report findings
- `pre-release-gate`: apply the release checklist and call out blockers
- `focused-audit`: inspect only a specific class of risks such as initialization, naming, commit handling, or file operations

If the user does not specify a mode, default to `code-review`.

## Required Workflow

Follow this route instead of loading every reference by default:

1. Identify the review scope: files, member type, and requested focus.
2. Identify source style: fixed-format, free-format, or mixed.
3. Read [references/review-playbook.md](./references/review-playbook.md) first.
4. Route by task:
   - `code-review` + free-format: read [references/rpg-best-practices.md](./references/rpg-best-practices.md) and [references/report-template.md](./references/report-template.md)
   - `code-review` + fixed-format: read [references/fixed-format-rpgle.md](./references/fixed-format-rpgle.md) and [references/report-template.md](./references/report-template.md)
   - `code-review` + mixed: read [references/fixed-format-rpgle.md](./references/fixed-format-rpgle.md), [references/mixed-source-review.md](./references/mixed-source-review.md), and [references/report-template.md](./references/report-template.md)
   - `focused-audit`: add only the domain reference you need, such as [references/rpg-variables.md](./references/rpg-variables.md) for initialization, [references/rpg-best-practices.md](./references/rpg-best-practices.md) for file and transaction review, or [references/card-domain-review.md](./references/card-domain-review.md) for card business logic
   - `pre-release-gate`: also read [references/release-gate.md](./references/release-gate.md)
5. Only if severity or wording is still ambiguous, read [references/golden-findings.md](./references/golden-findings.md) or [references/golden-cases.md](./references/golden-cases.md).
6. Produce findings first. Keep summaries secondary.

Do not produce a generic “looks good” checklist when concrete findings can be made.

## Core Review Rules

- Findings must be specific and actionable. Name the object, operation, and likely impact.
- Prefer evidence from the code over generic RPG advice.
- Treat missing `%FOUND`, `%EOF`, `%ERROR`, divide-by-zero guards, lock handling, and commit/rollback verification as higher priority than naming style.
- For fixed-format members, treat indicator leakage, opcode semantics, and found/not-found branch scope as first-class correctness risks.
- For mixed-source members, treat the fixed/free boundary itself as a risk surface and verify that protections carry across it explicitly.
- For card-domain members, treat balance movement, allocation order, statement/minimum-due formulas, delinquency aging, limit invariants, installment closure, loyalty-point lifecycle rules, and reversal idempotency as first-class correctness risks.
- Separate verified issues from potential risks when surrounding context is incomplete.
- If file definitions or field semantics are unavailable, say validation is partial rather than guessing.
- Treat release-readiness items as blockers only when the task is a pre-release or production gate review.
- Use `Open Risks` for concerns that depend on missing DDS, compile settings, object definitions, or runtime operations evidence.

## AS400 Risk Priorities

Escalate these quickly:

- uninitialized numeric, pointer, DS, or reused array state
- CHAIN, READ, READE, SETLL, SETGT, UPDATE, WRITE, DELETE paths without status handling
- fixed-format indicator state that leaks beyond the intended branch
- MOVE, MOVEL, Z-ADD, DIV, and legacy opcodes with unsafe truncation or arithmetic assumptions
- commit logic without rollback or failure-path verification
- object locking, timeout, or concurrent job risks
- DS layout or field-width mismatch
- arithmetic that can overflow or divide by zero
- misleading variable names that are likely to cause incorrect maintenance changes
- card balance or limit updates that can overstate available credit, understate outstanding debt, or break business allocation rules
- statement or minimum-due calculations that silently omit required debt buckets
- delinquency or installment status transitions that can desynchronize business status from financial balances
- loyalty-point accrual, reversal, or expiry logic that can double-credit, miss reversal, or expire the wrong bucket

## Output Contract

Use this order unless the user explicitly asks for a different format.

### Findings

- List findings first, ordered by severity.
- Each finding should include:
  - severity: `critical`, `medium`, or `info`
  - location: file/member and line if available
  - issue: what is wrong
  - impact: likely runtime or business effect
  - fix: the smallest safe correction

### Open Risks

- List risks that could not be fully verified because definitions, compile settings, or runtime context are missing.

### Release Gate

- Include this section only for pre-release or上线 reviews.
- State whether the code is `blocked`, `needs follow-up`, or `ready with noted risks`.

### Summary

- Keep this short.
- Report total findings by severity and the dominant risk theme.

## Severity Rules

- `critical`: can cause wrong data, crashes, failed transactions, broken file handling, or unsafe release
- `medium`: can cause incorrect behavior in non-catastrophic paths, maintainability traps, or production fragility
- `info`: worthwhile cleanup or convention issues that are not immediate release blockers

Use these tie-breakers:

- Missing initialization is `critical` only when the value is used before guaranteed assignment or sits on a sensitive business path.
- Naming issues are usually `info` unless they create a realistic maintenance or branching mistake.
- Release blockers should appear only in `pre-release-gate` mode or when the user explicitly asks about deployment safety.

## Prohibited Review Behaviors

- Do not lead with a checklist when you have concrete findings.
- Do not mix confirmed defects with stylistic preferences.
- Do not label something a blocker without explaining the failure mode.
- Do not recommend broad rewrites when a localized fix is safer.
- Do not assume external object definitions that were not provided.
- Do not drift into low-signal review behavior listed in [references/anti-patterns.md](./references/anti-patterns.md).

## Reference Usage

- Read [references/review-playbook.md](./references/review-playbook.md) first.
- Read [references/rpg-variables.md](./references/rpg-variables.md) for declaration and initialization issues.
- Read [references/rpg-best-practices.md](./references/rpg-best-practices.md) for control-flow, file, and transaction issues.
- Read [references/fixed-format-rpgle.md](./references/fixed-format-rpgle.md) for fixed-format and mixed-source review.
- Read [references/mixed-source-review.md](./references/mixed-source-review.md) when fixed and free logic coexist in one member.
- Read [references/card-domain-review.md](./references/card-domain-review.md) for card authorization, reversal, repayment, statement, and limit logic.
- Read [references/release-gate.md](./references/release-gate.md) for上线 or production-gate reviews.
- Read [references/golden-findings.md](./references/golden-findings.md) to calibrate finding quality.
- Read [references/golden-cases.md](./references/golden-cases.md) for realistic end-to-end review examples.
- Read [references/anti-patterns.md](./references/anti-patterns.md) to avoid low-value review output.
- Read [references/forward-test-notes.md](./references/forward-test-notes.md) for known review drift.
- Read [references/report-template.md](./references/report-template.md) to keep the review output stable.

Load only the references needed for the current review.
