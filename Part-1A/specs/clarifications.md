# Clarifications
- This is a local single-user domain service, not a multi-user server.
- IDs are supplied by caller to keep tests deterministic; no UUID generation is hidden inside the service.
- `done` is terminal in this assignment scope; reopening requires a future specification revision.
- Priority sort order is high, medium, low. Ties use `created_at`, then `id`.
- Returned Task objects are defensive snapshots. Although the dataclass is frozen, its nested tags list is mutable, so service methods return deep copies to prevent callers from changing stored state by reference.
