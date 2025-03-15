time_tracker_controller.py

from datetime import datetime
from typing import Optional
from rich.console import Console
from src.services.notification_service import NotificationService
from src.services.task_service import TaskService
from src.services.time_tracker_service import TimeTrackerService

class TimeTrackerController:
    """Controller for handling time tracking operations."""
    def __init__(self, user_id: int, task_id: int) -> None:
        self.user_id = user_id
        self.task_id = task_id
        self.console = Console()
        self.time_tracker_service = TimeTrackerService()
        self.notification_service = NotificationService(
            task_service=TaskService(),
            time_tracker_service=self.time_tracker_service,
        )

    def start_timer(self, category: str) -> None:
        """Start the timer for a task."""
        self.time_tracker_service.start_timer(self.task_id, category)
        self.console.print(f"[green]Timer started for task ID: {self.task_id}[/green]")
        self.notification_service.check_task_duration(self.user_id, self.task_id)
 
    def pause_timer(self) -> None:
        """Pause the timer for a task."""
        time_tracker = self.time_tracker_service.pause_timer(self.task_id)
        if time_tracker:
            self.console.print(f"[yellow]Timer paused for task ID: {self.task_id}[/yellow]")
            # Call the notification service
            notification = self.notification_service.check_task_duration(self.user_id, self.task_id)
            if notification:
                self.console.print(f"[yellow]{notification}[/yellow]")
        else:
            self.console.print("[red]No active timer to pause.[/red]")
 
    def stop_timer(self) -> None:
        """Stop the timer for a task and calculate the total time."""
        time_tracker = self.time_tracker_service.stop_timer(self.task_id)
        if time_tracker:
            elapsed_time = time_tracker.total_time
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.console.print(
                f"[green]Timer stopped for task ID: {self.task_id}. "
                f"Total time: {int(hours)}h {int(minutes)}m {int(seconds)}s[/green]"
            )
            self.notification_service.check_task_duration(self.user_id, self.task_id)
        else:
            self.console.print("[red]No active timer to stop.[/red]")
 
    def resume_timer(self, category: str) -> None:
        """Resume the timer for a task."""
        time_tracker = self.time_tracker_service.resume_timer(self.task_id, category)
        if time_tracker:
            self.console.print(
                f"[green]Timer resumed for task ID: {self.task_id}[/green]"
            )
        else:
            self.console.print("[red]No paused timer to resume.[/red]")
 
 
    def update_time_tracker(self, start_time: Optional[datetime], stop_time: Optional[datetime]) -> None:
        """Update the start and stop timings of a time tracker."""
        time_tracker = self.time_tracker_service.get_active_time_tracker(self.task_id)
        if time_tracker:
            time_tracker.start_time = start_time
            time_tracker.stop_time = stop_time
            self.time_tracker_service.db.update_time_tracker(time_tracker)
            self.console.print("[green]Time tracker updated successfully.[/green]")
        else:
            self.console.print("[red]No active time tracker found.[/red]")
