"""
category_database.py module.

This module handles database operations that are related to categories. This
includes creating, and retrieve categories.
"""

import sqlite3
from sqlite3 import Connection, Error
from typing import List, Optional

from src.models.category import Category


class CategoryDatabase:
    """Database class for managing categories."""

    def __init__(self, db_path: str = "src/database/categories.db") -> None:
        self.db_path = db_path
        self.conn: Optional[Connection] = None
        self.connect()
        self.create_categories_table()

    def connect(self) -> None:
        """Establishes a connection to the database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        except Error as e:
            raise Exception(f"Error connecting to database: {e}")

    def create_categories_table(self) -> None:
        """Creates the categories table if it doesn't exist."""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS categories (
            name TEXT UNIQUE NOT NULL
        );
        """
        try:
            if self.conn:
                cursor = self.conn.cursor()
                cursor.execute(create_table_sql)
                self.conn.commit()
        except Error as e:
            raise Exception(f"Error creating categories table: {e}")

    def get_or_create_category(self, name: str) -> Category:
        """Retrieves a category by name, or creates it if it doesn't exist."""
        select_sql = "SELECT * FROM categories WHERE name = ?"
        insert_sql = "INSERT INTO categories (name) VALUES (?)"
        try:
            if self.conn:
                cursor = self.conn.cursor()
                cursor.execute(select_sql, (name,))
                row = cursor.fetchone()
                if row:
                    return Category(name=row["name"])

                cursor.execute(insert_sql, (name,))
                self.conn.commit()
                return Category(name=name)

        except Error as e:
            raise Exception(f"Error retrieving or creating category: {e}")

        raise ValueError(f"Failed to create or retrieve category '{name}'.")

    def get_all_categories(self) -> List[Category]:
        """Retrieves all categories."""
        select_sql = "SELECT * FROM categories"
        try:
            if self.conn:
                cursor = self.conn.cursor()
                cursor.execute(select_sql)
                rows = cursor.fetchall()
                return [Category(name=row["name"]) for row in rows]
        except Error as e:
            raise Exception(f"Error retrieving categories: {e}")
        return []
