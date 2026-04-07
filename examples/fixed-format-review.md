# Fixed-Format Review Prompt

Use this when the code is old-style fixed-format RPG or mixed fixed/free source.

```text
Use $as400-code-review to review this fixed-format RPG/RPGLE member.

Focus on:
- indicator-driven logic
- CHAIN/READ/UPDATE status handling
- MOVE/MOVEL/Z-ADD/DIV behavior
- column-sensitive fixed-format risks

Treat free-format advice as secondary unless the member mixes styles.

Return:
1. Findings
2. Open Risks
3. Summary

Code:
[paste fixed-format RPG/RPGLE code here]
```
