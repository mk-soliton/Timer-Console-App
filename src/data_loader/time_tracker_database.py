"""
time_tracker_database.py module.

This module handles database operations for the TimeTracker model.
"""

import sqlite3
from datetime import datetime
from sqlite3 import Connection, Error
from typing import Optional

from src.models.time_tracker import TimeTracker


class TimeTrackerDatabase:
    """Database class for managing time tracking data."""

    def __init__(self, db_path: str = "src/database/timings.db") -> None:
        """Initialize the database with the path to the database file.

        Args:
            db_path (str, optional): The path to the database file.
            Defaults to "timings.db".
        """
        self.db_path = db_path
        self.conn: Optional[Connection] = None
        self.connect()
        self.create_time_trackers_table()

    def connect(self) -> None:
        """Establishes a connection to the database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        except Error as e:
            raise Exception(f"Error connecting to database: {e}")

    def create_time_trackers_table(self) -> None:
        """Creates the time trackers table if it doesn't exist."""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS time_trackers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            task TEXT NOT NULL,
            status TEXT NOT NULL,
            start_time TEXT,
            pause_time TEXT,
            resume_time TEXT,
            stop_time TEXT,
            total_time REAL DEFAULT 0
        );
        """
        try:
            if self.conn:
                cursor = self.conn.cursor()
                cursor.execute(create_table_sql)
                self.conn.commit()
        except Error as e:
            raise Exception(f"Error creating time trackers table: {e}")

    def save_time_tracker(self, time_tracker: TimeTracker) -> None:
        """Saves a new time tracker to the database.

        Args:
            time_tracker (TimeTracker): The time tracker object to save.
        """
        insert_sql = """
        INSERT INTO time_trackers (task_id, category, task, status,
        start_time, pause_time, resume_time, stop_time, total_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            if self.conn:
                cursor = self.conn.cursor()
                cursor.execute(
                    insert_sql,
                    (
                        time_tracker.task_id,
                        time_tracker.category,
                        time_tracker.task,
                        time_tracker.status,
                        time_tracker.start_time.isoformat()
                        if time_tracker.start_time
                        else None,
                        time_tracker.pause_time.isoformat()
                        if time_tracker.pause_time
                        else None,
                        time_tracker.resume_time.isoformat()
                        if time_tracker.resume_time
                        else None,
                        time_tracker.stop_time.isoformat()
                        if time_tracker.stop_time
                        else None,
                        time_tracker.total_time,
                    ),
                )
                self.conn.commit()
        except Error as e:
            raise Exception(f"Error saving time tracker: {e}")

    def get_active_time_tracker(self, task_id: int) -> Optional[TimeTracker]:
        """Retrieves the active time tracker for a task.

        Args:
            task_id (int): The ID of the task.

        Returns:
            Optional[TimeTracker]: The active time tracker for the task.
        """
        select_sql = """SELECT * FROM time_trackers
        WHERE task_id = ? AND stop_time IS NULL"""
        try:
            if self.conn:
                cursor = self.conn.cursor()
                cursor.execute(select_sql, (task_id,))
                row = cursor.fetchone()
                if row:
                    return TimeTracker(
                        id=row["id"],
                        task_id=row["task_id"],
                        category=row["category"],
                        task=row["task"],
                        status=row["status"],
                        start_time=datetime.fromisoformat(row["start_time"])
                        if row["start_time"]
                        else None,
                        pause_time=datetime.fromisoformat(row["pause_time"])
                        if row["pause_time"]
                        else None,
                        resume_time=datetime.fromisoformat(row["resume_time"])
                        if row["resume_time"]
                        else None,
                        stop_time=datetime.fromisoformat(row["stop_time"])
                        if row["stop_time"]
                        else None,
                        total_time=row["total_time"],
                    )
        except Error as e:
            raise Exception(f"Error retrieving active time tracker: {e}")
        return None

    def update_time_tracker(self, time_tracker: TimeTracker) -> None:
        """Updates a time tracker in the database.

        Args:
            time_tracker (TimeTracker): The time tracker object to update.
        """
        update_sql = """
        UPDATE time_trackers
        SET category = ?, task = ?, status = ?,
        start_time = ?, pause_time = ?, resume_time = ?, stop_time = ?,
        total_time = ?
        WHERE id = ?
        """
        try:
            if self.conn:
                cursor = self.conn.cursor()
                cursor.execute(
                    update_sql,
                    (
                        time_tracker.category,
                        time_tracker.task,
                        time_tracker.status,
                        time_tracker.start_time.isoformat()
                        if time_tracker.start_time
                        else None,
                        time_tracker.pause_time.isoformat()
                        if time_tracker.pause_time
                        else None,
                        time_tracker.resume_time.isoformat()
                        if time_tracker.resume_time
                        else None,
                        time_tracker.stop_time.isoformat()
                        if time_tracker.stop_time
                        else None,
                        time_tracker.total_time,
                        time_tracker.id,
                    ),
                )
                self.conn.commit()
        except Error as e:
            raise Exception(f"Error updating time tracker: {e}")
