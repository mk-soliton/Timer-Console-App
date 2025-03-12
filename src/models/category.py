"""
Defines Category model.

This module represents a category model with id and category_name attributes.
"""

from typing import Optional

from pydantic import BaseModel


class Category(BaseModel):
    """Represent a category model using Pydantic for validation."""

    id: Optional[int] = None
    name: str
