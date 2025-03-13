"""
Handles time tracking operations.

This module contains the controller for handling time tracking operations like
starting, pausing, resuming, and stopping the timer for a task.
"""

from rich.console import Console

from src.services.time_tracker_service import TimeTrackerService


class TimeTrackerController:
    """Controller for handling time tracking operations."""

    def __init__(
        self, user_id: int, task_id: int, category: str, task: str
    ) -> None:
        """Initialize the time tracker controller with necessary attributes.

        Args:
            user_id (int): The ID of the user.
            task_id (int): The ID of the task.
            category (str): The category of the task.
            task (str): The name of the task.
        """
        self.user_id = user_id
        self.task_id = task_id
        self.category = category
        self.task = task
        self.console = Console()
        self.time_tracker_service = TimeTrackerService()

    def start_timer(self) -> None:
        """Start the timer for a task."""
        self.time_tracker_service.start_timer(
            self.task_id, self.category, self.task
        )
        self.console.print(
            f"[green]Timer started for task ID: {self.task_id}[/green]"
        )

    def pause_timer(self) -> None:
        """Pause the timer for a task."""
        time_tracker = self.time_tracker_service.pause_timer(self.task_id)
        if time_tracker:
            self.console.print(
                f"[yellow]Timer paused for task ID: {self.task_id}[/yellow]"
            )
        else:
            self.console.print("[red]No active timer to pause.[/red]")

    def resume_timer(self) -> None:
        """Resume the timer for a task."""
        time_tracker = self.time_tracker_service.resume_timer(self.task_id)
        if time_tracker:
            self.console.print(
                f"[green]Timer resumed for task ID: {self.task_id}[/green]"
            )
        else:
            self.console.print("[red]No paused timer to resume.[/red]")

    def stop_timer(self) -> None:
        """Stop the timer for a task and calculates the total time."""
        time_tracker = self.time_tracker_service.stop_timer(self.task_id)
        if time_tracker:
            self.console.print(
                f"[green]Timer stopped for task ID: {self.task_id}. "
                f"Total time: {time_tracker.total_time} seconds[/green]"
            )
        else:
            self.console.print("[red]No active timer to stop.[/red]")
