Review this credit-card authorization reversal program for correctness and production risk:

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
