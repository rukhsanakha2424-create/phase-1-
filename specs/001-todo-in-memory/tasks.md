# Implementation Tasks: Todo In-Memory CLI

**Branch**: `001-todo-in-memory` | **Date**: 2026-01-02
**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md)

## Task Summary

1. Task model ✅ (done)
2. InMemoryStorage ✅ (done)
3. TaskService methods ✅ (done - needs toggle fix)
4. CLI commands ✅ (done)
5. Validation & error messages ✅ (done)
6. Verify behavior via CLI commands ⬅️ **DOING THIS**

---

## Task 1: Define Task model ✅ DONE

**Status**: Complete - `src/core/models.py`

- `Task` dataclass with `id`, `description`, `completed` fields
- Integer-based ID (auto-incremented)
- `to_dict()` method for potential future serialization

---

## Task 2: Implement InMemoryStorage ✅ DONE

**Status**: Complete - `src/core/storage.py`

- Dict-based storage: `_tasks: Dict[int, Task]`
- Methods: `get_all()`, `get()`, `save()`, `delete()`, `clear()`, `count()`

---

## Task 3: Implement TaskService methods ✅ DONE (needs toggle)

**Status**: Partial - `src/core/service.py`

| Method | Status | Notes |
|--------|--------|-------|
| `add` | ✅ | Validates non-empty description |
| `list` | ✅ | Returns all tasks |
| `update` | ✅ | Updates description by ID |
| `delete` | ✅ | Removes task by ID |
| `complete` | ⚠️ | Only marks complete - needs toggle |

### Task 3.1: Fix toggle functionality

**Description**: The spec says "toggle completion status" but current `complete()` only marks tasks as complete. Need to toggle (complete ↔ incomplete).

**File**: `src/core/service.py`

**Changes**:
- Rename `complete()` → `toggle()` or add new `toggle()` method
- Toggle should flip `completed` boolean (True → False, False → True)
- Update CLI `complete` command to call `toggle()`

**Acceptance Criteria**:
- [ ] Running complete on incomplete task marks it complete
- [ ] Running complete on complete task marks it incomplete
- [ ] Error handling for invalid task ID unchanged

---

## Task 4: Implement CLI commands ✅ DONE

**Status**: Complete - `src/cli/main.py`

Commands implemented:
- `todo add "description"` → Add new task
- `todo list` → Display all tasks
- `todo update <id> "description"` → Update task
- `todo delete <id>` → Remove task
- `todo complete <id>` → Mark complete (needs toggle)

---

## Task 5: Basic validation & error messages ✅ DONE

**Status**: Complete

Error handling:
- Empty description → "Error: Description cannot be empty"
- Invalid task ID → "Error: Task {id} not found"
- Invalid arguments → argparse errors

---

## Task 6: Verify behavior via CLI commands

**Description**: Test all functionality works as expected.

### 6.1: Verify CLI entry point

```bash
python -m src.cli.main --help
# Expected: Shows todo commands
```

### 6.2: Test add command

```bash
python -m src.cli.main add "Buy groceries"
python -m src.cli.main add "Call mom"
python -m src.cli.main add "Finish project"
# Expected: Each adds a task with IDs 1, 2, 3
```

### 6.3: Test list command

```bash
python -m src.cli.main list
# Expected: Shows 3 tasks with [ ] status
```

### 6.4: Test complete command (toggle)

```bash
python -m src.cli.main complete 1
python -m src.cli.main complete 2
python -m src.cli.main list
# Expected: Tasks 1 and 2 show [x], task 3 shows [ ]

python -m src.cli.main complete 1
python -m src.cli.main list
# Expected: Task 1 toggles back to [ ] (if toggle fixed)
```

### 6.5: Test update command

```bash
python -m src.cli.main update 1 "Buy milk and eggs"
python -m src.cli.main list
# Expected: Task 1 description updated
```

### 6.6: Test delete command

```bash
python -m src.cli.main delete 3
python -m src.cli.main list
# Expected: Only tasks 1 and 2 remain
```

### 6.7: Test error handling

```bash
python -m src.cli.main add ""
# Expected: "Error: Description cannot be empty"

python -m src.cli.main complete 999
# Expected: "Error: Task 999 not found"

python -m src.cli.main update 999 "test"
# Expected: "Error: Task 999 not found"

python -m src.cli.main delete 999
# Expected: "Error: Task 999 not found"
```

---

## Task 7: Run tests

```bash
# Run all tests
python -m pytest tests/ -v

# Expected: All tests pass
```

---

## Definition of Done

All tasks complete when:
- [ ] Toggle functionality works (complete → incomplete, incomplete → complete)
- [ ] All 5 commands work correctly via CLI
- [ ] All error messages are user-friendly
- [ ] `python -m pytest tests/` passes 100%
- [ ] Manual CLI verification complete for all scenarios
