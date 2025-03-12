"""
Handles task controller.

This module contains the TaskController class which is responsible for handling
task management operations like creating, updating, and deleting tasks.
"""

import inquirer  # type: ignore
from rich.console import Console

from src.services.category_service import CategoryService
from src.services.task_service import TaskService


class TaskController:
    def __init__(
        self,
        user_id: int,
        task_service: TaskService,
        category_service: CategoryService,
    ) -> None:
        self.user_id = user_id
        self.task_service = task_service
        self.category_service = category_service
        self.console = Console()

    def show_menu(self) -> None:
        while True:
            self.console.print("\n[cyan]Task Management Menu:[/cyan]")
            questions = [
                inquirer.List(
                    "action",
                    message="Select an action:",
                    choices=[
                        "View Tasks",
                        "Create Task",
                        "Delete Task",
                        "Update Task",
                        "Log out",
                    ],
                )
            ]
            answers = inquirer.prompt(questions)
            if not answers:
                break
            if answers["action"] == "View Tasks":
                self.view_tasks()
            elif answers["action"] == "Create Task":
                self.create_task()
            elif answers["action"] == "Update Task":
                self.console.print(
                    "[yellow]Update feature implementation is in progress."
                    "[/yellow]"
                )
                # self.update_task()
            elif answers["action"] == "Delete Task":
                self.delete_task()
            elif answers["action"] == "Log out":
                break

    def view_tasks(self) -> None:
        tasks = self.task_service.get_tasks(self.user_id)
        if not tasks:
            self.console.print("[yellow]No tasks found.[/yellow]")
            return
        self.console.print("[bold magenta]Your Tasks:[/bold magenta]")
        for task in tasks:
            self.console.print(
                f"ID: {task.id} | Task: {task.task_name} | "
                f"Duration: {task.duration} | Category: {task.category_name} |"
                f"Task Status: {task.task_status}"
            )

    def create_task(self) -> None:
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
                f"[red]Failed to create/retrieve category "
                f"'{category_name}'[/red]"
            )
            return

        task = self.task_service.create_task(
            self.user_id, category_obj.name, task_name, duration
        )

        self.console.print(
            f"[green]Task created successfully with ID: {task.id}[/green]"
        )

    def update_task(self) -> None:
        questions = [
            inquirer.Text("task_id", message="Enter Task ID to update"),
            inquirer.Text("category", message="Enter new category"),
            inquirer.Text("task_name", message="Enter new task/activity name"),
            inquirer.Text("duration", message="Enter new duration (in hours)"),
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            return
        try:
            task_id = int(answers["task_id"])
            category_name = answers["category"]
            task_name = answers["task_name"]
            duration = float(answers["duration"])
            self.task_service.update_task(
                self.user_id, task_id, category_name, task_name, duration
            )
            self.console.print("[green]Task updated successfully.[/green]")
        except ValueError:
            self.console.print("[red]Invalid Task ID or duration.[/red]")

    def delete_task(self) -> None:
        questions = [
            inquirer.Text("task_id", message="Enter Task ID to delete")
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            return
        try:
            task_id = int(answers["task_id"])
            self.task_service.delete_task(self.user_id, task_id)
            self.console.print("[green]Task deleted successfully.[/green]")
        except ValueError:
            self.console.print("[red]Invalid Task ID.[/red]")
