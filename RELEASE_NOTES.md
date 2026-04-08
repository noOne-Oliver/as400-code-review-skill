# Release Notes

## v2.2.0

This release hardens the repository as a maintainable product instead of only a content bundle.

### Highlights

- Added vendored validator support at `vendor/skill-creator/quick_validate.py`.
- Added CI in `.github/workflows/ci.yml` to run repository validation on push and pull request.
- Reworked `SKILL.md` workflow into explicit conditional routing instead of an implicit reading list.
- Added mixed-source review guidance, example prompt, and snapshot baseline:
  - `references/mixed-source-review.md`
  - `examples/mixed-source-review.md`
  - `tests/snapshots/mixed_source_review_*`
- Upgraded snapshot validation to use a manifest with finding-count, severity, and release-gate assertions.
- Clarified README installation semantics so the repository no longer implies a packaged `.skill` artifact exists.

### Why This Matters

- The repository is more self-contained and easier to validate on any machine.
- Mixed fixed/free IBM i members are now explicitly covered.
- Validation now protects not only structure, but also expected review behavior.

## v2.1.0

This release tightens repository portability, review calibration, and fixed-format RPGLE coverage.

### Highlights

- Added fixed-format RPGLE review guidance in `references/fixed-format-rpgle.md`.
- Added a fixed-format end-to-end review baseline to `golden-cases.md` and snapshot tests.
- Added copy-ready prompt examples in `examples/`, including a fixed-format review prompt.
- Improved `scripts/run_checks.sh` so validator lookup uses `CODEX_HOME` or `~/.codex` instead of a machine-specific absolute path.
- Strengthened `scripts/test_snapshots.py` with case-specific semantic anchors instead of structure-only checks.

### Why This Matters

- The repository is more portable across machines and contributors.
- Fixed-format and mixed-source IBM i members are now first-class review targets.
- Snapshot tests are better at catching accidental drift in expected findings.

### Validation

Run:

```bash
./scripts/run_checks.sh
```

## v2.0.0

This release upgrades the skill from a generic AS400/RPG checklist into a findings-first review workflow for IBM i code reviews and release gates.

### Highlights

- Reworked `SKILL.md` to focus on review modes, severity calibration, and prioritized findings.
- Added a dedicated review workflow with:
  - `review-playbook.md`
  - `release-gate.md`
  - `report-template.md`
- Added calibration material for consistent review quality:
  - `golden-findings.md`
  - `golden-cases.md`
  - `anti-patterns.md`
  - `forward-test-notes.md`
- Added Codex/UI metadata in `agents/openai.yaml`.
- Added local validation tooling:
  - `scripts/test_skill.py`
  - `scripts/test_snapshots.py`
  - `scripts/run_checks.sh`

### Why This Matters

- Review output is now findings-first instead of checklist-first.
- Severity is more consistent across correctness, naming, and release-gate issues.
- The skill now distinguishes confirmed defects from open risks when context is missing.
- The repository includes local regression checks so future edits are safer.

### Validation

Run:

```bash
./scripts/run_checks.sh
```

### Upgrade Notes

- Existing users should expect stricter review output with clearer blocker language.
- Pre-release /上线 reviews now explicitly produce a release decision section.
- Generic “looks good” responses are intentionally discouraged unless no concrete findings exist.
