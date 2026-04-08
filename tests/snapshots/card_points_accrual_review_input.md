Review this card loyalty-points accrual program for correctness and production risk:

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
