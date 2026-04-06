#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

python3 /Users/liujie/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$ROOT"
python3 "$ROOT/scripts/test_skill.py"
