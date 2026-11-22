# Part 1A Harness Log

Application: Smart Task Manager (Python 3.11+, standard-library runtime).

## Specification traceability
Reviewed artifacts: `specs/constitution.md`, `specs/specification.md`, `specs/clarifications.md`, `specs/plan.md`, and `specs/tasks.md`. The status-transition graph, validation rules, AND-combined filters, deterministic sort order and JSON persistence are implemented in `src/task_manager.py`.

## Actual harness execution
Command: `python Part-1A/.harness/run_harness.py` (also invoked by `python run_all.py`).
- Unit/contract suite: 10 tests passed.
- Syntax compilation: PASS.
- Lightweight style gate: PASS (trailing whitespace and tab indentation).
- Focused AST guard: PASS (no direct calls to `eval`, `exec`, `compile` or `__import__` in application source).
- Machine-readable result: `evidence/harness-results.json`.

Tooling qualification: the style and AST checks are intentionally lightweight standard-library checks. They are not full Ruff or Bandit scans and are labelled accordingly.

## Negative-path evidence
The contract suite exercises rejection of blank titles, duplicate IDs, invalid fields, illegal status transitions, unknown IDs and malformed JSON. In particular, `test_malformed_json_fails_closed` verifies that loading malformed JSON raises `PersistenceError` and leaves the corrupt source unchanged. The final run passed 10/10 tests. No failing Part 1A harness run is claimed; no failure was manufactured solely for submission.

## Human review and limitations
Decision: provisional ACCEPT for the limited assignment demonstration scope after reviewing source and harness output.
Residual risks: local single-process in-memory operation, JSON persistence, no concurrent-write coordination, and narrow AST rule coverage. Production controls would include a transactional database, authentication, concurrency control, backups, dependency scanning, comprehensive SAST, monitoring and human security review.
