# Mixed-Source Review Prompt

Use this when the member mixes fixed-format and free-format logic.

```text
Use $as400-code-review to review this mixed-source IBM i RPG/RPGLE member.

Focus on:
- behavior at the fixed/free boundary
- indicator state leaking across style transitions
- file-status handling across both styles
- arithmetic or move semantics that become unsafe after the transition

Return:
1. Findings
2. Open Risks
3. Summary

Code:
[paste mixed fixed/free RPG/RPGLE code here]
```
