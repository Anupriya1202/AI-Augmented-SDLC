# Part 1B Evaluation Log

## Provider and configuration
- Default evaluation provider: `FixtureProvider` (offline deterministic adapter).
- Optional live adapter: `OpenAICompatibleProvider`, selected with `REMINDER_PROVIDER=live` and `OPENAI_API_KEY` in the environment.
- Default live model: `gpt-4o-mini` (override with `OPENAI_MODEL`); temperature 0.2; JSON-object response mode.
- Reference date for the dataset: 2026-11-23.
- The recorded benchmark used the fixture provider. No API key was used or stored. The live path was not executed in this benchmark.

## Evaluation contract
- Dataset: `evals/dataset.json`, 15 cases spanning representative, missing-field, boundary, malformed, adversarial, create, reschedule and snooze behavior.
- Threshold declared before final run: schema 100%, invariants 100%, semantic score >= 0.80.
- Scoring: structured intent/date/time/snooze-duration checks; title quality uses content-token F1 >= 0.75 after stop-word removal; safety requires clarification for underspecified or unsupported inputs. Exact prose matching is not used.

## Actual initial run and failure evidence
- Command: `python Part-1B/.harness/run_evaluation.py`.
- Initial run: schema 100%, invariant 100%, semantic score 0.5556 (25/45); overall FAIL.
- Failing cases: E01, E02, E03 and E10 expected valid creates but received clarification outputs because the parsed title was reset to null.
- Initial snapshot: `evidence/initial-generation/reminder_agent.py`.

## Feedback and repair
The feedback included failed case IDs, expected intent/title/date/time, observed clarification output and the below-threshold score. Root cause was an unintended second title initialization that erased an extracted create title. The parser was corrected to retain the extracted title for create intents. The same 15 cases and 0.80 threshold were retained; the title evaluator uses content-token F1 >= 0.75 to allow wording variation. The final run produced schema 100%, invariant 100%, semantic 1.0000 (45/45), overall PASS. See `evidence/eval-results.json`.

## Human review and limitations
Decision: provisional ACCEPT for the offline assignment demonstration scope. The benchmark validates the parser/evaluation pipeline with a deterministic fixture; it does not establish live LLM quality. The optional live provider was not executed. The heuristic may miss subtle semantic errors and paraphrases outside the dataset. Before production use, evaluate a larger human-labelled dataset against the deployed model/version, define timezone/DST behavior, add monitoring, privacy and audit controls, and require user confirmation before real reminder side effects.
