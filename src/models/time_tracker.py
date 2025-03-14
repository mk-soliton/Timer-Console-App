"""
Defines the TimeTracker model.

This module represents a time tracker model with id, task_id, category, task,
status, start_time, pause_time, resume_time, stop_time, and total_time.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TimeTracker(BaseModel):
    """Represents a time tracker model for tracking task timings."""

    id: Optional[int] = None
    task_id: int  # Foreign key to the task
    category: str
    task: str
    status: str
    start_time: Optional[datetime] = None
    pause_time: Optional[datetime] = None
    resume_time: Optional[datetime] = None
    stop_time: Optional[datetime] = None
    total_time: float = 0.0

    @classmethod
    def create(
        cls, task_id: int, category: str, task: str, status: str
    ) -> "TimeTracker":
        """Create a new TimeTracker instance.

        Args:
            task_id (int): The task's unique identifier.
            category (str): The task's category.
            task (str): The task name.
            status (str): The task status.

        Returns:
            TimeTracker: A new TimeTracker instance.
        """
        return cls(
            task_id=task_id, category=category, task=task, status=status
        )
