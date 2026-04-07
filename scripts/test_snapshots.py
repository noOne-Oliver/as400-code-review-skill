#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOTS = ROOT / "tests" / "snapshots"


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    sys.exit(1)


def ok(message: str) -> None:
    print(f"[OK] {message}")


def read(path: Path) -> str:
    if not path.exists():
        fail(f"Missing file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    pairs = [
        ("query_review_input.md", "query_review_expected.md"),
        ("update_review_input.md", "update_review_expected.md"),
        ("release_gate_input.md", "release_gate_expected.md"),
    ]

    for input_name, expected_name in pairs:
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

        if "release_gate" in expected_name:
            if "### Release Gate" not in expected_text or "`blocked`" not in expected_text:
                fail(f"{expected_name} must include a blocked release decision")
        else:
            if "### Release Gate" in expected_text:
                fail(f"{expected_name} should not include a Release Gate section")

        ok(f"{input_name} -> {expected_name} snapshot structure looks valid")

    print("[PASS] snapshot checks passed")


if __name__ == "__main__":
    main()
