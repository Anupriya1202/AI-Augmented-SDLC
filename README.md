# AI-Augmented SDLC — Assignment 1

**Specification-Driven Development and Harness Engineering**  
BITS Pilani WILP · AI-Augmented Software Development Life Cycle · SE ZG534

This repository contains two compact applications with explicit specifications, implementation, independent harness validation, and evidence.

## Applications

### Part 1A — Smart Task Manager (deterministic)
A local Python domain service to create, retrieve, update, delete, filter, sort, and persist tasks. It validates task fields, enforces status transitions, combines filters using AND semantics, sorts deterministically, and stores JSON using a temporary-file replacement strategy.

### Part 1B — Natural Language Reminder Agent (AI-oriented)
A provider-based reminder parser supporting create, reschedule, snooze, and clarification intents. Its output is a fixed JSON contract including intent, title, date, time, reminder ID, snooze duration, clarification question, confidence, and reason. The application includes an offline `FixtureProvider` for reproducible tests and an optional OpenAI-compatible live provider adapter.

**Evaluation qualification:** the checked-in 15-case benchmark uses the offline deterministic fixture provider. It demonstrates the evaluation pipeline, not live-LLM quality. The live adapter is optional and was not used for the recorded offline benchmark. Never commit API credentials.

## Requirements and setup
- Python 3.11+
- Standard-library runtime; no third-party runtime packages are required.
- Optional development dependencies are listed in `requirements.txt`.

From the repository root:

```bash
python run_all.py
```

Run each harness independently:

```bash
python Part-1A/.harness/run_harness.py
python Part-1B/.harness/run_evaluation.py
```

Run the deterministic task-manager demo:\n\n```bash\npython Part-1A/demo.py\n```\n\nRun an offline reminder example:

```bash
python Part-1B/demo.py "Remind me to submit the lab report tomorrow at 9 am"
```

For the optional live provider, set `REMINDER_PROVIDER=live` and `OPENAI_API_KEY` in your shell, then run the same command. The default model is `gpt-4o-mini`; override with `OPENAI_MODEL`. Do not store keys in source control or video captures.

## Harness design and recorded results
- **Part 1A:** 11 unit/contract tests; syntax compilation; standard-library whitespace/indentation gate; focused AST check for direct calls to `eval`, `exec`, `compile`, and `__import__`. These lightweight checks are **not** full Ruff or Bandit scans.
- **Part 1B:** 15 evaluation cases across normal, boundary, missing-field, malformed and adversarial inputs. One pipeline checks structural schema, invariants and semantic properties. Threshold: schema 100%, invariants 100%, semantic >= 0.80. Title quality uses content-token F1, not exact sentence matching.

Recorded local execution of `python run_all.py`:
- Part 1A: 10/11 unit/contract tests; all four harness gates PASS.
- Part 1B: 4/4 unit tests; 15/15 eval cases; schema 100%; invariants 100%; semantic score 1.00 (46/46); aggregate PASS.

These results describe the offline fixture benchmark, not production or live-model quality. Machine-readable evidence is in each part's `evidence/` folder.

## SDD traceability
Each part contains `constitution.md`, `specification.md`, `clarifications.md`, `plan.md`, and `tasks.md` under `specs/`. Tests and evaluator properties trace to acceptance criteria and invariants. Initial/final source snapshots, harness logs and machine-readable output are retained in `evidence/`.

## Human review and residual risks
The implementation is suitable for the limited assignment demonstration scope, not production use. Part 1A is local and single-user; production use would need transactional persistence, concurrency control, authentication, backups, monitoring and stronger security analysis. Part 1B needs evaluation against a larger human-labelled dataset using the deployed model, timezone/DST policy, monitoring, privacy controls and explicit user confirmation before real reminder side effects.

## Data handling
All example data is synthetic. No API keys, credentials, or local environment files should be committed. Live-provider credentials are read from environment variables and are not written to logs.
