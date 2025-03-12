"""
Handle Task Service.

This module handles task management logic for the Time Tracker Console
Application.
It includes functions for creating, editing, deleting, and categorizing tasks.
"""

from typing import List, Optional

from src.data_loader.category_database import CategoryDatabase
from src.data_loader.task_database import TaskDatabase
from src.models.task import Task


class TaskService:
    """Service class for managing tasks."""

    def __init__(
        self,
        task_db: Optional[TaskDatabase] = None,
        category_db: Optional[CategoryDatabase] = None,
    ) -> None:
        """Initialize the task service with database instances."""
        self.task_db = task_db if task_db is not None else TaskDatabase()
        self.category_db = (
            category_db if category_db is not None else CategoryDatabase()
        )

    def create_task(
        self,
        user_id: int,
        category_name: str,
        task_name: str,
        duration: float = 0.0,
    ) -> Task:
        """Create a new task, ensuring category exists."""
        category = self.category_db.get_or_create_category(category_name)

        if not category or category.id is None:
            raise ValueError(
                f"Category '{category_name}' could not be created/retrieved."
            )

        category_id: int = category.id  # Ensure category_id is always an int

        new_task = Task.create(
            user_id=user_id,
            category_id=category_id,  # Now guaranteed to be int
            task_name=task_name,
            duration=duration,
        )

        self.task_db.save_task(new_task)
        return new_task

    def get_tasks(self, user_id: int) -> List[Task]:
        """Retrieve all tasks for a given user."""
        return self.task_db.get_tasks_by_user(user_id)

    def delete_task(self, user_id: int, task_id: int) -> None:
        """Delete a task by task ID for the given user."""
        self.task_db.delete_task(user_id, task_id)
