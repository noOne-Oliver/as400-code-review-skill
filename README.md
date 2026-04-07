# AS400 Code Review Skill

Structured review skill for IBM i / AS400 RPG and RPGLE code.

## Overview

This skill provides a findings-first review workflow for AS400/RPG applications, focusing on:

- **Variable Initialization** - Prevent random values and data corruption
- **Variable Naming** - Ensure clarity and maintainability
- **Common RPG Pitfalls** - Catch frequent bugs before production
- **AS400-Specific Checks** - Object locks, commitment control, job queues
- **Release Gate Reviews** - Pre-production blocker assessment for上线场景
- **Severity Calibration** - Consistent distinction between confirmed defects, open risks, and release blockers

## Usage

Use when reviewing AS400/RPG code, local patches, or pre-release IBM i changes:

```
$as400-code-review
```

## Validation

Run the local regression checks before publishing changes:

```bash
python3 scripts/test_skill.py
python3 scripts/test_snapshots.py
```

Or run the full validation bundle:

```bash
./scripts/run_checks.sh
```

## Release Notes

Current release notes live in [`RELEASE_NOTES.md`](./RELEASE_NOTES.md).

## Contents

```
├── SKILL.md                           # Main skill file
├── RELEASE_NOTES.md                   # Current release summary
├── scripts/
│   ├── test_skill.py                  # Structural regression checks
│   ├── test_snapshots.py              # Snapshot-style output checks
│   └── run_checks.sh                  # Full local validation runner
├── tests/
│   └── snapshots/                     # Example input/output review baselines
└── references/
    ├── review-playbook.md             # Review mode selection and workflow
    ├── release-gate.md                # Production readiness gate
    ├── golden-findings.md             # Example findings and severity calibration
    ├── golden-cases.md                # Realistic end-to-end review examples
    ├── anti-patterns.md               # Low-value review behaviors to avoid
    ├── forward-test-notes.md          # Known review drift patterns
    ├── report-template.md             # Stable findings-first output format
    ├── rpg-variables.md              # Variable definition reference
    └── rpg-best-practices.md          # RPG best practices guide
```

## Check Categories

### 1. Variable Initialization Issues
- Numeric variables without INZ
- Character variables defaulting to spaces
- Pointers not nullified
- DataStructure subfields missing initialization
- Arrays retaining old values

### 2. Variable Naming Issues
- TMP1/TMP2 garbage names
- Misleading variable names
- Missing unit annotations
- Magic numbers
- FLAG confusion (0/1 vs A/B)

### 3. Common RPG Pitfalls
- Division by zero
- CHAIN without %FOUND
- SETLL without %EQUAL
- MOVE vs EVAL behavior
- DS size mismatches

### 4. AS400-Specific Checks
- Object locks (WRKOBJLCK)
- Job queue backup
- COMMIT/ROLLBACK testing
- Change log configuration
- Memory/cursor leaks

### 5. Review Output
- Findings ordered by severity
- Separate open risks when context is incomplete
- Optional release decision for上线/production reviews

## For OpenClaw Users

This skill is designed for Codex/OpenClaw-style skill invocation. Install using:

```bash
openclaw skills install as400-code-review.skill
```

## License

MIT
