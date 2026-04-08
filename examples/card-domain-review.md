# Card Domain Review Prompt

Use this when the code belongs to a credit-card or consumer-card business flow.

```text
Use $as400-code-review to review this card-domain IBM i RPG/RPGLE change.

Focus on:
- authorization and reversal correctness
- repayment allocation order
- available-limit and total-limit integrity
- statement, fee, and minimum-payment business rules
- delinquency status movement after payment
- installment payoff / closure consistency
- loyalty-point accrual, reversal, and expiry correctness

Treat financial correctness and customer-impact risk as higher priority than naming or formatting.

Return:
1. Findings
2. Open Risks
3. Summary

Code:
[paste RPG/RPGLE code here]
```
