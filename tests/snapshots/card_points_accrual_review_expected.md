### Findings

- `critical` [PNTPOST.RPGLE:13] Loyalty points are granted as soon as the transaction is seen, with no visible check that the card transaction reached an eligible posting or clearing state.
  Impact: the same spend can grant points before final posting or after later reversal, causing duplicate or premature reward accrual.
  Fix: award points only at the documented lifecycle stage and gate the write with posting-state validation.

- `medium` [PNTPOST.RPGLE:12] The deduplication path only checks whether `inTxnNo` exists in `PNTLED`, but does not show any idempotency scope for partial retries, replays, or multi-step posting events.
  Impact: retry behavior can still create inconsistent points history when the same business transaction is replayed in a different processing phase.
  Fix: use a business-stable idempotency key that matches the actual reward-grant event.

### Open Risks

- The snippet does not show transaction posting status or campaign eligibility fields, so full accrual-policy validation is partial.

### Summary

- 2 findings total: 1 critical, 1 medium.
- Highest risk theme: premature or duplicate points accrual.
