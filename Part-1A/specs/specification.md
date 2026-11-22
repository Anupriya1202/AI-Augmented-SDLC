# Feature Specification — Smart Task Manager

## Problem and users
A single user needs a small local task manager to create, update, complete, remove, and find tasks. The application exposes a Python domain/service API; a web UI is out of scope.

## Task contract
A task contains `id`, `title`, `description`, `tags`, `priority`, `status`, `created_at`, and `updated_at`. IDs are unique. Text fields are strings; tags are a list of unique non-empty strings. Priority values: `low|medium|high`. Status values: `todo|in_progress|done`.

## Functional requirements
- FR-01 Create a task with a unique ID and valid title; defaults are empty description/tags, medium priority, and todo status.
- FR-02 Retrieve a task by ID; unknown IDs produce `TaskNotFound`.
- FR-03 Update title, description, tags, and priority after validation.
- FR-04 Delete an existing task; unknown IDs produce `TaskNotFound`.
- FR-05 Filter tasks by tag, priority, and status; filters combine with AND semantics.
- FR-06 Sort task lists by priority high-to-low, then creation time ascending, then ID ascending.
- FR-07 Persist and reload tasks using JSON without losing fields.
- FR-08 Enforce the constitution's status transition graph.
- FR-09 Return defensive copies of task data; caller mutation of a returned task or its tags must not mutate the manager's stored state.

## Acceptance criteria
- AC-01 Empty/whitespace title is rejected.
- AC-02 Duplicate IDs are rejected.
- AC-03 Invalid priority/status/tag types are rejected.
- AC-04 Illegal status transitions are rejected and leave state unchanged.
- AC-05 A deleted or unknown ID cannot be retrieved or updated.
- AC-06 Combined filters return only tasks satisfying every supplied filter.
- AC-07 Sorting is stable and follows the exact tie-break rules above.
- AC-08 JSON round-trip preserves all task fields.
- AC-09 Malformed JSON raises a clear persistence error and does not overwrite the source file.
- AC-10 Mutating the tags list on a Task returned by create/get/update/list does not change the stored task; state changes must go through validated service methods.

## Non-functional requirements
Python 3.11+, standard library runtime, deterministic behavior, no network calls, no secrets, and testable public methods. Lint and SAST are mandatory gates.
