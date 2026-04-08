### Findings

- `critical` [STMTGEN.RPGLE:12] Minimum payment `MNPMT` is derived only from principal `STPRIN` with no visible fee, interest, overdue, or over-limit components.
  Impact: statement output can show the wrong minimum payment and understate the customer's required payment.
  Fix: implement the documented minimum-payment formula using all required debt buckets and cycle rules.

- `medium` [STMTGEN.RPGLE:13] The statement update path does not show any validation that the computed minimum due is bounded by total outstanding amount or product floor rules.
  Impact: minimum due can be internally inconsistent with billed balances if formula inputs or rounding rules are wrong.
  Fix: validate the computed value against outstanding totals and documented minimum-payment constraints before update.

### Open Risks

- The snippet does not show cycle-level fee, interest, overdue, or over-limit fields, so full minimum-due verification is partial.

### Summary

- 2 findings total: 1 critical, 1 medium.
- Highest risk theme: incorrect minimum payment and unsafe statement math.
