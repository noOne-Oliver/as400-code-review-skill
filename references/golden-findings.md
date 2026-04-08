# Golden Findings

Use these examples to calibrate severity, wording, and fix recommendations. Prefer this style over generic checklist output.

## Example 1: Uninitialized Numeric In Critical Path

```text
critical [ORDPAY.RPGLE:42] Packed numeric `payAmt` is declared without `INZ` and is read before a guaranteed assignment.
Impact: payment calculations can use undefined data and write incorrect amounts to the order record.
Fix: initialize `payAmt` with `INZ(0)` or move the first assignment above every read path.
```

Why this is strong:

- Identifies the exact variable and where it matters.
- Explains concrete business impact.
- Recommends the smallest safe fix.

## Example 2: CHAIN Without Found Handling

```text
critical [ORDQRY.RPGLE:88] `CHAIN` to `ORDHDR` is followed by field access without a `%FOUND(ORDHDR)` guard.
Impact: the program can use stale or invalid field values on the not-found path and return incorrect results.
Fix: gate field access behind `%FOUND(ORDHDR)` and add an explicit not-found branch.
```

Why this is strong:

- Ties the finding to a specific file operation.
- Describes the incorrect runtime behavior instead of saying “best practice”.

## Example 3: Weak Naming With Real Maintenance Risk

```text
medium [CUSUPD.RPGLE:31] Variable `FLAG1` controls customer eligibility but its name does not indicate meaning or legal values.
Impact: later maintenance can apply the wrong branch logic or mis-handle status transitions.
Fix: rename it to a business-meaningful name such as `isEligible` or `custStatusFlg`, and document allowed values if it is not boolean.
```

Why this is strong:

- Keeps naming findings below correctness issues.
- Only escalates because the ambiguous name can drive wrong future changes.

## Example 4: Release Blocker On Commit Path

```text
critical [SETLJOB.RPGLE:120] Commit logic is present, but no rollback or failure-path behavior is visible for update errors.
Impact: partial settlement updates may persist without a verified recovery path.
Fix: add and test rollback handling for failed update or post-update validation paths before release.
```

Why this is strong:

- Appropriate for pre-release review.
- Explains why the issue blocks deployment rather than treating all COMMIT usage as equally risky.

## Example 5: Fixed-Format Indicator Leakage

```text
critical [ORDUPD.RPGLE:10] `UPDATE ORDHDR` runs outside the `*IN90 = *OFF` found-record branch after `CHAIN`.
Impact: the member can update with stale record state or on an invalid not-found path.
Fix: keep the entire update flow inside the found-record branch or exit immediately on indicator 90.
```

Why this is strong:

- It captures a fixed-format bug that a free-format-only review would often miss.
- It explains the indicator behavior in business terms rather than only citing legacy syntax.

## Example 6: Mixed-Source Guard Lost At Style Boundary

```text
critical [ORDMIX.RPGLE:8] Free-format logic reads `OHSTAT` after a fixed-format `CHAIN` without carrying the `*IN90` not-found guard across the style boundary.
Impact: the member can read stale or invalid record data when the order is not found.
Fix: keep the free-format branch inside an explicit found-record guard or exit immediately on `*IN90`.
```

Why this is strong:

- It catches a defect that exists at the seam between styles, not inside either style alone.
- It focuses on behavior leakage across the transition rather than generic modernization commentary.

## Example 7: Card Authorization Double Release Risk

```text
critical [AUTHRVS.RPGLE:12] Authorization reversal adds the held amount back to available credit without checking whether the authorization is already reversed or released.
Impact: repeated execution can overstate available credit and create a double-release defect.
Fix: make the reversal path idempotent and require a valid current hold state before releasing funds.
```

Why this is strong:

- It names the financial defect directly instead of describing it as a generic status bug.
- It matches a real card-business risk pattern where repeated reversal logic causes customer-visible balance errors.

## Example 8: Repayment Allocation Order Missing

```text
critical [CARDPAY.RPGLE:14] Repayment is applied directly to principal with no visible allocation order across fee, interest, and principal balances.
Impact: payoff behavior and outstanding balances can be wrong when business policy requires fees or interest to be paid first.
Fix: implement the required repayment allocation sequence before reducing principal.
```

