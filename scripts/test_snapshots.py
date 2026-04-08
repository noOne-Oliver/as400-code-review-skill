#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOTS = ROOT / "tests" / "snapshots"
MANIFEST = SNAPSHOTS / "manifest.json"


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
    if needle.lower() not in text.lower():
        fail(f"{label} missing expected token: {needle}")


def count_findings(text: str) -> int:
    return len(re.findall(r"^- `(?:critical|medium|info)`", text, re.MULTILINE))


def count_severity(text: str, severity: str) -> int:
    return len(re.findall(rf"^- `{severity}`", text, re.MULTILINE))


def main() -> None:
    manifest = json.loads(read(MANIFEST))
    cases = manifest.get("cases", [])
    if not cases:
        fail("manifest.json must define snapshot cases")

    for case in cases:
        input_name = case["input"]
        expected_name = case["expected"]
        input_path = SNAPSHOTS / input_name
        expected_path = SNAPSHOTS / expected_name
        input_text = read(input_path)
        expected_text = read(expected_path)

        if "```rpgle" not in input_text:
            fail(f"{input_name} must include an RPGLE code block")
        if "### Findings" not in expected_text:
            fail(f"{expected_name} must include a Findings section")
        if "### Summary" not in expected_text:
            fail(f"{expected_name} must include a Summary section")
        if "Impact:" not in expected_text or "Fix:" not in expected_text:
            fail(f"{expected_name} must include Impact and Fix lines")

        for token in case["input_tokens"]:
            assert_contains(input_text, token, input_name)
        for token in case["expected_tokens"]:
            assert_contains(expected_text, token, expected_name)

        if count_findings(expected_text) != case["findings"]:
            fail(f"{expected_name} expected {case['findings']} findings")

        for severity, expected_count in case["severity_counts"].items():
            if count_severity(expected_text, severity) != expected_count:
                fail(
                    f"{expected_name} expected {expected_count} '{severity}' findings"
                )

        if case["release_gate_required"]:
            if "### Release Gate" not in expected_text:
                fail(f"{expected_name} must include a Release Gate section")
            if expected_text.count("### Release Gate") != 1:
                fail(f"{expected_name} must include exactly one Release Gate section")
            assert_contains(expected_text, case["release_gate_value"], expected_name)
        else:
            if "### Release Gate" in expected_text:
                fail(f"{expected_name} should not include a Release Gate section")

        ok(f"{input_name} -> {expected_name} snapshot structure and anchors look valid")

    print("[PASS] snapshot checks passed")


if __name__ == "__main__":
    main()
