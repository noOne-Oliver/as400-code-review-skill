# Golden Review Cases

Use these cases to calibrate how the skill should review realistic AS400 code. Each case includes a representative code snippet, the expected findings, and the reasoning behind the severity.

## Case 1: Order Query Program With Missing Found Check

### Review Input

```rpgle
**FREE

ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-f ORDHDR keyed usage(*input) extfile('ORDHDR');

dcl-pi *n;
  inOrderNo char(10);
  outCustNo char(10);
  outStat char(1);
end-pi;

dcl-s wsAmt packed(9:2);

chain inOrderNo ORDHDR;
outCustNo = OHCUST;
outStat = OHSTAT;

if wsAmt > 0;
  outStat = 'A';
endif;

return;
```

### Expected Findings

- `critical` [ORDQRY.RPGLE:14] `CHAIN` to `ORDHDR` is followed by field access without a `%FOUND(ORDHDR)` guard.
  Impact: the program can return stale or invalid customer and status data when the order is not found.
  Fix: add a `%FOUND(ORDHDR)` check before reading `OHCUST` and `OHSTAT`, and define an explicit not-found path.

- `medium` [ORDQRY.RPGLE:12] Packed variable `wsAmt` has no initialization and is read in a branch condition without a guaranteed assignment.
  Impact: the branch can evaluate on undefined data and set an incorrect output status.
  Fix: initialize `wsAmt` with `INZ(0)` or assign it before the first comparison.

### Why This Case Matters

- It combines two very common RPG review failures: unsafe `CHAIN` handling and undefined numeric state.
- The findings should focus on correctness first, not formatting or naming.

## Case 2: Customer Update Program With Ambiguous Flag And Partial Validation

### Review Input

```rpgle
**FREE

ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-f CUSHDR keyed usage(*update) extfile('CUSHDR');

dcl-pi *n;
  inCustNo char(10);
  inLevel char(2);
end-pi;

dcl-s FLAG1 char(1) inz(*blanks);

chain inCustNo CUSHDR;
if %found(CUSHDR);
  if FLAG1 = 'Y';
    CULEVL = inLevel;
    update CUSHDRR;
  endif;
endif;

return;
```

### Expected Findings

- `medium` [CUSUPD.RPGLE:12] Variable `FLAG1` controls whether the customer level is updated, but its meaning and allowed values are not clear.
  Impact: future maintenance can apply the update branch incorrectly because the variable name does not convey business meaning.
  Fix: rename `FLAG1` to a business-specific name such as `isLevelUpdateAllowed` or document its legal values if renaming is not feasible.

- `medium` [CUSUPD.RPGLE:16] The update path has no visible validation for blank or invalid `inLevel` before writing `CULEVL`.
  Impact: invalid customer level values may be persisted if upstream validation is missing.
  Fix: validate `inLevel` before `update CUSHDRR` and reject blank or unsupported values explicitly.

### Why This Case Matters

- It shows that naming findings belong below hard runtime defects, but still matter when they influence branching logic.
- It also demonstrates how to report a likely business-rule hole without pretending to know external validation rules.

## Case 3: Settlement Batch Job With Commit Path But No Failure Handling

### Review Input

```rpgle
**FREE

ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-f SETLHDR usage(*update) keyed extfile('SETLHDR');

dcl-s wsCnt packed(7:0) inz(0);

setll *loval SETLHDR;
read SETLHDR;
dow not %eof(SETLHDR);
  if SHSTAT = 'P';
    SHSTAT = 'C';
    update SETLHDRR;
    wsCnt += 1;
  endif;

  read SETLHDR;
enddo;

commit;
return;
```

### Expected Findings

- `critical` [SETLJOB.RPGLE:19] `COMMIT` is executed, but no rollback or failure-path handling is visible for update errors in the batch loop.
  Impact: partial settlement updates can persist without a verified recovery path if one update fails or downstream checks fail.
  Fix: add rollback handling and failure-path verification for update errors before allowing release.

