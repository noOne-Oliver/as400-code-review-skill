# Focused Initialization Audit Prompt

Use this when you only want initialization and declaration issues.

```text
Use $as400-code-review in focused-audit mode.

Audit only:
- numeric variables without guaranteed initialization
- pointers not initialized to *NULL
- DS and array initialization risks
- variables read before assignment

Do not spend time on naming, style, or release checks unless they directly affect correctness.

Return:
1. Findings
2. Open Risks
3. Summary

Code:
[paste RPG/RPGLE code here]
```
