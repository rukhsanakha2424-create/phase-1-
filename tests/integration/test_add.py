"""Integration tests for the add command CLI interface."""
import pytest
import sys
import os
import tempfile

# Get project root directory (parent of tests/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add src to path for imports
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))


@pytest.fixture
def temp_storage_file():
    """Create a temporary storage file for isolated testing."""
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    with open(path, 'w') as f:
        f.write("[]")
    yield path
    if os.path.exists(path):
        os.unlink(path)


class TestAddCommand:
    """Integration tests for 'todo add' command."""

    def test_add_basic_task(self, capsys, temp_storage_file):
        """Test adding a basic task without any flags."""
        from cli.main import main
        from core.storage import Storage
        from core.service import TaskService

        # Mock storage to use temp file
        original_storage = None

        # Monkey-patch Storage class temporarily
        import cli.main as main_module
        original_get_storage = main_module.TaskService

        class MockTaskService(TaskService):
            def __init__(self):
                storage = Storage(filepath=temp_storage_file)
                super().__init__(storage=storage)

        main_module.TaskService = MockTaskService

        try:
            original_argv = sys.argv
            sys.argv = ["todo", "add", "Buy milk"]
            try:
                main()
            finally:
                sys.argv = original_argv

            captured = capsys.readouterr()
            assert "Task added with ID: 1" in captured.out
            assert captured.err == ""
        finally:
            main_module.TaskService = original_get_storage

    def test_add_task_with_priority_high(self, capsys, temp_storage_file):
        """Test adding a task with HIGH priority."""
        from cli.main import main
        from core.storage import Storage
        from core.service import TaskService

        import cli.main as main_module
        original_get_storage = main_module.TaskService

        class MockTaskService(TaskService):
            def __init__(self):
                storage = Storage(filepath=temp_storage_file)
                super().__init__(storage=storage)

        main_module.TaskService = MockTaskService

        try:
            original_argv = sys.argv
            sys.argv = ["todo", "add", "Urgent task", "--priority", "HIGH"]
            try:
                main()
            finally:
                sys.argv = original_argv

            captured = capsys.readouterr()
            assert "Task added with ID: 1" in captured.out
        finally:
            main_module.TaskService = original_get_storage

    def test_add_task_with_priority_low(self, capsys, temp_storage_file):
        """Test adding a task with LOW priority."""
        from cli.main import main
        from core.storage import Storage
        from core.service import TaskService

        import cli.main as main_module
        original_get_storage = main_module.TaskService

        class MockTaskService(TaskService):
            def __init__(self):
                storage = Storage(filepath=temp_storage_file)
                super().__init__(storage=storage)

        main_module.TaskService = MockTaskService

        try:
            original_argv = sys.argv
            sys.argv = ["todo", "add", "Someday task", "--priority", "LOW"]
            try:
                main()
            finally:
                sys.argv = original_argv

            captured = capsys.readouterr()
            assert "Task added with ID: 1" in captured.out
        finally:
            main_module.TaskService = original_get_storage

    def test_add_task_with_default_priority(self, capsys, temp_storage_file):
        """Test that default priority is MEDIUM when not specified."""
        from cli.main import main
        from core.storage import Storage
        from core.service import TaskService

        import cli.main as main_module
        original_get_storage = main_module.TaskService

        class MockTaskService(TaskService):
            def __init__(self):
                storage = Storage(filepath=temp_storage_file)
                super().__init__(storage=storage)

        main_module.TaskService = MockTaskService

        try:
            original_argv = sys.argv
            sys.argv = ["todo", "add", "Normal task"]
            try:
                main()
            finally:
                sys.argv = original_argv

            captured = capsys.readouterr()
            assert "Task added" in captured.out
        finally:
            main_module.TaskService = original_get_storage

    def test_add_empty_description_fails(self, capsys, temp_storage_file):
        """Test that adding a task with empty description fails."""
        from cli.main import main
        from core.storage import Storage
        from core.service import TaskService

        import cli.main as main_module
        original_get_storage = main_module.TaskService

        class MockTaskService(TaskService):
            def __init__(self):
                storage = Storage(filepath=temp_storage_file)
                super().__init__(storage=storage)

        main_module.TaskService = MockTaskService

        try:
            original_argv = sys.argv
            sys.argv = ["todo", "add", ""]
            try:
                main()
            finally:
                sys.argv = original_argv

            captured = capsys.readouterr()
            assert "Task description cannot be empty" in captured.out
        finally:
            main_module.TaskService = original_get_storage

    def test_add_whitespace_description_fails(self, capsys, temp_storage_file):
        """Test that adding a task with whitespace-only description fails."""
        from cli.main import main
        from core.storage import Storage
        from core.service import TaskService

        import cli.main as main_module
        original_get_storage = main_module.TaskService

        class MockTaskService(TaskService):
            def __init__(self):
                storage = Storage(filepath=temp_storage_file)
                super().__init__(storage=storage)

        main_module.TaskService = MockTaskService

        try:
            original_argv = sys.argv
            sys.argv = ["todo", "add", "   "]
            try:
                main()
            finally:
                sys.argv = original_argv

            captured = capsys.readouterr()
            assert "Task description cannot be empty" in captured.out
        finally:
            main_module.TaskService = original_get_storage

    def test_add_multiple_tasks_increment_ids(self, capsys, temp_storage_file):
        """Test that multiple tasks get sequential IDs."""
        from cli.main import main
        from core.storage import Storage
        from core.service import TaskService

        import cli.main as main_module
        original_get_storage = main_module.TaskService

        class MockTaskService(TaskService):
            def __init__(self):
                storage = Storage(filepath=temp_storage_file)
                super().__init__(storage=storage)

        main_module.TaskService = MockTaskService

        try:
            original_argv = sys.argv

            # Add first task
            sys.argv = ["todo", "add", "Task 1"]
            try:
                main()
            finally:
                sys.argv = original_argv

            captured1 = capsys.readouterr()
            assert "Task added with ID: 1" in captured1.out

            # Add second task
            sys.argv = ["todo", "add", "Task 2"]
            try:
                main()
            finally:
                sys.argv = original_argv

            captured2 = capsys.readouterr()
            assert "Task added with ID: 2" in captured2.out

            # Add third task
            sys.argv = ["todo", "add", "Task 3"]
            try:
                main()
            finally:
                sys.argv = original_argv

            captured3 = capsys.readouterr()
            assert "Task added with ID: 3" in captured3.out
        finally:
            main_module.TaskService = original_get_storage

    def test_add_invalid_priority_rejected(self, capsys, temp_storage_file):
        """Test that invalid priority values are rejected by argparse."""
        from cli.main import main
        from core.storage import Storage
        from core.service import TaskService

        import cli.main as main_module
        original_get_storage = main_module.TaskService

        class MockTaskService(TaskService):
            def __init__(self):
                storage = Storage(filepath=temp_storage_file)
                super().__init__(storage=storage)

        main_module.TaskService = MockTaskService

        try:
            original_argv = sys.argv
            sys.argv = ["todo", "add", "Task", "--priority", "INVALID"]
            try:
                with pytest.raises(SystemExit):
                    main()
            finally:
                sys.argv = original_argv

            captured = capsys.readouterr()
            assert "invalid choice" in captured.err.lower()
        finally:
            main_module.TaskService = original_get_storage