- `medium` [SETLJOB.RPGLE:13] `update SETLHDRR` has no visible `%ERROR` or equivalent failure handling.
  Impact: update failures may be missed and the job can continue with an incorrect success count.
  Fix: check the update result and route failures to an explicit error path before incrementing `wsCnt`.

### Why This Case Matters

- It calibrates release-gate thinking: commit-related findings can become `critical` when they threaten recovery and data integrity.
- It also shows that operational correctness matters more than whether the loop style is modern.

## Case 4: Fixed-Format Order Update With Indicator Leakage

### Review Input

```rpgle
     FORDHDR    IF   E           K DISK
     D AMT             S              7P 2
     D ORDNO           S             10A
     C     *ENTRY        PLIST
     C                   PARM                    ORDNO
     C     ORDNO         CHAIN     ORDHDR                     90
     C     *IN90         IFEQ      *OFF
     C                   Z-ADD     OHAMT         AMT
     C                   ENDIF
     C     AMT           DIV       OHQTY         AVGAMT
     C                   UPDATE    ORDHDR
     C                   RETURN
```

### Expected Findings

- `critical` [ORDUPD.RPGLE:9] `DIV` uses `OHQTY` without a visible zero check before dividing `AMT`.
  Impact: a zero quantity can trigger arithmetic failure or produce invalid average values in the update path.
  Fix: guard the divide with an explicit zero check before executing `DIV`.

- `critical` [ORDUPD.RPGLE:10] `UPDATE ORDHDR` executes even when indicator `90` signals that the `CHAIN` did not find a record.
  Impact: the member can attempt an unsafe update using stale record state or an invalid access path.
  Fix: move `UPDATE ORDHDR` inside the found-record branch or add an explicit not-found exit path.

- `medium` [ORDUPD.RPGLE:7] Indicator `90` protects `Z-ADD` but does not protect the later arithmetic and update flow.
  Impact: the member appears partially guarded, which makes the not-found path easy to misread and maintain incorrectly.
  Fix: keep the full business path, including divide and update, inside the same found-record branch.

### Why This Case Matters

- It exercises fixed-format review instead of free-format review.
- It forces the reviewer to reason about indicators, opcode semantics, and stale-record risks together.

## Case 5: Mixed-Source Member With Lost Not-Found Guard

### Review Input

```rpgle
     FORDHDR    IF   E           K DISK
     D ORDNO           S             10A
     D WSSTAT          S              1A
     C     *ENTRY        PLIST
     C                   PARM                    ORDNO
     C     ORDNO         CHAIN     ORDHDR                     90
 /FREE
   if OHSTAT = 'A';
     WSSTAT = 'A';
   else;
     WSSTAT = 'H';
   endif;
   return;
 /END-FREE
```

### Expected Findings

- `critical` [ORDMIX.RPGLE:8] Free-format logic reads `OHSTAT` after a fixed-format `CHAIN` without carrying the `*IN90` not-found guard across the style boundary.
  Impact: the member can read stale or invalid record data when `ORDHDR` is not found.
  Fix: keep the free-format branch inside an explicit found-record guard or exit immediately on `*IN90`.

- `medium` [ORDMIX.RPGLE:7] The fixed/free transition does not make ownership of record-validity state explicit.
  Impact: later maintenance can misread the free-format block as safe even though it depends on fixed-format indicator state.
  Fix: make the found/not-found branch explicit at the transition point and document the boundary in code structure.

### Why This Case Matters

- It exercises the seam between fixed-format and free-format logic.
- It prevents the skill from treating mixed-source review as only a subset of fixed-format review.

## Case 6: Card Authorization Reversal Without Idempotency

### Review Input

```rpgle
**FREE

ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-f AUTHHDR usage(*update) keyed extfile('AUTHHDR');

dcl-pi *n;
  inAuthNo char(12);
end-pi;

chain inAuthNo AUTHHDR;
if %found(AUTHHDR);
  availAmt += AHHOLD;
  AHSTAT = 'R';
  update AUTHHDRR;
endif;

return;
```

