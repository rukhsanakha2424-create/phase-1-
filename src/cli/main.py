import argparse
import sys
from src.core.service import TaskService
from src.core.models import TaskStatus, TaskPriority

def main():
    service = TaskService()
    parser = argparse.ArgumentParser(description="Evolution of Todo CLI - Phase 1")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")
    add_parser.add_argument("--priority", choices=["LOW", "MEDIUM", "HIGH"], default="MEDIUM", help="Task priority (default: MEDIUM)")

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("--status", choices=["pending", "completed"], help="Filter by status")
    list_parser.add_argument("--priority", choices=["LOW", "MEDIUM", "HIGH"], help="Filter by priority")
    list_parser.add_argument("--sort", choices=["id", "priority", "status"], default="id", help="Sort by (default: id)")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("id", type=int, help="Task ID")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update task description")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("description", help="New description")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    # This represents a skeletal CLI for US implementation
    # Note: Because this is in-memory, we can't actually persistent state between runs
    # as per Phase 1 spec. We will simulate a session loop or just handle individual args.

    args = parser.parse_args()

    if args.command == "add":
        try:
            priority = TaskPriority(args.priority)
            task = service.add_task(args.description, priority=priority)
            print(f"Task added with ID: {task.id}")
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "list":
        # Convert string arguments to enums
        status_filter = TaskStatus(args.status) if args.status else None
        priority_filter = TaskPriority(args.priority) if args.priority else None

        tasks = service.get_all_tasks(status=status_filter, priority=priority_filter)
        tasks = service.sort_tasks(tasks, by=args.sort)

        if not tasks:
            print("Your todo list is empty.")
        else:
            for t in tasks:
                status_mark = "[x]" if t.status == TaskStatus.COMPLETED else "[ ]"
                priority_mark = f"[{t.priority.value}]"
                print(f"{t.id}. {status_mark} {priority_mark} {t.description}")

    elif args.command == "complete":
        try:
            service.update_task(args.id, status=TaskStatus.COMPLETED)
            print(f"Task {args.id} marked as completed.")
        except KeyError as e:
            print(f"Error: {e}")

    elif args.command == "update":
        try:
            service.update_task(args.id, description=args.description)
            print(f"Task {args.id} updated.")
        except (KeyError, ValueError) as e:
            print(f"Error: {e}")

    elif args.command == "delete":
        try:
            service.delete_task(args.id)
            print(f"Task {args.id} deleted.")
        except KeyError as e:
            print(f"Error: {e}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
