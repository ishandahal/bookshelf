import sqlite3
from pathlib import Path

from bookshelf.models import Book


def init_db(db_path: Path) -> None:
    """Create the bookshelf database and books table if they don't exist.

    Args:
        db_path: Path to the SQLite database file.
    """
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'want-to-read',
            genre TEXT NOT NULL DEFAULT '',
            notes TEXT NOT NULL DEFAULT '',
            source TEXT NOT NULL DEFAULT '',
            added_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_book(db_path: Path, book: Book) -> int:
    """Insert a book into the database.

    Args:
        db_path: Path to the SQLite database file.
        book: Book instance to insert.

    Returns:
        The ID of the newly inserted book.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.execute(
        """
        INSERT INTO books (title, author, status, genre, notes, source, added_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (book.title, book.author, book.status, book.genre,
         book.notes, book.source, book.added_at, book.updated_at),
    )
    conn.commit()
    book_id = cursor.lastrowid
    conn.close()
    return book_id
