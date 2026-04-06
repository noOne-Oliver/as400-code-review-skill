# Review Anti-Patterns

Use this file to avoid low-value review behavior.

## Output Anti-Patterns

- Do not produce a long checklist when two or three concrete findings would be more useful.
- Do not hide the most severe issue under a broad summary.
- Do not end with “looks good overall” when unresolved critical risks remain.

## Reasoning Anti-Patterns

- Do not cite general RPG advice without tying it to a specific line, object, or operation.
- Do not escalate naming or style problems above real runtime defects.
- Do not call something a blocker unless you explain the release failure mode.
- Do not recommend a rewrite when a local fix is clearly safer.

## Evidence Anti-Patterns

- Do not claim a field, record format, or DDS mismatch unless the code or supplied definitions support it.
- Do not present missing context as a confirmed bug; move it to `Open Risks`.
- Do not infer rollback coverage, lock handling, or compile safety from intent alone.

## Severity Anti-Patterns

- Do not label every missing `INZ` as `critical`; only do so when the variable is used before guaranteed assignment or sits on a sensitive path.
- Do not label every naming issue as `medium`; many should be `info` unless they create maintenance risk.
- Do not treat release checklist items as blockers during a normal code review unless the user asked for release readiness.
