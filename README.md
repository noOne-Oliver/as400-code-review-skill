# AS400 Code Review Skill

Automated quality checks for AS400/RPG code.

## Overview

This skill provides comprehensive code review checklists for AS400/RPG applications, focusing on:

- **Variable Initialization** - Prevent random values and data corruption
- **Variable Naming** - Ensure clarity and maintainability
- **Common RPG Pitfalls** - Catch frequent bugs before production
- **AS400-Specific Checks** - Object locks, commitment control, job queues

## Usage

Install via OpenClaw skill management, then use when reviewing AS400/RPG code:

```
/as400-code-review
```

## Contents

```
├── SKILL.md                           # Main skill file
└── references/
    ├── rpg-variables.md              # Variable definition reference
    └── rpg-best-practices.md          # RPG best practices guide
```

## Check Categories

### 1. Variable Initialization Issues
- Numeric variables without INZ
- Character variables defaulting to spaces
- Pointers not nullified
- DataStructure subfields missing initialization
- Arrays retaining old values

### 2. Variable Naming Issues
- TMP1/TMP2 garbage names
- Misleading variable names
- Missing unit annotations
- Magic numbers
- FLAG confusion (0/1 vs A/B)

### 3. Common RPG Pitfalls
- Division by zero
- CHAIN without %FOUND
- SETLL without %EQUAL
- MOVE vs EVAL behavior
- DS size mismatches

### 4. AS400-Specific Checks
- Object locks (WRKOBJLCK)
- Job queue backup
- COMMIT/ROLLBACK testing
- Change log configuration
- Memory/cursor leaks

## For OpenClaw Users

This skill is designed for OpenClaw AI assistant. Install using:

```bash
openclaw skills install as400-code-review.skill
```

## License

MIT
