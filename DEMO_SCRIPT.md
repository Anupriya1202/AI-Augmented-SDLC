# Silent Demonstration Guide (approximately 2–3 minutes)

## Part 1A — Smart Task Manager
From the repository root run:

```bash
python Part-1A/demo.py
```

Show the deterministic task ordering, AND-combined tag/priority filter, and JSON save/load round-trip.

## Part 1B — Natural Language Reminder Agent
Run representative create, clarification and snooze requests:

```bash
python Part-1B/demo.py "Remind me to submit the lab report tomorrow at 9 am"
python Part-1B/demo.py "Remind me to attend standup at 10 am"
python Part-1B/demo.py "Snooze reminder #r12 for 15 minutes"
```

Show the JSON response schema, date/time extraction and clarification when required information is missing.

## Harness verification
Run:

```bash
python run_all.py
```

Show Part 1A's 10 unit/contract tests and four harness gates, Part 1B's four unit tests, and the 15-case structural/invariant/semantic evaluation. Clearly state that the benchmark uses the deterministic offline `FixtureProvider`, not a live LLM. Part 1A's style/security checks are focused standard-library checks, not full Ruff/Bandit scans.

## Recording guidance
- A silent terminal capture is sufficient; add short captions for Part 1A, Part 1B and the harness result.
- Keep API keys and credentials off screen.
- Upload the video to Google Drive or OneDrive with access enabled for BITS evaluators, then paste the URL into the submission template.
