# Part 1B Evaluation Log

## Provider and configuration
- Default evaluation provider: `FixtureProvider` (offline deterministic adapter).
- Optional live adapter: `OpenAICompatibleProvider`, selected with `REMINDER_PROVIDER=live` and `OPENAI_API_KEY` in the environment.
- Default live model: `gpt-4o-mini` (override with `OPENAI_MODEL`); temperature 0.2; JSON-object response mode.
- Reference date for the dataset: 2026-11-23.
- The recorded benchmark uses the fixture provider. No API key was used or stored. The live path was not executed in this run.

## Evaluation contract
- Dataset: `evals/dataset.json`, 15 cases spanning representative create requests, missing fields, boundaries, malformed input, adversarial requests, reschedule and snooze behavior.
- Acceptance threshold: schema 100%, invariant 100%, semantic score >= 0.80.
- Scoring: structured intent, reminder ID, date, time and snooze-duration checks; title quality uses content-token F1 >= 0.75 after stop-word removal; safety requires clarification for underspecified or unsupported inputs. Exact prose matching is not used.

## Initial-generation issue and reproducible failure evidence
The preserved initial source in `evidence/initial-generation/reminder_agent.py` returned `provider.generate(...)` directly. I exercised that initial snapshot with a malformed provider that returned only `{"intent":"create","title":"submit report","date":"not-a-date"}`. The initial implementation passed this incomplete, invalid payload through unchanged: it had only three keys instead of the required output contract and contained an invalid date. This is a reproducible structural-validation defect.

## Feedback and repair
The malformed provider output and contract mismatch were supplied as failure evidence. The final implementation adds `_valid_output_contract`, which checks the exact key set, types, supported intent, confidence bounds, ISO date, 24-hour time, snooze duration and intent-specific mandatory fields. Invalid provider output is converted into a safe clarification result rather than being passed downstream. `test_agent_rejects_malformed_provider_output` preserves this regression case. The evaluation dataset and 0.80 semantic threshold were not weakened.

## Final evaluation
- Command: `python Part-1B/.harness/run_evaluation.py`.
- Provider: offline `FixtureProvider` (not a live LLM).
- Dataset: 15/15 cases.
- Schema pass rate: 100%.
- Invariant pass rate: 100%.
- Semantic score: 1.0000 (46/46 applicable points).
- Overall: PASS.
- Machine-readable per-case report: `evidence/eval-results.json`.

## Human review and limitations
Decision: provisional ACCEPT for the offline assignment demonstration scope. The benchmark validates the parser/evaluation pipeline with a deterministic fixture; it does not establish live LLM quality. The optional live provider was not executed. The heuristic may miss subtle semantic errors and paraphrases outside the dataset. Before production use, evaluate a larger human-labelled dataset against the deployed model/version, define timezone/DST behavior, add monitoring, privacy and audit controls, and require user confirmation before real reminder side effects.
