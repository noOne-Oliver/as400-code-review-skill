# Basic Review Prompt

Use this when you want a normal code review on one or more RPG/RPGLE members.

```text
Use $as400-code-review to review this IBM i RPGLE change.

Focus on:
- runtime correctness
- file I/O safety
- variable initialization
- naming only when it creates maintenance risk

Return:
1. Findings
2. Open Risks
3. Summary

Code:
[paste RPG/RPGLE code here]
```
