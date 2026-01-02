# Implementation Plan: Todo In-Memory CLI

**Branch**: `001-todo-in-memory` | **Date**: 2026-01-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-in-memory/spec.md`

## Summary

Design and implement a clean, minimal in-memory Todo CLI application in Python 3.13+. The architecture follows a three-layer pattern (CLI, Core, Storage) with tasks stored in memory using Python data structures. All five core operations (add, list, update, delete, toggle) are supported via command-line arguments using argparse. Task IDs are auto-incremented integers stored in memory.

## Technical Context

**Language/Version**: Python 3.13+ (as per constitution and user requirements)
**Primary Dependencies**: argparse (stdlib), dataclasses (stdlib)
**Storage**: In-memory only (Python dict) - no persistence
**Testing**: pytest (unit tests for core logic, integration tests for CLI)
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux)
**Project Type**: Single Python package (CLI application)
**Performance Goals**: Sub-5-second command execution, minimal memory footprint (<50MB)
**Constraints**: No files, databases, or external services; data resets on restart
**Scale/Scope**: Single-user local session (~100s of tasks max)

## Architecture (User-Specified)

```
┌─────────────────────────────────────────┐
│           CLI Layer                     │
│      (src/cli/main.py)                  │
│   - Parses commands with argparse       │
│   - Prints output to console            │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│           Core Layer                    │
│      (src/core/service.py)              │
│   - Task business logic                 │
│   - Orchestrates storage operations     │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│         Storage Layer                   │
│     (src/core/storage.py)               │
│   - In-memory dict for tasks            │
│   - Auto-incremented task IDs           │
│   - One instance per runtime            │
└────────────────┬────────────────────────┘
                 │
                 ▼
            Output / Errors
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Task IDs auto-incremented in memory | Simple, deterministic, fits spec requirements |
| One service instance per runtime | Single source of truth for task state |
| Errors shown explicitly | No silent failures (constitution rule) |
| No persistence layer | Phase I constraint - data resets on exit |

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| Spec-driven development | ✅ PASS | All functionality derived from spec.md |
| Phase I constraints | ✅ PASS | In-memory only, CLI interface, no persistence |
| Clean separation of concerns | ✅ PASS | CLI/Core/Storage layers defined |
| Simplicity over optimization | ✅ PASS | Using stdlib only, minimal dependencies |
| Forward compatibility | ✅ PASS | No future phase influence in Phase I design |
| Spec is authority | ✅ PASS | No features beyond spec scope |
| Smallest viable diff | ✅ PASS | Single package, focused scope |

## Project Structure

### Source Code (repository root)

```text
src/
├── __init__.py
├── cli/
│   ├── __init__.py
│   └── main.py          # Entry point: python -m src.cli.main
├── core/
│   ├── __init__.py
│   ├── models.py        # Task dataclass
│   ├── storage.py       # InMemoryStorage (dict + auto-increment ID)
│   └── service.py       # TaskService (business logic)
└── utils/
    └── __init__.py      # Shared utilities (empty for Phase I)

tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_models.py   # Task dataclass tests
│   ├── test_storage.py  # InMemoryStorage tests
│   └── test_service.py  # TaskService tests
└── integration/
    ├── __init__.py
    └── test_cli.py      # CLI command integration tests
```

**Structure Decision**: Three-layer architecture as specified by user:
- **CLI Layer** (`src/cli`): Command parsing and output
- **Core Layer** (`src/core`): Models, Storage, and Service
- **Utilities** (`src/utils`): Reserved for future phases

### Data Flow

| Operation | Flow |
|-----------|------|
| Add Task | CLI → Service.add() → Storage.create() |
| View Tasks | CLI → Service.list() → Storage.get_all() → Output |
| Update Task | CLI → Service.update() → Storage.modify() |
| Delete Task | CLI → Service.delete() → Storage.remove() |
| Toggle Complete | CLI → Service.toggle() → Storage.update_status() |

## Complexity Tracking

*No constitution violations requiring justification.*
