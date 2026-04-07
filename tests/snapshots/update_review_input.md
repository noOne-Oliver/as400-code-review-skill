Review this RPGLE update program:

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
