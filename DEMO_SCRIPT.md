# Demonstration Video Script (approximately 3–4 minutes)

## Opening
"This assignment demonstrates Specification-Driven Development and harness engineering through one deterministic application and one AI-oriented application. The repository includes specifications, source, tests, evaluation cases and machine-readable evidence."

## Part 1A — Smart Task Manager
1. Open `Part-1A/specs/specification.md`; show task fields, status transitions and acceptance criteria.
2. Show `Part-1A/src/task_manager.py`; point out input validation, status transitions, combined filters, sorting and JSON persistence.
3. Run `python Part-1A/.harness/run_harness.py` from the repository root.
4. Show the 10 passing unit/contract tests, syntax compilation, lightweight style gate and focused AST security gate.
5. Open `Part-1A/evidence/harness-results.json`. Explain that the style/security checks are focused standard-library checks, not full Ruff/Bandit scans.

## Part 1B — Natural Language Reminder Agent
1. Show `Part-1B/specs/specification.md`, especially the JSON output schema and create/reschedule/snooze/clarify invariants.
2. Show `Part-1B/evals/dataset.json`, identifying normal, missing-field, boundary, malformed and adversarial cases.
3. Run `python Part-1B/.harness/run_evaluation.py`.
4. Explain the three independent validation layers: schema, invariants and semantic evaluation. The threshold is schema 100%, invariants 100% and semantic score at least 0.80.
5. Open `Part-1B/evidence/eval-results.json` and show per-case results.
6. State clearly that the checked-in benchmark uses the offline FixtureProvider, not a live LLM. A live adapter exists but is not the basis of the recorded metrics.

## Closing
"The PASS is limited to assignment demonstration scope. Part 1A would need stronger persistence and concurrency controls for production. Part 1B needs live-model benchmarking, timezone/DST handling, monitoring, privacy controls and user confirmation before a real reminder side effect."

## Recording checklist
- Show the public repository and both project folders.
- Keep API keys and other secrets off screen.
- Ensure test outputs and JSON reports are legible.
- Upload to Google Drive or OneDrive with BITS-accessible permissions and paste the shareable link into the submission template.
