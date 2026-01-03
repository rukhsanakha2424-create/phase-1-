#!/usr/bin/env python3
"""Interactive Todo Application - Phase I
Menu-driven, in-memory console application.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Task:
    """Represents a single todo task."""
    id: int
    description: str
    completed: bool = False


class TodoApp:
    """Interactive Todo Application with menu-driven interface."""

    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id = 1

    def add_task(self):
        """Add a new task to the list."""
        description = input("Enter task description: ").strip()

        if not description:
            print("Error: Description cannot be empty")
            return

        task = Task(id=self.next_id, description=description)
        self.tasks.append(task)
        self.next_id += 1
        print("Task added successfully")

    def view_all_tasks(self):
        """Display all tasks."""
        if not self.tasks:
            print("No tasks available")
            return

        print("--- All Tasks ---")
        for task in self.tasks:
            status = "[x]" if task.completed else "[ ]"
            print(f"{task.id}. {status} {task.description}")
        print("-----------------")

    def update_task(self):
        """Update an existing task's description."""
        if not self.tasks:
            print("No tasks available")
            return

        self.view_all_tasks()
        task_id_input = input("Enter Task ID to update: ").strip()

        if not task_id_input:
            print("Error: Task ID cannot be empty")
            return

        try:
            task_id = int(task_id_input)
        except ValueError:
            print("Error: Invalid Task ID")
            return

        task = self._find_task(task_id)
        if task is None:
            print(f"Error: Task {task_id} not found")
            return

        new_description = input("Enter new description: ").strip()

        if not new_description:
            print("Error: Description cannot be empty")
            return

        task.description = new_description
        print(f"Task {task_id} updated successfully")

    def delete_task(self):
        """Delete a task from the list."""
        if not self.tasks:
            print("No tasks available")
            return

        self.view_all_tasks()
        task_id_input = input("Enter Task ID to delete: ").strip()

        if not task_id_input:
            print("Error: Task ID cannot be empty")
            return

        try:
            task_id = int(task_id_input)
        except ValueError:
            print("Error: Invalid Task ID")
            return

        task = self._find_task(task_id)
        if task is None:
            print(f"Error: Task {task_id} not found")
            return

        self.tasks.remove(task)
        print(f"Task {task_id} deleted successfully")

    def mark_complete(self):
        """Mark a task as completed."""
        if not self.tasks:
            print("No tasks available")
            return

        self.view_all_tasks()
        task_id_input = input("Enter Task ID to mark complete: ").strip()

        if not task_id_input:
            print("Error: Task ID cannot be empty")
            return

        try:
            task_id = int(task_id_input)
        except ValueError:
            print("Error: Invalid Task ID")
            return

        task = self._find_task(task_id)
        if task is None:
            print(f"Error: Task {task_id} not found")
            return

        task.completed = True
        print(f"Task {task_id} marked as complete")

    def mark_incomplete(self):
        """Mark a task as incomplete."""
        if not self.tasks:
            print("No tasks available")
            return

        self.view_all_tasks()
        task_id_input = input("Enter Task ID to mark incomplete: ").strip()

        if not task_id_input:
            print("Error: Task ID cannot be empty")
            return

        try:
            task_id = int(task_id_input)
        except ValueError:
            print("Error: Invalid Task ID")
            return

        task = self._find_task(task_id)
        if task is None:
            print(f"Error: Task {task_id} not found")
            return

        task.completed = False
        print(f"Task {task_id} marked as incomplete")

    def _find_task(self, task_id: int) -> Task | None:
        """Find a task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def show_menu(self):
        """Display the main menu."""
        print("\n--- Todo Application ---")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete")
        print("6. Mark Task Incomplete")
        print("7. Exit")
        print("-------------------------")

    def run(self):
        """Main application loop."""
        while True:
            self.show_menu()
            choice = input("Enter your choice (1-7): ").strip()

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.view_all_tasks()
            elif choice == "3":
                self.update_task()
            elif choice == "4":
                self.delete_task()
            elif choice == "5":
                self.mark_complete()
            elif choice == "6":
                self.mark_incomplete()
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Error: Invalid choice. Please enter a number between 1 and 7")


def main():
    """Entry point for the Todo application."""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()
