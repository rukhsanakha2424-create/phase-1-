# Research: Todo In-Memory CLI Architecture

**Feature**: 001-todo-in-memory | **Date**: 2026-01-02

## Research Questions & Answers

### Q1: Python CLI Argument Parsing Best Practices
**Finding**: Python's `argparse` module (stdlib) is the recommended approach for CLI applications. It's mature, well-documented, and supports subcommands natively via `argparse.ArgumentParser` with `add_subparsers()`.

**Decision**: Use `argparse` with subparsers for the five commands (add, list, update, delete, complete).

### Q2: Task ID Generation Strategy
**Finding**: Options include:
- Sequential integers (1, 2, 3...)
- UUID4 (random unique identifiers)
- UUID1 (time-based)

**Decision**: Use sequential integers (1, 2, 3...) as specified in the assumptions. This provides human-readable, deterministic IDs suitable for CLI interaction.

### Q3: In-Memory Storage Pattern
**Finding**: Simple Python `dict[int, Task]` mapping ID to Task object provides O(1) lookups. For iteration, use `list()` or iterate over dict values directly.

**Decision**: Use `dict[int, Task]` for storage. Use Python dataclass for Task entity.

### Q4: CLI Exit Conventions
**Finding**: CLI tools should exit with:
- `0` on success
- `1` on user errors (invalid input, not found)
- `2` on system errors (unexpected)

**Decision**: Follow standard exit code conventions.

## Alternatives Considered

| Approach | Decision | Rationale |
|----------|----------|-----------|
| Click vs argparse | argparse | Stdlib, no dependencies, sufficient for this use case |
| UUID vs int IDs | int | Human-readable, deterministic, CLI-friendly |
| Global state vs service pattern | Service pattern | Better testability, clear separation |
| Single file vs modular | Modular | Extensibility, follows constitution |

## Best Practices Applied

1. **Layered Architecture**: CLI → Service → Model
2. **Dataclasses**: Type hints, immutability where appropriate
3. **Error Handling**: Domain exceptions translated to user messages
4. **Testing**: Unit tests for core logic, integration for CLI
