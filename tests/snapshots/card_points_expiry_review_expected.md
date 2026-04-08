### Findings

- `critical` [PNTEXP.RPGLE:14] Expiry processing deducts from total points `PTOTAL` rather than an explicitly eligible available bucket.
  Impact: the batch can expire frozen, redeemed-tracking, or protected promotional points and create customer-visible balance disputes.
  Fix: expire only the eligible available bucket and enforce bucket-level expiry rules before update.

- `medium` [PNTEXP.RPGLE:15] `wsExpCnt` is incremented after the update with no visible exception handling or audit of which bucket was expired.
  Impact: expiry reporting can overstate success and make disputes difficult to trace when individual updates fail or hit the wrong bucket.
  Fix: record the expired bucket decision and check update success before counting the account as processed.

### Open Risks

- The snippet does not show available, frozen, or campaign-protected point buckets, so the exact expiry scope is only partially visible.

### Summary

- 2 findings total: 1 critical, 1 medium.
- Highest risk theme: expiry targets the wrong loyalty-point bucket.