### Expected Findings

- `critical` [AUTHRVS.RPGLE:12] Authorization reversal adds `AHHOLD` back to available amount without checking whether the hold is already reversed or released.
  Impact: repeated execution can double-release the same authorization amount and overstate available credit.
  Fix: guard the reversal path with an explicit current-state check and make the release operation idempotent.

- `medium` [AUTHRVS.RPGLE:13] Status is changed to `'R'` only after balance movement, but there is no visible not-eligible path for unexpected authorization states.
  Impact: invalid or duplicate reversals can silently proceed without a business-state rejection.
  Fix: validate the current authorization status before changing balances and exit on already-reversed or terminal states.

### Why This Case Matters

- It introduces a real card-business authorization scenario.
- It teaches the skill to look for idempotency and state-machine correctness, not just generic update handling.

## Case 7: Card Repayment Applied Directly To Principal

### Review Input

```rpgle
**FREE

ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-f CARDACCT usage(*update) keyed extfile('CARDACCT');

dcl-pi *n;
  inAcctNo char(16);
  inPayAmt packed(9:2);
end-pi;

chain inAcctNo CARDACCT;
if %found(CARDACCT);
  if inPayAmt > 0;
    ACPRIN -= inPayAmt;
    update CARDACCTR;
  endif;
endif;

return;
```

### Expected Findings

- `critical` [CARDPAY.RPGLE:14] Repayment is applied directly to principal `ACPRIN` without any visible allocation order across fee, interest, and principal buckets.
  Impact: outstanding balances and customer payoff behavior can be wrong if business policy requires fees or interest to be paid first.
  Fix: implement and document the required repayment allocation sequence before reducing principal.

- `medium` [CARDPAY.RPGLE:13] Positive-amount validation exists, but there is no visible protection against repayment amounts that exceed the remaining principal or total outstanding balance.
  Impact: over-allocation can drive balances negative or hide upstream settlement errors.
  Fix: cap allocation against outstanding components and route excess amounts to a controlled overpayment or rejection path.

### Why This Case Matters

- It covers a core line-of-business rule that generic RPG review would miss.
- It forces the skill to reason about business bucket ordering, not just syntax.

## Case 8: Card Limit Batch Without Post-Update Invariant Checks

### Review Input

```rpgle
**FREE

ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-f CARDLIM usage(*update) keyed extfile('CARDLIM');

dcl-s wsUpdCnt packed(7:0) inz(0);
dcl-s inRaiseAmt packed(7:0) inz(5000);

setll *loval CARDLIM;
read CARDLIM;
dow not %eof(CARDLIM);
  if CLGRADE = 'G';
    CLAVL = CLAVL + inRaiseAmt;
    CLLMT = CLLMT + inRaiseAmt;
    update CARDLIMR;
    wsUpdCnt += 1;
  endif;
  read CARDLIM;
enddo;

return;
```

### Expected Findings

- `critical` [LIMBATCH.RPGLE:13] The batch raises both available limit `CLAVL` and total limit `CLLMT` by the same amount without any visible invariant check against outstanding balance or product cap rules.
  Impact: accounts can receive an invalid available-credit state or exceed approved limit policy.
  Fix: validate product cap, outstanding exposure, and post-update balance invariants before applying the limit increase.

- `medium` [LIMBATCH.RPGLE:15] `wsUpdCnt` is incremented immediately after `update CARDLIMR` with no visible failure handling.
  Impact: the job can over-report successful limit increases if updates fail on individual accounts.
  Fix: check the update result before counting the record as successfully processed.

### Why This Case Matters

- It gives the skill a realistic line-of-business batch case.
- It teaches the difference between “field update succeeded” and “financial invariant remains valid”.

## Case 9: Statement Minimum Payment Computed From Principal Only

### Review Input

```rpgle
**FREE

ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-f STMTCTL usage(*update) keyed extfile('STMTCTL');

dcl-pi *n;
  inAcctNo char(16);
end-pi;

chain inAcctNo STMTCTL;
if %found(STMTCTL);
  MNPMT = STPRIN * 0.10;
  update STMTCTLR;
endif;

return;
```

