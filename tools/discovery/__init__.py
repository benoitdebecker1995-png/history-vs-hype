"""
Discovery Tools for YouTube Topic Research

Keyword extraction, search intent classification, and discovery diagnostics
for YouTube SEO and topic selection.

Main exports:
    - KeywordDB: SQLite database connection and CRUD operations
    - init_database: Initialize keyword database from schema
"""

from .database import KeywordDB, init_database

__all__ = ['KeywordDB', 'init_database']
