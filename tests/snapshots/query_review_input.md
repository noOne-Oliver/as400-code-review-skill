Review this RPGLE code for correctness and production risk:

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
