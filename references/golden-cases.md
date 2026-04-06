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
