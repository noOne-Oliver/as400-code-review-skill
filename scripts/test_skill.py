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
    anti_patterns = ROOT / "references" / "anti-patterns.md"
    notes = ROOT / "references" / "forward-test-notes.md"
    agents = ROOT / "agents" / "openai.yaml"
    release_notes = ROOT / "RELEASE_NOTES.md"
    snapshot_script = ROOT / "scripts" / "test_snapshots.py"

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
        ],
    )
    assert_sections(
        cases_text,
        "golden-cases.md",
        [
            "## Case 1: Order Query Program With Missing Found Check",
            "## Case 2: Customer Update Program With Ambiguous Flag And Partial Validation",
            "## Case 3: Settlement Batch Job With Commit Path But No Failure Handling",
        ],
    )

    for path in [skill, readme]:
        assert_markdown_links_exist(path)

    for path in [playbook, release_gate, anti_patterns, notes, agents, release_notes, snapshot_script]:
        read(path)
    ok("required reference files exist")

    expected_case_sections = len(re.findall(r"## Case \d+:", cases_text))
    if expected_case_sections != 3:
        fail(f"Expected 3 golden cases, found {expected_case_sections}")
    for required in ["### Review Input", "### Expected Findings", "### Why This Case Matters"]:
        count = cases_text.count(required)
        if count != 3:
            fail(f"Expected '{required}' 3 times in golden-cases.md, found {count}")
    ok("golden cases structure is complete")

    if "critical [" not in findings_text or "medium [" not in findings_text:
        fail("golden-findings.md must include concrete critical and medium findings")
    ok("golden findings cover multiple severities")

    assert_contains(readme_text, "python3 scripts/test_skill.py", "README testing command")
    assert_contains(readme_text, "python3 scripts/test_snapshots.py", "README snapshot testing command")
    ok("README includes test command")

    release_notes_text = read(release_notes)
    assert_contains(release_notes_text, "## v2.0.0", "RELEASE_NOTES.md version section")
    assert_contains(release_notes_text, "./scripts/run_checks.sh", "RELEASE_NOTES.md validation command")
    ok("release notes contain expected release metadata")

    print("[PASS] skill regression checks passed")


if __name__ == "__main__":
    main()
