# Focused File And Commit Audit Prompt

Use this when the main risk is file status handling, transaction safety, or batch update correctness.

```text
Use $as400-code-review in focused-audit mode.

Audit only:
- CHAIN/READ/READE/SETLL/UPDATE/WRITE/DELETE status handling
- %FOUND/%EOF/%ERROR coverage
- commit and rollback safety
- batch loop correctness

Treat naming and formatting as secondary unless they affect branch meaning.

Return:
1. Findings
2. Open Risks
3. Summary

Code:
[paste RPG/RPGLE code here]
```
