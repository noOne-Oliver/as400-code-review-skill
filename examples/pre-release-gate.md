# Pre-Release Gate Prompt

Use this before deployment or上线 when you want blocker language, not just general review comments.

```text
Use $as400-code-review in pre-release-gate mode for this IBM i batch/update change.

Check specifically:
- commit and rollback behavior
- update failure handling
- lock and concurrency risks
- release blockers before production

Return:
1. Findings
2. Open Risks
3. Release Gate
4. Summary

Code:
[paste RPG/RPGLE code here]
```
