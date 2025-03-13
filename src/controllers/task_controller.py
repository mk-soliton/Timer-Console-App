"""
Handles task controller.

This module contains the TaskController class which is responsible for handling
task management operations like creating, updating, and deleting tasks.
"""

from typing import Optional

import inquirer  # type: ignore
from rich.console import Console
from rich.panel import Panel

from src.controllers.time_tracker_controller import TimeTrackerController
from src.services.category_service import CategoryService
from src.services.task_service import TaskService


class TaskController:
    """Controller for handling task management operations."""

    def __init__(
        self,
        user_id: int,
        task_service: TaskService,
        category_service: CategoryService,
    ) -> None:
        """Initialize the TaskController.

        Args:
            user_id (int): The ID of the logged-in user.
            task_service (TaskService): The task service instance.
            category_service (CategoryService): The category service instance.
        """
        self.user_id = user_id
        self.task_service = task_service
        self.category_service = category_service
        self.console = Console()

    def show_dashboard(self) -> Optional[str]:
        """Display the updated dashboard with current and recent tasks.

        Returns:
            Optional[str]: The action to take after displaying the dashboard.
        """
        tasks = self.task_service.get_tasks(self.user_id)
        current_tasks = [
            task
            for task in tasks
            if task.task_status in ["In Progress", "Paused"]
        ]
        recent_tasks = [
            task for task in tasks if task.task_status == "Completed"
        ]

        self.console.print(
            Panel.fit("[bold magenta]Current Tasks[/bold magenta]")
        )
        if current_tasks:
            for task in current_tasks:
                self.console.print(
                    f"[cyan]Status: {task.task_status}[/cyan] | "
                    f"Task: {task.task_name} | "
                    f"Category: {task.category_name}"
                )
        else:
            self.console.print("[yellow]No current tasks.[/yellow]")

        self.console.print(
            Panel.fit("[bold magenta]Recent Tasks[/bold magenta]")
        )
        if recent_tasks:
            for task in recent_tasks:
                self.console.print(
                    f"[cyan]Status: {task.task_status}[/cyan] | "
                    f"Task: {task.task_name} | "
                    f"Category: {task.category_name}"
                )
        else:
            self.console.print("[yellow]No recent tasks.[/yellow]")

        return self.show_task_menu()

    def show_task_menu(self) -> Optional[str]:
        """Display the task management menu with dynamic options.

        Returns:
            Optional[str]: The action to take after displaying the task menu.
        """
        tasks = self.task_service.get_tasks(self.user_id)
        task_choices = [
            ("Create New Task", "create"),
            *[
                (
                    f"Status: {task.task_status} | "
                    f"Task: {task.task_name} | "
                    f"Category: {task.category_name}",
                    task.id,
                )
                for task in tasks
            ],
            ("Back", "back"),
        ]

        questions = [
            inquirer.List(
                "task",
                message="Select a task or create a new one:",
                choices=task_choices,
            )
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            return None

        selected_task_id = answers["task"]
        if selected_task_id == "create":
            self.create_task()  # Fix: Ensure create_task is defined
        elif selected_task_id == "logout":
            return "logout"  # Go back to the dashboard
        else:
            self.handle_task_options(int(selected_task_id))

        return None

    def create_task(self) -> None:
        """Handle the creation of a new task."""
        questions = [
            inquirer.Text("category", message="Enter category"),
            inquirer.Text("task_name", message="Enter task/activity name"),
            inquirer.Text(
                "duration", message="Enter duration (in hours)", default="0"
            ),
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            return

        category_name = answers["category"]
        task_name = answers["task_name"]

        try:
            duration = float(answers["duration"])
        except ValueError:
            duration = 0.0

        category_obj = self.category_service.create_category(category_name)

        if not category_obj or not hasattr(category_obj, "name"):
            self.console.print(
                f"[red]Failed to create/retrieve category '{category_name}'"
                "[/red]"
            )
            return

        task = self.task_service.create_task(
            self.user_id, category_obj.name, task_name, duration
        )
        self.console.print(
            f"[green]Task created successfully with ID: {task.id}[/green]"
        )

    def handle_task_options(self, task_id: int) -> Optional[str]:
        """Handle the options for a selected task.

        Args:
            task_id (int): The ID of the selected task.

        Returns:
            Optional[str]: The action to take after handling the task options.
        """
        task = self.task_service.get_task_by_id(self.user_id, task_id)
        if not task:
            self.console.print("[red]Task not found.[/red]")
            return None

        time_tracker = TimeTrackerController(
            user_id=self.user_id,
            task_id=task_id,
            category=task.category_name,
            task=task.task_name,
        )

        if task.task_status == "Not Started":
            options = ["Start Task", "Update Task", "Delete Task", "Log Out"]
        elif task.task_status == "In Progress":
            options = [
                "Pause Task",
                "Stop Task",
                "Update Task",
                "Delete Task",
                "Log Out",
            ]
        elif task.task_status == "Paused":
            options = [
                "Resume Task",
                "Stop Task",
                "Update Task",
                "Delete Task",
                "Log Out",
            ]
        elif task.task_status == "Completed":
            options = ["Edit Timing", "Update Task", "Delete Task", "Log Out"]
        else:
            options = []

        questions = [
            inquirer.List(
                "action",
                message="Select an action:",
                choices=options,
            )
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            return None

        action = answers["action"]
        if action == "Start Task":
            time_tracker.start_timer()
            self.task_service.update_task_status(task_id, "In Progress")
            self.show_dashboard()
        elif action == "Pause Task":
            time_tracker.pause_timer()
            self.task_service.update_task_status(task_id, "Paused")
            self.show_dashboard()
        elif action == "Resume Task":
            time_tracker.resume_timer()
            self.task_service.update_task_status(task_id, "In Progress")
            self.show_dashboard()
        elif action == "Stop Task":
            time_tracker.stop_timer()
            self.task_service.update_task_status(task_id, "Completed")
            self.show_dashboard()
        elif action == "Update Task":
            self.update_task(task_id)
            self.show_dashboard()
        elif action == "Delete Task":
            self.delete_task(task_id)
            self.show_dashboard()
        elif action == "Edit Timing":
            self.console.print(
                "[yellow]Edit Timing feature is under development.[/yellow]"
            )
            self.show_dashboard()
        elif action == "Log Out":
            return "logout"
        return None

    def update_task(self, task_id: int) -> None:
        """Update an existing task.

        Args:
            task_id (int): The ID of the task to update.
        """
        questions = [
            inquirer.Text("category", message="Enter new category name"),
            inquirer.Text("task_name", message="Enter new task/activity name"),
            inquirer.Text(
                "duration",
                message="Enter new duration (in hours)",
                default="0",
            ),
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            return

        category_name = answers["category"]
        task_name = answers["task_name"]

        try:
            duration = float(answers["duration"])
        except ValueError:
            duration = 0.0

        self.task_service.update_task(
            self.user_id, task_id, category_name, task_name, duration
        )
        self.console.print("[green]Task updated successfully.[/green]")

    def delete_task(self, task_id: int) -> None:
        """Delete an existing task.

        Args:
            task_id (int): The ID of the task to delete.
        """
        self.task_service.delete_task(self.user_id, task_id)
        self.console.print("[green]Task deleted successfully.[/green]")
