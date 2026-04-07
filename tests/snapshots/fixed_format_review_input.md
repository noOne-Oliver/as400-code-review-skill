Review this fixed-format RPGLE member for correctness and production risk:

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