Why this is strong:

- It elevates a business-policy omission to a correctness issue, not a style preference.
- It is specific enough to guide remediation without inventing a policy the code did not show.

## Example 9: Credit Limit Invariant Risk

```text
critical [LIMBATCH.RPGLE:13] The batch raises available and total credit limits together without a visible post-update invariant check.
Impact: the account can end up with an invalid available-credit state or exceed approved product limits.
Fix: validate product cap, outstanding exposure, and post-update limit invariants before updating the record.
```

Why this is strong:

- It frames the issue around financial invariants rather than just “missing validation”.
- It fits high-risk card operations where unit and exposure mistakes are business-critical.

## Example 10: Minimum Payment Formula Missing Required Buckets

```text
critical [STMTGEN.RPGLE:18] Minimum due `MNPMT` is calculated from principal only with no visible fee, interest, overdue, or over-limit components.
Impact: statements can show the wrong minimum payment and misstate customer delinquency obligations.
Fix: implement the documented minimum-payment formula using all required balance buckets and cycle rules.
```

Why this is strong:

- It treats statement math as a production correctness issue, not a reporting preference.
- It names the customer-visible defect directly, which makes triage easier for card teams.

## Example 11: Delinquency Status Cleared Too Early

```text
critical [DELINQ.RPGLE:16] Any positive payment clears delinquency status without checking whether overdue balances remain outstanding.
Impact: the account can return to a healthy status while still carrying delinquent debt, which breaks collections and aging logic.
Fix: clear delinquency only after overdue buckets are fully satisfied and the post-payment status is recomputed from remaining exposure.
```

Why this is strong:

- It connects status movement to financial truth instead of describing it as a generic flag problem.
- It highlights a common card-servicing defect where lifecycle state drifts away from balances.

## Example 12: Installment Closure Without Final Reconciliation

```text
critical [INSTCLS.RPGLE:20] Installment plan status is set to closed before remaining principal and fee balances are reconciled.
Impact: the plan can appear settled while residual receivables remain on the ledger.
Fix: recompute and validate residual principal, fee, and payoff amount before moving the plan to a closed status.
```

Why this is strong:

- It captures a high-risk closeout bug that generic RPG checks would miss.
- It anchors the finding in ledger consistency, which is what business owners care about.

## Example 13: Points Accrued Before Eligible Posting State

```text
critical [PNTPOST.RPGLE:17] Loyalty points are credited as soon as the transaction is seen, with no visible posting-state or idempotency check.
Impact: the same card transaction can grant points multiple times or grant points for transactions that later reverse.
Fix: award points only at the documented lifecycle stage and protect the path with a transaction-level idempotency key.
```

Why this is strong:

- It captures the core points-ledger defect directly: duplicate or premature accrual.
- It ties review severity to customer-visible reward inflation and reconciliation risk.

## Example 14: Refund Path Does Not Symmetrically Reverse Points

```text
critical [PNTRVS.RPGLE:19] Refund logic reverses transaction amount but does not verify how many points were previously granted before subtracting from available points.
Impact: points can remain overstated after refund, or the reversal can drive the points balance negative on repeated execution.
Fix: reconcile refund reversal against the original earned-points record and make the adjustment idempotent.
```

Why this is strong:

- It focuses on symmetry between spend and reward reversal, which is essential in card points systems.
- It avoids vague “missing validation” language and points to the original-transaction linkage that must exist.

## Example 15: Points Expiry Batch Expires The Wrong Buckets

```text
critical [PNTEXP.RPGLE:22] Expiry processing deducts from total points without distinguishing available, frozen, redeemed, or protected promotional buckets.
Impact: the batch can expire ineligible points and create customer-visible balance disputes.
Fix: expire only the eligible available bucket and enforce bucket-level rules before updating balances.
```

Why this is strong:

- It turns a subtle accounting rule into a crisp invariant the reviewer can enforce.
- It matches a common reward-system production defect that generic AS400 review would not catch.
