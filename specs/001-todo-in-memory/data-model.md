# Data Model: Todo In-Memory CLI

**Feature**: 001-todo-in-memory | **Date**: 2026-01-02

## Task Entity

```python
@dataclass
class Task:
    id: int                          # Unique identifier (1-indexed, sequential)
    description: str                 # Task description (1-1000 chars)
    completed: bool = False          # Completion status
    created_at: datetime = field(default_factory=datetime.utcnow)
```

## Validation Rules

| Field | Rule | Error Message |
|-------|------|---------------|
| description | Must be non-empty | "Task description cannot be empty" |
| description | Max 1000 characters | "Description exceeds maximum length" |
| id | Must exist for operations | "Task with ID {id} not found" |

## State Transitions

```
         ┌─────────────┐
         │   PENDING   │ (default)
         └──────┬──────┘
                │ complete()
         ┌──────▼──────┐
         │   COMPLETE  │
         └─────────────┘
```

## Storage Structure

```python
# In-memory task store (TaskService)
tasks: dict[int, Task] = {}
_next_id: int = 1
```

## Methods

| Method | Input | Output | Side Effects |
|--------|-------|--------|--------------|
| add(description) | str | Task | Adds to tasks dict |
| list() | None | list[Task] | Returns all tasks |
| get(id) | int | Task \| None | Returns task or None |
| update(id, description) | int, str | Task | Modifies description |
| delete(id) | int | bool | Removes from dict |
| complete(id) | int | Task | Sets completed=True |
