import pytest
import tempfile
import os
from src.core.service import TaskService
from src.core.storage import Storage
from src.core.models import TaskStatus

def _create_service():
    """Create a TaskService with a temporary storage file."""
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    storage = Storage(filepath=path)
    return TaskService(storage=storage), path

def test_add_task():
    service, path = _create_service()
    try:
        task = service.add_task("Test task")
        assert task.id == 1
        assert task.description == "Test task"
        assert task.status == TaskStatus.PENDING
    finally:
        os.unlink(path)

def test_add_empty_task():
    service, path = _create_service()
    try:
        with pytest.raises(ValueError, match="Task description cannot be empty"):
            service.add_task("")
    finally:
        os.unlink(path)

def test_get_all_tasks():
    service, path = _create_service()
    try:
        service.add_task("Task 1")
        service.add_task("Task 2")
        tasks = service.get_all_tasks()
        assert len(tasks) == 2
    finally:
        os.unlink(path)

def test_update_task_status():
    service, path = _create_service()
    try:
        service.add_task("Task 1")
        service.update_task(1, status=TaskStatus.COMPLETED)
        tasks = service.get_all_tasks()
        assert tasks[0].status == TaskStatus.COMPLETED
    finally:
        os.unlink(path)

def test_delete_task():
    service, path = _create_service()
    try:
        service.add_task("Task 1")
        service.delete_task(1)
        assert len(service.get_all_tasks()) == 0
    finally:
        os.unlink(path)

def test_delete_non_existent_task():
    service, path = _create_service()
    try:
        with pytest.raises(KeyError):
            service.delete_task(99)
    finally:
        os.unlink(path)