### Expected Findings

- `critical` [STMTGEN.RPGLE:12] Minimum payment `MNPMT` is derived only from principal `STPRIN` with no visible fee, interest, overdue, or over-limit components.
  Impact: statement output can show the wrong minimum due and understate the customer's required payment.
  Fix: implement the documented minimum-payment formula using all required debt buckets and cycle rules.

- `medium` [STMTGEN.RPGLE:13] The statement update path does not show any validation that the computed minimum due is bounded by total outstanding amount or product floor rules.
  Impact: minimum due can be internally inconsistent with billed balances if formula inputs or rounding rules are wrong.
  Fix: validate the computed value against outstanding totals and documented minimum-payment constraints before update.

### Why This Case Matters

- It covers one of the most customer-visible defects in credit-card systems.
- It forces the skill to review statement math as business logic, not as a harmless formula detail.

## Case 10: Delinquency Status Cleared On Any Positive Payment

### Review Input

```rpgle
**FREE

ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-f CARDDLY usage(*update) keyed extfile('CARDDLY');

dcl-pi *n;
  inAcctNo char(16);
  inPayAmt packed(9:2);
end-pi;

chain inAcctNo CARDDLY;
if %found(CARDDLY);
  if inPayAmt > 0;
    DQSTAT = '0';
    update CARDDLYR;
  endif;
endif;

return;
```

### Expected Findings

- `critical` [DELINQ.RPGLE:14] Any positive payment clears delinquency status `DQSTAT` without checking whether overdue balances remain outstanding.
  Impact: the account can return to a normal status while delinquent debt still exists, breaking aging and collections behavior.
  Fix: recompute delinquency from remaining overdue buckets after payment and clear the status only when the account is actually cured.

- `medium` [DELINQ.RPGLE:15] The update path changes delinquency status with no visible audit of which overdue bucket or aging rule was satisfied.
  Impact: later reconciliation and collections analysis cannot explain why the account left delinquent status.
  Fix: retain or derive the supporting overdue-bucket decision before updating the status.

### Why This Case Matters

- It teaches the skill that status flags in card systems are derived from money movement, not independent toggles.
- It adds a realistic servicing and collections scenario that generic RPG review would under-detect.

## Case 11: Installment Plan Closed Without Residual Reconciliation

### Review Input

```rpgle
**FREE

ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-f INSTPLAN usage(*update) keyed extfile('INSTPLAN');

dcl-pi *n;
  inPlanNo char(12);
  inCloseAmt packed(9:2);
end-pi;

chain inPlanNo INSTPLAN;
if %found(INSTPLAN);
  if inCloseAmt >= INREMN;
    INSTAT = 'C';
    update INSTPLANR;
  endif;
endif;

return;
```

### Expected Findings

- `critical` [INSTCLS.RPGLE:14] Installment plan status is set to closed when `inCloseAmt` covers only remaining principal `INREMN`, with no visible reconciliation of residual fees, payoff adjustments, or pending accruals.
  Impact: the plan can appear settled while receivable components still remain on the ledger.
  Fix: validate residual principal, fee, and payoff balances before moving the plan to closed status.

- `medium` [INSTCLS.RPGLE:15] The close path updates plan status immediately with no visible post-close consistency check or exception handling.
  Impact: downstream servicing can treat the plan as closed even if final settlement posting fails or residual balances remain.
  Fix: add a post-close validation path and fail the status change when final reconciliation does not succeed.

### Why This Case Matters

- It extends the skill into installment and loan-like card features that many card issuers support.
- It reinforces that lifecycle closure must be reconciled to ledger state, not just an amount comparison.

## Case 12: Points Granted Before Posting Finality

### Review Input

```rpgle
**FREE

ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-f PNTLED usage(*update) keyed extfile('PNTLED');

dcl-pi *n;
  inTxnNo char(20);
  inTxnAmt packed(9:2);
end-pi;

chain inTxnNo PNTLED;
if not %found(PNTLED);
  PAVAIL += %int(inTxnAmt / 10);
  write PNTLEDR;
endif;

return;
```

