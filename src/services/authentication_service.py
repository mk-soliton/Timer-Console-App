"""
Handle Authentication Service.

This module handles the authentication logic for the Time Tracker Console
Application.
It includes functions for user account creation, login, and secure password
management.
"""

import datetime
from typing import Optional

import bcrypt  # type: ignore
import jwt  # type: ignore
from pydantic import EmailStr

from src.data.user_database import UserData
from src.exceptions.authentication_exceptions import (
    AuthenticationError,
    UserAlreadyExistsError,
)
from src.models.user import User
from src.utils.config import SECRET_KEY


class AuthenticationService:
    """Service class for handling user authentication operations."""

    def __init__(self, db: Optional[UserData] = None) -> None:
        """
        Initializes the authentication service with a database instance.

        Args:
            db (Optional[Database]): A Database instance. If None, a new
            instance is created.
        """
        self.db = db if db is not None else UserData()

    @staticmethod
    def hash_password(password: str) -> str:
        """Hashes a password using bcrypt.

        Args:
            password (str): The plain text password.

        Returns:
            str: The hashed password.
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

    @staticmethod
    def verify_password(password: str, hashed_password: str):
        """Verifies if the provided password matches the stored hashed
        password.

        Args:
            password (str): The plain text password.
            hashed_password (str): The stored hashed password.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    @staticmethod
    def generate_token(user_id: str) -> str:
        """Generates a JWT authentication token for a user.

        Args:
            user_id (str): The ID of the authenticated user.

        Returns:
            str: A JWT token string.
        """
        payload = {
            "user_id": user_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        """Decodes and verifies a JWT authentication token.

        Args:
            token (str): The JWT token.

        Returns:
            Optional[dict]: The decoded payload if valid, or None if invalid
            or expired.
        """
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:  # type: ignore
            return None
        except jwt.InvalidTokenError:  # type: ignore
            return None

    @staticmethod
    def is_strong_password(password: str) -> bool:
        """Checks if the password meets minimum security requirements.

        Args:
            password (str): The plain text password.

        Returns:
            bool: True if the password is strong, False otherwise.
        """
        # For this example, the password must be at least 8 characters.
        return len(password) >= 8

    def register_user(self, email: EmailStr, password: str) -> User:
        """Registers a new user by storing hashed credentials in the database.

        Args:
            email (EmailStr): The user's validated email address.
            password (str): The user's plain text password.

        Raises:
            UserAlreadyExistsError: If a user with the given email already
            exists.
            ValueError: If the password does not meet security requirements.

        Returns:
            User: The newly registered user object.
        """
        if self.db.get_user_by_email(email):
            raise UserAlreadyExistsError(
                f"User with email {email} already exists."
            )

        if not self.is_strong_password(password):
            raise ValueError("Password must be at least 8 characters long.")

        hashed_password = self.hash_password(password)
        new_user = User.create(email=email, hashed_password=hashed_password)
        self.db.save_user(new_user)
        return new_user

    def login_user(self, email: EmailStr, password: str) -> str:
        """Authenticates a user and returns a JWT token if successful.

        Args:
            email (EmailStr): The user's validated email address.
            password (str): The user's plain text password.

        Raises:
            AuthenticationError: If authentication fails due to incorrect
            credentials.

        Returns:
            str: A JWT token if authentication is successful.
        """
        user = self.db.get_user_by_email(email)
        if not user or not self.verify_password(
            password, user.hashed_password
        ):
            raise AuthenticationError("Invalid email or password.")

        return self.generate_token(user.id)
