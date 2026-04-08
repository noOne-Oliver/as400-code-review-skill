Review this card statement minimum-payment calculation for correctness and production risk:

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
