### Findings

- `critical` [CARDPAY.RPGLE:14] Repayment is applied directly to principal `ACPRIN` without any visible allocation order across fee, interest, and principal buckets.
  Impact: outstanding balances and customer payoff behavior can be wrong if business policy requires fees or interest to be paid first.
  Fix: implement and document the required repayment allocation sequence before reducing principal.

- `medium` [CARDPAY.RPGLE:13] Positive-amount validation exists, but there is no visible protection against repayment amounts that exceed the remaining principal or total outstanding balance.
  Impact: over-allocation can drive balances negative or hide upstream settlement errors.
  Fix: cap allocation against outstanding components and route excess amounts to a controlled overpayment or rejection path.

### Open Risks

- The snippet does not show fee, interest, or delinquency fields, so full allocation-policy validation is partial.

### Summary

- 2 findings total: 1 critical, 1 medium.
- Highest risk theme: incomplete repayment allocation policy.
