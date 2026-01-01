from typing import List, Optional
from src.core.models import Task, TaskStatus, TaskPriority
from src.core.storage import Storage
from src.utils.id_gen import IDGenerator

class TaskService:
    def __init__(self, storage: Optional[Storage] = None):
        self._storage = storage or Storage()
        self._tasks = {t.id: t for t in self._storage.load_tasks()}
        self._id_gen = IDGenerator()
        # Advance ID generator past highest existing ID
        if self._tasks:
            max_id = max(t.id for t in self._tasks.values())
            for _ in range(max_id):
                self._id_gen.next_id()

    def _save(self):
        self._storage.save_tasks(list(self._tasks.values()))

    def add_task(self, description: str, priority: TaskPriority = TaskPriority.MEDIUM) -> Task:
        if not description or not description.strip():
            raise ValueError("Task description cannot be empty")

        task_id = self._id_gen.next_id()
        task = Task(id=task_id, description=description.strip(), priority=priority)
        self._tasks[task_id] = task
        self._save()
        return task

    def get_all_tasks(self, status: Optional[TaskStatus] = None, priority: Optional[TaskPriority] = None) -> List[Task]:
        tasks = list(self._tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        return tasks

    def search_tasks(self, query: str) -> List[Task]:
        query = query.lower()
        return [t for t in self._tasks.values() if query in t.description.lower()]

    def sort_tasks(self, tasks: List[Task], by: str = "id") -> List[Task]:
        if by == "priority":
            # HIGH (2) > MEDIUM (1) > LOW (0)
            priority_order = {TaskPriority.HIGH: 2, TaskPriority.MEDIUM: 1, TaskPriority.LOW: 0}
            return sorted(tasks, key=lambda t: priority_order.get(t.priority, 0), reverse=True)
        elif by == "status":
            return sorted(tasks, key=lambda t: t.status.value)
        elif by == "id":
            return sorted(tasks, key=lambda t: t.id)
        return tasks

    def update_task(self, task_id: int, description: Optional[str] = None, status: Optional[TaskStatus] = None, priority: Optional[TaskPriority] = None) -> Task:
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} not found")

        task = self._tasks[task_id]
        if description is not None:
            if not description.strip():
                raise ValueError("Task description cannot be empty")
            task.description = description.strip()
        if status is not None:
            task.status = status
        if priority is not None:
            task.priority = priority

        self._save()
        return task

    def delete_task(self, task_id: int) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            self._save()
            return True
        raise KeyError(f"Task with ID {task_id} not found")
