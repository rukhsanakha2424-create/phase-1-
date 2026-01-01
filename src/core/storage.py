import json
import os
from typing import List
from src.core.models import Task, TaskStatus, TaskPriority

class Storage:
    def __init__(self, filepath: str = "data/todos.json"):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump([], f)

    def load_tasks(self) -> List[Task]:
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                return [Task(
                    id=item['id'],
                    description=item['description'],
                    status=TaskStatus(item['status']),
                    priority=TaskPriority(item.get('priority', 'MEDIUM'))
                ) for item in data]
        except (json.JSONDecodeError, KeyError, ValueError):
            return []

    def save_tasks(self, tasks: List[Task]):
        data = [task.to_dict() for task in tasks]
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)
