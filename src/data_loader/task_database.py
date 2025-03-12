"""
task_database.py module.

This module handles database operations that are related to tasks. This
includes viewing, creating, updating, and deleting tasks.
"""

import sqlite3
from sqlite3 import Connection, Error
from typing import List, Optional

from src.models.task import Task


class TaskDatabase:
    """Database class for managing tasks."""

    def __init__(self, db_path: str = "src/database/tasks.db") -> None:
        self.db_path = db_path
        self.conn: Optional[Connection] = None
        self.connect()
        self.create_tasks_table()

    def connect(self) -> None:
        """Establishes a connection to the database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        except Error as err:
            raise Exception(f"Error connecting to database: {err}")

    def create_tasks_table(self) -> None:
        """Creates the tasks table if it doesn't exist."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category_name TEXT NOT NULL,
            task_name TEXT NOT NULL,
            duration REAL DEFAULT 0,
            task_status TEXT DEFAULT 'not started',
            FOREIGN KEY (category_name) REFERENCES categories(name)
        );
        """
        try:
            if self.conn:
                cursor = self.conn.cursor()
                cursor.execute(create_table_query)
                self.conn.commit()
        except Error as err:
            raise Exception(f"Error creating tasks table: {err}")

    def save_task(self, task: Task) -> None:
        """Saves a new task into the database."""
        insert_sql = """
        INSERT INTO tasks (user_id, category_name, task_name, duration,
        task_status) VALUES (?, ?, ?, ?, ?)
        """
        try:
            if self.conn:
                cursor = self.conn.cursor()
                cursor.execute(
                    insert_sql,
                    (
                        task.user_id,
                        task.category_name,
                        task.task_name,
                        task.duration,
                        task.task_status,
                    ),
                )
                self.conn.commit()
        except Error as err:
            raise Exception(f"Error saving task: {err}")

    def get_tasks_by_user(self, user_id: int) -> List[Task]:
        """Retrieves all tasks for a given user."""
        select_sql = "SELECT * FROM tasks WHERE user_id = ?"
        try:
            if self.conn:
                cursor = self.conn.cursor()
                cursor.execute(select_sql, (user_id,))
                rows = cursor.fetchall()
                return [
                    Task(
                        id=row["id"],
                        user_id=row["user_id"],
                        category_name=row["category_name"],
                        task_name=row["task_name"],
                        duration=row["duration"],
                        task_status=row["task_status"],
                    )
                    for row in rows
                ]
        except Error as err:
            raise Exception(f"Error retrieving tasks: {err}")
        return []

    def update_task(
        self,
        user_id: int,
        task_id: int,
        task_name: str,
        duration: float,
    ) -> None:
        """Update a task's category, task name, or duration for the
        given user."""
        check_query = "SELECT id FROM tasks WHERE id = ? AND user_id = ?"
        update_query = """
        UPDATE tasks
        SET category_id = ?, task_name = ?, duration = ?
        WHERE id = ? AND user_id = ?
        """
        try:
            if self.conn:
                cursor = self.conn.cursor()
                cursor.execute(check_query, (task_id, user_id))
                task = cursor.fetchone()
                if task is None:
                    raise ValueError(
                        f"Task with ID {task_id} for user {user_id} "
                        "does not exist."
                    )
                cursor.execute(
                    update_query,
                    (task_name, duration, task_id, user_id),
                )
                self.conn.commit()
        except Error as err:
            raise Exception(f"Error updating task: {err}")

    def delete_task(self, user_id: int, task_id: int) -> None:
        """Deletes a task by task ID for the given user."""
        check_sql = "SELECT id FROM tasks WHERE id = ? AND user_id = ?"
        delete_sql = "DELETE FROM tasks WHERE id = ? AND user_id = ?"
        try:
            if self.conn:
                cursor = self.conn.cursor()
                cursor.execute(check_sql, (task_id, user_id))
                task = cursor.fetchone()
                if task is None:
                    raise ValueError(
                        f"Task with ID {task_id} for user {user_id} "
                        "does not exist."
                    )
                cursor.execute(delete_sql, (task_id, user_id))
                self.conn.commit()
        except Error as err:
            raise Exception(f"Error deleting task: {err}")
