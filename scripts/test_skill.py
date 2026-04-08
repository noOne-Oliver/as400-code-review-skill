#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    sys.exit(1)


def ok(message: str) -> None:
    print(f"[OK] {message}")


def read(path: Path) -> str:
    if not path.exists():
        fail(f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"{label} missing: {needle}")


def assert_markdown_links_exist(path: Path) -> None:
    text = read(path)
    links = re.findall(r"\[[^\]]+\]\((\./[^)]+)\)", text)
    for link in links:
        target = (path.parent / link).resolve()
        if not target.exists():
            fail(f"Broken relative link in {path.name}: {link}")
    ok(f"{path.name} relative links resolve")


def assert_sections(text: str, label: str, sections: list[str]) -> None:
    for section in sections:
        assert_contains(text, section, label)
    ok(f"{label} contains required sections")


def main() -> None:
    skill = ROOT / "SKILL.md"
    readme = ROOT / "README.md"
    report = ROOT / "references" / "report-template.md"
    golden_findings = ROOT / "references" / "golden-findings.md"
    golden_cases = ROOT / "references" / "golden-cases.md"
    playbook = ROOT / "references" / "review-playbook.md"
    release_gate = ROOT / "references" / "release-gate.md"
    fixed_format = ROOT / "references" / "fixed-format-rpgle.md"
    anti_patterns = ROOT / "references" / "anti-patterns.md"
    notes = ROOT / "references" / "forward-test-notes.md"
    agents = ROOT / "agents" / "openai.yaml"
    release_notes = ROOT / "RELEASE_NOTES.md"
    snapshot_script = ROOT / "scripts" / "test_snapshots.py"
    examples_dir = ROOT / "examples"
    vendor_readme = ROOT / "vendor" / "README.md"
    vendor_validator = ROOT / "vendor" / "skill-creator" / "quick_validate.py"
    mixed_source = ROOT / "references" / "mixed-source-review.md"
    manifest = ROOT / "tests" / "snapshots" / "manifest.json"

    skill_text = read(skill)
    readme_text = read(readme)
    report_text = read(report)
    findings_text = read(golden_findings)
    cases_text = read(golden_cases)

    assert_sections(
        skill_text,
        "SKILL.md",
        [
            "## Review Modes",
            "## Required Workflow",
            "## Output Contract",
            "## Severity Rules",
            "## Prohibited Review Behaviors",
        ],
    )
    assert_sections(
        report_text,
        "report-template.md",
        ["### Findings", "### Open Risks", "### Release Gate", "### Summary"],
    )
    assert_sections(
        findings_text,
        "golden-findings.md",
        [
            "## Example 1: Uninitialized Numeric In Critical Path",
            "## Example 2: CHAIN Without Found Handling",
            "## Example 3: Weak Naming With Real Maintenance Risk",
            "## Example 4: Release Blocker On Commit Path",
            "## Example 5: Fixed-Format Indicator Leakage",
            "## Example 6: Mixed-Source Guard Lost At Style Boundary",
        ],
    )
    assert_sections(
        cases_text,
        "golden-cases.md",
        [
            "## Case 1: Order Query Program With Missing Found Check",
            "## Case 2: Customer Update Program With Ambiguous Flag And Partial Validation",
            "## Case 3: Settlement Batch Job With Commit Path But No Failure Handling",
            "## Case 4: Fixed-Format Order Update With Indicator Leakage",
            "## Case 5: Mixed-Source Member With Lost Not-Found Guard",
        ],
    )

    for path in [skill, readme]:
        assert_markdown_links_exist(path)

    for path in [
        playbook,
        release_gate,
        fixed_format,
        mixed_source,
        anti_patterns,
        notes,
        agents,
        release_notes,
        snapshot_script,
        vendor_readme,
        vendor_validator,
        manifest,
    ]:
        read(path)
    ok("required reference files exist")

    example_files = [
        examples_dir / "basic-review.md",
        examples_dir / "pre-release-gate.md",
        examples_dir / "focused-initialization-audit.md",
        examples_dir / "focused-file-and-commit-audit.md",
        examples_dir / "fixed-format-review.md",
        examples_dir / "mixed-source-review.md",
    ]
    for path in example_files:
        text = read(path)
        assert_contains(text, "Use $as400-code-review", path.name)
        assert_contains(text, "Code:", path.name)
    ok("example prompts exist and reference the skill")

    expected_case_sections = len(re.findall(r"## Case \d+:", cases_text))
    if expected_case_sections != 5:
        fail(f"Expected 5 golden cases, found {expected_case_sections}")
    for required in ["### Review Input", "### Expected Findings", "### Why This Case Matters"]:
        count = cases_text.count(required)
        if count != 5:
            fail(f"Expected '{required}' 5 times in golden-cases.md, found {count}")
    ok("golden cases structure is complete")

    if "critical [" not in findings_text or "medium [" not in findings_text:
        fail("golden-findings.md must include concrete critical and medium findings")
    ok("golden findings cover multiple severities")

    assert_contains(readme_text, "python3 scripts/test_skill.py", "README testing command")
    assert_contains(readme_text, "python3 scripts/test_snapshots.py", "README snapshot testing command")
    ok("README includes test command")

    release_notes_text = read(release_notes)
    assert_contains(release_notes_text, "## v2.2.0", "RELEASE_NOTES.md latest version section")
    assert_contains(release_notes_text, "## v2.1.0", "RELEASE_NOTES.md latest version section")
    assert_contains(release_notes_text, "## v2.0.0", "RELEASE_NOTES.md prior version section")
    assert_contains(release_notes_text, "./scripts/run_checks.sh", "RELEASE_NOTES.md validation command")
    ok("release notes contain expected release metadata")

    agents_text = read(agents)
    consistency_terms = [
        "fixed-format",
        "release",
        "risk",
    ]
    for term in consistency_terms:
        if term not in skill_text.lower():
            fail(f"SKILL.md missing consistency term: {term}")
        if term not in readme_text.lower():
            fail(f"README.md missing consistency term: {term}")
    if "mixed-source" not in skill_text.lower():
        fail("SKILL.md should mention mixed-source review")
    if "mixed-source" not in readme_text.lower():
        fail("README.md should mention mixed-source review")
    if "release readiness" not in agents_text.lower():
        fail("agents/openai.yaml should mention release readiness in its interface text")
    if "fixed-format" not in release_notes_text.lower():
        fail("RELEASE_NOTES.md should mention fixed-format coverage")
    if "snapshot" not in release_notes_text.lower():
        fail("RELEASE_NOTES.md should mention snapshot validation")
    ok("core metadata and docs are aligned on key capabilities")

    print("[PASS] skill regression checks passed")


if __name__ == "__main__":
    main()
