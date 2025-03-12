"""
Handle Authentication Service.

This module handles the authentication logic for the Time Tracker Console
Application.
It includes functions for user account creation, login, and secure password
management.
"""

from typing import Optional

import inquirer  # type: ignore
from pydantic import EmailStr, TypeAdapter, ValidationError
from rich.console import Console

from src.services.authentication_service import (
    AuthenticationError,
    AuthenticationService,
    UserAlreadyExistsError,
)


class AuthenticationController:
    """
    Authentication Controller.

    Controller class for handling user authentication operations.
    """

    def __init__(
        self, auth_service: Optional[AuthenticationService] = None
    ) -> None:
        self.console = Console()
        self.auth_service = auth_service or AuthenticationService()

    def register_user(self) -> None:
        """
        Handle user registration by collecting email and password.
        """
        questions = [
            inquirer.Text("email", message="Enter your email"),
            inquirer.Password("password", message="Enter your password"),
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            self.console.print("[red]Registration cancelled.[/red]")
            return

        email_input: str = answers.get("email", "")
        password: str = answers.get("password", "")

        if not email_input:
            self.console.print(
                "[red]No email provided. Please try again.[/red]"
            )
            return

        try:
            email = TypeAdapter(EmailStr).validate_python(email_input)
        except ValidationError:
            self.console.print(
                "[red]Invalid email format. Please try again.[/red]"
            )
            return

        try:
            user = self.auth_service.register_user(email, password)
            self.console.print(
                "[green]User registered successfully. "
                f"User ID: {user.id}[/green]"
            )
        except UserAlreadyExistsError as e:
            self.console.print(f"[red]Registration failed: {e}[/red]")
        except ValueError as e:
            self.console.print(f"[red]Registration failed: {e}[/red]")
        except Exception as e:
            self.console.print(
                "[red]An unexpected error occurred during registration: "
                f"{e}[/red]"
            )

    def login_user(self):
        """
        Handle user login by collecting email and password.
        """
        questions = [
            inquirer.Text("email", message="Enter your email"),
            inquirer.Password("password", message="Enter your password"),
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            self.console.print("[red]Login cancelled.[/red]")
            return None  # Explicitly return None

        email_input = answers.get("email", "")
        password = answers.get("password", "")

        if not email_input:
            self.console.print(
                "[red]No email provided. Please try again.[/red]"
            )
            return None

        try:
            email = TypeAdapter(EmailStr).validate_python(email_input)
        except ValidationError:
            self.console.print(
                "[red]Invalid email format. Please try again.[/red]"
            )
            return None

        try:
            token, user = self.auth_service.login_user(
                email, password
            )  # Assuming login_user now returns user object
            self.console.print("[green]Login successful![/green]")
            self.console.print(
                f"Your JWT token is:\n[bold cyan]{token}[/bold cyan]"
            )
            return user  # Return the user object
        except AuthenticationError as e:
            self.console.print(f"[red]Login failed: {e}[/red]")
            return None
        except Exception as e:
            self.console.print(
                f"[red]An unexpected error occurred during login: {e}[/red]"
            )
            return None