### Expected Findings

- `critical` [PNTPOST.RPGLE:13] Loyalty points are granted as soon as the transaction is seen, with no visible check that the card transaction reached an eligible posting or clearing state.
  Impact: the same spend can grant points before final posting or after later reversal, causing duplicate or premature reward accrual.
  Fix: award points only at the documented lifecycle stage and gate the write with posting-state validation.

- `medium` [PNTPOST.RPGLE:12] The deduplication path only checks whether `inTxnNo` exists in `PNTLED`, but does not show any idempotency scope for partial retries, replays, or multi-step posting events.
  Impact: retry behavior can still create inconsistent points history when the same business transaction is replayed in a different processing phase.
  Fix: use a business-stable idempotency key that matches the actual reward-grant event.

### Why This Case Matters

- It adds a real loyalty-points accrual scenario that is common in card ecosystems.
- It teaches the skill that points awarding depends on transaction lifecycle, not just amount arithmetic.

## Case 13: Refund Reverses Points Without Earned-Points Reconciliation

### Review Input

```rpgle
**FREE

ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-f PNTACCT usage(*update) keyed extfile('PNTACCT');

dcl-pi *n;
  inAcctNo char(16);
  inRefundAmt packed(9:2);
end-pi;

chain inAcctNo PNTACCT;
if %found(PNTACCT);
  PAVAIL -= %int(inRefundAmt / 10);
  update PNTACCTR;
endif;

return;
```

### Expected Findings

- `critical` [PNTRVS.RPGLE:13] Refund reversal subtracts points from `PAVAIL` using only refund amount, with no visible reconciliation to the points originally granted for the refunded transaction.
  Impact: points can remain overstated after refund or become negative if the same refund reversal runs more than once.
  Fix: link refund reversal to the original earned-points record and reverse only the confirmed granted amount once.

- `medium` [PNTRVS.RPGLE:14] The points balance is updated directly with no visible floor check or protected-bucket handling.
  Impact: refunds can push the available-points balance below zero or consume points that should not be reversed automatically.
  Fix: validate available and protected point buckets before applying the reversal.

### Why This Case Matters

- It enforces symmetry between spend accrual and refund reversal.
- It gives the skill a customer-dispute-heavy case that generic financial checks often miss.

## Case 14: Points Expiry Batch Expires Total Balance Instead Of Eligible Bucket

### Review Input

```rpgle
**FREE

ctl-opt dftactgrp(*no) actgrp(*caller);

dcl-f PNTEXP usage(*update) keyed extfile('PNTEXP');

dcl-s wsExpCnt packed(7:0) inz(0);
dcl-s inExpAmt packed(7:0) inz(100);

setll *loval PNTEXP;
read PNTEXP;
dow not %eof(PNTEXP);
  if PXDATE <= %date();
    PTOTAL -= inExpAmt;
    update PNTEXPR;
    wsExpCnt += 1;
  endif;
  read PNTEXP;
enddo;

return;
```

### Expected Findings

- `critical` [PNTEXP.RPGLE:14] Expiry processing deducts from total points `PTOTAL` rather than an explicitly eligible available bucket.
  Impact: the batch can expire frozen, redeemed-tracking, or campaign-protected points and create customer-visible balance disputes.
  Fix: expire only the eligible available bucket and enforce bucket-level expiry rules before update.

- `medium` [PNTEXP.RPGLE:15] `wsExpCnt` is incremented after the update with no visible exception handling or audit of which bucket was expired.
  Impact: expiry reporting can overstate success and make disputes difficult to trace when individual updates fail or hit the wrong bucket.
  Fix: record the expired bucket decision and check update success before counting the account as processed.

### Why This Case Matters

- It extends the skill into batch reward maintenance, which is common in card loyalty systems.
- It reinforces that points are multi-bucket balances, not a single fungible counter.
