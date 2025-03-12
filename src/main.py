"""
main.py module.

This module is the entry point for Time Tracker Console Application.
"""

import inquirer  # type: ignore
from rich.console import Console
from rich.panel import Panel

from src.controllers.authentication_controller import AuthenticationController
from src.controllers.task_controller import TaskController
from src.services.category_service import CategoryService
from src.services.task_service import TaskService

# Create a Rich console instance
console = Console()


def main() -> None:
    """Run main function to handle authentication and task management."""
    auth_controller = AuthenticationController()
    task_service = TaskService()
    category_service = CategoryService()
    logged_in_user = None

    console.print(
        Panel.fit(
            "[bold magenta]Welcome to Time Tracker App[/bold magenta]",
            title="Time Tracker",
        )
    )

    while True:
        if not logged_in_user:
            questions = [
                inquirer.List(
                    "action",
                    message="What do you want to do?",
                    choices=["Register", "Login", "Exit"],
                )
            ]
            answers = inquirer.prompt(questions)
            if not answers or "action" not in answers:
                console.print("[red]No action selected. Exiting.[/red]")
                break

            action = answers.get("action")

            if action == "Register":
                auth_controller.register_user()

            elif action == "Login":
                result = auth_controller.login_user()
                if result is None:
                    console.print("[red]Login failed. Please try again.[/red]")
                    continue

                token, logged_in_user = result

                if logged_in_user is None:
                    console.print("[red]Login failed. Please try again.[/red]")
                    continue

                console.print(
                    "[bold green]Login successful."
                    f"Welcome, {logged_in_user.email}![/bold green]"
                )
                continue

            elif action == "Exit":
                console.print(
                    "[bold magenta]Exiting the application. "
                    "Goodbye![/bold magenta]"
                )
                break

        else:
            console.print(
                Panel.fit(
                    f"[green]Logged in as {logged_in_user.email}[/green]",
                    title="User Dashboard",
                )
            )
            task_controller = TaskController(
                logged_in_user.id, task_service, category_service
            )
            task_controller.show_menu()
            logged_in_user = None  # Logout after task operations


if __name__ == "__main__":
    main()
