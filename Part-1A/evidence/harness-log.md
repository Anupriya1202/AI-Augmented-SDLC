# Part 1A Harness Log

Application: Smart Task Manager (Python 3.11+, standard-library runtime).

## Specification traceability
Reviewed artifacts: `specs/constitution.md`, `specs/specification.md`, `specs/clarifications.md`, `specs/plan.md`, and `specs/tasks.md`. The transition graph, validation rules, combined filters, deterministic sort order, and JSON persistence are implemented in `src/task_manager.py`.

## Recorded validation
Command: `python Part-1A/.harness/run_harness.py`

The harness runs 10 unit/contract tests, syntax compilation, a lightweight whitespace/tab style gate, and an AST guard against selected dynamic-execution primitives. The recorded local execution completed with all four gates PASS and all 10 tests passing. Machine-readable output is in `evidence/harness-results.json`.

Tooling qualification: the style and AST checks are intentionally lightweight standard-library checks. They are not Ruff or Bandit results. Ruff/Bandit are listed as optional developer tools only.

## Failure/repair record
No genuine Part 1A implementation failure was observed in the recorded final run. No failure was manufactured for submission. Negative-path contract tests exercise rejected blank titles, duplicate IDs, invalid fields, illegal terminal-state transitions, unknown IDs, and malformed JSON.

## Human review
Decision: provisional ACCEPT for the assignment's local single-user scope, after reviewing the source and harness output.

Residual risks: in-memory operation is single-process; JSON storage is local; the AST guard covers a narrow set of patterns; concurrent updates and full crash-recovery guarantees are not covered. Production controls would include a transactional database, authenticated API, concurrency control, backups, dependency scanning, comprehensive SAST, monitoring, and human security review.
