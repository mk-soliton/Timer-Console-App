"""
Handle Time Tracking Service.

This module handles time tracking logic for the Time Tracker Console
Application.
It includes functions for starting, pausing, resuming, stopping timers, and
recording timestamps for tasks.
"""

from datetime import datetime
from typing import Optional

from src.data_loader.time_tracker_database import TimeTrackerDatabase
from src.models.time_tracker import TimeTracker


class TimeTrackerService:
    """Service class for handling time tracking operations."""

    def __init__(self, db: Optional[TimeTrackerDatabase] = None) -> None:
        """Initialize the time tracker service with a database instance.

        Args:
            db (Optional[TimeTrackerDatabase], optional): A TimeTrackerDatabase
            instance. If None, a new instance is created. Defaults to None.
        """
        self.db = db if db is not None else TimeTrackerDatabase()

    def start_timer(
        self, task_id: int, category: str, task: str
    ) -> TimeTracker:
        """Start the timer for a task.

        Args:
            task_id (int): The task ID.
            category (str): The category of the task.
            task (str): The task description.

        Returns:
            TimeTracker: The time tracker object.
        """
        time_tracker = TimeTracker.create(
            task_id=task_id, category=category, task=task, status="In Progress"
        )
        time_tracker.start_time = datetime.now()
        self.db.save_time_tracker(time_tracker)
        return time_tracker

    def pause_timer(self, task_id: int) -> Optional[TimeTracker]:
        """Pause the timer for a task.

        Args:
            task_id (int): The task ID.

        Returns:
            Optional[TimeTracker]: The time tracker instance.
        """
        active_tracker = self.db.get_active_time_tracker(task_id)
        if (
            active_tracker
            and active_tracker.start_time
            and not active_tracker.stop_time
        ):
            active_tracker.stop_time = datetime.now()
            active_tracker.status = "Paused"
            # Calculate total time so far
            elapsed_time = (
                active_tracker.stop_time - active_tracker.start_time
            ).total_seconds()
            active_tracker.total_time = elapsed_time
            self.db.save_time_tracker(active_tracker)
            return active_tracker
        return None

    def resume_timer(
        self, task_id: int, category: str
    ) -> Optional[TimeTracker]:
        """Resume the timer for a task.

        Args:
            task_id (int): The task ID.
            category (str): The task category.

        Returns:
            Optional[TimeTracker]: The time tracker instance.
        """
        paused_tracker = self.db.get_last_paused_time_tracker(task_id)
        if paused_tracker:
            time_tracker = TimeTracker.create(
                task_id=task_id, status="In Progress", category=category
            )
            time_tracker.start_time = datetime.now()
            self.db.save_time_tracker(time_tracker)
            return time_tracker
        return None

    def stop_timer(self, task_id: int) -> Optional[TimeTracker]:
        """Stop the timer for a task and calculate the total time.

        Args:
            task_id (int): The task ID.

        Returns:
            Optional[TimeTracker]: The time tracker instance.
        """
        active_tracker = self.db.get_active_time_tracker(task_id)
        if active_tracker and active_tracker.start_time:
            active_tracker.stop_time = datetime.now()
            active_tracker.status = "Completed"
            # Calculate total time
            elapsed_time = (
                active_tracker.stop_time - active_tracker.start_time
            ).total_seconds()
            active_tracker.total_time = elapsed_time
            self.db.save_time_tracker(active_tracker)
            return active_tracker
        return None

    def get_task_timings(self, task_id: int) -> Optional[TimeTracker]:
        """Retrieve the timings for a specific task.

        Args:
            task_id (int): The task ID.

        Returns:
            Optional[TimeTracker]: The time tracker object.
        """
        return self.db.get_active_time_tracker(task_id)
