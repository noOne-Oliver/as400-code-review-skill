---
name: as400-code-review
description: "Automated quality checks for AS400/RPG code. Use when: (1) reviewing RPG/RPGLE code for bugs, (2) pre-production quality gate, (3) variable initialization checks, (4) naming convention audits, (5) AS400 best practices validation. Covers variable initialization, naming issues, common RPG pitfalls, and AS400-specific checks."
---

# AS400 Code Review

Automated quality checks for AS400/RPG code focusing on variable initialization, naming conventions, and common pitfalls.

## Usage

Use when reviewing AS400/RPG code for quality issues, especially before production deployment.

```
/as400-code-review [options]
```

## Check Categories

### 1. Variable Initialization Issues

| Check | RPG Syntax | Risk Level | Description |
|-------|------------|------------|-------------|
| Numeric not initialized | `D var S 5P 0` (no INZ) | 🔴 Critical | 计算结果随机值 |
| Character default spaces | `D var S 10A` (no INZ) | 🟡 Medium | 拼接/比对失败 |
| Pointer not nullified | `D ptr S *` (no INZ(*NULL)) | 🔴 Critical | 莫名宕机/段错误 |
| DS subfields missing | DataStructure without subfield INZ | 🔴 Critical | 数据错位 |
| Array without initial values | `D arr S 10P 0 DIM(100)` | 🟡 Medium | 旧数据残留 |
| Indicator array wild | `D ind S 1N DIM(99)` | 🟡 Medium | 未预期状态残留 |

**Good Examples:**
```rpg
D price         S              7P 2    INZ(0)
D customerName  S             50A     INZ(*BLANKS)
D ptrCust       S                  *   INZ(*NULL)
D orderRec      DS                  INZ
D   orderId                     10A
D   orderAmt                    7P 2
```

**Bad Examples:**
```rpg
D price         S              7P 2          // Risk: random value
D ptrCust       S                  *          // Risk: garbage pointer
```

### 2. Variable Naming Issues

| Check | Example | Risk Level | Issue |
|-------|---------|------------|-------|
| TMP garbage | `TMP1`, `TMP2`, `X`, `XX` | 🟡 Medium | 意图不明，难以维护 |
| Misleading name | `CUSTNAME` stores address | 🔴 Critical | 名实不符，误导开发者 |
| Missing unit | `AMOUNT` (yuan? cent? ten-thousands?) | 🟡 Medium | 单位不清，计算易错 |
| Magic numbers | `IF ORD = 999` | 🟡 Medium | 999是什么？ |
| FLAG confusion | FLAG = 'A'/'B' vs 0/1 | 🟡 Medium | 判断逻辑混乱 |
| Single char names | `D K S 5P 0` | 🟡 Medium | 无意义，vs RPG的K命名 |

### 3. Common RPG Pitfalls

| Category | Issue | Risk | Fix |
|----------|-------|------|-----|
| **Compile** | Warning treated as OK | 🔴 | Warning = Error |
| **Logic** | DIV divide by zero | 🔴 | Test divisor first |
| **Logic** | CHAIN without %FOUND | 🟡 | Always check %FOUND/%ERROR |
| **Logic** | SETLL without %EQUAL | 🟡 | Know exact vs approximate |
| **Data** | Z-ADD vs EVAL | 🟡 | Know numeric conversion |
| **Data** | MOVE vs EVAL | 🟡 | Know string behavior |
| **Memory** | DS size mismatch | 🔴 | Verify DS layout |
| **File** | COMMIT without ROLLBACK test | 🔴 | Test both paths |
| **File** | LOCK timeout missing | 🟡 | Always handle timeout |

### 4. AS400-Specific Checks

| Check | Command/Action | Risk |
|-------|----------------|------|
| Object locks | `WRKOBJLCK` not verified | 🔴 | 其他Job持有锁 |
| Job queue backup | `WRKJOBQ` / `WRKUSRJOBQ` | 🟡 | 队列堆积 |
| Commitment control | `COMMIT` / `ROLLBACK` not tested | 🔴 | 事务失败无回滚 |
| Change log missing | `CHGJOB` logs not configured | 🟡 | 问题难追溯 |
| Memory leak | `WRKACTJOB` monitor | 🟡 | 长期Job内存增长 |
| Cursor leak | ODP handles not closed | 🔴 | 文件句柄耗尽 |

## Report Format

```markdown
# AS400 Code Review Report

## Summary
- Files Scanned: XX
- Total Issues: XX
  - 🔴 Critical: XX
  - 🟡 Medium: XX
  - 🟢 Info: XX

## Critical Issues (Must Fix Before Production)

| File | Line | Issue | Recommendation |
|------|------|-------|---------------|
| ORD010.RPGLE | 45 | Numeric VARX not initialized | Add INZ(0) |
| ... | | | |

## Medium Issues (Should Fix)

| File | Line | Issue | Recommendation |
|------|------|-------|---------------|
| ... | | | |

## Naming Convention Violations

| File | Variable | Issue | Suggestion |
|------|----------|-------|------------|
| ... | | | |

## Good Practices Found

- ✓ Module XXX uses proper INZ on all numerics
- ✓ ...
```

## Scan Checklist

- [ ] Numeric variables have INZ (or 0 default understood)
- [ ] Character variables have INZ(*BLANKS) or explicit init
- [ ] Pointers explicitly initialized with INZ(*NULL)
- [ ] DataStructure subfields individually initialized
- [ ] No "TMP1/TMP2/X/XX" variable names
- [ ] No magic numbers (extract to named constants)
- [ ] FLAG usage is consistent (0/1 or A/B, documented)
- [ ] Unit annotations on numeric variables (AMT_YUAN, AMT_CENT, etc.)
- [ ] DIV operations check divisor != 0
- [ ] File operations check %FOUND/%ERROR/%EOF
- [ ] COMMIT operations have ROLLBACK test
- [ ] No compile warnings (or warnings treated as errors)

## See Also

- [RPG Variable Definitions](references/rpg-variables.md)
- [RPG Best Practices](references/rpg-best-practices.md)
