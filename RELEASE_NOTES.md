# Release Notes

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
