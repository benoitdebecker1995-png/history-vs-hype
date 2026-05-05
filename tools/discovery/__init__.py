"""
Discovery Tools for YouTube Topic Research

Keyword extraction, search intent classification, and discovery diagnostics
for YouTube SEO and topic selection.

Main exports:
    - KeywordDB: SQLite database connection and CRUD operations
    - init_database: Initialize keyword database from schema
    - KeywordPayload: Immutable contract for keyword addition operations
"""

from .database import KeywordDB, init_database
from .keyword_store import KeywordPayload

__all__ = ['KeywordDB', 'init_database', 'KeywordPayload']
