from enum import Enum
from dataclasses import dataclass, field
from typing import Optional

class TaskStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class TaskPriority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

@dataclass
class Task:
    id: int
    description: str
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value
        }
