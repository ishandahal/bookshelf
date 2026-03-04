import sqlite3
from pathlib import Path

from bookshelf.db import add_book, init_db
from bookshelf.models import Book


def test_init_db_creates_books_table(tmp_path: Path):
    db_path = tmp_path / "test.db"
    init_db(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='books'"
    )
    assert cursor.fetchone() is not None
    conn.close()


def test_add_book_returns_id(tmp_path: Path):
    db_path = tmp_path / "test.db"
    init_db(db_path)

    book = Book(title="Dune", author="Frank Herbert")
    book_id = add_book(db_path, book)

    assert isinstance(book_id, int)
    assert book_id > 0


def test_add_book_persists_data(tmp_path: Path):
    db_path = tmp_path / "test.db"
    init_db(db_path)

    book = Book(title="Dune", author="Frank Herbert", genre="sci-fi")
    add_book(db_path, book)

    conn = sqlite3.connect(db_path)
    row = conn.execute("SELECT title, author, genre FROM books WHERE id=1").fetchone()
    conn.close()

    assert row == ("Dune", "Frank Herbert", "sci-fi")