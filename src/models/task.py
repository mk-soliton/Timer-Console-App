"""
Defines Task model.

This module represents a task model with id, category, task, task_duration,
and owner_id.
"""

from typing import Optional

from pydantic import BaseModel


class Task(BaseModel):
    """Represent a task model using Pydantic for validation."""

    id: Optional[int] = None
    user_id: int
    category_id: int
    task_name: str
    duration: float = 0.0

    @classmethod
    def create(
        cls,
        user_id: int,
        category_id: int,
        task_name: str,
        duration: float = 0.0,
    ) -> "Task":
        """
        Create new task.

        Factory method to create a new Task instance.

        Args:
            user_id (int): The user's unique identifier.
            category_id (int): The category's unique identifier.
            task_name (str): The task name.
            duration (float, optional): The task duration. Defaults to 0.0.

        Returns:
            Task: A new Task instance.
        """
        return cls(
            user_id=user_id,
            category_id=category_id,
            task_name=task_name,
            duration=duration,
        )
