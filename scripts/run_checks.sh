#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

VALIDATOR_VENDOR="$ROOT/vendor/skill-creator/quick_validate.py"
VALIDATOR_CODEX="${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py"

if [[ -f "$VALIDATOR_VENDOR" ]]; then
  VALIDATOR="$VALIDATOR_VENDOR"
else
  VALIDATOR="$VALIDATOR_CODEX"
fi

if [[ ! -f "$VALIDATOR" ]]; then
  echo "[FAIL] quick_validate.py not found at: $VALIDATOR" >&2
  echo "Set CODEX_HOME, install the skill-creator system skill, or vendor the validator at vendor/skill-creator/quick_validate.py." >&2
  exit 1
fi

python3 "$VALIDATOR" "$ROOT"
python3 "$ROOT/scripts/test_skill.py"
python3 "$ROOT/scripts/test_snapshots.py"
