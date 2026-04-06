# Release Gate

Use this reference when the task is about production readiness or上线 review.

## Blockers

- uninitialized numeric, pointer, or DS state in production paths
- file operations without `%FOUND`, `%EOF`, `%ERROR`, or equivalent checks
- commit processing without verified rollback or failure handling
- known lock risks without timeout or fallback behavior
- compile warnings that indicate truncation, precision loss, or unsafe conversion

## Follow-Up Required

- naming or readability issues that could cause maintenance mistakes
- missing logs on critical business transitions
- magic numbers or undocumented status codes
- checklist items awaiting operational confirmation

## Operational Checks

- verify rollback plan exists and has been tested
- verify monitoring, logs, and alerting are ready
- verify object-lock and queue risk has been considered for hot paths

## Release Decision

- `blocked`: one or more blockers remain
- `needs follow-up`: no hard blocker found, but unresolved operational or medium-severity risks remain
- `ready with noted risks`: only info-level items or clearly accepted medium risks remain
