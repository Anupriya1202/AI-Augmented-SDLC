# Assignment 1 — Final Submission Summary

**Student:** Varshney Anupriya Rakesh  
**Student ID:** 2026NS93089  
**Course:** AI-Augmented Software Development Life Cycle (SE ZG534)

## Contents
- `Part-1A/`: deterministic Smart Task Manager, SDD artifacts, 11 unit/contract tests, harness and evidence.
- `Part-1B/`: Natural Language Reminder Agent, SDD artifacts, output contract and guardrails, 15-case evaluation dataset, three-layer evaluation harness and results.
- `DEMO_SCRIPT.md`: short video demonstration guide.
- `run_all.py`: runs both test suites and both harnesses.

## Latest local verification
Executed from the repository root using `python run_all.py`:
- Part 1A: 11/11 unit/contract tests passed.
- Part 1B: 4/4 unit tests passed.
- Part 1A: syntax compilation, lightweight style gate and focused AST security gate passed (four harness gates total).
- Part 1B: 15/15 evaluation cases passed; schema 100%; invariant 100%; semantic 46/46 = 1.00; aggregate PASS.

Part 1A checks are focused standard-library checks, not full Ruff or Bandit reports. Part 1B benchmark uses the deterministic offline fixture provider; its metrics do not establish live-LLM quality. The optional live provider was not used for these results.

## Human review and residual risks
The applications are acceptable for the limited assignment demonstration scope, not production use. Part 1A needs transactional persistence and concurrency controls for production. Part 1B needs a larger human-labelled evaluation set against the deployed model, timezone/DST policy, monitoring, privacy controls and explicit user confirmation before real reminder actions.

## Before LMS upload
1. Record the video using `DEMO_SCRIPT.md`.
2. Upload to Google Drive or OneDrive and grant access to BITS email accounts.
3. Replace the video-link placeholder in the DOCX.
4. Upload the reflection report/template to LMS and verify the GitHub repository remains public.
