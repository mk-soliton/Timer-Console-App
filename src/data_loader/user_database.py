"""
user_database.py

This module handles database operations for the User model.
"""

import sqlite3
from datetime import datetime
from sqlite3 import Connection, Error
from typing import Optional

from pydantic import EmailStr

from src.models.user import User


class UserDatabase:
    """
    User database operations.

    Database class to handle user storage using SQLite3.
    """

    def __init__(self, db_path: str = "src/data/database/users.db") -> None:
        """
        Initialize the database connection and ensures the users table exists.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path = db_path
        self.conn: Optional[Connection] = None
        self.connect()
        self.create_users_table()

    def connect(self) -> None:
        """Establish a connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        except Error as err:
            raise Exception(f"Error connecting to database: {err}")

    def create_users_table(self) -> None:
        """Create the users table if it does not already exist."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """
        try:
            if self.conn:
                with self.conn:
                    cursor = self.conn.cursor()
                    cursor.execute(create_table_query)
                    self.conn.commit()
        except Error as err:
            if self.conn:
                self.conn.rollback()
            raise Exception(f"Error creating users table: {err}")

    def save_user(self, user: User) -> None:
        """Save a new user to the database.

        Args:
            user (User): The user object to be saved.
        """
        insert_user_data_query = """
        INSERT INTO users (id, email, hashed_password, created_at)
        VALUES (?, ?, ?, ?)
        """
        try:
            if self.conn:
                with self.conn:
                    cursor = self.conn.cursor()
                    cursor.execute(
                        insert_user_data_query,
                        (
                            str(user.id),
                            user.email,
                            user.hashed_password,
                            user.created_at.isoformat(),
                        ),
                    )
                    self.conn.commit()
        except Error as err:
            if self.conn:
                self.conn.rollback()
            raise Exception(f"Error saving user: {err}")

    def get_user_by_email(self, email: EmailStr) -> Optional[User]:
        """Retrieve a user by email.

        Args:
            email (EmailStr): The validated email of the user.

        Returns:
            Optional[User]: The user object if found, else None.
        """
        select_user_query = "SELECT * FROM users WHERE email = ?"
        try:
            if self.conn:
                with self.conn:
                    cursor = self.conn.cursor()
                    cursor.execute(select_user_query, (email,))
                    row = cursor.fetchone()
                    if row:
                        return User(
                            id=row["id"],
                            email=row["email"],
                            hashed_password=row["hashed_password"],
                            created_at=datetime.fromisoformat(
                                row["created_at"]
                            ),
                        )
            return None
        except Error as err:
            raise Exception(f"Error retrieving user by email: {err}")
