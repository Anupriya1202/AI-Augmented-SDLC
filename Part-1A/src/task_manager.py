"""Deterministic task-management domain service."""
from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PRIORITIES = ("low", "medium", "high")
STATUSES = ("todo", "in_progress", "done")
TRANSITIONS = {
    "todo": {"in_progress", "done"},
    "in_progress": {"done", "todo"},
    "done": set(),
}
PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}


class TaskError(ValueError):
    """Base class for task-domain errors."""


class TaskNotFound(TaskError):
    """Raised when a task ID does not exist."""


class DuplicateTask(TaskError):
    """Raised when a task ID is already present."""


class PersistenceError(TaskError):
    """Raised when task data cannot safely be loaded or saved."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _validate_text(value: Any, field: str, allow_empty: bool = True) -> str:
    if not isinstance(value, str):
        raise TaskError(f"{field} must be a string")
    cleaned = value.strip()
    if not allow_empty and not cleaned:
        raise TaskError(f"{field} must not be empty")
    return cleaned


def _validate_tags(tags: Any) -> list[str]:
    if not isinstance(tags, list):
        raise TaskError("tags must be a list")
    cleaned = [_validate_text(tag, "tag", allow_empty=False) for tag in tags]
    if len(set(cleaned)) != len(cleaned):
        raise TaskError("tags must be unique")
    return cleaned


@dataclass(frozen=True)
class Task:
    id: str
    title: str
    description: str
    tags: list[str]
    priority: str
    status: str
    created_at: str
    updated_at: str


class TaskManager:
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}

    def create(self, task_id: str, title: str, description: str = "", tags: list[str] | None = None,
               priority: str = "medium") -> Task:
        task_id = _validate_text(task_id, "id", allow_empty=False)
        if task_id in self._tasks:
            raise DuplicateTask(f"task '{task_id}' already exists")
        title = _validate_text(title, "title", allow_empty=False)
        description = _validate_text(description, "description")
        tags = _validate_tags([] if tags is None else tags)
        if priority not in PRIORITIES:
            raise TaskError(f"priority must be one of {PRIORITIES}")
        timestamp = _now()
        task = Task(task_id, title, description, tags, priority, "todo", timestamp, timestamp)
        self._tasks[task_id] = task
        return deepcopy(task)

    def get(self, task_id: str) -> Task:
        try:
            return deepcopy(self._tasks[task_id])
        except KeyError as exc:
            raise TaskNotFound(f"task '{task_id}' not found") from exc

    def update(self, task_id: str, **changes: Any) -> Task:
        current = self.get(task_id)
        allowed = {"title", "description", "tags", "priority"}
        unknown = set(changes) - allowed
        if unknown:
            raise TaskError(f"unsupported fields: {sorted(unknown)}")
        values = asdict(current)
        if "title" in changes:
            values["title"] = _validate_text(changes["title"], "title", allow_empty=False)
        if "description" in changes:
            values["description"] = _validate_text(changes["description"], "description")
        if "tags" in changes:
            values["tags"] = _validate_tags(changes["tags"])
        if "priority" in changes:
            if changes["priority"] not in PRIORITIES:
                raise TaskError(f"priority must be one of {PRIORITIES}")
            values["priority"] = changes["priority"]
        values["updated_at"] = _now()
        updated = Task(**values)
        self._tasks[task_id] = updated
        return deepcopy(updated)

    def transition(self, task_id: str, new_status: str) -> Task:
        current = self.get(task_id)
        if new_status not in STATUSES:
            raise TaskError(f"status must be one of {STATUSES}")
        if new_status not in TRANSITIONS[current.status]:
            raise TaskError(f"transition {current.status} -> {new_status} is not allowed")
        values = asdict(current)
        values["status"] = new_status
        values["updated_at"] = _now()
        updated = Task(**values)
        self._tasks[task_id] = updated
        return deepcopy(updated)

    def delete(self, task_id: str) -> None:
        if task_id not in self._tasks:
            raise TaskNotFound(f"task '{task_id}' not found")
        del self._tasks[task_id]

    def list_tasks(self, tag: str | None = None, priority: str | None = None,
                   status: str | None = None) -> list[Task]:
        if priority is not None and priority not in PRIORITIES:
            raise TaskError(f"priority must be one of {PRIORITIES}")
        if status is not None and status not in STATUSES:
            raise TaskError(f"status must be one of {STATUSES}")
        items = [task for task in self._tasks.values()
                 if (tag is None or tag in task.tags)
                 and (priority is None or task.priority == priority)
                 and (status is None or task.status == status)]
        ordered = sorted(items, key=lambda task: (PRIORITY_RANK[task.priority], task.created_at, task.id))
        return deepcopy(ordered)

    def save(self, path: str | Path) -> None:
        destination = Path(path)
        payload = [asdict(task) for task in self._tasks.values()]
        temporary = destination.with_suffix(destination.suffix + ".tmp")
        try:
            temporary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            temporary.replace(destination)
        except OSError as exc:
            temporary.unlink(missing_ok=True)
            raise PersistenceError(f"could not save tasks: {exc}") from exc

    @classmethod
    def load(cls, path: str | Path) -> "TaskManager":
        manager = cls()
        try:
            raw = json.loads(Path(path).read_text(encoding="utf-8"))
            if not isinstance(raw, list):
                raise ValueError("root must be a list")
            for item in raw:
                if not isinstance(item, dict):
                    raise ValueError("each task must be an object")
                expected = set(Task.__dataclass_fields__)
                if set(item) != expected:
                    raise ValueError("task fields do not match contract")
                task = Task(**item)
                if task.id in manager._tasks:
                    raise ValueError("duplicate task ID in file")
                _validate_text(task.id, "id", allow_empty=False)
                _validate_text(task.title, "title", allow_empty=False)
                _validate_text(task.description, "description")
                _validate_tags(task.tags)
                if task.priority not in PRIORITIES or task.status not in STATUSES:
                    raise ValueError("invalid priority or status")
                manager._tasks[task.id] = task
        except (OSError, json.JSONDecodeError, TypeError, TaskError, ValueError) as exc:
            raise PersistenceError(f"invalid task data: {exc}") from exc
        return manager
