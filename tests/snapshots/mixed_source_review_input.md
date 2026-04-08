Review this mixed-source RPGLE member for correctness and production risk:

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
