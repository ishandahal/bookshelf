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

SORTABLE_COLUMNS = {"title", "author", "status", "genre", "added_at", "updated_at"}


def list_books(
    db_path: Path,
    status: str | None = None,
    genre: str | None = None,
    sort_by: str = "added_at",
) -> list[Book]:
    """Fetch books from the database with optional filters and sorting.

    Args:
        db_path: Path to the SQLite database file.
        status: Filter by status if provided.
        genre: Filter by genre if provided.
        sort_by: Column name to sort results by.

    Returns:
        List of matching Book instances.

    Raises:
        ValueError: If sort_by is not a valid column name.
    """
    if sort_by not in SORTABLE_COLUMNS:
        raise ValueError(f"Invalid sort column: {sort_by}")

    query = "SELECT id, title, author, status, genre, notes, source, added_at, updated_at FROM books"
    conditions = []
    params = []

    if status is not None:
        conditions.append("status = ?")
        params.append(status)
    if genre is not None:
        conditions.append("genre = ?")
        params.append(genre)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += f" ORDER BY {sort_by}"

    conn = sqlite3.connect(db_path)
    rows = conn.execute(query, params).fetchall()
    conn.close()

    return [
        Book(
            id=row[0], title=row[1], author=row[2], status=row[3],
            genre=row[4], notes=row[5], source=row[6],
            added_at=row[7], updated_at=row[8],
        )
        for row in rows
    ]