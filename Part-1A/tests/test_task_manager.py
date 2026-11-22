import tempfile
import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.task_manager import DuplicateTask, PersistenceError, TaskError, TaskManager, TaskNotFound


class TaskManagerTests(unittest.TestCase):
    def manager_with_tasks(self):
        manager = TaskManager()
        manager.create("a", "Write spec", tags=["school"], priority="high")
        manager.create("b", "Review tests", tags=["school", "qa"], priority="medium")
        manager.create("c", "Buy milk", tags=["home"], priority="low")
        return manager

    def test_create_defaults_and_duplicate_id(self):
        manager = TaskManager()
        task = manager.create("t1", "  Read  ")
        self.assertEqual((task.title, task.priority, task.status, task.tags), ("Read", "medium", "todo", []))
        with self.assertRaises(DuplicateTask):
            manager.create("t1", "Another")

    def test_rejects_invalid_title(self):
        for title in ("", "   ", None):
            with self.subTest(title=title), self.assertRaises(TaskError):
                TaskManager().create("x", title)

    def test_update_validates_and_preserves_unmodified_fields(self):
        manager = self.manager_with_tasks()
        updated = manager.update("a", title="Updated", tags=["work"])
        self.assertEqual((updated.title, updated.tags, updated.priority), ("Updated", ["work"], "high"))
        with self.assertRaises(TaskError):
            manager.update("a", priority="urgent")

    def test_status_transition_graph_and_atomic_rejection(self):
        manager = TaskManager()
        manager.create("x", "Task")
        manager.transition("x", "in_progress")
        manager.transition("x", "done")
        before = manager.get("x")
        with self.assertRaises(TaskError):
            manager.transition("x", "todo")
        self.assertEqual(manager.get("x"), before)

    def test_combined_filters_use_and_semantics(self):
        results = self.manager_with_tasks().list_tasks(tag="school", priority="medium", status="todo")
        self.assertEqual([task.id for task in results], ["b"])

    def test_priority_order_is_deterministic(self):
        self.assertEqual([task.id for task in self.manager_with_tasks().list_tasks()], ["a", "b", "c"])

    def test_delete_and_unknown_id(self):
        manager = self.manager_with_tasks()
        manager.delete("a")
        with self.assertRaises(TaskNotFound):
            manager.get("a")
        with self.assertRaises(TaskNotFound):
            manager.delete("missing")

    def test_json_round_trip(self):
        manager = self.manager_with_tasks()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            manager.save(path)
            loaded = TaskManager.load(path)
        self.assertEqual([task.id for task in loaded.list_tasks()], ["a", "b", "c"])
        self.assertEqual(loaded.get("b").tags, ["school", "qa"])

    def test_malformed_json_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text("{broken", encoding="utf-8")
            with self.assertRaises(PersistenceError):
                TaskManager.load(path)
            self.assertEqual(path.read_text(encoding="utf-8"), "{broken")

    def test_rejects_duplicate_tags(self):
        with self.assertRaises(TaskError):
            TaskManager().create("x", "Task", tags=["a", "a"])


if __name__ == "__main__":
    unittest.main()
