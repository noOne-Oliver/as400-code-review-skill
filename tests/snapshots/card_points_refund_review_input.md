Review this card loyalty-points refund reversal for correctness and production risk:

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
