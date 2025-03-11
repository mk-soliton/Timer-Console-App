"""
main.py

This module is the entry point for Time Tracker Console Application.
"""

import inquirer  # type: ignore
from pydantic import EmailStr, TypeAdapter, ValidationError
from rich.console import Console

from src.data.user_database import UserData
from src.services.authentication_service import (
    AuthenticationError,
    AuthenticationService,
)

# Create a Rich console instance
console = Console()


def main() -> None:
    """Run the main function for Time Tracker Console Application."""
    auth_service = AuthenticationService()
    user_data = UserData()

    log_welcome_message()
    while True:
        action = get_user_action()
        if action == "Register":
            handle_registration(auth_service, user_data)
        elif action == "Login":
            handle_login(auth_service)
        elif action == "Exit":
            console.log(
                "[bold magenta]Exiting the application. "
                "Goodbye![/bold magenta]"
            )
            break


def log_welcome_message() -> None:
    """Log the welcome message."""
    console.log(
        "[bold magenta]Welcome to Time Tracker App[/bold magenta]",
        justify="center",
    )
    console.log("[cyan]Please choose an option from the menu below:[/cyan]\n")


def get_user_action() -> str:
    """Prompt the user to choose an action."""
    questions = [
        inquirer.List(
            "action",
            message="What do you want to do?",
            choices=["Register", "Login", "Exit"],
        )
    ]
    answers = inquirer.prompt(questions)
    if not answers or "action" not in answers:
        console.log("[red]No action selected. Exiting.[/red]")
        return "Exit"
    return answers["action"]


def handle_registration(
    auth_service: AuthenticationService, user_data: UserData
) -> None:
    """Handle user registration."""
    questions = [
        inquirer.Text("email", message="Enter your email"),
        inquirer.Password("password", message="Enter your password"),
    ]
    answers = inquirer.prompt(questions)
    if not answers:
        console.log("[red]Registration cancelled.[/red]")
        return

    email_input: str = answers.get("email", "")
    password: str = answers.get("password", "")

    if not email_input:
        console.log("[red]No email provided. Please try again.[/red]")
        return

    try:
        email = TypeAdapter(EmailStr).validate_python(email_input)
    except ValidationError:
        console.log("[red]Invalid email format. Please try again.[/red]")
        return

    try:
        user = auth_service.register_user(email, password)
        console.log(
            f"[green]User registered successfully. User ID: {user.id}[/green]"
        )

    except ValueError as err:
        console.log(f"[red]Registration failed: {err}[/red]")
    except Exception as err:
        console.log(
            "[red]An unexpected error occurred during registration: "
            f"{err}[/red]"
        )


def handle_login(auth_service: AuthenticationService) -> None:
    """Handle user login."""
    questions = [
        inquirer.Text("email", message="Enter your email"),
        inquirer.Password("password", message="Enter your password"),
    ]
    answers = inquirer.prompt(questions)
    if not answers:
        console.log("[red]Login cancelled.[/red]")
        return

    email_input = answers.get("email", "")
    password = answers.get("password", "")

    if not email_input:
        console.log("[red]No email provided. Please try again.[/red]")
        return

    try:
        email = TypeAdapter(EmailStr).validate_python(email_input)
    except ValidationError:
        console.log("[red]Invalid email format. Please try again.[/red]")
        return

    try:
        token = auth_service.login_user(email, password)
        console.log("[green]Login successful![/green]")
        console.log(f"Your JWT token is:\n[bold cyan]{token}[/bold cyan]")
    except AuthenticationError as e:
        console.log(f"[red]Login failed: {e}[/red]")
    except Exception as e:
        console.log(
            f"[red]An unexpected error occurred during login: {e}[/red]"
        )


if __name__ == "__main__":
    main()
