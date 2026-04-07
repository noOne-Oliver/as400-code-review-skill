# Fixed-Format RPGLE Review Guide

Use this reference when the reviewed source uses fixed-format RPG or mixed fixed/free source.

## What Makes Fixed-Format Review Different

Fixed-format defects are often hidden in column usage, indicators, result fields, and opcode behavior. A review that only applies free-format rules will miss real AS400 production risks.

## High-Priority Checks

### Column Discipline

- Verify opcodes, factors, and result fields are in valid columns.
- Flag lines that appear shifted and may change opcode meaning.
- Flag continuation misuse when the source depends on column-6 continuation.

### Indicator-Driven Logic

- Review numbered indicators as business state, not just syntax.
- Flag indicators that are set but never cleared on later paths.
- Flag reuse of the same indicator for unrelated meanings.
- Treat missing indicator reset on reused loops or subroutines as a correctness risk.

### File Operations

- Review `CHAIN`, `SETLL`, `READE`, `READ`, `UPDATE`, `WRITE`, and `DELETE` together with their resulting indicators or status checks.
- Flag file operations whose failure or not-found path is only partially handled.
- Distinguish “indicator exists” from “indicator actually protects downstream field usage”.

### Arithmetic And Movement Semantics

- Check `MOVE`, `MOVEL`, `Z-ADD`, `ADD`, `SUB`, `DIV`, and legacy opcodes for truncation or implicit conversion risk.
- Flag divide operations without a visible zero guard.
- Flag string movement where blank padding or truncation can change business meaning.

### Subroutine Flow

- Review `EXSR`, `BEGSR`, `ENDSR`, `TAG`, `GOTO`, and cabxx-style flow carefully.
- Flag paths where a subroutine depends on hidden global state or indicator state from earlier branches.
- Prefer targeted findings over blanket anti-GOTO opinions.

## Severity Guidance

- `critical`: wrong data, stale record access, unsafe indicator state, invalid update path, truncation or arithmetic risk in sensitive logic
- `medium`: fragile flow, ambiguous indicator reuse, maintenance traps, partial file-status handling
- `info`: style cleanup that does not change business behavior

## Common Fixed-Format Findings

- `CHAIN` followed by field usage without the correct not-found indicator check
- result indicators reused across unrelated branches
- `MOVE/MOVEL` causing silent truncation or padding in key business fields
- update or write operations relying on stale indicator state
- subroutine calls that mutate state without a visible contract

## Review Output Notes

- Explain the relevant opcode or indicator behavior in plain language.
- Do not assume the reader remembers fixed-format column semantics.
- When a line number alone is not enough, cite the opcode and indicator together.
