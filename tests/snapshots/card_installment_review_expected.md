### Findings

- `critical` [INSTCLS.RPGLE:14] Installment plan status is set to closed when `inCloseAmt` covers only remaining principal `INREMN`, with no visible reconciliation of residual fees, payoff adjustments, or pending accruals.
  Impact: the installment plan can appear settled while receivable components still remain on the ledger.
  Fix: validate residual principal, fee, and payoff balances before moving the installment plan to closed status.

- `medium` [INSTCLS.RPGLE:15] The close path updates plan status immediately with no visible post-close consistency check or exception handling.
  Impact: downstream servicing can treat the plan as closed even if final settlement posting fails or residual balances remain.
  Fix: add a post-close validation path and fail the status change when final reconciliation does not succeed.

### Open Risks

- The snippet does not show payoff fee, accrued interest, or residual adjustment fields, so full installment settlement validation is partial.

### Summary

- 2 findings total: 1 critical, 1 medium.
- Highest risk theme: installment closure is not reconciled to final ledger state.
