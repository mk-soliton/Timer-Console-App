"""
Handle category service.

This module handles category management logic including creating and retrieving
categories.
"""

from typing import List, Optional

from src.data_loader.category_database import CategoryDatabase
from src.models.category import Category


class CategoryService:
    """Service class for managing categories."""

    def __init__(self, db: Optional[CategoryDatabase] = None) -> None:
        """Initializes the category service with a database instance."""
        self.db = db if db is not None else CategoryDatabase()

    def create_category(self, name: str) -> Category:
        """Creates a new category if it doesn't exist."""
        return self.db.get_or_create_category(name)

    def get_all_categories(self) -> List[Category]:
        """Retrieves all categories."""
        return self.db.get_all_categories()
