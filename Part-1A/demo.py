"""Small terminal demonstration of the deterministic Smart Task Manager."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from src.task_manager import TaskManager


def main() -> None:
    manager = TaskManager()
    manager.create("T-101", "Submit architecture assignment", tags=["BITS", "study"], priority="high")
    manager.create("T-102", "Review unit tests", tags=["engineering", "qa"], priority="medium")
    manager.create("T-103", "Buy groceries", tags=["personal"], priority="low")
    manager.transition("T-101", "in_progress")
    manager.update("T-102", description="Check boundary and invalid-input cases")

    print("SMART TASK MANAGER - DEMO")
    print("1) Tasks sorted by priority:")
    print(json.dumps([task.__dict__ for task in manager.list_tasks()], indent=2))
    print("2) Combined filter (tag=BITS AND priority=high):")
    print(json.dumps([task.__dict__ for task in manager.list_tasks(tag="BITS", priority="high")], indent=2))

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "tasks.json"
        manager.save(path)
        restored = TaskManager.load(path)
        print("3) JSON persistence round-trip:")
        print(json.dumps({"saved_count": len(manager.list_tasks()), "loaded_count": len(restored.list_tasks())}, indent=2))


if __name__ == "__main__":
    main()
