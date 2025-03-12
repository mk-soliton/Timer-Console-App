"""
main.py

This module is the entry point for Time Tracker Console Application.
"""

import inquirer  # type: ignore
from rich.console import Console
from rich.panel import Panel

from src.controllers.authentication_controller import AuthenticationController

# Create a Rich console instance
console = Console()


def main() -> None:
    """Main function to handle authentication and task management."""
    auth_controller = AuthenticationController()
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
                if (
                    result is None
                ):  # If login_user() returned None, exit or handle accordingly
                    console.print("[red]Login failed. Please try again.[/red]")
                    continue

                token, logged_in_user = (
                    result  # Properly unpacking after checking it's not None
                )

                if logged_in_user is None:  # Additional safety check
                    console.print("[red]Login failed. Please try again.[/red]")
                    continue

            elif action == "Exit":
                console.print(
                    "[bold magenta]Exiting the application. "
                    "Goodbye![/bold magenta]"
                )
                break


if __name__ == "__main__":
    main()
