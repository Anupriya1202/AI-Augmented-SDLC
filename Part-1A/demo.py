"""Small terminal demonstration of the deterministic Smart Task Manager."""
from __future__ import annotations
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
    print("TASK ID  PRIORITY  STATUS       TITLE")
    for task in manager.list_tasks():
        print(f"{task.id:<8} {task.priority:<9} {task.status:<12} {task.title}")
    print("\nCOMBINED FILTER: tag=BITS AND priority=high")
    for task in manager.list_tasks(tag="BITS", priority="high"):
        print(f"{task.id}: {task.title} ({task.priority}, {task.status})")
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "tasks.json"
        manager.save(path)
        restored = TaskManager.load(path)
        print(f"\nJSON PERSISTENCE: saved={len(manager.list_tasks())}, loaded={len(restored.list_tasks())}")

if __name__ == "__main__":
    main()
