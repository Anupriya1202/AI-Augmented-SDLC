# Part 1A Constitution — Smart Task Manager

1. Correctness is defined by this constitution and `specification.md`, not by generated code.
2. All domain operations must be deterministic and independently testable.
3. Task IDs are unique non-empty strings; titles are trimmed and non-empty.
4. Priority is one of `low`, `medium`, `high`; status is one of `todo`, `in_progress`, `done`.
5. Only transitions `todo -> in_progress`, `in_progress -> done`, `in_progress -> todo`, and `todo -> done` are allowed. A `done` task is terminal in this version.
6. Persistence must use JSON and must fail safely on malformed data; writes must not silently discard existing tasks.
7. Tests and mandatory harness gates must not be removed or weakened to obtain PASS.
8. No credentials, personal data, or secrets may be committed.
9. The final decision is made by a human after reviewing test, lint, and SAST evidence.
10. Public Task return values must be defensive copies; mutating a returned object must not bypass service validation or alter stored state.
