### Findings

- `critical` [PNTRVS.RPGLE:13] Refund reversal subtracts points from `PAVAIL` using only refund amount, with no visible reconciliation to the points originally granted for the refunded transaction.
  Impact: points can remain overstated after refund or become negative if the same refund reversal runs more than once.
  Fix: link refund reversal to the original earned-points record and reverse only the confirmed granted amount once.

- `medium` [PNTRVS.RPGLE:14] The points balance is updated directly with no visible floor check or protected-bucket handling.
  Impact: refunds can push the available-points balance negative or consume points that should not be reversed automatically.
  Fix: validate available and protected point buckets before applying the reversal.

### Open Risks

- The snippet does not show campaign-protected or already-redeemed points, so the full reversal policy is only partially visible.

### Summary

- 2 findings total: 1 critical, 1 medium.
- Highest risk theme: refund reversal is not reconciled to original earned points.
