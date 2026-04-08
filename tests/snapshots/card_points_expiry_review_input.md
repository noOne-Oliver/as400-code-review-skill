Review this card loyalty-points expiry batch for correctness and production risk:

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
