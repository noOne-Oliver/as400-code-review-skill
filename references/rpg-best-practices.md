# RPG Best Practices Reference

## File Operations

### Always Check File Status

```rpg
// ❌ RISKY
CHAIN (key: orderNum) orderFile;
total = orderAmt;  // What if not found?

// ✅ SAFE
CHAIN (key: orderNum) orderFile;
if %found(orderFile);
  total = orderAmt;
else;
  total = 0;
  // Handle "order not found"
endif;
```

### Commitment Control

```rpg
// Always test COMMIT and ROLLBACK paths
C     *ENTRY        PLIST
C                   PARM                    pMode          1

/FREE
  BegSR processOrder;
    EXSR beginTran;

    // Business logic here
    chain e orderNum orderFile;
    if %found();
      // Update
      update orderRecord;
      if pMode = 'C';
        COMMIT;
        exSr logSuccess;
      else;
        ROLLBACK;
        exSr logRolledBack;
      endif;
    endif;

    BegSR beginTran;
      // Set up transaction
    EndSR;
  EndSR;
```

### Lock Handling

```rpg
// ❌ No timeout - hangs forever
setll (key) file;
reade (key) file;
// If locked by another job, WAITS forever

// ✅ With timeout/exit
setll (key) file;
if %lock();
  reade (key) file;
  if %found();
    // Process
  endif;
else;
  // Handle lock failure
  exsr handleLockTimeout;
endif;
```

## Division and Arithmetic

### Always Check Divisor

```rpg
// ❌ RISKY - divide by zero
avgPrice = totalAmt / orderCount;

// ✅ SAFE
if orderCount <> 0;
  avgPrice = totalAmt / orderCount;
else;
  avgPrice = 0;
endif;

// ✅ EVEN BETTER - use built-in
if orderCount <> 0;
  avgPrice = %div(totalAmt : orderCount);  // More precise
endif;
```

## String Operations

### MOVE vs EVAL

```rpg
// MOVE - left-to-right, pads/truncates
D var1           S             10A     INZ('ABC')
D var2           S             10A     INZ(*BLANKS)
MOVE var1 var2;                    // var2 = 'ABC       '

// EVAL - exact assignment
var2 = var1;                        // var2 = 'ABC       '
// Same result for alphanumeric, but:
var1 = 'ABC';
var2 = '1234567890';
EVAL var1 = var2;                  // var1 = '1234567890'
MOVE var2 var1;                    // var1 = '123456789 ' (truncated!)
```

### String Concatenation

```rpg
// ⚠️ Watch for trailing spaces
fullName = firstName + lastName;
// If firstName = 'JOHN    ' (10A)
// and lastName = 'DOE'    (10A)
// Result = 'JOHN      DOE' (spaces in middle!)

// ✅ Trim first
fullName = %trim(firstName) + ' ' + %trim(lastName);
// Result = 'JOHN DOE'
```

## Data Structure Alignment

### Verify DS Size Matches

```rpg
// ❌ RISKY - size mismatch causes data corruption
D header         DS                  INZ
D   recType                      1A
D   recLen                       5P 0
D   data                        50A
// Total = 1 + 5 + 50 = 56 bytes

// But if buffer is only 54 bytes...
// Data gets corrupted!

// ✅ SAFE - always verify sizes
// 56 bytes = 1 + 5 + 50 ✓ matches
// Use PSDS or properly sized external DS
```

## Compile and Build

### Treat Warnings as Errors

```rpg
// In CRTBNDRPG / CRTRPGPGM:
// Specify DFTACTGRP(*NO) for service programs
// Always review compile listing for warnings

// ⚠️ Common warnings to fix:
// RNF5409 - Implicit conversion
// RNF5410 - Loss of precision
// RNF5411 - Variable not used
// RNF7030 - Constants truncated
```

### Required Compiler Options

```rpg
// For production:
CRTBNDRPG PGM(lib/prodpgm)
           SRCFILE(lib/QRPGLESRC)
           SRCMBR(prodpgm)
           OPTION(*NOSECLVL : *NOUNREF : *NOEXT)
           GENLVL(*NONE)           // No generation data
           ALWNULL(*YES)            // Allow nulls
           DFTACTGRP(*NO)           // Activation group control
           ACTGRP(*NEW)            // Or *CALLER
```

## Program Structure

### Entry Parameter Validation

```rpg
D pOrderNum      S              10A
D pAmount        S              7P 2
D pMode          S              1A

C     *ENTRY        PLIST
C                   PARM                    pOrderNum
C                   PARM                    pAmount
C                   PARM                    pMode

/FREE
  // Always validate inputs first
  if pOrderNum = *BLANKS;
    *INLR = *ON;
    return;
  endif;

  if pAmount < 0;
    // Handle error
    exsr handleInvalidAmount;
    return;
  endif;

  select;
    when pMode = 'A';
      exsr processAdd;
    when pMode = 'D';
      exsr processDelete;
    other;
      exsr handleInvalidMode;
  endsl;
```

## Error Handling

### Indicator vs Exception

```rpg
// Method 1: Indicator (old style)
C     orderNum      CHAIN     orderFile
C     *IN90         IFEQ      *ON           // Not found
// Handle not found
C                   ENDIF

// Method 2: %ERROR (modern, preferred)
if %error;
  // Handle error
endif;

// Method 3: Monitor (exception handling)
monitor;
  // Risky operation
  result = total / divisor;
on-error;
  // Handle any error
  result = 0;
endmon;
```

## Logging and Debugging

### Essential Logging Points

```rpg
D LOG_FILE       S             20A   INZ('APPLOG')
D logMsg         S            100A

/FREE
  BegSR writeLog;
    logMsg = %trim(%char(%timestamp())) + ' ' +
             %trim(procName) + ' ' +
             logText;
    // Write to log file or table
    EXFMT logRecord;
  EndSR;

  BegSR validateOrder;
    // Log entry
    exsr writeLog: 'VALIDATE ORDER START';

    // Validation logic...

    // Log exit
    if valid;
      exsr writeLog: 'VALIDATE ORDER END - OK';
    else;
      exsr writeLog: 'VALIDATE ORDER END - FAIL: ' + errMsg;
    endif;
  EndSR;
```

## Performance Tips

### Avoid Unnecessary I/O

```rpg
// ❌ SLOW - multiple file reads in loop
for i = 1 to 1000;
  orderNum = orderIds(i);
  chain orderNum orderFile;
  // process
endfor;

// ✅ FASTER - READ vs CHAIN in loop
setll *loval orderFile;
read(e) orderFile;
dow not %eof(orderFile);
  // process
  read(e) orderFile;
enddo;
```

### Use Set-Based Operations When Possible

```rpg
// Instead of record-by-record in RPG:
// Consider SQL for bulk operations
/FREE
  exec sql DELETE FROM orderHist
    WHERE orderDate < :cutoffDate
    AND status = 'CLOSED';
  // One DB call instead of thousands of RPG operations
/FREE
```
