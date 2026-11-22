# Technical Plan

Use a small `TaskManager` service with an in-memory dictionary and a separate JSON persistence adapter. Validate all inputs at the service boundary. Keep the harness outside `src/` and run unit/contract tests, Ruff, and Bandit independently. The harness reports each gate and exits non-zero if any mandatory gate fails.

Return deep copies at all public Task boundaries so nested mutable tag lists cannot alias internal state.
