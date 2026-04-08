# Card Domain Review Guide

Use this reference when reviewing credit card or consumer card business logic on IBM i.

## Domain Priorities

In card systems, review business correctness before code elegance. Small logic mistakes can create financial loss, reconciliation breaks, customer-visible balance errors, or regulatory exposure.

Prioritize these business paths:

- authorization and reversal
- repayment allocation
- statement and minimum-payment computation
- credit-limit and available-balance movement
- fees, interest, and status transitions
- delinquency aging and collections status movement
- installment booking, payoff, and closure
- loyalty-point accrual, reversal, and expiry

## High-Risk Patterns

### Authorization And Reversal

- Verify reversal and release paths are idempotent.
- Flag logic that can release the same authorization twice.
- Flag updates to available balance without a matching hold-state transition.
- Verify that not-found or already-reversed paths do not silently continue.

### Repayment Allocation

- Verify allocation order is explicit and matches business policy.
- Flag repayment logic that applies to principal before fee or interest when policy requires the opposite.
- Flag negative or over-allocation paths that can double-reduce outstanding balances.
- Treat rounding and unit conversion errors as correctness issues, not style issues.

### Limit And Balance Management

- Verify whether amounts are stored in cents, yuan, or mixed units.
- Flag available-limit updates that do not also protect total limit or outstanding balance invariants.
- Flag batch limit jobs that continue after failed updates but still accumulate success counts.

### Statement And Billing

- Verify cutoff, due-date, and minimum-payment logic with explicit business branches.
- Flag use of unvalidated status codes in billing decisions.
- Flag paths where fee, interest, and principal are rolled up without a documented ordering rule.
- Flag minimum-payment calculations that omit fee, interest, overdue, or over-limit components.

### Delinquency And Status Movement

- Verify that overdue or delinquent status is cleared only after all required overdue buckets are satisfied.
- Flag logic that downgrades collection status on any positive payment without checking remaining delinquent balance.
- Treat bucket-aging transitions as correctness logic, not reporting logic.

### Installment And Loan-Like Card Features

- Verify installment closure only after remaining principal, fee, and residual adjustments are reconciled.
- Flag status transitions that close a plan before final ledger movement is validated.
- Verify payoff, foreclosure, and reversal paths are idempotent and ledger-consistent.

### Loyalty Points

- Verify whether points are granted on authorization, clearing, billing, or posting completion.
- Flag point accrual logic without transaction idempotency or posting-state validation.
- Flag refund, reversal, or chargeback paths that do not symmetrically reverse previously granted points.
- Verify expiry jobs distinguish available, frozen, redeemed, and protected promotional points.

## Domain Questions To Resolve Early

If code context is incomplete, try to answer these before finalizing severity:

- Are amounts stored in cents, fen, yuan, or mixed units?
- What is the repayment bucket order: fee, interest, overdue principal, current principal, or another contract?
- Which statuses are terminal, reversible, or retryable?
- Which object owns the source of truth for available credit, held funds, and billed balances?
- What is the authoritative minimum-payment formula?
- Does the flow require idempotency by request number, authorization number, statement cycle, or posting sequence?
- Are loyalty points earned on auth, posting, settlement, bill generation, or another lifecycle stage?
- Which point buckets exist: available, pending, frozen, redeemed, expired, campaign-protected?

## Business Invariants Worth Naming Explicitly

When these are violated, call them out directly in findings:

- available credit must not exceed approved limit or ignore held / outstanding exposure
- repayment must not reduce a lower-priority bucket before higher-priority debt is satisfied
- statement due and minimum due must remain derivable from documented buckets
- delinquency status must reflect remaining overdue exposure, not merely payment presence
- installment closure must not leave residual principal, fee, or status mismatch
- point accrual must happen once per eligible transaction lifecycle event
- point reversal and expiry must not drive available points negative or touch protected buckets

## Output Notes

- Name the financial effect in the impact line: double release, incorrect outstanding balance, wrong minimum due, unsafe limit increase, and similar.
- Prefer the smallest safe fix, but never understate data-integrity or customer-impact risk.
