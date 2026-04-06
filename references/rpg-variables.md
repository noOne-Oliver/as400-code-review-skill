# RPG Variable Definitions Reference

## Variable Types and Initialization

### Numeric Variables

```rpg
D price           S              7P 2    INZ(0)        // Price in yuan.yy
D quantity       S              5P 0    INZ           // Integer quantity
D rate           S              3P 2    INZ           // Percentage rate
D flag           S              1N     INZ(*OFF)     // Boolean flag
```

**Initialization Rules:**
- `INZ` defaults to 0 for numeric
- Explicit `INZ(0)` preferred for clarity
- `INZ(*ZEROS)` equivalent to INZ(0)
- `INZ(*NULL)` for nullable numerics (requires SQL)

### Character Variables

```rpg
D customerName    S             50A     INZ(*BLANKS)  // Name field
D address        S            100A     INZ(*BLANKS)  // Address
D remark         S             80A                     // Nullable remark
```

**Initialization Rules:**
- `INZ(*BLANKS)` or `INZ(*NULL)` for strings
- Default is PAD SPACES (80A = 80 spaces)
- *BLANKS = all spaces
- *NULL = all NULL bytes (different from *BLANKS!)

### Date/Time Variables

```rpg
D orderDate      S               D     INZ(*DATE)    // Date type
D processTime    S               T     INZ           // Time type
D timestamp      S               Z     INZ           // Timestamp
```

### Pointer Variables

```rpg
D ptrData        S               *     INZ(*NULL)    // Must initialize!
D ptrBase        S               *     INZ(%addr(baseArray))
```

**⚠️ CRITICAL:** Always initialize pointers. Uninitialized pointers cause unpredictable behavior.

### Indicator Variables

```rpg
D isValid        S               1N     INZ(*OFF)     // Boolean
D errFlag        S               1N     INZ(*OFF)
D debugMode      S               1N     INZ(*OFF)
```

### Data Structures

```rpg
// Simple DS
D orderRec       DS                  INZ
D   orderId                     10A
D   orderAmt                    7P 2
D   orderQty                     5P 0

// Nested DS
D custRec        DS                  INZ
D   custId                       10A
D   custName                     50A
D   custAddr        DS                  INZ
D     addrLine1                    80A
D     addrLine2                    80A
```

**⚠️ CRITICAL:** DS initialization with INZ does NOT initialize subfields individually. Always explicitly initialize subfields for guaranteed state.

### Arrays

```rpg
D prices         S              7P 2    DIM(100)  CTDATA INZ
D names          S             50A     DIM(50)   INZ(*BLANKS)
D flags          S              1N     DIM(99)   INZ(*OFF)
```

**⚠️ MEDIUM:** Arrays without INZ retain old values between calls. Always initialize arrays if reused.

## Variable Naming Conventions

### Recommended Patterns

| Pattern | Example | Use Case |
|---------|---------|----------|
| `camelCase` | `customerName` | Local variables |
| `prefix_type` | `numOrderCount` | Type annotation prefix |
| `suffix_unit` | `amt Yuan` or `amtCent` | Unit in name |
| `bIs_` | `bIsValid` | Boolean flags |

### Anti-Patterns to Avoid

| Bad Name | Problem | Fix |
|----------|---------|-----|
| `TMP1`, `TMP2` | Meaningless | `tmpCustOrder` |
| `X`, `XX`, `K` | Single char | `loopIndex`, `custId` |
| `DATA`, `REC` | Too generic | `custRecord` |
| `FLAG` (unspecified) | 0/1 or A/B? | `cIsActive` (1/0) |
| `AMT` | What unit? | `amtYuan` or `amtCent` |

## Data Types Quick Reference

| RPG Type | Description | Default Value | Notes |
|----------|-------------|---------------|-------|
| `S` | Standalone | undefined | Must INZ |
| `P` | Packed decimal | undefined | Must INZ |
| `S` with `A` | Alphanumeric | spaces | Must INZ |
| `S` with `N` | Indicator | *OFF | INZ(*OFF) |
| `S` with `*` | Pointer | undefined | MUST INZ |
| `D` | Date | *DATE | INZ(*DATE) |
| `T` | Time | *TIME | INZ(*TIME) |
| `Z` | Timestamp | *ZEROTIMESTAMP | INZ |

## Common Mistakes

### 1. Assuming Numeric Defaults to 0

```rpg
// ❌ WRONG - assumes 0
D counter       S              5P 0
// ... later ...
D subtotal      S              7P 2
subtotal = counter * 100;     // counter might be garbage!

// ✅ CORRECT
D counter       S              5P 0    INZ(0)
```

### 2. Confusing *BLANKS and *NULL

```rpg
// *BLANKS = spaces (x'40')
// *NULL = NULL bytes (x'00')
// Different behavior in string operations!

D name1         S             50A     INZ(*BLANKS)
D name2         S             50A     INZ(*NULL)
// name1 = 'JOHN  '
// name2 = 'JOHN' followed by NULLs
// %len(name2) = 4, not 50!
```

### 3. DataStructure Subfield Initialization

```rpg
// ❌ RISKY
D rec           DS                  INZ
D   f1                        10A
D   f2                         5P 0
// INZ only initializes the DS as a whole

// ✅ SAFE
D rec           DS                  INZ
D   f1                        10A     INZ(*BLANKS)
D   f2                         5P 0    INZ(0)
```
