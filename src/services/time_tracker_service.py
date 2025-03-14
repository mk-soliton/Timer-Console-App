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
        """Initialize the time tracker service with a database instance."""
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
            Optional[TimeTracker]: The time tracker object.
        """
        time_tracker = self.db.get_active_time_tracker(task_id)
        if (
            time_tracker
            and time_tracker.start_time
            and not time_tracker.pause_time
        ):
            time_tracker.pause_time = datetime.now()
            time_tracker.status = "Paused"
            self.db.update_time_tracker(time_tracker)
            return time_tracker
        return None

    def resume_timer(self, task_id: int) -> Optional[TimeTracker]:
        """Resume the timer for a task.

        Args:
            task_id (int): The task ID.

        Returns:
            Optional[TimeTracker]: The time tracker object.
        """
        time_tracker = self.db.get_active_time_tracker(task_id)
        if time_tracker and time_tracker.pause_time:
            time_tracker.resume_time = datetime.now()
            time_tracker.status = "In Progress"
            self.db.update_time_tracker(time_tracker)
            return time_tracker
        return None

    def stop_timer(self, task_id: int) -> Optional[TimeTracker]:
        """Stop the timer for a task and calculates the total time.

        Args:
            task_id (int): The task ID.

        Returns:
            Optional[TimeTracker]: The time tracker object.
        """
        time_tracker = self.db.get_active_time_tracker(task_id)
        if time_tracker and time_tracker.start_time:
            time_tracker.stop_time = datetime.now()
            time_tracker.status = "Completed"

            # Calculate total time
            if time_tracker.pause_time and time_tracker.resume_time:
                total_paused_time = (
                    time_tracker.resume_time - time_tracker.pause_time
                ).total_seconds()
                total_time = (
                    time_tracker.stop_time - time_tracker.start_time
                ).total_seconds() - total_paused_time
            else:
                total_time = (
                    time_tracker.stop_time - time_tracker.start_time
                ).total_seconds()

            time_tracker.total_time = total_time
            self.db.update_time_tracker(time_tracker)
            return time_tracker
        return None

    def get_task_timings(self, task_id: int) -> Optional[TimeTracker]:
        """Retrieve the timings for a specific task.

        Args:
            task_id (int): The task ID.

        Returns:
            Optional[TimeTracker]: The time tracker object.
        """
        return self.db.get_active_time_tracker(task_id)
